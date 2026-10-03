use crate::combat::{Hit, SimulationResult, TargetContext, simulate_attack};
use crate::items::Inventory;

pub fn simulate_inventory_attack(
    root_hit: &Hit,
    inventory: &Inventory,
    target_context: &TargetContext,
    luck: i32,
) -> SimulationResult {
    let on_hit_effects = inventory.on_hit_effects();

    let modifiers = inventory.final_damage_modifiers();

    simulate_attack(root_hit, &on_hit_effects, target_context, &modifiers, luck)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{ItemKind, Target, TargetId};

    const EPSILON: f64 = 1e-12;

    fn assert_close(actual: f64, expected: f64) {
        assert!(
            (actual - expected).abs() < EPSILON,
            "expected {expected}, got {actual}",
        );
    }

    #[test]
    fn empty_inventory_simulates_plain_attack() {
        let inventory = Inventory::new();

        let target = Target::full_health(TargetId::PRIMARY, 10_000.0);

        let targets = TargetContext::new(target, Vec::new());

        let root = Hit::root(10.0, 100.0, 1.0);

        let simulation = simulate_inventory_attack(&root, &inventory, &targets, 0);

        assert!(simulation.is_complete());

        assert_close(simulation.expected_complete_damage().unwrap(), 100.0);
    }

    #[test]
    fn inventory_simulation_respects_crowbar_state_changes() {
        let mut inventory = Inventory::new();

        inventory.add(ItemKind::AtgMissile, 1);

        inventory.add(ItemKind::Crowbar, 1);

        let target = Target::new(
            TargetId::PRIMARY,
            // Starts at 95%.
            950.0,
            1000.0,
            0.0,
            false,
        );

        let targets = TargetContext::new(target, Vec::new());

        let root = Hit::root(10.0, 100.0, 1.0);

        let simulation = simulate_inventory_attack(&root, &inventory, &targets, 0);

        assert!(simulation.is_complete());

        // Root qualifies for Crowbar:
        //
        // 100 * 1.75 = 175
        //
        // Target:
        //
        // 950 -> 775
        //
        // Now Crowbar is OFF.
        //
        // AtG:
        //
        // 10% * 300 damage
        //
        // Expected:
        //
        // 175 + 0.10 * 300
        // = 205
        assert_close(simulation.expected_complete_damage().unwrap(), 205.0);
    }

    #[test]
    fn inventory_simulation_combines_atg_and_ap_rounds() {
        let mut inventory = Inventory::new();

        inventory.add(ItemKind::AtgMissile, 1);

        inventory.add(ItemKind::ArmorPiercingRounds, 1);

        let boss = Target::new(TargetId::PRIMARY, 10_000.0, 10_000.0, 0.0, true);

        let targets = TargetContext::new(boss, Vec::new());

        let root = Hit::root(10.0, 100.0, 1.0);

        let simulation = simulate_inventory_attack(&root, &inventory, &targets, 0);

        assert!(simulation.is_complete());

        assert_eq!(simulation.branches.len(), 2,);

        assert_close(simulation.probability_mass(), 1.0);

        assert_close(simulation.expected_complete_damage().unwrap(), 156.0);
    }
}
