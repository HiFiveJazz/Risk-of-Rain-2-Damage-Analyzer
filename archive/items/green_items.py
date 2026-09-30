
class pc_item:
    def __init__(self, 
                 name,
                 chance,
                 stat_list,
                 proc_coefficient,
                 damage,
                 damage_increase_per_stack,
                 proc_add_list,
                 tag):

        self.name = name
        self.chance = chance
        self.stat_list = stat_list
        self.proc_cofficient = proc_coefficient 
        self.proc_add_list = proc_add_list
        self.damage = damage
        self.damage_increase_per_stack = damage_increase_per_stack
        self.tag = tag 

class utility_item:
    def __init__(self, 
                 name,
                 chance,
                 stat_list,
                 proc_coefficient,
                 damage,
                 damage_increase_per_stack,
                 proc_add_list,
                 category):

        self.chance = chance
        self.stat_list = stat_list
        self.proc_cofficient = proc_coefficient 
        self.proc_add_list = proc_add_list
        self.damage = damage
        self.damage_increase_per_stack = damage_increase_per_stack
        self.proc_add_list = proc_add_list
        self.category = category
#Green Items
#AtG Missile Mk. 1
atg_missile_mk_1 = pc_item('AtG Missile Mk. 1', 
                           0.1, 
                           ['Damage'],
                           1.0, 
                           [3.0], 
                           [3.0], 
                           ['Linear'],
                           ['Damage'])
#Will-o'-the-wisp
will_o_the_wisp = pc_item("Will-o'-the-wisp", 
                           'OnKillEffect', 
                           ['Damage','Radius'],
                           1.0, 
                           [3.5, 12], 
                           [2.8, 2.4], 
                           ['Linear','Linear'],
                           ['Damage', 'OnKillEffect'])
#Hopoo Feather
hopoo_feather = pc_item("Hopoo Feather", 
                       'OnJump', 
                       ['Extra Jump'],
                       0, 
                       [1], 
                       [1], 
                       ['Linear'],
                       ['Utility', 'AIBlacklist'])
#Ukulele
ukulele = pc_item('Ukulele', 
                  0.25, 
                  ['Target', 'Radius'], 
                  0.2, 
                  [0.8],
                  [3, 20], 
                  ['Linear', 'Linear'],
                  ['Damage'])
#Leeching Seed
leeching_seed = pc_item('Leeching Seed', 
                  'OnHit', 
                  ['Heal'],  
                  0.2, 
                  [1],
                  [1], 
                  ['Linear'],
                  ['Healing'])
#Need to adjust for adding a stack of an effect
predatory_instincts = pc_item('Predatory Instincts', 
                  'OnCrit', 
                  ['Attack Speed Cap', 'Crit Chance'],  
                  0, #Unknown, address 
                  [0.36, 0.05],
                  [0.24, 0.05], 
                  ['Linear', 'Addition'],
                  ['Damage'])
red_whip = pc_item('Red Whip', 
                  'OnOutOfCombat', 
                  ['Movement Speed'],  
                  0, #Unknown, address 
                  [0.30],
                  [0.30], 
                  ['Linear', 'Addition'],
                  ['Utility'])
old_war_stealthkit = pc_item('Old War Stealthkit', 
                  'OnLowHealth', 
                  ['Cooldown', 'owsk'],  
                  0, #Unknown, address 
                  [30, 0.25],
                  [0.5, 0.40], 
                  ['Exponential', 'owsk'],
                  ['Utility', 'LowHealth'])
harvesters_scythe = "Harvester's Scythe"
harvesters_scythe = pc_item("Harvester's Scythe", 
                  'OnCrit', 
                  ['Heal', 'Crit Chance'],  
                  0, #Unknown, address 
                  [8, 0.05],
                  [4, 0.05], 
                  ['Linear', 'Addition'],
                  ['Healing'])
fuel_cell = pc_item('Fuel Cell', 
                  'OnOutOfCombat', 
                  ['Charges', 'Cooldown Reduction'],  
                  0, #Unknown, address 
                  [1, 0.15],
                  [1, 0.15], 
                  ['Linear', 'Exponential'],
                  ['Utility', 'EquipmentRelated', 'Experimenting'])
infusion = pc_item('Infusion', 
                  'OnKillEffect', 
                  ['Max Health Increase', 'Health Per Kill'],  
                  0, #Unknown, address 
                  [100, 1],
                  [100, 1], 
                  ['Linear', 'Linear'],
                  ['Utility'])
bandolier = pc_item('Bandolier', 
                  'OnKillEffect', 
                  ['Chance'],  
                  0, #Unknown, address 
                  [0.18],
                  [0.1], 
                  ['Special'],
                  ['Utility', 'Healing', 'OnKillEffect'])
#Needs to account for the War Cry Buff
bezerkers_pauldron = pc_item("Bezerker's Pauldron", 
                  'On4KillEffect', 
                  ['Frenzy Duration'],  
                  0, #Unknown, address 
                  [6],
                  [4], 
                  ['Linear'], 
                  ['Damage', 'OnKillEffect','Glorious Battle'])
