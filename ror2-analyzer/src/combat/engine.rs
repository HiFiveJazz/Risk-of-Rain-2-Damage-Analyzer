use super::types::*;
use std::time::Duration;

pub fn simulate_attack(
    root_hit: &Hit,
    on_hit_effects: &[OnHitEffect],
    target_context: &TargetContext,
    modifiers: &[FinalDamageModifier],
    luck: i32,
) -> SimulationResult {
    let initial_branches =
        begin_combat_branches(root_hit, on_hit_effects, target_context, modifiers, luck);

    let mut results = Vec::new();

    for branch in initial_branches {
        results.extend(run_branch_until_blocked(
            &branch,
            on_hit_effects,
            modifiers,
            luck,
        ));
    }

    SimulationResult { branches: results }
}

pub fn armor_damage_multiplier(armor: f64) -> f64 {
    1.0 - armor / (100.0 + armor.abs())
}

pub fn apply_armor(damage: f64, armor: f64) -> f64 {
    if damage <= 0.0 {
        return 0.0;
    }

    let modified = damage * armor_damage_multiplier(armor);

    modified.max(1.0)
}

pub fn advance_branch(
    branch: &CombatBranch,
    on_hit_effects: &[OnHitEffect],
    modifiers: &[FinalDamageModifier],
    luck: i32,
) -> Result<Vec<CombatBranch>, AdvanceError> {
    let mut base_branch = branch.clone();

    let Some((event_time, batch)) = base_branch.pending_events.pop_next_batch() else {
        return Err(AdvanceError::NoPendingEvents);
    };

    let batch_len = batch.len();

    let mut generated_hits = Vec::with_capacity(batch_len);

    let mut seen_targets = std::collections::HashSet::new();

    for event in batch {
        match event.effect {
            GeneratedEffect::Hit(hit) => {
                // Two simultaneous hits against the same
                // target may be order-sensitive.
                if !seen_targets.insert(hit.hit.target) {
                    return Err(AdvanceError::SimultaneousEvents { count: batch_len });
                }

                generated_hits.push(hit);
            }

            GeneratedEffect::Bleed(_) => {
                return Err(AdvanceError::UnsupportedBleedEvent);
            }
        }
    }

    base_branch.current_time = event_time;

    let mut resolutions = Vec::with_capacity(generated_hits.len());

    // These hits all land at the same time, but they affect
    // distinct targets, so their mutation order is irrelevant.
    for generated_hit in generated_hits {
        let resolution =
            resolve_and_apply_hit(&generated_hit.hit, &mut base_branch.targets, modifiers);

        base_branch.resolved_hits.push(resolution.clone());

        resolutions.push(resolution);
    }

    // All simultaneous damage has now been applied.
    //
    // Generate the possible proc outcomes for each hit
    // against that resulting target state.
    let proc_outcome_sets: Vec<Vec<ProcOutcome>> = resolutions
        .iter()
        .map(|resolution| {
            enumerate_direct_proc_outcomes(
                &resolution.hit,
                on_hit_effects,
                &base_branch.targets,
                luck,
            )
        })
        .collect();

    // Start with the state after the entire simultaneous batch.
    let mut branches = vec![base_branch];

    // Cartesian-product the possible proc outcomes from
    // every hit in the batch.
    for proc_outcomes in proc_outcome_sets {
        let mut next_branches = Vec::new();

        for branch in branches {
            for proc_outcome in &proc_outcomes {
                let mut child_branch = branch.clone();

                child_branch.probability *= proc_outcome.probability;

                for effect in proc_outcome.effects.iter().cloned() {
                    schedule_generated_effect(&mut child_branch.pending_events, event_time, effect);
                }

                next_branches.push(child_branch);
            }
        }

        branches = next_branches;
    }

    Ok(branches)
}

pub fn run_branch_until_blocked(
    branch: &CombatBranch,
    on_hit_effects: &[OnHitEffect],
    modifiers: &[FinalDamageModifier],
    luck: i32,
) -> Vec<BranchRunResult> {
    let mut work = vec![branch.clone()];
    let mut results = Vec::new();

    while let Some(current) = work.pop() {
        if current.pending_events.is_empty() {
            results.push(BranchRunResult {
                branch: current,
                reason: BranchStopReason::Complete,
            });

            continue;
        }

        match advance_branch(&current, on_hit_effects, modifiers, luck) {
            Ok(children) => {
                work.extend(children);
            }

            Err(AdvanceError::NoPendingEvents) => {
                results.push(BranchRunResult {
                    branch: current,
                    reason: BranchStopReason::Complete,
                });
            }

            Err(AdvanceError::SimultaneousEvents { count }) => {
                results.push(BranchRunResult {
                    branch: current,
                    reason: BranchStopReason::SimultaneousEvents { count },
                });
            }

            Err(AdvanceError::UnsupportedBleedEvent) => {
                results.push(BranchRunResult {
                    branch: current,
                    reason: BranchStopReason::UnsupportedBleedEvent,
                });
            }
        }
    }

    results
}

