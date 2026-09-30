use super::*;

const EPSILON: f64 = 1e-12;
// Helpers

fn assert_close(actual: f64, expected: f64) {
    assert!(
        (actual - expected).abs() < EPSILON,
        "expected {expected}, got {actual}"
    );
}

fn contains_chain(effects: &[ResolvedEffect], chain: &[ProcKind]) -> bool {
    if chain.is_empty() {
        return true;
    }

    effects.iter().any(|effect| {
        let ResolvedEffect::Hit(hit) = effect else {
            return false;
        };

        if hit.source != chain[0] {
            return false;
        }

        if chain.len() == 1 {
            return true;
        }

        contains_chain(&hit.effects, &chain[1..])
    })
}

#[test]
fn recursively_enumerates_atg_and_ukulele_proc_trees() {
    let root = Hit::root(10.0, 100.0, 1.0);

    let on_hit_effects = [
        OnHitEffect::TotalDamage(TotalDamageProc {
            kind: ProcKind::Atg,
            base_chance: 0.10,
            damage_multiplier: 3.0,
            proc_coefficient: 1.0,
            targeting: AttackTargeting::SingleTarget,
        }),
        OnHitEffect::TotalDamage(TotalDamageProc {
            kind: ProcKind::Ukulele,
            base_chance: 0.25,
            damage_multiplier: 0.8,
            proc_coefficient: 0.2,
            targeting: AttackTargeting::Chain {
                max_targets: 3,
                radius_m: 20.0,
            },
        }),
    ];

    let targets = TargetContext::with_secondary_targets(1);

    let outcomes = enumerate_proc_tree_outcomes(&root, &on_hit_effects, &targets, 0);

    // There are 9 complete mutually exclusive proc-tree outcomes.
    assert_eq!(outcomes.len(), 9);

    let total_probability: f64 = outcomes.iter().map(|outcome| outcome.probability).sum();

    assert_close(total_probability, 1.0);

    // Probability that an AtG branch eventually produces Ukulele:
    //
    // 0.10 * 0.25 = 0.025
    let atg_to_ukulele_probability: f64 = outcomes
        .iter()
        .filter(|outcome| contains_chain(&outcome.effects, &[ProcKind::Atg, ProcKind::Ukulele]))
        .map(|outcome| outcome.probability)
        .sum();

    assert_close(atg_to_ukulele_probability, 0.025);

    // Probability that a Ukulele branch eventually produces AtG:
    //
    // 0.25 * (0.10 * 0.20)
    // = 0.005
    let ukulele_to_atg_probability: f64 = outcomes
        .iter()
        .filter(|outcome| contains_chain(&outcome.effects, &[ProcKind::Ukulele, ProcKind::Atg]))
        .map(|outcome| outcome.probability)
        .sum();

    assert_close(ukulele_to_atg_probability, 0.005);

    // Expected generated proc damage:
    //
    // Root AtG:
    //   10% * 300 = 30
    //
    // Root Ukulele:
    //   25% * 80 = 20
    //
    // AtG -> Ukulele:
    //   2.5% * 240 = 6
    //
    // Ukulele -> AtG:
    //   0.5% * 240 = 1.2
    //
    // Total = 57.2
    let expected_generated_damage: f64 = outcomes
        .iter()
        .map(|outcome| outcome.probability * outcome.total_generated_damage())
        .sum();

    assert_close(expected_generated_damage, 57.2);
}