rose_buckler = pc_item('Rose Buckler', 
                  'OnSprint', 
                  ['Armor'],  
                  0, #Unknown, address 
                  [30],
                  [30], 
                  ['Linear'],
                  ['Utility', 'SprintRelated'])
#
runalds_band = pc_item("Runald's Band", 
                  'On400%', 
                  ['Slow Duration','Damage'],  
                  0, #Unknown, address
                  [3, 2.5], 
                  [3, 2.5], 
                  ['Linear', 'Linear'],
                  ['Damage'])
kjaros_band = pc_item("Kjaro's Band",
                  'On400%', 
                  ['Damage'],  
                  0, #Unknown, address 
                  [3.0],
                  [3.0], 
                  ['Linear'],
                  ['Damage'])
chronobauble = pc_item("Chronobauble",
                  'OnHit', 
                  ['Slow Duration'],  
                  0, #Unknown, address 
                  [2],
                  [2], 
                  ['Linear'],
                  ['Utility'])
wax_quail = pc_item("Wax Quail",
                  'OnJumpandSprint', 
                  ['Movement Speed'],  
                  0, #Unknown, address 
                  [10],
                  [10], 
                  ['Linear'],
                  ['Utility', 'SprintRelated'])
old_guillotine = pc_item("Old Guillotine",
                  'OnHit', 
                  ['Threshold'],  
                  0, #Unknown, address 
                  [0.13],
                  [0.13], 
                  ['Hyperbolic'],
                  ['Damage', 'AIBlacklist'])
war_horn = pc_item("War Horn",
                  'OnActivateEquipment', 
                  ['Duration'],  
                  0, #Unknown, address 
                  [8],
                  [4], 
                  ['Linear'],
                  ['Damage','EquipmentRelated'])
lepton_daisy = pc_item("Lepton Daisy",
                  'OnTeleporterCharge', 
                  ['Healing Nova'],  
                  0, #Unknown, address 
                  [1],
                  [1], 
                  ['Linear'],
                  ['Healing', 'AIBlacklist', 'TurretBlacklist', 'HoldoutZoneRelated'])
razorwire = pc_item("Razorwire",
                  'OnTakingHit', 
                  ['Targets','Radius'],  
                  0, #Unknown, address 
                  [5,25],
                  [2,10], 
                  ['Linear', 'Linear'],
                  ['Damage','AIBlacklist'])
ghors_tome = pc_item("Ghors Tome",
                  'OnKillEffect', 
                  ['Drop Chance'],  
                  0, #Unknown, address 
                  [0.04],
                  [0.04], 
                  ['Linear'],
                  ['Utility', 'OnKillEffect'])
squid_polyp = pc_item("Squid Polyp",
                  'OnUse', 
                  ['Attack Speed'],  
                  0, #Unknown, address 
                  [1.0],
                  [1.0], 
                  ['Linear'],
                  ['Damage', 'AIBlacklist', 'InteractableRelated', 'Automation Activation'])
death_mark = pc_item("Death Mark",
                  'On4Debuff', 
                  ['Debuff Duration'],  
                  0, #Unknown, address 
                  [7],
                  [7], 
                  ['Linear'],
                  ['Damage'])
hunters_harpoon = pc_item("Hunter's Harpoon",
                  'OnKillEffect', 
                  ['Duration'],  
                  0, #Unknown, address 
                  [1],
                  [0.5], 
                  ['Linear'],
                  ['Utility', 'OnKillEffect'])
ignition_tank = pc_item("Ignition Tank",
                  'OnIgnite', 
                  ['Damage'],  
                  0, #Unknown, address 
                  [3.0],
                  [3.0], 
                  ['Linear'],
                  ['Damage'])
shuriken = pc_item("Shuriken",
                  'OnPrimarySkill', 
                  ['Damage', 'Shurikens'],  
                  0, #Unknown, address 
                  [4.0, 3],
                  [1.0, 1], 
                  ['Linear', 'Linear'],
                  ['Damage'])
#Item based items
#-----STOPPING POINT-----------
regenerating_scrap = ("Regeneration Scrap",
                  'OnStageBeginEffect', 
                  ['Movement Speed'],  
                  0, #Unknown, address 
                  [0.30],
                  [0.30], 
                  ['Linear', 'Addition'],
                  ['Utility'])
shipping_request_form = "Shipping Request Form"
red_whip = pc_item('Red Whip', 
                  'OnOutOfCombat', 
                  ['Movement Speed'],  
                  0, #Unknown, address 
                  [0.30],
                  [0.30], 
                  ['Linear', 'Addition'],
                  ['Utility'])
#Specaial
# .79 for common
# .2 * n for uncommon
# .01 * n^2 for legendary
item_scrap_green = "Item Scrap, Green"
red_whip = pc_item('Red Whip', 
                  'OnOutOfCombat', 
                  ['Movement Speed'],  
                  0, #Unknown, address 
                  [0.30],
                  [0.30], 
                  ['Linear', 'Addition'],
                  ['Utility'])
