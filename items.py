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
bandolier = "Bandolier"
'Chance', 0.18, 'Special', 0.1  
bezerkers_pauldron = "Bezerker's Pauldron"
'Frenzy Duration', 6, 'Linear', 4
rose_buckler = "Rose Buckler"
'Armor', 30, 'Linear', 30
runalds_band = "Runald's Band"
'Slow Duration', 3, 'Linear', 3
'Damage', 2.5, 'Linear', 2.5
kjaros_band = "Kjaro's Band"
'Damage', 3.0, 'Linear', 3.0
chronobauble = "Chronobauble"
'Slow Duration', 2, 'Linear', 2
wax_quail = "Wax Quail"
'Boost', 10, 'Linear', 10
old_guillotine = "Old Guillotine"
'Threshold', 0.13, 'Hyperbolic', 0.13
war_horn = "War Horn"
'Duration', 8, 'Linear', 4
lepton_daisy = "Lepton Daisy"
'Healing Nova', 1, 'Linear', 1
razorwire = "Razorwire"
'Targets', 5, 'Linear', 2
'Radius', 25, 'Linear', 10
ghors_tome = "Ghors Tome"
'Drop Chance', 0.04, 'Linear', 4
squid_polyp = "Squid Polyp"
'Attack Speed', 1.0, 'Linear', 1.0
death_mark = "Death Mark"
'Debuff Duration', 7, 'Linear', 7
hunters_harpoon = "Hunter's Harpoon"
'Duration', 1, 'Linear', 0.5
ignition_tank = "Ignition Tank"
'Damage', 3.0, 'Linear', 3.0
shuriken = "Shuriken"
'Damage', 4.0, 'Linear', 1.0
'Shurikens', 3, 'Linear', 1
regenerating_scrap = "Regeneration Scrap"
shipping_request_form = "Shipping Request Form"
#Specaial
# .79 for common
# .2 * n for uncommon
# .01 * n^2 for legendary
item_scrap_green = "Item Scrap, Green"

#Red Items
brilliant_behemoth = "Brilliant Behemoth" 
'Explosion Radius', 4, 'Linear', 2.5
ceremonial_dagger = "Ceremonial Dagger"
'Damage', 1.5, 'Linear', 1.5
frost_relic = "Frost Relic"
'Maximum Radius', 18, 'Linear', 12
happiest_mask = "Happiest Mask"
'Ghost Duration', 30, 'Linear', 30
h3ad_5t_v2 = "H3AD-5T v2"
'Cooldown', 10, 'Reciprocal', 1
nkuhanas_opinion = "N'kuhana's Opinion"
'Damage', 1.0, 'Linear', 1.0
unstable_tesla_coil = "Unstable Tesla Coil"
'Targets', 3, 'Linear', 2
fifty_seven_leaf_clover = "57 Leaf Clover"
'Luck', 1, 'Linear', 1
sentient_meat_hook = "Sentient Meat Hook"
'Chance', 0.2, 'Hyperbolic', 0.2
'Targets', 10, 'Linear', 5
alien_head = "Alien Head"
'Cooldown', 0.25, 'Exponential', 0.25
soulbound_catalyst = "Soulbound Catalyst"
'Cooldown Reduction', 4, 'Linear', 2
dios_best_friend = "Dio's Best Friend"
'Uses', 1, 'Linear', 1
hardlight_afterburner = "Hardlight Afterburner"
'Charges', 2, 'Linear', 2
wake_of_vultures = "Wake of Vultures"
'Duration', 8, 'Linear', 5
brainstalks = "Brainstalks"
'Duration', 4, 'Linear', 4
rejuvenation_rack = "Rejuvenation Rack"
'Heal', 1.0, 'Linear', 1.0
aegis = "Aegis"
'Healing Converted', 0.5, 'Linear', 0.5
shattering_justice = "Shattering Justice"
'Duration', 8, 'Linear', 8
resonance_disc = "Resonance Disc"
'Damage', 3.0, 'Linear', 3.0
'Explosion', 10.0, 'Lienar', 10.0
interstellar_desk_plant = "Interstellar Desk Plant"
'Radius', 5, 'Linear', 5
defensive_microbots = "Defensive Microbots"
'Projectiles Shot', 1, 'Linear', 1
laser_scope = "Laser Scope"
'Damage', 1.0, 'Linear', 1.0
pocket_icbm = "Pocket I.C.B.M."
'Damage', 0, 'Linear', 0.5
'Extra Missiles', 2, None, None
spare_drone_parts = "Spare Drone Parts"
'Attack Speed', 0.5, 'Linear', 0.5
symbiotic_scorpion = "Symbiotic Scorpion"
'Armor Reduction', 2, 'Linear', 2
bens_raincoat = "Ben's Raincoat"
'Debuffs Blocked', 1, 'Linear', 1
'Cooldown', 5, None, None
bottled_chaos = "Bottled Chaos"
'Effects', 1, 'Linear', 1
item_scrap_red = "Item Scrap, Red"

