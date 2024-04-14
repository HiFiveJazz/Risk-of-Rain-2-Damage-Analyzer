from items import white_items
from survivors import *
# class Survivor:
#     def __init__(self,
#                  name,
#                  base_damage,
#                  damage_growth_per_level,
#                  hp,
#                  hp_growth,
#                  hp_regen,
#                  hp_regen_growth,
#                  armor,
#                  level,
#                  ms):
#         self.base_damage = base_damage 
#         self.damage_growth_per_level= damage_growth_per_level 
#         self.hp = hp 
#         self.hp_growth = hp_growth 
#         self.hp_regen = hp_regen
#         self.hp_regen_growth = hp_regen_growth
#         self.armor = armor
#         self.level = level
#         self.ms = ms
# class Ability:
#     def __init__(self,
#                  Survivor,
#                  ability_type,
#                  proc_coeffecient,
#                  attack_speed,
#                  damage_multiplier):
#         self.survivor = Survivor
#         self.ability_type =  ability_type
#         self.proc_coefficient = proc_coeffecient
#         self.attack_speed = attack_speed
def getBaseDamage(ability, survivor, level):
    dps = ability.attack_speed * (survivor.base_damage + 
    ((level-1)*survivor.damage_growth_per_level))

    return dps

damage = getBaseDamage(commando_double_tap, commando, 2)
print(damage)

# class pc_item:
#     def __init__(self, 
#                  name,
#                  chance,
#                  stat_list,
#                  proc_coefficient,
#                  value,
#                  value_increase_per_stack,
#                  scaling_type,
#                  tag,
#                  number):
#
#         self.name = name
#         self.chance = chance
#         self.stat_list = stat_list
#         self.proc_cofficient = proc_coefficient 
#         self.value = value
#         self.value_increase_per_stack = value_increase_per_stack
#         self.scaling_type = scaling_type 
#         self.tag = tag 
#         self.number = number
# lens_makers_glasses = pc_item("Lens-Maker's Glasses",
#                           'OnAttack',
#                           ['Critical Chance'],
#                           None,
#                           [0.10],
#                           [0.10],
#                           ['Linear'],
#                           ['Damage'])

# def readItem(item): item.
# print(white_items.lens_makers_glasses.chance)
def compileItem(item,dps,ability): 
    # match item.scalingtype
    match item.scaling_type:
        case 'Linear':
            chance = item.value + (item.number * item.value_increase_per_stack)
        case 'Hyperbolic':
            m1 = (item.value_increase_per_stack * item.number)
            chance = m1/(m1 + 1)
        case 'Reciprocal':
            chance = item.value_increase_per_stack/item.number;
        case 'Reciprocal2':
            chance = item.value_increase_per_stack/(item.number + 1);
        case 'Exponential':
            chance = item.value_increase_per_stack ** item.number;
        case 'Bandolier':
            chance = ((1+item.number) ** 0.33) - 1
    if item.stat_list[0] == 'Critical Chance':
        chance = item.value[0] +  (item.number * item.value_increase_per_stack[0]);
        dps = dps + chance * (2.0 * dps)
        print(dps)
    if item.stat_list[0] == 'Soldier Syringe':
        ability.attack_speed = ability.attack_speed*chance 
    # if item.stat_list[0] == ' ':

    
compileItem(white_items.lens_makers_glasses, damage, commando_double_tap)

# if item.scaling_type == 'Hyperbolic':
    # m1 = (item.value_increase_per_stack * item.number)
