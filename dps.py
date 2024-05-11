from items import white_items
test
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
    dps = dps + (survivor.critical_chance*2*dps)
    return dps

damage = getBaseDamage(commando_double_tap, commando, 1)
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

white_items.tougher_times.count = 255
def compileItem(item,dps,survivor,ability): 
    # match item.scalingtype
    i = 0
    match item.scaling_type[i]:
        case 'Linear':
            chance = item.count * item.value_increase_per_stack[i]
            print('Linear')
        case 'Hyperbolic':
            m1 = (item.value_increase_per_stack[i] * item.count)
            chance = m1/(m1 + 1)
            print('Hyperbolic')
        case 'Reciprocal':
            chance = item.value_increase_per_stack/item.count;
            print('Reciprocal')
        case 'Reciprocal2':
            chance = item.value_increase_per_stack/(item.count+ 1);
            print('Reciprocal2')
        case 'Exponential':
            chance = item.value_increase_per_stack ** item.count;
            print('Exponential')
        case 'Bandolier':
            chance = ((1+item.count) ** 0.33) - 1
            print('Bandolier')
    match item.name:
        case "Lens-Maker's Glasses":
            dps = dps + chance * (dps)
            print(chance)
            print(dps)
        case 'Soldier Syringe':
            dps = dps * (1+chance)
        case 'Tougher Times':
            block_chance = chance
            print("Block Chance:",block_chance)

    return dps
    
hi = compileItem(white_items.tougher_times, damage, commando, commando_double_tap)
print(hi)
# if item.scaling_type == 'Hyperbolic':
    # m1 = (item.value_increase_per_stack * item.number)