#[test]
fn atg_and_ukulele_can_proc_simultaneously() {
    let root = Hit::root(10.0, 100.0, 1.0);

    let on_hit_effects = [
        OnHitEffect::TotalDamage(TotalDamageProc {
            kind: ProcKind::Atg,
            base_chance: 0.10,
            damage_multiplier: 3.0,
            proc_coefficient: 1.0,
            targeting: AttackTargeting::SingleTarget,
        }),
        OnHitEffect::TotalDamage(TotalDamageProc {
            kind: ProcKind::Ukulele,
            base_chance: 0.25,
            damage_multiplier: 0.8,
            proc_coefficient: 0.2,
            targeting: AttackTargeting::Chain {
                max_targets: 3,
                radius_m: 20.0,
            },
        }),
    ];

    let targets = TargetContext::with_secondary_targets(1);

    let outcomes = enumerate_direct_proc_outcomes(&root, &on_hit_effects, &targets, 0);

    assert_eq!(outcomes.len(), 4);

    // All mutually exclusive outcomes should sum to exactly 1.
    let total_probability: f64 = outcomes.iter().map(|outcome| outcome.probability).sum();

    assert_close(total_probability, 1.0);

    let neither = outcomes
        .iter()
        .find(|outcome| outcome.effects.is_empty())
        .unwrap();

    assert_close(neither.probability, 0.675);

    let atg_only = outcomes
        .iter()
        .find(|outcome| {
            let hits: Vec<_> = outcome.hits().collect();

            hits.len() == 1 && hits[0].source == ProcKind::Atg
        })
        .unwrap();

    assert_close(atg_only.probability, 0.075);

    let atg = atg_only.hits().next().unwrap();
    assert_close(atg.hit.proc_damage, 300.0);

    let ukulele_only = outcomes
        .iter()
        .find(|outcome| {
            let hits: Vec<_> = outcome.hits().collect();

            hits.len() == 1 && hits[0].source == ProcKind::Ukulele
        })
        .unwrap();

    assert_close(ukulele_only.probability, 0.225);

    let ukulele = ukulele_only.hits().next().unwrap();
    assert_close(ukulele.hit.proc_damage, 80.0);

    let both = outcomes
        .iter()
        .find(|outcome| outcome.hits().count() == 2)
        .unwrap();

    assert_close(both.probability, 0.025);

    let atg = both.hits().find(|hit| hit.source == ProcKind::Atg).unwrap();

    let ukulele = both
        .hits()
        .find(|hit| hit.source == ProcKind::Ukulele)
        .unwrap();

    assert_close(atg.hit.proc_damage, 300.0);
    assert_close(ukulele.hit.proc_damage, 80.0);

    assert!(atg.hit.proc_mask.contains(ProcKind::Atg));
    assert!(!atg.hit.proc_mask.contains(ProcKind::Ukulele));

    assert!(ukulele.hit.proc_mask.contains(ProcKind::Ukulele));
    assert!(!ukulele.hit.proc_mask.contains(ProcKind::Atg));

    // These are independent branches.
    assert!(atg.hit.proc_mask.contains(ProcKind::Atg));
    assert!(!atg.hit.proc_mask.contains(ProcKind::Ukulele));

    assert!(ukulele.hit.proc_mask.contains(ProcKind::Ukulele));
    assert!(!ukulele.hit.proc_mask.contains(ProcKind::Atg));
}

#[test]
fn atg_then_ukulele() {
    let root = Hit::root(10.0, 100.0, 1.0);

    let atg_probability = effective_proc_chance(0.10, root.proc_coefficient, 0);

    let atg = root
        .spawn_total_damage_proc(ProcKind::Atg, 3.0, 1.0)
        .unwrap();

    let ukulele_probability = effective_proc_chance(0.25, atg.proc_coefficient, 0);

    let ukulele = atg
        .spawn_total_damage_proc(ProcKind::Ukulele, 0.8, 0.2)
        .unwrap();

    assert_close(atg_probability * ukulele_probability, 0.025);

    assert_close(atg.proc_damage, 300.0);
    assert_close(ukulele.proc_damage, 240.0);

    assert!(ukulele.proc_mask.contains(ProcKind::Atg));
    assert!(ukulele.proc_mask.contains(ProcKind::Ukulele));

    // AtG cannot appear twice in the same proc chain.
    assert!(
        ukulele
            .spawn_total_damage_proc(ProcKind::Atg, 3.0, 1.0,)
            .is_none()
    );
}

