from items import white_items
from survivors import *
import survivors

# Returns base damage, DOES NOT account for base crit, used for calculations involving crit
def getBaseDamage(ability, survivor, level):
    dps = ability.attack_speed * (survivor.base_damage + 
    ((level-1)*survivor.damage_growth_per_level))
    return dps

# Returns base damage, DOES account for base crit, used for calculations  NOT involving crit
def getBaseDamageCrit(ability, survivor, level):
    dps = ability.attack_speed * (survivor.base_damage + 
    ((level-1)*survivor.damage_growth_per_level))
    if (survivor.critical_chance > 1):
        temp_crit = 1;
    else:
        temp_crit = survivor.critical_chance;
    dps = dps + (temp_crit*dps)
    return dps


damage = getBaseDamage(commando_double_tap, commando, 1)
print("Base Damage: ")
print(damage)
print("\n")


# damage_with_base_crit = getBaseDamageCrit(commando_double_tap, commando, 1)
# print("Base Damage (Accounting for base crit): ")
# print(damage_with_base_crit)
# print("\n")


white_items.lens_makers_glasses.count = 20
def compile_item(item,dps,survivor,ability): 
    # match item.scalingtype
    i = 0
    match item.scaling_type[i]:
        case 'Linear':
            chance = item.count * item.value_increase_per_stack[i];
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
    #Special exceptions to the typical chance calculations
    match item.name:
        case "Lens-Maker's Glasses":
            if ((survivor.critical_chance + chance) > 1): 
                temp_crit = 1;
            else:
                temp_crit = survivor.critical_chance + chance;
            dps = dps + (temp_crit*dps);
        case 'Soldier Syringe':
            dps = dps * (1+chance)
        case 'Tougher Times':
            block_chance = chance
            print("Block Chance:",block_chance)
    return dps

    
print("Damage after items: ")
test = compile_item(white_items.lens_makers_glasses, damage, commando, commando_double_tap)
print(test)
# if item.scaling_type == 'Hyperbolic':
    # m1 = (item.value_increase_per_stack * item.number)
