#This file defines all the stats for items in Risk of Rain 2 up to the Void DLC
import numpy as np
class Proc_Coeffecient_Item:
    def __init__(self, 
                 chance,
                 proc_coefficient,
                 damage):

        self.chance = chance
        self.proc_coefficient = proc_coefficient  
        self.damage = damage
#Creating Items
atg_missile_mk = Proc_Coeffecient_Item(0.1, 1.0, 3.0)
ukulele = Proc_Coeffecient_Item(0.2, 2.0, 6.0)
dang = Proc_Coeffecient_Item(0.3, 3.0, 9.0)

class Proc_Coeffecient_Item:
    def __init__(self, 
                 chance,
                 proc_coefficient,
                 damage):

        self.chance = chance
        self.proc_coefficient = proc_coefficient  
        self.damage = damage

soldier_syringe = ('Attack Speed', stack, 0.15, 0.15, 0)
#Defensive Items
tougher_times = ('Block', stack, 0.15, 0.15, 0)

#Healing Items

#Base item
monster_tooth = ('Heal', stack * maximum_health + 8, 0.02, 0.02, 0) 
bustling_fungus = ('Heal', stack * health,  0.045, 0.045, 0) 
#Critical Strike
lens_maker_glasses = ('Crit Chance' stack = 0.1)
pauls_goat_hoof = ('Movement Speed', +14%)
crowbar = (0.75 * stack)
enemy_maximum_hp= 1000000
enemy_hp = 6000
gold = ???
#Status Effects
tri_tip_dagger = 'Status Effect', 0.1, 'Linear', 0.1, 2.4
warbanner = 'Radius', 16, 'Linear', 8
cautious_slug = 'Health Regen', 3, 'Linear', 3
personal_shield_generator = 'Shield', 0.08, 'Linear', 0.08
medkit = 'Heal', 0.05, 'Linear', 0.05
gasoline = 'Damage', 1.5, 'Linear', 0.75
'Radius', 12, 'Linear', 4 
stun_grenade = 'Chance', 0.05, 'Hyperbolic', 0.05
bundle_of_fireworks = 'Firework', 8, 'Linear', 4,
    Proc_Coeffecient = 0, 0.2, 3.0
#This item has to start the proc chain
energy_drink = 'Sprint Speed', 0.25, 'Linear', 0.25
back_up_magazine = 'Charge', 1, 'Linear', 1
sticky_bomb = 'Chance', 0.05, 'Linear', 0.05
rusted_key = ???
armor_piercing_rounds = 'Damage', 0.2, 'Linear', 0.2
stat = 'Barrier', 15, 'Linear', 15
focus_crystal = 'Damage', 0.2, 'Linear', 0.2
bison_steak = 'Health', 25, 'Linear', 25
repulsion_armor_plate = "Damage Reduction", 5, 'Linear', 5 #Cannot be reduced below 1
mocha = "Attack Speed", 0.075, 'Linear', 0.075
"Movement Speed", 0.07, 'Linear', 0.07
power_elixer = ???
delicate_watch = 'Damage', 0.2, 'Linear', 0.2
oddly_shaped_opal = 'Armor', 100, 'Linear', 100
roll_of_pennies = 'Base Gold', 3, 'Linear', 3
white_scrap = ??

#Green Items
atg_missile_mk_1 = 'Damage', 3.0, 'Linear', 3.0
will_o_the_wisp = "Will-o'-the-wisp"
'Damage', 3.5, 'Linear', 2.8
'Radius', 12, 'Linear', 2.4
hopoo_feather = 'Hopoo Feather'
'Extra Jump', 1, 'Linear', 1
ukulele = 'Ukulele'
'Targets', 3, 'Linear', 2
'Radius', 20, 'Linear', 2
leeching_seed = 'Leeching Seed'
'Heal', 1, 'Linear', 1
predatory_instincts = "Predatory Instincts"
'Attack Speed Cap', 0.36, 'Linear', 0.24
'Crit Chance', 0.05, 'None'
red_whip = 'Red Whip'
'Movement', 0.3, 'Linear', 0.3
old_war_stealthkit = 'Old War Stealthkit'
'Cooldown', 30, 'Exponential', -0.5
harvesters_scythe = "Harvester's Scythe"
'Heal', 8, 'Linear', 4
'Crit Chance', 0.05, 'None'
fuel_cell = "Fuel Cell"
'Charges', 1, 'Linear', 1
'Cooldown Reduction', 0.15, 'Exponential', 0.15
infusion = "Infusion"
'Max Health Increase', 100, 'Linear', 100
'Health Per Kill', 1, 'Linear', 1







    Proc_Coeffecient_Item = 0.05, 0
Linear = stack * item
Hyperbolic = (1-(1/(probability.item + 1)))
#Void Items

