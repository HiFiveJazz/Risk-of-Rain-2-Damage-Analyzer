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

# white_items.tougher_times.count = 1;


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
            dps = chance
            print("Block Chance:",dps)
        case 'Tri-Tip Dagger':
            if (chance > 1):
                chance = 1;
            duration_sec = 3*ability.proc_coefficient
            duration_tick = duration_sec*4
            damage_per_tick = dps * 0.2
            total_bleed_damage = duration_tick * damage_per_tick
            print("Bleed Chance (%):",chance*100)
            print("Duration (Seconds):",duration_sec)
            print("Duration (Ticks):",duration_tick)
            print("Damage Per Tick:",damage_per_tick)
            print("Total Bleed Damage:",total_bleed_damage)
        case 'Armor-Piercing Rounds':
            print("Armor-Piercing Round")
            print("Additional Boss Chance (%)", chance*100)
            additional_boss_damage = (dps*chance); 
            print("Additional Boss Damage", additional_boss_damage)
            dps = dps + additional_boss_damage;
            print("Total Boss Damage", dps)
        case 'Crowbar':
            print("Crowbar")
            print("Additional Damage to Enemies above 90% HP(%)", chance*100)
            #:TODO: Depends on enemy hp, have function take in enemy hp for this calc
        case 'Bundle of Fireworks':
            print("Bundle of Fireworks")
            if (item.count > 1):
                number_of_fireworks = item.value + item.value_increase_per_stack * (item.count-1);
                print("Number of Fireworks", number_of_fireworks)
                print("Base Damage", dps)
                firework_damage = (dps * 3) * number_of_fireworks;
                print("Firework Damage", firework_damage)
                dps = dps + firework_damage;
                print("Total Damage", dps)
            else:
                print("Count < 1")
        case 'Delicate Watch':
            print("Delicate Watch")
            watch_damage_increase = item.value*(item.value_increase_per_stack * item.count);
            print("Watch Damage Increase (%)", watch_damage_increase*100)
            dps = dps * (watch_damage_increase) + dps
            print("Total Damage", dps)
            #:TODO: Depends on user hp, break watch and add broken_delicate_watch to item pool if below 25% hp

            # print("Additional Damage to Enemies aboe 90% HP(%)", chance*100)
        case 'Gasoline':
            print("Gasoline")
            if (item.count > 1):
                gasoline_range = item.value[1]+(item.value_increase_per_stack[1] * (item.count-1)); #In meters
                print("Gasoline Range (m)", gasoline_range)
                gasoline_burn_multiplier = item.value[2]+(item.value_increase_per_stack[2] * (item.count-1)); #In meters 
                print("Gasoline damage multiplier (%)", gasoline_burn_multiplier*100);
                ignition_explosion_damage = 1.5 * dps
                burn_damage = gasoline_burn_multiplier * dps 
                print("Initial Ignition Damage", ignition_explosion_damage);
                print("Burn Damage", burn_damage);
            else:
                print("Item count < 0");

            # print("Additional Damage to Enemies aboe 90% HP(%)", chance*100)
    return dps

white_items.crowbar.count = 10;

    
print("Damage after items: ")
test = compile_item(white_items.crowbar, damage, commando, commando_double_tap)
print(test)
# if item.scaling_type == 'Hyperbolic':
    # m1 = (item.value_increase_per_stack * item.number)