#Yellow Items
titanic_knurl = "Titanic Knurl"
'Maxium Health', 40, 'Linear', 40
'Health Regen', 1.6, 'Linear', 1.6
queens_gland = "Queen's Gland"
'Beetle Guard', 1, 'Linear', 1
halcyon_seed = "Halcyon Seed"
'Health', 1.0, 'Linear', 1.0
'Damage', 1.0, 'Linear', 0.5
little_disciple = "Little Disciple"
'Damage', 3.0, 'Linear', 3.0
pearl = "Pearl"
'Health', 0.1, 'Linear', 0.1
irradiant_pearl = "Irradiant Pearl"
'Health', 0.1, 'Linear', 0.1
'Health Regen', 0.1, 'Linear', 0.02
'Movement Speed', 0.1, 'Linear', 0.1
'Damage', 0.1, 'Linear', 0.1
'Attack Speed', 0.1, 'Linear', 0.1
'Crit Chance', 0.1, 'Linear', 0.1
'Armor Multiplier', 0.1, 'Linear', 0.1
genesis_loop = "Genesis Loop"
'Recharge Speed', 1.0, 'Linear', 0.5
artifact_key = "Artifact Key"
molten_perforator = "Molten Perforator"
'Damage', 3.0, 'Linear', 3.0
shatterspleen = "Shatterspleen"
'Damage(Base)', 4.0, 'Linear', 4.0
'Damage (Max HP)', 0.15, 'Linear', 0.15
'Crit Chance', 0.05, None, None
mired_urn = "Mired Urn"
'Tethered Enemies', 1, 'Linear', 1
charged_perforator = "Charged Perforator"
'Damage', 5.0, 'Linear', 5.0
empathy_cores = "Empathy Cores"
'Probe Damage', 1.0, 'Linear', 1.0
planula = "Planula"
'Healing', 15, 'Linear', 15
defense_nucleus = "Defense Nucleas"
'Max Constructs', 4, 'Linear', 4
item_scrap_yellow = "Item Scrap, Yellow"

#Void
benthnic_bloom = "Bethnic Bloom"
'Items Upgraded', 3, 'Linear', '3'
encrusted_key = "Encrusted Key"
# Return to wiki for more information
lost_seers_lenses = "Lost Seer's Lenses"
'Kill Chance', 0.5, 'Linear', 0.5
lysate_cell = "Lysate Cell"
'Charges', 1, 'Linear', 1
needletick = "Needletick"
'Chance to Collapse', 0.1, 'Linear', 0.1
newly_hatched_zora = "Newly Hatched Zora"
'Charge Time', 60, 'Reciprocal', 1
'Max Allies', 1, 'Linear', 1
plasma_shrimp = "Plasma Shrimp"
'Damage', 0.4, 'Linear', 0.4
pluripotent_larva = "Pluripotent Larva"
'Uses', 1, 'Linear', 1
polylute = "Polylute"
'Hits', 3, 'Linear', 3
safer_spaces = "Safer Spaces"
'Recharge', 15, 'Exponential', -0.1
singularity_band = "Singurality Band"
'Damage', 1.0, 'Linear', 1.0
tentabauble = "Tentabauble"
'Root Chance', 0.05, 'Hyperbolic', 0.05
'Duration', 1, 'Linear', 1
voidsent_flame = "Voidsent Flame"
'Damage', 2.6, 'Linear', 1.56
'Radius', 12, 'Linear', 2.4
weeping_fungus = "Weeping Fungus"
'HP per second', 0.02, 'Linear', 0.02