#[test]
fn ukulele_then_atg() {
    let root = Hit::root(10.0, 100.0, 1.0);

    let ukulele_probability = effective_proc_chance(0.25, root.proc_coefficient, 0);

    let ukulele = root
        .spawn_total_damage_proc(ProcKind::Ukulele, 0.8, 0.2)
        .unwrap();

    let atg_probability = effective_proc_chance(0.10, ukulele.proc_coefficient, 0);

    let atg = ukulele
        .spawn_total_damage_proc(ProcKind::Atg, 3.0, 1.0)
        .unwrap();

    assert_close(ukulele_probability * atg_probability, 0.005);

    assert_close(ukulele.proc_damage, 80.0);
    assert_close(atg.proc_damage, 240.0);
}

#[test]
fn luck_modifies_each_roll() {
    // No luck.
    let atg = effective_proc_chance(0.10, 1.0, 0);
    let ukulele = effective_proc_chance(0.25, 1.0, 0);

    assert_close(atg * ukulele, 0.025);

    // One 57 Leaf Clover.
    let atg = effective_proc_chance(0.10, 1.0, 1);
    let ukulele = effective_proc_chance(0.25, 1.0, 1);

    assert_close(atg, 0.19);
    assert_close(ukulele, 0.4375);
    assert_close(atg * ukulele, 0.083125);

    // One Purity.
    let atg = effective_proc_chance(0.10, 1.0, -1);
    let ukulele = effective_proc_chance(0.25, 1.0, -1);

    assert_close(atg, 0.01);
    assert_close(ukulele, 0.0625);
    assert_close(atg * ukulele, 0.000625);
}

#[test]
fn low_proc_coefficient_scales_bleed_chance_and_duration() {
    let root = Hit::root(10.0, 100.0, 0.5);

    let on_hit_effects = [OnHitEffect::Bleed(BleedProc { base_chance: 0.10 })];

    let targets = TargetContext::isolated();

    let outcomes = enumerate_direct_proc_outcomes(&root, &on_hit_effects, &targets, 0);

    assert_eq!(outcomes.len(), 2);

    let no_bleed = outcomes
        .iter()
        .find(|outcome| outcome.effects.is_empty())
        .unwrap();

    assert_close(no_bleed.probability, 0.95);

    let bleed_outcome = outcomes
        .iter()
        .find(|outcome| outcome.bleeds().count() == 1)
        .unwrap();

    // 10% Tri-Tip chance × 0.5 proc coefficient.
    assert_close(bleed_outcome.probability, 0.05);

    let bleed = bleed_outcome.bleeds().next().unwrap();

    // 3 seconds × 0.5 proc coefficient.
    assert_close(bleed.duration_seconds, 1.5);

    assert_close(bleed.ticks_per_second, 4.0);

    // 20% of 10 character base damage.
    assert_close(bleed.damage_per_tick, 2.0);

    // 1.5 seconds × 4 ticks/sec.
    assert_close(bleed.nominal_ticks(), 6.0);

    // 6 ticks × 2 damage.
    assert_close(bleed.nominal_total_damage(), 12.0);

    let expected_bleed_damage: f64 = outcomes
        .iter()
        .flat_map(|outcome| {
            outcome
                .bleeds()
                .map(move |bleed| outcome.probability * bleed.nominal_total_damage())
        })
        .sum();

    // 5% × 12 conditional damage.
    assert_close(expected_bleed_damage, 0.6);
    assert_eq!(bleed.target, TargetId::PRIMARY,);
}

#[test]
fn final_damage_does_not_feed_total_damage_procs() {
    let mut root = Hit::root(10.0, 100.0, 1.0);

    // Pretend this is one Armor-Piercing Rounds against a boss.
    root.apply_final_damage_multiplier(1.2);

    assert_close(root.proc_damage, 100.0);
    assert_close(root.final_damage, 120.0);

    let mut atg = root
        .spawn_total_damage_proc(ProcKind::Atg, 3.0, 1.0)
        .unwrap();

    // AtG inherits 100, NOT the modified 120.
    assert_close(atg.proc_damage, 300.0);

    // AP Rounds then independently modifies the AtG hit.
    atg.apply_final_damage_multiplier(1.2);

    assert_close(atg.proc_damage, 300.0);
    assert_close(atg.final_damage, 360.0);

    let ukulele = atg
        .spawn_total_damage_proc(ProcKind::Ukulele, 0.8, 0.2)
        .unwrap();

    // This is the critical assertion:
    //
    // 300 * 0.8 = 240
    //
    // NOT:
    //
    // 360 * 0.8 = 288
    assert_close(ukulele.proc_damage, 240.0);
}

