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
        }),
        OnHitEffect::TotalDamage(TotalDamageProc {
            kind: ProcKind::Ukulele,
            base_chance: 0.25,
            damage_multiplier: 0.8,
            proc_coefficient: 0.2,
        }),
    ];

    let outcomes = enumerate_proc_tree_outcomes(&root, &on_hit_effects, 0);

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
        }),
        OnHitEffect::TotalDamage(TotalDamageProc {
            kind: ProcKind::Ukulele,
            base_chance: 0.25,
            damage_multiplier: 0.8,
            proc_coefficient: 0.2,
        }),
    ];

    let outcomes = enumerate_direct_proc_outcomes(&root, &on_hit_effects, 0);

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

    let outcomes = enumerate_direct_proc_outcomes(&root, &on_hit_effects, 0);

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
