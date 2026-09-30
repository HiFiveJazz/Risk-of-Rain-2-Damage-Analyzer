use super::*;
use crate::combat::*;

const EPSILON: f64 = 1e-12;

fn assert_close(actual: f64, expected: f64) {
    assert!(
        (actual - expected).abs() < EPSILON,
        "expected {expected}, got {actual}"
    );
}

#[test]
fn inventory_tracks_item_stacks() {
    let mut inventory = Inventory::new();

    assert_eq!(inventory.stack_count(ItemKind::AtgMissile), 0);

    inventory.add(ItemKind::AtgMissile, 2);
    inventory.add(ItemKind::TriTipDagger, 4);

    assert_eq!(inventory.stack_count(ItemKind::AtgMissile), 2);

    assert_eq!(inventory.stack_count(ItemKind::TriTipDagger), 4);

    inventory.remove(ItemKind::AtgMissile, 1);

    assert_eq!(inventory.stack_count(ItemKind::AtgMissile), 1);
}

#[test]
fn inventory_builds_atg_effect_from_stacks() {
    let mut inventory = Inventory::new();

    inventory.add(ItemKind::AtgMissile, 2);

    let effects = inventory.on_hit_effects();

    assert_eq!(effects.len(), 1);

    let OnHitEffect::TotalDamage(atg) = effects[0] else {
        panic!("expected total damage proc");
    };

    assert_eq!(atg.kind, ProcKind::Atg);

    assert_close(atg.base_chance, 0.10);

    // Two AtGs:
    //
    // 300% + 300% = 600%
    assert_close(atg.damage_multiplier, 6.0);

    assert_close(atg.proc_coefficient, 1.0);
}

#[test]
fn ukulele_stacks_increase_target_count_and_radius() {
    let mut inventory = Inventory::new();

    inventory.add(ItemKind::Ukulele, 3);

    let effects = inventory.on_hit_effects();

    assert_eq!(effects.len(), 1);

    let OnHitEffect::TotalDamage(ukulele) = effects[0] else {
        panic!("expected total damage proc");
    };

    assert_eq!(ukulele.kind, ProcKind::Ukulele);

    // Still 25%.
    assert_close(ukulele.base_chance, 0.25);

    // Still 80% TOTAL damage per target.
    assert_close(ukulele.damage_multiplier, 0.80);

    // Still a 0.2 proc coefficient per lightning hit.
    assert_close(ukulele.proc_coefficient, 0.20);

    let AttackTargeting::Chain {
        max_targets,
        radius_m,
    } = ukulele.targeting
    else {
        panic!("expected chain targeting");
    };

    // 3 + 2 + 2
    assert_eq!(max_targets, 7,);

    // 20 + 2 + 2
    assert_close(radius_m, 24.0);
}

#[test]
fn tri_tip_stacks_increase_bleed_chance() {
    let mut inventory = Inventory::new();

    inventory.add(ItemKind::TriTipDagger, 4);

    let effects = inventory.on_hit_effects();

    assert_eq!(effects.len(), 1);

    let OnHitEffect::Bleed(bleed) = effects[0] else {
        panic!("expected bleed proc");
    };

    assert_close(bleed.base_chance, 0.40);
}

#[test]
fn inventory_can_drive_proc_tree_evaluation() {
    let mut inventory = Inventory::new();

    inventory.add(ItemKind::AtgMissile, 1);
    inventory.add(ItemKind::Ukulele, 1);

    let effects = inventory.on_hit_effects();

    let root = Hit::root(10.0, 100.0, 1.0);

    let targets = TargetContext::with_secondary_targets(1);

    let outcomes = enumerate_proc_tree_outcomes(&root, &effects, &targets, 0);

    assert_eq!(outcomes.len(), 9);

    let total_probability: f64 = outcomes.iter().map(|outcome| outcome.probability).sum();

    assert_close(total_probability, 1.0);

    let expected_generated_damage: f64 = outcomes
        .iter()
        .map(|outcome| outcome.probability * outcome.total_generated_damage())
        .sum();

    assert_close(expected_generated_damage, 57.2);
}

#[test]
fn inventory_builds_crowbar_modifier_from_stacks() {
    let mut inventory = Inventory::new();

    inventory.add(ItemKind::Crowbar, 2);

    let modifiers = inventory.final_damage_modifiers();

    assert_eq!(modifiers.len(), 1,);

    let modifier = modifiers[0];

    assert_eq!(
        modifier.condition,
        DamageCondition::TargetHealthAbove { fraction: 0.90 },
    );

    assert_close(modifier.bonus_per_stack, 0.75);

    assert_eq!(modifier.stacks, 2,);
}

#[test]
fn inventory_builds_armor_piercing_rounds_modifier() {
    let mut inventory = Inventory::new();

    inventory.add(ItemKind::ArmorPiercingRounds, 3);

    let modifiers = inventory.final_damage_modifiers();

    assert_eq!(modifiers.len(), 1,);

    let modifier = modifiers[0];

    assert_eq!(modifier.condition, DamageCondition::TargetIsBoss,);

    assert_close(modifier.bonus_per_stack, 0.20);

    assert_eq!(modifier.stacks, 3,);
}