#[test]
fn ukulele_creates_one_hit_per_available_target_up_to_cap() {
    let root = Hit::root(10.0, 100.0, 1.0);

    let on_hit_effects = [OnHitEffect::TotalDamage(TotalDamageProc {
        kind: ProcKind::Ukulele,

        // Guaranteed here so we're testing
        // target expansion rather than RNG.
        base_chance: 1.0,

        damage_multiplier: 0.8,
        proc_coefficient: 0.2,

        targeting: AttackTargeting::Chain {
            max_targets: 3,
            radius_m: 20.0,
        },
    })];

    let targets = TargetContext::with_secondary_targets(5);

    let outcomes = enumerate_direct_proc_outcomes(&root, &on_hit_effects, &targets, 0);

    // Guaranteed proc, so only one outcome.
    assert_eq!(outcomes.len(), 1);

    let outcome = &outcomes[0];

    assert_close(outcome.probability, 1.0);

    // Five enemies are available, but one Ukulele
    // can contact at most three.
    assert_eq!(outcome.hits().count(), 3,);

    let contacted_targets: Vec<_> = outcome.hits().map(|hit| hit.hit.target).collect();

    assert_eq!(
        contacted_targets,
        vec![TargetId::new(1), TargetId::new(2), TargetId::new(3),],
    );

    assert!(!contacted_targets.contains(&TargetId::PRIMARY));

    for hit in outcome.hits() {
        assert_eq!(hit.source, ProcKind::Ukulele,);

        assert_close(hit.hit.proc_damage, 80.0);

        assert_close(hit.hit.proc_coefficient, 0.2);

        assert!(hit.hit.proc_mask.contains(ProcKind::Ukulele));
    }

    // Three contacts × 80 damage.
    let generated_damage: f64 = outcome.hits().map(|hit| hit.hit.final_damage).sum();

    assert_close(generated_damage, 240.0);
}

#[test]
fn multi_target_ukulele_contacts_proc_independently() {
    let root = Hit::root(10.0, 100.0, 1.0);

    let on_hit_effects = [
        OnHitEffect::TotalDamage(TotalDamageProc {
            kind: ProcKind::Atg,
            base_chance: 0.10,
            damage_multiplier: 3.0,
            proc_coefficient: 1.0,
            targeting: AttackTargeting::SingleTarget,
        }),
        OnHitEffect::TotalDamage(TotalDamageProc {
            kind: ProcKind::Ukulele,
            base_chance: 0.25,
            damage_multiplier: 0.8,
            proc_coefficient: 0.2,
            targeting: AttackTargeting::Chain {
                max_targets: 3,
                radius_m: 20.0,
            },
        }),
    ];

    let targets = TargetContext::with_secondary_targets(3);

    let outcomes = enumerate_proc_tree_outcomes(&root, &on_hit_effects, &targets, 0);

    let total_probability: f64 = outcomes.iter().map(|outcome| outcome.probability).sum();

    assert_close(total_probability, 1.0);

    let expected_generated_damage: f64 = outcomes
        .iter()
        .map(|outcome| outcome.probability * outcome.total_generated_damage())
        .sum();

    assert_close(expected_generated_damage, 111.6);
}

