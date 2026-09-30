use std::collections::HashMap;

use crate::{
    AttackTargeting,
    combat::{
        BleedProc, DamageCondition, FinalDamageModifier, OnHitEffect, ProcKind, TotalDamageProc,
    },
};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum ItemKind {
    AtgMissile,
    Ukulele,
    TriTipDagger,
    Crowbar,
    ArmorPiercingRounds,
}

#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct Inventory {
    stacks: HashMap<ItemKind, u32>,
}

impl Inventory {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn stack_count(&self, item: ItemKind) -> u32 {
        self.stacks.get(&item).copied().unwrap_or(0)
    }

    pub fn add(&mut self, item: ItemKind, count: u32) {
        if count == 0 {
            return;
        }

        *self.stacks.entry(item).or_insert(0) += count;
    }

    pub fn remove(&mut self, item: ItemKind, count: u32) {
        if count == 0 {
            return;
        }

        let Some(current) = self.stacks.get_mut(&item) else {
            return;
        };

        *current = current.saturating_sub(count);

        if *current == 0 {
            self.stacks.remove(&item);
        }
    }

    pub fn on_hit_effects(&self) -> Vec<OnHitEffect> {
        let mut effects = Vec::new();

        let atg_stacks = self.stack_count(ItemKind::AtgMissile);

        if atg_stacks > 0 {
            effects.push(OnHitEffect::TotalDamage(TotalDamageProc {
                kind: ProcKind::Atg,

                // Stacking AtG increases damage,
                // not activation chance.
                base_chance: 0.10,

                // 300% TOTAL damage per stack.
                damage_multiplier: 3.0 * f64::from(atg_stacks),

                proc_coefficient: 1.0,

                targeting: AttackTargeting::SingleTarget,
            }));
        }

        let ukulele_stacks = self.stack_count(ItemKind::Ukulele);

        if ukulele_stacks > 0 {
            let additional_stacks = ukulele_stacks - 1;

            let max_targets = 3 + (2 * additional_stacks);

            let radius_m = 20.0 + (2.0 * f64::from(additional_stacks));

            effects.push(OnHitEffect::TotalDamage(TotalDamageProc {
                kind: ProcKind::Ukulele,
                base_chance: 0.25,
                damage_multiplier: 0.80,
                proc_coefficient: 0.20,

                targeting: AttackTargeting::Chain {
                    max_targets,
                    radius_m,
                },
            }));
        }

        let tri_tip_stacks = self.stack_count(ItemKind::TriTipDagger);

        if tri_tip_stacks > 0 {
            effects.push(OnHitEffect::Bleed(BleedProc {
                // +10 percentage points per stack.
                base_chance: 0.10 * f64::from(tri_tip_stacks),
            }));
        }

        effects
    }

    pub fn final_damage_modifiers(&self) -> Vec<FinalDamageModifier> {
        let mut modifiers = Vec::new();

        let crowbar_stacks = self.stack_count(ItemKind::Crowbar);

        if crowbar_stacks > 0 {
            modifiers.push(FinalDamageModifier {
                condition: DamageCondition::TargetHealthAbove { fraction: 0.90 },

                bonus_per_stack: 0.75,

                stacks: crowbar_stacks,
            });
        }

        let ap_rounds_stacks = self.stack_count(ItemKind::ArmorPiercingRounds);

        if ap_rounds_stacks > 0 {
            modifiers.push(FinalDamageModifier {
                condition: DamageCondition::TargetIsBoss,

                bonus_per_stack: 0.20,
                stacks: ap_rounds_stacks,
            });
        }

        modifiers
    }
}
