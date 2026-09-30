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
    pub attacker_base_damage: f64,
    pub proc_damage: f64,
    pub final_damage: f64,
    pub proc_coefficient: f64,
    pub proc_mask: ProcMask,
    pub crit: bool,
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

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct TotalDamageProc {
    pub kind: ProcKind,
    pub base_chance: f64,
    pub damage_multiplier: f64,
    pub proc_coefficient: f64,
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
    pub fn total_generated_damage(&self) -> f64 {
        self.effects.iter().map(ResolvedEffect::total_damage).sum()
    }

    pub fn total_damage_with_root(&self, root: &Hit) -> f64 {
        root.final_damage + self.total_generated_damage()
    }
}