#[test]
fn ukulele_contacts_have_distinct_target_ids() {
    let root = Hit::root(10.0, 100.0, 1.0);

    assert_eq!(root.target, TargetId::PRIMARY);

    let effects = [OnHitEffect::TotalDamage(TotalDamageProc {
        kind: ProcKind::Ukulele,
        base_chance: 1.0,
        damage_multiplier: 0.8,
        proc_coefficient: 0.2,

        targeting: AttackTargeting::Chain {
            max_targets: 3,
            radius_m: 20.0,
        },
    })];

    let targets = TargetContext::with_secondary_targets(5);

    let outcomes = enumerate_direct_proc_outcomes(&root, &effects, &targets, 0);

    assert_eq!(outcomes.len(), 1);

    let contacted_targets: Vec<_> = outcomes[0].hits().map(|hit| hit.hit.target).collect();

    assert_eq!(
        contacted_targets,
        vec![TargetId::new(1), TargetId::new(2), TargetId::new(3),],
    );

    assert!(!contacted_targets.contains(&TargetId::PRIMARY));
}

#[test]
fn single_target_proc_stays_on_triggering_contact_target() {
    let root = Hit::root(10.0, 100.0, 1.0);

    let targets = TargetContext::with_secondary_targets(1);

    let ukulele_effects = [OnHitEffect::TotalDamage(TotalDamageProc {
        kind: ProcKind::Ukulele,
        base_chance: 1.0,
        damage_multiplier: 0.8,
        proc_coefficient: 0.2,

        targeting: AttackTargeting::Chain {
            max_targets: 3,
            radius_m: 20.0,
        },
    })];

    let ukulele_outcomes = enumerate_direct_proc_outcomes(&root, &ukulele_effects, &targets, 0);

    let ukulele_hit = ukulele_outcomes[0].hits().next().unwrap().hit.clone();

    assert_eq!(ukulele_hit.target, TargetId::new(1),);

    let atg_effects = [OnHitEffect::TotalDamage(TotalDamageProc {
        kind: ProcKind::Atg,

        // 5.0 × Ukulele's 0.2 PC = 100%
        // for deterministic testing.
        base_chance: 5.0,

        damage_multiplier: 3.0,
        proc_coefficient: 1.0,

        targeting: AttackTargeting::SingleTarget,
    })];

    let outcomes = enumerate_proc_tree_outcomes(&ukulele_hit, &atg_effects, &targets, 0);

    assert_eq!(outcomes.len(), 1);
    assert_eq!(outcomes[0].effects.len(), 1);

    let ResolvedEffect::Hit(atg) = &outcomes[0].effects[0] else {
        panic!("expected AtG hit");
    };

    assert_eq!(atg.hit.target, TargetId::new(1),);

    assert_eq!(atg.hit.target, ukulele_hit.target,);
}

#[test]
fn health_threshold_modifier_only_applies_above_threshold() {
    let modifier = FinalDamageModifier {
        condition: DamageCondition::TargetHealthAbove { fraction: 0.90 },

        bonus_per_stack: 0.75,
        stacks: 1,
    };

    let above = Target::new(TargetId::PRIMARY, 91.0, 100.0, 0.0, false);

    let exactly = Target::new(TargetId::PRIMARY, 90.0, 100.0, 0.0, false);

    let below = Target::new(TargetId::PRIMARY, 50.0, 100.0, 0.0, false);

    let mut hit = Hit::root(10.0, 100.0, 1.0);

    apply_final_damage_modifiers(&mut hit, &above, &[modifier]);

    assert_close(hit.final_damage, 175.0);

    let mut hit = Hit::root(10.0, 100.0, 1.0);

    apply_final_damage_modifiers(&mut hit, &exactly, &[modifier]);

    assert_close(hit.final_damage, 100.0);

    let mut hit = Hit::root(10.0, 100.0, 1.0);

    apply_final_damage_modifiers(&mut hit, &below, &[modifier]);

    assert_close(hit.final_damage, 100.0);
}

#[test]
fn health_threshold_modifier_stacks_linearly() {
    let target = Target::full_health(TargetId::PRIMARY, 1000.0);

    let modifier = FinalDamageModifier {
        condition: DamageCondition::TargetHealthAbove { fraction: 0.90 },

        bonus_per_stack: 0.75,
        stacks: 2,
    };

    let mut hit = Hit::root(10.0, 100.0, 1.0);

    apply_final_damage_modifiers(&mut hit, &target, &[modifier]);

    // 1 + 0.75 + 0.75 = 2.5
    assert_close(hit.final_damage, 250.0);
}