pub fn effective_proc_chance(base_chance: f64, source_proc_coefficient: f64, luck: i32) -> f64 {
    assert!(base_chance >= 0.0);
    assert!(source_proc_coefficient >= 0.0);

    let chance = (base_chance * source_proc_coefficient).clamp(0.0, 1.0);

    match luck {
        0 => chance,

        n if n > 0 => 1.0 - (1.0 - chance).powi(n + 1),

        n => chance.powi((-n) + 1),
    }
}

pub fn begin_combat_branches(
    root_hit: &Hit,
    on_hit_effects: &[OnHitEffect],
    target_context: &TargetContext,
    modifiers: &[FinalDamageModifier],
    luck: i32,
) -> Vec<CombatBranch> {
    // Every combat calculation begins from its own state.
    let mut post_hit_targets = target_context.clone();

    // Damage happens before on-hit effects are processed.
    let root_resolution = resolve_and_apply_hit(root_hit, &mut post_hit_targets, modifiers);

    let proc_outcomes = enumerate_direct_proc_outcomes(
        &root_resolution.hit,
        on_hit_effects,
        &post_hit_targets,
        luck,
    );

    proc_outcomes
        .into_iter()
        .map(|outcome| {
            let mut pending_events = EventQueue::new();

            for effect in outcome.effects {
                schedule_generated_effect(&mut pending_events, Duration::ZERO, effect);
            }

            CombatBranch {
                probability: outcome.probability,

                root_resolution: root_resolution.clone(),
                resolved_hits: Vec::new(),

                // Critical:
                //
                // every probabilistic branch receives
                // its own independent target state.
                targets: post_hit_targets.clone(),
                current_time: Duration::ZERO,

                pending_events,
            }
        })
        .collect()
}

pub fn resolve_and_apply_hit(
    hit: &Hit,
    target_context: &mut TargetContext,
    modifiers: &[FinalDamageModifier],
) -> HitResolution {
    let target_health_before = target_context
        .target(hit.target)
        .expect("hit target must exist in target context")
        .health();

    let mut resolved_hit = hit.clone();

    {
        let target = target_context
            .target(hit.target)
            .expect("hit target must exist in target context");

        apply_final_damage_modifiers(&mut resolved_hit, target, modifiers);
        resolved_hit.final_damage = apply_armor(resolved_hit.final_damage, target.armor());
    }

    let target = target_context
        .target_mut(hit.target)
        .expect("hit target must exist in target context");

    target.apply_damage(resolved_hit.final_damage);

    HitResolution {
        hit: resolved_hit,
        target_health_before,
        target_health_after: target.health(),
    }
}

pub fn apply_final_damage_modifiers(
    hit: &mut Hit,
    target: &Target,
    modifiers: &[FinalDamageModifier],
) {
    let multiplier: f64 = modifiers
        .iter()
        .map(|modifier| modifier.multiplier_for(target))
        .product();

    // Critically, only final_damage changes.
    //
    // proc_damage stays untouched so TOTAL-damage
    // child effects do not double-dip.
    hit.final_damage = hit.proc_damage * multiplier;
}

fn schedule_generated_effect(
    queue: &mut EventQueue,
    current_time: Duration,
    effect: GeneratedEffect,
) {
    let delay = match &effect {
        GeneratedEffect::Hit(hit) => hit.timing.delay(),

        // Bleed timing becomes its own system later.
        // For now this preserves existing behavior.
        GeneratedEffect::Bleed(_) => Duration::ZERO,
    };

    queue.schedule_after(current_time, delay, effect);
}

