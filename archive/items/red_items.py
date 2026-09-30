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
#Red Items
brilliant_behemoth = pc_item("Brilliant Behemoth", 
                            'OnAttack',   
                            'Explosion Radius', 
                             0,
                             [1.0],
                             [4], 
                             ['Linear'], 
                             ['Damage'])
#Needs to account for all 3 daggers
ceremonial_dagger = pc_item("Ceremonial Dagger",
                            'OnKillEffect', 
                            'Damage',
                            1.0,
                            [1.5], 
                            [1.5], 
                            ['Linear'], 
                            ['Damage', 'OnKillEffect', 'AIBlacklist'])
#Doesn't account for damage per second
frost_relic = pc_item("Frost Relic",
               'OnKillEffect',
               'Maximum Radius', 
               0.2,
               [18], 
               [12],
               'Linear', 
               ['Damage', 'OnKillEffect'])
#Doesn't account for damage per second
happiest_mask = pc_item("Happiest Mask",
                        'OnKillEffect',
                        'Ghost Duration', 
                        0.07,
                        [30], 
                        [30],
                        ['Linear'], 
                        ['Damage','Utility','OnKillEffect'])
h3ad_5t_v2 = pc_item("H3AD-5T v2",
                     'onInteract',
                     ['Cooldown'], 
                     0,
                     [10], 
                     [1],
                     ['Reciprocal'], 
                     ['Damage','Utility','AIBlacklist'])
nkuhanas_opinion = pc_item("N'kuhana's Opinion",
                           'onSoulEnergy',
                           ['Damage'], 
                           0.2,
                           [1.0], 
                           [1.0], 
                           ['Linear'], 
                           ['Damage'])
#Doesn't account for damage
unstable_tesla_coil = pc_item("Unstable Tesla Coil",
                              "OnTesla",
                              ['Targets'], 
                              0.3,
                              [3], 
                              [2],
                              ['Linear'], 
                              ['Damage'])
#Doesn't account for item math
fifty_seven_leaf_clover = pc_item("57 Leaf Clover",
                                  'OnRoll',
                                  ['Luck'], 
                                  0,
                                  [1], 
                                  [1], 
                                  ['Linear'], 
                                  ['Utility'])
sentient_meat_hook = pc_item("Sentient Meat Hook",
                             0.2,
                             ['Chance', 'Targets'], 
                             0.33,
                             [0.2, 10],
                             [0.2, 5],
                             ['Hyperbolic', 'Linear'], 
                             ['Damage'])
alien_head = pc_item("Alien Head",
                     "OnPermanent",
                     ['Cooldown'], 
                     None,
                     [0.25], 
                     [0.25], 
                     ['Exponential'], 
                     ['Utility'])
soulbound_catalyst = pc_item("Soulbound Catalyst",
                             'OnKillEffect',
                             ['Cooldown Reduction'], None,
                             [4], 
                             [2],
                             ['Linear'], 
                             ['Utility','OnKillEffect','EquipmentRelated'])
dios_best_friend = pc_item("Dio's Best Friend",
                           "OnDeath",
                           ['Uses'], 
                           None,
                           1, 
                           1, 
                           ['Linear'], 
                           ['Utility'])
                           
hardlight_afterburner = pc_item("Hardlight Afterburner",
                                'OnShift',
                                ['Charges'], 
                                None,
                                [2], 
                                [2], 
                                ['Linear'], 
                                ['Utility'])
wake_of_vultures = pc_item("Wake of Vultures",
                           'OnKillElite',
                           ['Duration'], 
                           None,
                           [8], 
                           [5],
                           ['Linear'], 
                           ['Damage','Utility','AIBlacklist','OnKillEffect'])
brainstalks = pc_item("Brainstalks",
                      "OnKillElite",
                      ['Duration'], 
                      None,
                      [4], 
                      [4], 
                      ['Linear'], 
                      ['Utility','AIBlacklist','OnKillEffect'])
rejuvenation_rack = pc_item("Rejuvenation Rack",
                            'OnPermanent',
                            ['Heal'], 
                            None,
                            [1.0], 
                            [1.0], 
                            ['Linear'], 
                            ['Healing'])
aegis = pc_item("Aegis",
                'OnHeal',
                ['Healing Converted'], 
                None,
                [0.5], 
                [0.5], 
                ['Linear'], 
                ['Utility','Healing'])
shattering_justice = pc_item("Shattering Justice",
                             'OnHit',
                             ['Duration'], 
                             None,
                             [8], 
                             [8], 
                             ['Linear'], 
                             ['Damage'])
resonance_disc = pc_item("Resonance Disc",
                         'OnKill4in7',
                         ['Damage', 'Explosion'],
                         1.0,
                         [3.0,10.0], 
                         [3.0,10.0], 
                         ['Linear', 'Linear'],
                         ['Damage','OnKillEffect'])
interstellar_desk_plant = pc_item("Interstellar Desk Plant",
                                  'OnKillEffect',
                                  ['Radius'], 
                                  None,
                                  [5], 
                                  [5], 
                                  ['Linear'], 
                                  ['Healing','OnKillEffect'])
defensive_microbots = pc_item("Defensive Microbots",
                              'OnPermanent',
                              ['Projectiles Shot'], 
                              None,
                              [1.0], 
                              [1.0], 
                              ['Linear'], 
                              ['Utility', 'WorldUnique'])
laser_scope = pc_item("Laser Scope",
                      'OnCrit',
                      ['Damage'], 
                      None,
                      [1.0], 
                      [1.0], 
                      ['Linear'], 
                      ['Damager'])
pocket_icbm = pc_item("Pocket I.C.B.M.",
                      'OnMissile',
                      ['Damage','Extra Missiles'], 
                      None,
                      [0, 2], 
                      [50, None], 
                      ['Linear','None'], 
                      ['Damage'])
spare_drone_parts = pc_item("Spare Drone Parts",
                            'OnPermanent',
                            ['Attack Speed'], 
                            None,
                            0.5, 
                            0.5, 
                            ['Linear'], 
                            ['Damage','AIBlacklist','TurretBlacklist','BrotherBlacklist'])
symbiotic_scorpion = pc_item("Symbiotic Scorpion",
                             'OnHit',
                             ['Armor Reduction'], 
                             None,
                             2.0, 
                             2.0, 
                             ['Linear'], 
                             ['Damage'])
bens_raincoat = pc_item("Ben's Raincoat",
                        'OnDebuff',
                        ['Debuffs Blocked','Cooldown'], 
                        None,
                        [1.0,5], 
                        [1.0,None], 
                        ['Linear', None], 
                        ['Utility','Healing'])

bottled_chaos = pc_item("Bottled Chaos",
                        'OnEquipment',
                        'Effects', 
                        None,
                        [1], 
                        [1], 
                        ['Linear'], 
                        ['Utility','EquipmentRelated'])
#--------STOPPING POINT----------
item_scrap_red = "Item Scrap, Red"