#[test]
fn health_threshold_bonus_does_not_feed_total_damage_proc() {
    let target = Target::full_health(TargetId::PRIMARY, 10_000.0);

    let modifier = FinalDamageModifier {
        condition: DamageCondition::TargetHealthAbove { fraction: 0.90 },

        bonus_per_stack: 0.75,
        stacks: 1,
    };

    let mut root = Hit::root(10.0, 100.0, 1.0);

    apply_final_damage_modifiers(&mut root, &target, &[modifier]);

    assert_close(root.proc_damage, 100.0);

    assert_close(root.final_damage, 175.0);

    let atg = root
        .spawn_total_damage_proc(ProcKind::Atg, 3.0, 1.0)
        .unwrap();

    // Crowbar's 175 damage does NOT become:
    //
    // 175 * 3 = 525
    //
    // AtG inherits the unmodified 100.
    assert_close(atg.proc_damage, 300.0);
}

#[test]
fn resolved_hit_reduces_target_health() {
    let primary = Target::new(TargetId::PRIMARY, 1000.0, 1000.0, 0.0, false);

    let mut targets = TargetContext::new(primary, Vec::new());

    let hit = Hit::root(10.0, 100.0, 1.0);

    let resolution = resolve_and_apply_hit(&hit, &mut targets, &[]);

    assert_close(resolution.hit.final_damage, 100.0);

    assert_close(resolution.target_health_before, 1000.0);

    assert_close(resolution.target_health_after, 900.0);

    assert_close(resolution.damage_dealt(), 100.0);

    assert!(!resolution.killed_target());
}

#[test]
fn crowbar_can_turn_off_during_a_proc_chain() {
    let primary = Target::new(
        TargetId::PRIMARY,
        // 95% HP.
        950.0,
        1000.0,
        0.0,
        false,
    );

    let mut targets = TargetContext::new(primary, Vec::new());

    let crowbar = FinalDamageModifier {
        condition: DamageCondition::TargetHealthAbove { fraction: 0.90 },

        bonus_per_stack: 0.75,
        stacks: 1,
    };

    let root = Hit::root(10.0, 100.0, 1.0);

    let root_resolution = resolve_and_apply_hit(&root, &mut targets, &[crowbar]);

    // Target starts above 90%:
    //
    // 100 × 1.75 = 175
    assert_close(root_resolution.hit.proc_damage, 100.0);

    assert_close(root_resolution.hit.final_damage, 175.0);

    assert_close(root_resolution.target_health_after, 775.0);

    let atg = root_resolution
        .hit
        .spawn_total_damage_proc(ProcKind::Atg, 3.0, 1.0)
        .unwrap();

    // Crowbar did not feed into TOTAL damage.
    assert_close(atg.proc_damage, 300.0);

    let atg_resolution = resolve_and_apply_hit(&atg, &mut targets, &[crowbar]);

    // Target is now at 77.5% HP,
    // so Crowbar no longer qualifies.
    assert_close(atg_resolution.hit.proc_damage, 300.0);

    assert_close(atg_resolution.hit.final_damage, 300.0);

    assert_close(atg_resolution.target_health_before, 775.0);

    assert_close(atg_resolution.target_health_after, 475.0);
}

#[test]
fn target_health_does_not_go_below_zero() {
    let primary = Target::new(TargetId::PRIMARY, 50.0, 100.0, 0.0, false);

    let mut targets = TargetContext::new(primary, Vec::new());

    let hit = Hit::root(10.0, 100.0, 1.0);

    resolve_and_apply_hit(&hit, &mut targets, &[]);

    assert_close(targets.target(TargetId::PRIMARY).unwrap().health(), 0.0);
}

