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
ghors_tome = "Ghors Tome"
squid_polyp = "Squid Polyp"
death_mark = "Death Mark"
hunters_harpoon = "Hunter's Harpoon"
ignition_tank = "Ignition Tank"
shuriken = "Shuriken"
regenerating_scrap = "Regeneration Scrap"
shipping_request_form = "Shipping Request Form"
item_scrap_green = "Item Scrap, Green"

#Red Items
brilliant_behemoth = "Brilliant Behemoth" 
ceremonial_dagger = "Ceremonial Dagger"
frost_relic = "Frost Relic"
happiest_mask = "Happiest Mask"
h3ad_5t_v2 = "H3AD-5T v2"
nkuhanas_opinion = "N'kuhana's Opinion"
unstable_tesla_coil = "Unstable Tesla Coil"
fifty_seven_leaf_clover = "57 Leaf Clover"
sentient_meat_hook = "Sentient Meat Hook"
alien_head = "Alien Head"
soulbound_catalyst = "Soulbound Catalyst"
dios_best_friend = "Dio's Best Friend"
hardlight_afterburner = "Hardlight Afterburner"
wake_of_vultures = "Wake of Vultures"
brainstalks = "Brainstalks"
rejuvenation_rack = "Rejuvenation Rack"
aegis = "Aegis"
shattering_justice = "Shattering Justice"
resonance_disc = "Resonance Disc"
interstellar_desk_plant = "Interstellar Desk Plant"
defensive_microbots = "Defensive Microbots"
laser_scope = "Laser Scope"
pocket_icbm = "Pocket I.C.B.M."
spare_drone_parts = "Spare Drone Parts"
symbiotic_scorpion = "Symbiotic Scorpion"
bens_raincoat = "Ben's Raincoat"
bottled_chaos = "Bottled Chaos"
item_scrap_red = "Item Scrap, Red"

#Yellow Items
titanic_knurl = "Titanic Knurl"
queens_gland = "Queen's Gland"
halcyon_seed = "Halcyon Seed"
little_disciple = "Little Disciple"
pearl = "Pearl"
irradiant_pearl = "Irradiant Pearl"
genesis_loop = "Genesis Loop"
artifact_key = "Artifact Key"
molten_perforator = "Molten Perforator"
shatterspleen = "Shatterspleen"
mired_urn = "Mired Urn"
charged_perforator = "Charged Perforator"
empathy_cores = "Empathy Cores"
planula = "Planula"
defense_nucleus = "Defense Nucleas"
item_scrap_yellow = "Item Scrap, Yellow"

#Void
benthnic_bloom = "Bethnic Bloom"
encrusted_key = "Encrusted Key"
lost_seers_lenses = "Lost Seer's Lenses"
lysate_cell = "Lysate Cell"
needletick = "Needletick"
newly_hatched_zora = "Newly Hatched Zora"
plasma_shrimp = "Plasma Shrimp"
pluripotent_larva = "Pluripotent Larva"
polylute = "Polylute"
safer_spaces = "Safer Spaces"
singularity_band = "Singurality Band"
tentabauble = "Tentabauble"
voidsent_flame = "Voidsent Flame"
weeping_fungus = "Weeping Fungus"

#Lunar Items
shaped_glass = "Shaped Glass"
brittle_crown = "Brittle Crown"
transcendance = "Transcendance"
corpsebloom = "Corpse Bloom"
gesture_of_the_drowned = "Gesture of the Drowned"
strides_of_heresy = "Strides of Heresy"
visions_of_heresy = "Visions of Heresy"
beads_of_fealty = "Beads of Fealty"
focused_convergence = "Focused Convergence"
defiant_gouge = "Defiant Gouge"
mercurial_rachis = "Mercurial Rachis"
purity = "Purity"
hooks_of_heresy = "Hooks of Heresy"
egocentrism = "Egocentrism"
eulogy_zero = "Eulogy Zero"
stone_flux_pauldron = "Stone Flux Pauldron"
light_flux_pauldron = "Light Flux Pauldron"
essence_of_heresy = "Essence of Heresy"
glowing_meteorites = "Glowing Meteorite"
helfire_tincture = "Helfire Tincture"
effigy_of_grief = "Effigy of Grief"
spinel_tonic = "Spinel Tonic"

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

