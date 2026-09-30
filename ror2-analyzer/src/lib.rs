use std::collections::HashSet;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum ProcKind {
    Atg,
    Ukulele,
    StickyBomb,
}

#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct ProcMask {
    seen: HashSet<ProcKind>,
}

impl ProcMask {
    pub fn contains(&self, proc_kind: ProcKind) -> bool {
        self.seen.contains(&proc_kind)
    }

    pub fn insert(&mut self, proc_kind: ProcKind) {
        self.seen.insert(proc_kind);
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Hit {
    /// Character damage stat used by BASE-damage effects such as Bleed.
    pub attacker_base_damage: f64,

    /// Damage inherited by TOTAL-damage proc effects.
    pub proc_damage: f64,

    /// Damage this hit actually deals after hit-specific modifiers.
    pub final_damage: f64,

    /// Proc coefficient belonging to this hit.
    pub proc_coefficient: f64,

    /// Total-damage procs that have already participated in this chain.
    pub proc_mask: ProcMask,

    /// For now, child total-damage effects simply inherit crit state.
    pub crit: bool,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct TotalDamageProc {
    pub kind: ProcKind,
    pub base_chance: f64,
    pub damage_multiplier: f64,
    pub proc_coefficient: f64,
}

#[derive(Debug, Clone, PartialEq)]
pub struct ResolvedHit {
    pub source: ProcKind,
    pub hit: Hit,
    pub effects: Vec<ResolvedEffect>,
}

#[derive(Debug, Clone, PartialEq)]
pub enum ResolvedEffect {
    Hit(ResolvedHit),
    Bleed(Bleed),
}

impl ResolvedEffect {
    pub fn total_damage(&self) -> f64 {
        match self {
            ResolvedEffect::Hit(resolved_hit) => {
                resolved_hit.hit.final_damage
                    + resolved_hit
                        .effects
                        .iter()
                        .map(ResolvedEffect::total_damage)
                        .sum::<f64>()
            }

            ResolvedEffect::Bleed(bleed) => bleed.nominal_total_damage(),
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct CombatOutcome {
    pub probability: f64,
    pub effects: Vec<ResolvedEffect>,
}

impl CombatOutcome {
    /// Damage produced by proc/status effects, excluding the original hit.
    pub fn total_generated_damage(&self) -> f64 {
        self.effects.iter().map(ResolvedEffect::total_damage).sum()
    }

    /// Total damage including the original hit.
    pub fn total_damage_with_root(&self, root: &Hit) -> f64 {
        root.final_damage + self.total_generated_damage()
    }
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct BleedProc {
    pub base_chance: f64,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum OnHitEffect {
    TotalDamage(TotalDamageProc),
    Bleed(BleedProc),
}

#[derive(Debug, Clone, PartialEq)]
pub struct GeneratedHit {
    pub source: ProcKind,
    pub hit: Hit,
}

#[derive(Debug, Clone, PartialEq)]
pub struct Bleed {
    pub duration_seconds: f64,
    pub ticks_per_second: f64,
    pub damage_per_tick: f64,
}

impl Bleed {
    pub fn nominal_ticks(&self) -> f64 {
        self.duration_seconds * self.ticks_per_second
    }

    pub fn nominal_total_damage(&self) -> f64 {
        self.nominal_ticks() * self.damage_per_tick
    }
}

#[derive(Debug, Clone, PartialEq)]
pub enum GeneratedEffect {
    Hit(GeneratedHit),
    Bleed(Bleed),
}

#[derive(Debug, Clone, PartialEq)]
pub struct ProcOutcome {
    pub probability: f64,
    pub effects: Vec<GeneratedEffect>,
}

impl ProcOutcome {
    pub fn hits(&self) -> impl Iterator<Item = &GeneratedHit> {
        self.effects.iter().filter_map(|effect| match effect {
            GeneratedEffect::Hit(hit) => Some(hit),
            _ => None,
        })
    }

    pub fn bleeds(&self) -> impl Iterator<Item = &Bleed> {
        self.effects.iter().filter_map(|effect| match effect {
            GeneratedEffect::Bleed(bleed) => Some(bleed),
            _ => None,
        })
    }
}

impl Hit {
    pub fn root(attacker_base_damage: f64, proc_damage: f64, proc_coefficient: f64) -> Self {
        assert!(attacker_base_damage >= 0.0);
        assert!(proc_damage >= 0.0);
        assert!(proc_coefficient >= 0.0);

        Self {
            attacker_base_damage,
            proc_damage,
            final_damage: proc_damage,
            proc_coefficient,
            proc_mask: ProcMask::default(),
            crit: false,
        }
    }

    pub fn apply_final_damage_multiplier(&mut self, multiplier: f64) {
        assert!(multiplier >= 0.0);

        self.final_damage *= multiplier;
    }

    pub fn spawn_total_damage_proc(
        &self,
        proc_kind: ProcKind,
        damage_multiplier: f64,
        proc_coefficient: f64,
    ) -> Option<Self> {
        assert!(damage_multiplier >= 0.0);
        assert!(proc_coefficient >= 0.0);

        if self.proc_mask.contains(proc_kind) {
            return None;
        }

        let mut proc_mask = self.proc_mask.clone();
        proc_mask.insert(proc_kind);

        let proc_damage = self.proc_damage * damage_multiplier;

        Some(Self {
            attacker_base_damage: self.attacker_base_damage,
            proc_damage,
            final_damage: proc_damage,
            proc_coefficient,
            proc_mask,
            crit: self.crit,
        })
    }
}

/// Calculate the probability of an item proc.
///
/// `base_chance` belongs to the item.
/// `source_proc_coefficient` belongs to the hit attempting the proc.
///
/// Luck is applied after proc coefficient scaling.
pub fn effective_proc_chance(base_chance: f64, source_proc_coefficient: f64, luck: i32) -> f64 {
    assert!(base_chance >= 0.0);
    assert!(source_proc_coefficient >= 0.0);

    let chance = (base_chance * source_proc_coefficient).clamp(0.0, 1.0);

    match luck {
        0 => chance,

        // Favorable rerolls.
        n if n > 0 => 1.0 - (1.0 - chance).powi(n + 1),

        // Unfavorable rerolls.
        n => chance.powi((-n) + 1),
    }
}

pub fn enumerate_direct_proc_outcomes(
    source_hit: &Hit,
    on_hit_effects: &[OnHitEffect],
    luck: i32,
) -> Vec<ProcOutcome> {
    let mut outcomes = vec![ProcOutcome {
        probability: 1.0,
        effects: Vec::new(),
    }];

    for effect in on_hit_effects {
        let base_chance = match effect {
            OnHitEffect::TotalDamage(proc_effect) => {
                // A masked total-damage proc cannot participate in
                // this chain again.
                if source_hit.proc_mask.contains(proc_effect.kind) {
                    continue;
                }

                proc_effect.base_chance
            }

            OnHitEffect::Bleed(bleed) => bleed.base_chance,
        };

        let chance = effective_proc_chance(base_chance, source_hit.proc_coefficient, luck);

        let mut next_outcomes = Vec::with_capacity(outcomes.len() * 2);

        for outcome in outcomes {
            let ProcOutcome {
                probability,
                effects,
            } = outcome;

            // Effect fails.
            let failure_probability = probability * (1.0 - chance);

            if failure_probability > 0.0 {
                next_outcomes.push(ProcOutcome {
                    probability: failure_probability,
                    effects: effects.clone(),
                });
            }

            // Effect succeeds.
            let success_probability = probability * chance;

            if success_probability > 0.0 {
                let generated_effect = match effect {
                    OnHitEffect::TotalDamage(proc_effect) => {
                        let child = source_hit
                            .spawn_total_damage_proc(
                                proc_effect.kind,
                                proc_effect.damage_multiplier,
                                proc_effect.proc_coefficient,
                            )
                            .expect("proc should not be blocked after mask check");

                        GeneratedEffect::Hit(GeneratedHit {
                            source: proc_effect.kind,
                            hit: child,
                        })
                    }

                    OnHitEffect::Bleed(_) => {
                        let bleed = Bleed {
                            duration_seconds: 3.0 * source_hit.proc_coefficient,

                            ticks_per_second: 4.0,

                            damage_per_tick: source_hit.attacker_base_damage * 0.20,
                        };

                        GeneratedEffect::Bleed(bleed)
                    }
                };

                let mut success_effects = effects;
                success_effects.push(generated_effect);

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
    luck: i32,
) -> Vec<CombatOutcome> {
    let direct_outcomes = enumerate_direct_proc_outcomes(source_hit, on_hit_effects, luck);

    let mut resolved_outcomes = Vec::new();

    for direct_outcome in direct_outcomes {
        // Begin with the probability of this particular set of direct
        // proc results.
        let mut combinations = vec![CombatOutcome {
            probability: direct_outcome.probability,
            effects: Vec::new(),
        }];

        // Every directly generated effect may itself have multiple
        // possible descendant outcomes.
        for generated_effect in direct_outcome.effects {
            let alternatives = match generated_effect {
                GeneratedEffect::Bleed(bleed) => {
                    vec![CombatOutcome {
                        probability: 1.0,
                        effects: vec![ResolvedEffect::Bleed(bleed)],
                    }]
                }

                GeneratedEffect::Hit(generated_hit) => {
                    let descendant_outcomes =
                        enumerate_proc_tree_outcomes(&generated_hit.hit, on_hit_effects, luck);

                    descendant_outcomes
                        .into_iter()
                        .map(|descendants| CombatOutcome {
                            probability: descendants.probability,

                            effects: vec![ResolvedEffect::Hit(ResolvedHit {
                                source: generated_hit.source,
                                hit: generated_hit.hit.clone(),
                                effects: descendants.effects,
                            })],
                        })
                        .collect()
                }
            };

            // Cartesian product:
            //
            // If AtG has 2 possible futures and Ukulele has 2 possible
            // futures, their sibling branches together have 4 possible
            // combinations.
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

#[cfg(test)]
mod tests {
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
}