#[test]
fn hit_resolution_detects_kills_and_actual_damage_dealt() {
    let primary = Target::new(TargetId::PRIMARY, 50.0, 100.0, 0.0, false);

    let mut targets = TargetContext::new(primary, Vec::new());

    let hit = Hit::root(10.0, 100.0, 1.0);

    let resolution = resolve_and_apply_hit(&hit, &mut targets, &[]);

    // Raw hit is still 100.
    assert_close(resolution.hit.final_damage, 100.0);

    // But only 50 HP actually existed.
    assert_close(resolution.damage_dealt(), 50.0);

    assert_close(resolution.target_health_after, 0.0);

    assert!(resolution.killed_target());
}

#[test]
fn root_damage_is_applied_before_proc_branches_are_created() {
    let primary = Target::new(TargetId::PRIMARY, 1000.0, 1000.0, 0.0, false);

    let targets = TargetContext::new(primary, vec![Target::full_health(TargetId::new(1), 1000.0)]);

    let root = Hit::root(10.0, 100.0, 1.0);

    let effects = [
        OnHitEffect::TotalDamage(TotalDamageProc {
            kind: ProcKind::Atg,
            base_chance: 0.10,
            damage_multiplier: 3.0,
            proc_coefficient: 1.0,
            targeting: AttackTargeting::SingleTarget,
        }),
        OnHitEffect::TotalDamage(TotalDamageProc {
            kind: ProcKind::Ukulele,
            base_chance: 0.25,
            damage_multiplier: 0.8,
            proc_coefficient: 0.2,

            targeting: AttackTargeting::Chain {
                max_targets: 3,
                radius_m: 20.0,
            },
        }),
    ];

    let branches = begin_combat_branches(&root, &effects, &targets, &[], 0);

    // Same four direct outcomes as before:
    //
    // neither
    // AtG
    // Ukulele
    // both
    assert_eq!(branches.len(), 4);

    let total_probability: f64 = branches.iter().map(|branch| branch.probability).sum();

    assert_close(total_probability, 1.0);

    // Root hit happened BEFORE branching, so every
    // branch starts with the primary at 900 HP.
    for branch in &branches {
        let primary = branch.targets.target(TargetId::PRIMARY).unwrap();

        assert_close(primary.health(), 900.0);

        assert_close(branch.root_resolution.hit.final_damage, 100.0);
    }
}

#[test]
fn combat_branches_have_independent_target_state() {
    let primary = Target::full_health(TargetId::PRIMARY, 1000.0);

    let targets = TargetContext::new(primary, Vec::new());

    let root = Hit::root(10.0, 100.0, 1.0);

    let effects = [OnHitEffect::Bleed(BleedProc { base_chance: 0.5 })];

    let mut branches = begin_combat_branches(&root, &effects, &targets, &[], 0);

    assert_eq!(branches.len(), 2);

    // Both branches initially see:
    //
    // 1000 - 100 = 900 HP
    for branch in &branches {
        assert_close(
            branch.targets.target(TargetId::PRIMARY).unwrap().health(),
            900.0,
        );
    }

    // Mutate only branch 0.
    branches[0]
        .targets
        .target_mut(TargetId::PRIMARY)
        .unwrap()
        .apply_damage(200.0);

    assert_close(
        branches[0]
            .targets
            .target(TargetId::PRIMARY)
            .unwrap()
            .health(),
        700.0,
    );

    // Branch 1 MUST remain unchanged.
    assert_close(
        branches[1]
            .targets
            .target(TargetId::PRIMARY)
            .unwrap()
            .health(),
        900.0,
    );
}

