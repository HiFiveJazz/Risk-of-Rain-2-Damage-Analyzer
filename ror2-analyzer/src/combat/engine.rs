use super::types::*;

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

pub fn resolve_and_apply_hit(
    hit: &Hit,
    target_context: &mut TargetContext,
    modifiers: &[FinalDamageModifier],
) -> Hit {
    let mut resolved_hit = hit.clone();

    {
        let target = target_context
            .target(hit.target)
            .expect("hit target must exist in target context");

        apply_final_damage_modifiers(&mut resolved_hit, target, modifiers);
    }

    target_context
        .target_mut(hit.target)
        .expect("hit target must exist in target context")
        .apply_damage(resolved_hit.final_damage);

    resolved_hit
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