pub fn enumerate_direct_proc_outcomes(
    source_hit: &Hit,
    on_hit_effects: &[OnHitEffect],
    target_context: &TargetContext,
    luck: i32,
) -> Vec<ProcOutcome> {
    let mut outcomes = vec![ProcOutcome {
        probability: 1.0,
        effects: Vec::new(),
    }];

    for effect in on_hit_effects {
        let (base_chance, contact_targets) = match effect {
            OnHitEffect::TotalDamage(proc_effect) => {
                // This proc already participated in this chain.
                if source_hit.proc_mask.contains(proc_effect.kind) {
                    continue;
                }

                let targets =
                    target_context.contact_targets(source_hit.target, proc_effect.targeting);

                // No valid targets means this effect cannot generate a hit.
                if targets.is_empty() {
                    continue;
                }

                (proc_effect.base_chance, Some(targets))
            }

            OnHitEffect::Bleed(bleed) => (bleed.base_chance, None),
        };

        let chance = effective_proc_chance(base_chance, source_hit.proc_coefficient, luck);

        let mut next_outcomes = Vec::with_capacity(outcomes.len() * 2);

        for outcome in outcomes {
            let ProcOutcome {
                probability,
                effects,
            } = outcome;

            // Failure branch.
            let failure_probability = probability * (1.0 - chance);

            if failure_probability > 0.0 {
                next_outcomes.push(ProcOutcome {
                    probability: failure_probability,
                    effects: effects.clone(),
                });
            }

            // Success branch.
            let success_probability = probability * chance;

            if success_probability > 0.0 {
                let generated_effects = match effect {
                    OnHitEffect::TotalDamage(proc_effect) => contact_targets
                        .as_ref()
                        .unwrap()
                        .iter()
                        .copied()
                        .map(|target| {
                            let child = source_hit
                                .spawn_total_damage_proc_on(
                                    proc_effect.kind,
                                    target,
                                    proc_effect.damage_multiplier,
                                    proc_effect.proc_coefficient,
                                )
                                .expect("proc should not be blocked after mask check");

                            GeneratedEffect::Hit(GeneratedHit {
                                source: proc_effect.kind,
                                hit: child,
                                targeting: proc_effect.targeting,
                                timing: proc_effect.timing,
                            })
                        })
                        .collect::<Vec<_>>(),

                    OnHitEffect::Bleed(_) => {
                        vec![GeneratedEffect::Bleed(Bleed {
                            target: source_hit.target,

                            duration_seconds: 3.0 * source_hit.proc_coefficient,

                            ticks_per_second: 4.0,

                            damage_per_tick: source_hit.attacker_base_damage * 0.20,
                        })]
                    }
                };

                let mut success_effects = effects;

                success_effects.extend(generated_effects);

                next_outcomes.push(ProcOutcome {
                    probability: success_probability,
                    effects: success_effects,
                });
            }
        }

        outcomes = next_outcomes;
    }

    outcomes
}

pub fn enumerate_proc_tree_outcomes(
    source_hit: &Hit,
    on_hit_effects: &[OnHitEffect],
    target_context: &TargetContext,
    luck: i32,
) -> Vec<CombatOutcome> {
    let direct_outcomes =
        enumerate_direct_proc_outcomes(source_hit, on_hit_effects, target_context, luck);

    let mut resolved_outcomes = Vec::new();

    for direct_outcome in direct_outcomes {
        let mut combinations = vec![CombatOutcome {
            probability: direct_outcome.probability,
            effects: Vec::new(),
        }];

        for generated_effect in direct_outcome.effects {
            let alternatives = match generated_effect {
                GeneratedEffect::Bleed(bleed) => {
                    vec![CombatOutcome {
                        probability: 1.0,
                        effects: vec![ResolvedEffect::Bleed(bleed)],
                    }]
                }

                GeneratedEffect::Hit(generated_hit) => {
                    let descendant_outcomes = enumerate_proc_tree_outcomes(
                        &generated_hit.hit,
                        on_hit_effects,
                        target_context,
                        luck,
                    );

                    descendant_outcomes
                        .into_iter()
                        .map(|descendants| CombatOutcome {
                            probability: descendants.probability,

                            effects: vec![ResolvedEffect::Hit(ResolvedHit {
                                source: generated_hit.source,
                                hit: generated_hit.hit.clone(),
                                targeting: generated_hit.targeting,
                                effects: descendants.effects,
                            })],
                        })
                        .collect()
                }
            };

            let mut next_combinations = Vec::new();

            for combination in &combinations {
                for alternative in &alternatives {
                    let mut effects = combination.effects.clone();

                    effects.extend(alternative.effects.clone());

                    next_combinations.push(CombatOutcome {
                        probability: combination.probability * alternative.probability,

                        effects,
                    });
                }
            }

            combinations = next_combinations;
        }

        resolved_outcomes.extend(combinations);
    }

    resolved_outcomes
}