#Lunar Items
shaped_glass = "Shaped Glass"
'Damage', 1.0, 'Exponential', 1.0
'Health Reduction', 0.5, 'Exponential', -0.5
brittle_crown = "Brittle Crown"
'Gold Gained', 2, 'Linear', 2
'Gold Lost', 1.0, 'Linear', 1.0
transcendance = "Transcendance"
'Maximum Health', 0.5, 'Linear', 0.25
corpsebloom = "Corpse Bloom"
'Heal', 1.0, 'Linear', 1.0
'Maximum Heal', 0.1, 'Reciprocal', 1
gesture_of_the_drowned = "Gesture of the Drowned"
'Cooldown Reduction', 0.5, 'Exponential', 0.15
strides_of_heresy = "Strides of Heresy"
'Heal', 0.182, 'Linear', 0.182
'Duration', 3, 'Linear', 3
visions_of_heresy = "Visions of Heresy"
'Charges', 12, 'Linear', 12
'Reload', 2, 'Linear', 2
beads_of_fealty = "Beads of Fealty"
focused_convergence = "Focused Convergence"
'Charge Speed', 0.3, 'Linear', 0.3
'Teleporter Zone', 1.0, 'Reciprocal', 2
defiant_gouge = "Defiant Gouge"
'Enemy Difficulty', 0.4, 'Linear', 0.4
mercurial_rachis = "Mercurial Rachis"
'Range', 16, 'Exponential', 0.5
purity = "Purity"
'Cooldown Reduction', 2, 'Linear', 1
'Luck', -1, 'Linear', -1
hooks_of_heresy = "Hooks of Heresy"
'Root Duration', 3, 'Linear', 3
'Cooldown', 5, 'Linear', 5
egocentrism = "Egocentrism"
'Charge Time', 3, 'Reciprocal', 1
'Max Orbs', 3, 'Linear', 1
eulogy_zero = "Eulogy Zero"
'Effect Chance', 0.05, 'Linear', 0.05
stone_flux_pauldron = "Stone Flux Pauldron"
'Max Health', 1.0, 'Linear', 1.0
'Speed', 1.0, 'Reciprocal', 1
light_flux_pauldron = "Light Flux Pauldron"
'Skill Cooldowns', 0.5, 'Exponential', -0.5
'Attack Speed', 1.0, 'Reciprocal', 1
essence_of_heresy = "Essence of Heresy"
'Ruin Duration', 10, 'Linear', 10
'Cooldown', 8, 'Linear', 8
glowing_meteorites = "Glowing Meteorite"
helfire_tincture = "Helfire Tincture"
effigy_of_grief = "Effigy of Grief"
spinel_tonic = "Spinel Tonic"
'Most', -0.05, 'Exponential', -0.05

#Equipments
disposable_missile_launcher = "Disposable Missile Launcher"
foreign_fruit = "Foreign Fruit"
primordial_cube = "Primordial Cube"
trophy_hunters_tricorne = "Trophy Hunter's Tricorne"
ocular_hud = "Ocular HUD"
the_back_up = "The Back-up"
preon_accumulator = "Preon Accumulator"
goobo_jr = "Goobo Jr."
milky_chrysalis = "Milky Chrysalis"
royal_capacitor = "Royal Capacitor"
molotov_6_pack = "Molotov (6-Pack)"
executive_card = "Executive Card"
the_crowdfunder = "The CrowdFunder"
gnarled_woodsprite = "Gnarled Woodsprite"
radar_scanner = "Radar Scanner"
eccentric_vase = "Eccentric Vase" 
blast_shower = "Blast Shower"
volcanic_egg = "Volcanic Egg"
jade_elephant = "Jade Elephant"
sawmerang = "Sawmerang"
recycler = "Recycler"
super_massive_leech = "Super Massive Leech"
gorags_opus = "Gorag's Opus"
forgive_me_please = "Forgive Me Please"
remote_caffeinator = "Remote Caffeinator"
ifrits_distinction = "Ifrit's Distinction"
his_reassurance = "His Reassurance"
silence_between_two_strikes = "Silence Between Two Strikes"
her_biting_embrace = "Her Biting Embrace"
nkuhanas_retort = "N'kuhana's Retort"
spectral_circlet = "Spectral Circlet"
fuel_array = "Fuel Array"

    Proc_Coeffecient_Item = 0.05, 0
Linear = stack * item
Hyperbolic = (1-(1/(probability.item + 1)))
#Void Items

