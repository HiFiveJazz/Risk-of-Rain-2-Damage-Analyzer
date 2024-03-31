#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 07:17:25 2024

@author: jazz
"""
        
class Survivor:
    def __init__(self,
                 name,
                 base_damage,
                 damage_growth_per_level,
                 hp,
                 hp_growth,
                 hp_regen,
                 hp_regen_growth,
                 armor,
                 level,
                 ms):
        self.base_damage = base_damage 
        self.damage_growth_per_level= damage_growth_per_level 
        self.hp = hp 
        self.hp_growth = hp_growth 
        self.hp_regen = hp_regen
        self.hp_regen_growth = hp_regen_growth
        self.armor = armor
        self.level = level
        self.ms = ms

class Ability:
    def __init__(self,
                 Survivor,
                 ability_type,
                 proc_coeffecient,
                 attack_speed,
                 damage_multiplier):
        self.survivor = Survivor
        self.ability_type =  ability_type
        self.proc_coefficient = proc_coeffecient
        self.attack_speed = attack_speed
        self.damage_multiplier = damage_multiplier

#Creating Survivors and Abilities
#---------------------------------------------------------------------------------------------------------
#Acrid
acrid = Survivor("Acrid", 15, 3, 160, 48, 1.5, 0.3,  20, 1, 7)
#Primary
#Unknown cooldown/attackspeed for Acrid Primary
# acrid_primary = Survivor("Acrid", 15, (3*1.0), ?, 20, 160, 1.5, 1, 7, 3, 48, 0.3)

#Utility
#Needs to account for poison damage
acrid_caustic_leap_max_dps = Ability(acrid,"Caustic Leap", 1.0, (1/6), 5.0)
acrid_caustic_leap_min_dps = Ability(acrid,"Caustic Leap", 1.0, (1/6), 3.2)
acrid_caustic_leap_min_dps = Ability(acrid,"Frenzied Leap", 1.0, (1/10), 5.5)

#---------------------------------------------------------------------------------------------------------
#Artificer
artificier = ("Artificier", 12, 2.4, 110, 33, 0.6, 0.12, 0, 1, 7)

#Primaries
#Both of Artificer's Primaries are very similar, and so we define them as the same
artificer_flame_bolt = Ability(artificier, "Flame Bolt", 1.0, (1/1.3), 2.8) 
artificer_plasma_bolt = Ability(artificier, "Plasma Bolt", 1.0, (1/1.3), 2.8) 

#Secondaries
artificer_charged_nano_bomb_explosion_max = Ability(artificier, "Charged Nano-Bomb Explosion (Max)", 1.0, (1/5), 20.0) 
artificer_charged_nano_bomb_explosion_min = Ability(artificier, "Charged Nano-Bomb Explosion (Min)", 1.0, (1/5), 4.0) 
#Check on whether the attack speed for sparks is accurate
artificer_charged_nano_bomb_spark_max = Ability(artificier, "Charged Nano-Bomb Sparks", 0.3, (1/(5*0.125)), 20.0) 
artificer_charged_nano_bomb_spark_min = Ability(artificier, "Charged Nano-Bomb Sparks", 0.3, (1/(5*0.125)), 4.0) 

#ACCOUNT: Does not account for freezing debuff
artificer_cast_nano_spear_max = Ability(artificier, "Cast Nano-Spear (Max)", 1.0, (1/5), 12.0) 
artificer_cast_nano_spear_min = Ability(artificier, "Cast Nano-Spear (Min)", 1.0, (1/5), 4.0) 

#Utility
#ASSUMPTION: assumes all 12 pillars hit (1.0 * 12)
artificer_snapfreeze = Ability(artificier, "Snapfreeze", (1.0*12), (1/12), 1.0) 

#Special
#INCACCURATE will fix later
artificer_flamethrower = Ability(artificier, "Flamethrower", (1.0*22), (1/5), 20.95) 
#Accurate
artificer_ion_surge = Ability(artificier, "Ion Surge", 1.0, (1/8), 8.0) 

#---------------------------------------------------------------------------------------------------------
#Bandit
#ACCOUNT: Does not account for bandit passive
bandit = Survivor("Bandit", 12, 2.4, 110, 33, 0.6, 0.12, 0, 1, 7)

#Primaries
#ASSUMPTION: Burst assumes all 5 bullets hit in all 4 shots 
bandit_burst= Ability(bandit, "Burst", .5, (5*4/1.2),  1.0) 
bandit_blast= Ability(bandit, "Blast", 1.0, (4/1.2), 3.3)

#Secondaries
#ACCOUNT: Currently does not account for hemmorrhaging
#ACCOUNT: Does not account for range difference
bandit_serrated_dagger = Ability(bandit, "Serrated Dagger", 1.0, (1/4), 3.6)
bandit_serrated_shiv = Ability(bandit, "Serrated Shiv", 1.0, (1/4), 2.4)

#Utility
bandit_smoke_bomb_initial = Ability(bandit, "Smoke Bomb Initial", 1.0, (1/6), 2.0)
bandit_smoke_bomb_impact = Ability(bandit, "Smoke Bomb Impact", 1.0, (1/6), 2.0)

#Special
#ACCOUNT: does not currently account for resetting all skill cooldowns
bandit_lights_out = Ability(bandit, "Lights Out", 1.0, (1/4), 6.0)
#ACCOUNT: does not currently account for increasing stacks
bandit_desperado = Ability(bandit, "Desperado", 1.0, (1/4), 6.0)


#---------------------------------------------------------------------------------------------------------
#Captain
captain = Survivor("Captain", 12, 2.4, 110, 33, 0.6, 0.12, 0, 1, 7)

#Primaries
#Base Attack speed approximated as average of charged vs uncharged primary 
captain_vulcan_shotgun_max_dps = Ability(captain, "Vulcan Shotgun (Maximum DPS)", 0.75, (8/1.0), 1.2)
captain_vulcan_shotgun_min_dps = Ability(captain, "Vulcan Shotgun (Minimum DPS)", 0.75, (8/2.2), 1.2)

#Secondary
captain_power_tazer= Ability(captain, "Power Tazer", 1.0, (1/6), 1.0) 

#Utility
captain_orbital_probe= Ability(captain, "Orbital Probe", 1.0, (1/11), 10.0) 
captain_ogm_72_diable_strike= Ability(captain, "OGM-72 'Diable' Strike", 1.0, (1/40), 400.0)

#Specials
#ASSUMPTION: Beacon Time Approximated to 
#completing a stage every 8 minutes (240 seconds)
captain_beacon = Ability(captain, "Beacon", 0.0, 1/240, 20.0)

#---------------------------------------------------------------------------------------------------------
#Commando
commando = Survivor("Commando", 12, 2.4, 110, 33, 0.6, 0.12, 0, 1, 7)

#Primary
commando_double_tap = Ability(commando, "Double Tap", 1.0, 6, 1.0) 

#Secondary
#ACCOUNT: Doesn't account for damaging passing through enemies
commando_phase_round = Ability(commando, "Phase Round", 1.0, (1/3), 3.0) 
commando_phase_blast = Ability(commando, "Phase Blast", 0.5, (8/3), 2.0) 

#Special
commando_suppressive_fire = Ability(commando, "Suppressive Fire", 1.0, (6/9), 1.0) 
#ACCOUNT: Doesn't account for hitting multiple enemies
commando_frag_grenade = Ability(commando, "Frag Grenade", 1.0, (1/5), 7.0) 

#---------------------------------------------------------------------------------------------------------
#Engineer
engineer = Survivor("Engineer", 14, 2.8, 130, 39, 0.6, 0.12, 0, 1, 7)

#Primary
#TEST - No description on time needed to charge 8 grenades, need to change attack speed to tested value
#ASSUMPTION - Assumes a max of 8 grenades
engineer_bouncing_grenades = Ability(engineer, "Bouncing Grenades", 1.0, (8/2), 1.0) 

#Secondary
engineer_pressure_mines_max_dps= Ability(engineer, "Pressure Mines (Maximum DPS)", 1.0, (1/8), 9.0)
engineer_pressure_mines_min_dps= Ability(engineer, "Pressure Mines (Minimum DPS)", 1.0, (1/8), 3.0)
engineer_pressure_spider_mines= Ability(engineer, "Spider Mines", 1.0, (1/8), 6.0)

#Utility
engineer_pressure_thermal_harpoons = Ability(engineer, "Thermal Harpoons", 1.0, (1/2.5), 5.0)

#Special
#ASSUMPTION - assumes 1 turret is placed down
#ACCOUNT - Could account for attack speed of turrets
engineer_tr12_gauss_auto_turret = Ability(engineer, "TR12 Gauss Auto-Turret", 1.0, 3, 0.7)
engineer_tr58_carbonizer_turret= Ability(engineer, "TR58 Carbonizer Turret", 0.6, 5, 0.4)

#---------------------------------------------------------------------------------------------------------
#Heretic
heretic = Survivor("Heretic", 18, 3.6, 440, 132, -3.6, -0.72, 0, 1, 8)

#Primary
#TEST: Attack Speed Approximated, should be checked and verified, likely wrong
#ASSUMPTION - Assumes only the explosion damage, not the intial hit damage
#TEST: unsure about the damage of initial hit, assumed from the wiki
heretic_hungering_gaze_initial = Ability(heretic, "Hungering Gaze (Initial)", 0.1, (2/12), 0.05)
heretic_hungering_gaze_explosion = Ability(heretic, "Hungering Gaze (Explosition)", 1.0, (2/12), 1.2)

#Secondary
#INCORRECT: implementation does not accoutn for continuous dps of item
#heretic_slicing_maelstrom = Ability(heretic, "Slicing Maelstrom", 1.0, (2/5), 1.2)


#---------------------------------------------------------------------------------------------------------
#Huntress
huntress = Survivor('Huntress', 12, 2.4, 90, 27, 0.6, 0.12, 0, 1, 7)
#Primaries
huntress_strafe = Ability(huntress, "Strafe", 1.0, 2, 1.5) 
#If huntress crits, proc_coeffecient = 0.7*6
#Formula for flurry crit = crit chance decimal * 2 * huntress DPS
huntress_flurry = Ability(huntress, "Flurry", 0.7, (3/1.3), 1.0) 
#ASSUMPTION - Wiki is contradicting, giving 330% or 110%, we assumed 110%
huntress_arrow_rain = Ability(huntress, "Arrow Rain", 0.2, (19/12), 1.1) 
huntress_ballista = Ability(huntress, "Ballista", 1.0, (3/12), 9.0) 

#---------------------------------------------------------------------------------------------------------
#Loader
loader = Survivor("Loader", 12, 2.4, 160, 48, 1.5, 0.3, 20, 1, 7)
#Primary
#ASSUMPTION - Unknown Attack Speed, guesstimate, likely wrong
#TEST - Need to test the attack speed of Knuckleboom, wiki does not have data
loader_knuckleboom = Ability(loader, "Knuckleboom", 1.0, (1/3), 3.2)
#Secondary
#Grapple Fist = 0
loader_spiked_fist = Ability(loader, "Spiked Fist", 1.0, (1/5), 3.2)
#Utility
loader_charged_gauntlet_max_dps = Ability(loader, "Charged Gauntlet (Maximum DPS)", 1.0, (1/5), 27.0)
loader_charged_gauntlet_min_dps = Ability(loader, "Loader's Charged Gauntlet (Minimum DPS)", 1.0, (1/5), 6.0)
#Doesn't account for 1000% Cone 
loader_thunder_gauntlet= Ability(loader, "Charged Gauntlet", 1.0, (1/5), 21.0)
#Special
loader_m551_pylon_6_targets = Ability(loader, "M551 Pylon (6 targets)", 0.5, (6), 1.0)
loader_m551_pylon_1_target = Ability(loader, "M551 Pylon (1 target)", 0.5, (1), 1.0)
loader_thunderslam = Ability(loader, "Thunderslam", 1.0, (1/8), 20.0)

#---------------------------------------------------------------------------------------------------------
#Mercenary
mercenary = Survivor("Mercenary", 12, 2.4, 110, 33, 0.6, 0.12, 20, 1, 7)
#Primary
#ASSUMPTION - Doesn't account for the damage of Expose
#ASSUMPTION - Doesn't account for attack speed
mercenary_laser_sword = Ability(mercenary, "Laser Sword", 1.0, (3/1.9), 1.3)

#---------------------------------------------------------------------------------------------------------
#MUL-T
mul_t = Survivor("MUL-T", 11, 2.2, 200, 60, 0.6, 0.12, 12, 1, 7)

#Primaries
mul_t_auto_nailgun= Ability(mul_t, "Auto-Nailgun", 0.6, (12/1), 0.7)
mul_t_rebar_punch= Ability(mul_t, "Rebar Punch", 1.0, (1/1.8), 6.0)
mul_t_scap_launcher= Ability(mul_t, "Scrap Launcher", 1.0, (4/2.4), 3.6)
mul_t_power_saw= Ability(mul_t, "Power-Saw", 1.0, (10/1), 1.0)

#Secondary
mul_t_blast_canister= Ability(mul_t, "Blast Canister", 1.0, (1/6), 2.2)
mul_t_blast_bomblets= Ability(mul_t, "Blast Bomblets", 0.3, (5/6), 0.44)

#Utility
#ASSUMPTION - assumes an enemy is just hit by the ram, not the charge
mul_t_transport_mode = Ability(mul_t, "Transport Mode", 1.0, (1/6), 2.5)

#---------------------------------------------------------------------------------------------------------
#Railgunner
railgunner = Survivor("Railgunner", 12, 2.4, 110, 33, 0.6, 0.12, 0, 1, 7)

#Primaries
#ASSUMPTION: M99 Sniper Assumes a Perfect Reload
railgunner_xqr_smart_round_system = Ability(railgunner, "XQR Smart Round System", 1.0, (4/1), 1.0)
railgunner_m99_sniper = Ability(railgunner, "M99 Sniper", 1.0, (1/0.849), 10.0)
#Acccounts for perfect reload bonus damage
#ASSUMPTION - Perfect Reload is additive, not multiplicative, likely wrong
#ASSUMPTION - Doesn't account for crit yet, will fix
railgunner_m99_sniper_perfect_reload = Ability(railgunner, "M99 Sniper, Perfect Reloading", 1.0, (1/0.849), (10.0*5.0))
#TEST - Wiki doesn't have a definitive value on the prof coeff for HH44
railgunner_hh44_marksman = Ability(railgunner, "HH44 Marksman", 1.0, (2/1), 4.0)

#Specials
#TEST - Need to verify that weak point damage is multiplicative, not additive
railgunner_supercharge = Ability(railgunner, "Supercharge", 3.0, 15, (40.0*1.5))
railgunner_cryocharge = Ability(railgunner, "Cryocharge", 1.5, 15, 20.0)


#---------------------------------------------------------------------------------------------------------
#REX
rex = Survivor("REX", 12, 2.4, 130, 39, 0.6, 0.12, 20, 1, 7)

#Primary
#ASSUMPTION - Assumes the time to fire one burst is 0.8 seconds based on the wiki
rex_directive_inject = Ability(rex, "DIRECTIVE: Inject", 0.5, (3/0.8), 0.8) 

#---------------------------------------------------------------------------------------------------------
#Void Fiend
void_fiend = Survivor("V??oid Fiend", 12, 2.4, 110, 33, 0.6, 0.12, 0, 1, 7)

#Primaries
void_fiend_drown = Ability(void_fiend, "Drown", 1.0, (5/3), 3.0) 
#ASSUMPTION - Does not account for piercing
void_fiend_corrupted_drown = Ability(void_fiend, "Corrupted Drown", 0.625, (8/1), 20.0) 
