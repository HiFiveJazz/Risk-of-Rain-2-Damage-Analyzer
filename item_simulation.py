import random 
# red items -> 1% chance
# green items -> 20%
# white items -> 79%

class Difficulty:
    def __init__(self, 
                 items,
                 time,
                 damage):

        self.items = items 
        self.time = time
        self.damage = damage

# Defining Chests
class Chest:
    def __init__(self, 
                 type,
                 probability_white,
                 probability_green,
                 probability_red,
                 probability_void,
                 probability_orange,
                 base_cost,
                 item_type):

        self.type = type
        self.probability_white = probability_white
        self.probability_green = probability_green
        self.probability_red = probability_red
        self.probability_orange = probability_orange
        self.probability_void = probability_void
        self.base_cost = base_cost 
        self.item_type = item_type

small_chest = Chest('Small Chest', 0.792, 0.198, 0.099, 0, 0, 25, 'Regular')
large_chest = Chest('Large Chest', 0, 0.198, 0.099, 0, 0, 50, 'Regular')
equipment_barrel = Chest('Equipment Barrel', 0, 0, 0, 1.0, 0, 25, 'Equipment')
legendary_chest = Chest('Legendary Chest', 0, 0.198, 0.099, 0, 0, 400, 'Red')
multishop_green = Chest('Multishop', 0, 0.198, 0.099, 0, 0, 400, 'Common & Uncommon')
equipment_multishop = Chest('Equipement Multishop', 0, 0, 0, 1.0, 0, 50, 'Common & Uncommon')

# Category Chests
small_damage = Chest('Damage Chest ', 0, 0, 0, 1.0, 0, 30, 'Damage')
small_healing = Chest('Healing Chest ', 0, 0, 0, 1.0, 0, 30, 'Healing')
small_utility = Chest('Utility Chest ', 0, 0, 0, 1.0, 0, 30, 'Utility')
large_damage = Chest('Damage Chest ', 0, 0, 0, 1.0, 0, 60, 'Damage')
large_healing = Chest('Healing Chest ', 0, 0, 0, 1.0, 0, 60, 'Healing')
large_utility = Chest('Utility Chest ', 0, 0, 0, 1.0, 0, 60, 'Utility')
adaptive_chest = Chest('Utility Chest ', 0, 0, 0, 1.0, 0, 50, 'Utility')
                        
rusty_lockbox = Chest('Rusty Lockbox', 0, 0, 0, 1.0, 0, 50, 'Regular')
encrusted_cache = Chest('Encrusted Cache', 0, 0, 0, 1.0, 0, 50, 'Void')
crashed_multishop_deliver = Chest('Encrusted Cache', 0, 0, 0, 1.0, 0, 50, 'Void')

#Adjust based on each patch
total_white_item_count = 29 
total_green_item_count = 29 
total_red_item_count = 
total_yellow_item_count =
total_void_item_count =
total_lunar_item_count =
# Not sure if I should be accounting for cloaked chests
# cloaked_chest = ?


difficulties = ['Drizzle', 'Rainstorm', 'Monsoon', 'Eclipse']
#Choose inital difficulty

#Implementation of terminal use of code
def get_difficulty_and_player_count():
    try:
        while True:
                print("Choose a difficulty:")
                difficulty_value = input("Drizzle (1), Rainstorm (2), or Monsoon (3)?\n")
                try:
                    difficulty_value = int(difficulty_value)
                    if difficulty_value in [1, 2, 3]:
                        player_count = input("How many people are you playing with? (0 if single player)\n")
                        try:
                            player_count = int(player_count)
                            if type(player_count) == int:
                                print('success')
                                break
                        except ValueError:
                            print("Invalid. Please input a number for the number of players (0 if singleplayer)")
                except ValueError:
                    print("Invalid Input. Please input a number, 1 -3, for difficulty.")
    except KeyboardInterrupt:
        print("\nThanks for playing!")
    return [player_count, difficulty_value]

[player_count, difficulty_value] = get_difficulty_and_player_count()

# Calculating the Difficulty Coeffecient
player_factor = 1 + (3 * (player_count - 1))
time_factor = 0.0506 * difficulty_value * (player_count ** 0.2)
# print(time_factor)
stages_completed = 1
stage_factor = (1.15 ** stages_completed)
difficulty_coeffecient = (player_factor + time_factor + stage_factor)

chests = 2
def Item_Acquistion_Simulator():
    while True:
        input = input("Open a small chest? (y/n)")
        try: 
            if input == 'y'

            else if input == 'n'
                break