#[test]
fn crowbar_root_damage_is_applied_before_pending_atg() {
    let primary = Target::new(TargetId::PRIMARY, 950.0, 1000.0, 0.0, false);

    let targets = TargetContext::new(primary, Vec::new());

    let root = Hit::root(10.0, 100.0, 1.0);

    let effects = [OnHitEffect::TotalDamage(TotalDamageProc {
        kind: ProcKind::Atg,

        // Guaranteed purely for this test.
        base_chance: 1.0,

        damage_multiplier: 3.0,
        proc_coefficient: 1.0,
        targeting: AttackTargeting::SingleTarget,
    })];

    let crowbar = FinalDamageModifier {
        condition: DamageCondition::TargetHealthAbove { fraction: 0.90 },

        bonus_per_stack: 0.75,
        stacks: 1,
    };

    let branches = begin_combat_branches(&root, &effects, &targets, &[crowbar], 0);

    assert_eq!(branches.len(), 1);

    let branch = &branches[0];

    // Root qualified for Crowbar:
    //
    // 100 * 1.75 = 175
    assert_close(branch.root_resolution.hit.final_damage, 175.0);

    // 950 - 175 = 775.
    assert_close(
        branch.targets.target(TargetId::PRIMARY).unwrap().health(),
        775.0,
    );

    let atg = branch.pending_hits().next().unwrap();

    // Still inherits proc_damage, NOT final_damage:
    //
    // 100 * 3 = 300
    assert_close(atg.hit.proc_damage, 300.0);

    // AtG has not landed yet.
    assert_close(
        branch.targets.target(TargetId::PRIMARY).unwrap().health(),
        775.0,
    );
}

#[test]
fn positive_armor_reduces_damage() {
    assert_close(armor_damage_multiplier(100.0), 0.5);

    assert_close(apply_armor(100.0, 100.0), 50.0);
}

#[test]
fn negative_armor_increases_damage() {
    assert_close(armor_damage_multiplier(-100.0), 1.5);

    assert_close(apply_armor(100.0, -100.0), 150.0);
}

#[test]
fn resolved_hit_applies_target_armor() {
    let primary = Target::new(
        TargetId::PRIMARY,
        1000.0,
        1000.0,
        // 50% damage reduction.
        100.0,
        false,
    );

    let mut targets = TargetContext::new(primary, Vec::new());

    let hit = Hit::root(10.0, 100.0, 1.0);

    let resolution = resolve_and_apply_hit(&hit, &mut targets, &[]);

    // Proc inheritance remains 100.
    assert_close(resolution.hit.proc_damage, 100.0);

    // But this target only receives 50.
    assert_close(resolution.hit.final_damage, 50.0);

    assert_close(resolution.damage_dealt(), 50.0);

    assert_close(resolution.target_health_after, 950.0);
}

#[test]
fn armor_cannot_reduce_positive_hit_below_one_damage() {
    assert_close(apply_armor(1.0, 10_000.0), 1.0);
}

#[test]
fn boss_damage_modifier_only_applies_to_bosses() {
    let modifier = FinalDamageModifier {
        condition: DamageCondition::TargetIsBoss,

        bonus_per_stack: 0.20,
        stacks: 1,
    };

    let boss = Target::new(TargetId::PRIMARY, 1000.0, 1000.0, 0.0, true);

    let normal_enemy = Target::new(TargetId::PRIMARY, 1000.0, 1000.0, 0.0, false);

    let mut boss_hit = Hit::root(10.0, 100.0, 1.0);

    apply_final_damage_modifiers(&mut boss_hit, &boss, &[modifier]);

    assert_close(boss_hit.final_damage, 120.0);

    let mut normal_hit = Hit::root(10.0, 100.0, 1.0);

    apply_final_damage_modifiers(&mut normal_hit, &normal_enemy, &[modifier]);

    assert_close(normal_hit.final_damage, 100.0);
}

#[test]
fn boss_damage_modifier_stacks_linearly() {
    let boss = Target::new(TargetId::PRIMARY, 1000.0, 1000.0, 0.0, true);

    let modifier = FinalDamageModifier {
        condition: DamageCondition::TargetIsBoss,

        bonus_per_stack: 0.20,
        stacks: 3,
    };

    let mut hit = Hit::root(10.0, 100.0, 1.0);

    apply_final_damage_modifiers(&mut hit, &boss, &[modifier]);

    // 1 + 0.20 * 3 = 1.6
    assert_close(hit.final_damage, 160.0);
}
