import random
import os
class Environment:
    def __init__(self, 
                 stage_name,
                 stage_number,
                 time,
                 number_of_chests,
                 void_dlc,
                 seeker_dlc,
                 bazaar_statement):
        self.stage_name = stage_name
        self.stage_number = stage_number 
        self.time = time 
        self.number_of_chests = number_of_chests 
        self.void_dlc = void_dlc
        self.seeker_dlc= seeker_dlc
        self.bazaar_statement = bazaar_statement

#Stage 1 Environments
distant_roost = Environment('Distant Roost', #Stage Name 
                            1, # Stage Number
                            10, # Time
                            10, # Number of Chests
                            0, # Void DLC
                            0, # Seeker DLC
                            'waves, crashing on cliffsides')
titanic_plains = Environment('Titanic Plains', 
                             1, # Stage Number
                             10, # Time
                             10, # Number of Chests
                             0, # Void DLC
                             0, # Seeker DLC
                             'rollings hills')
verdant_falls = Environment('Verdant Falls', 
                              1, # Stage Number
                              10, # Time
                              10, # Number of Chests
                              0, # Void DLC
                              0, # Seeker DLC
                              'sweet fruits, and bitter promises')

#Verdant Falls Variant
viscous_falls = Environment('Viscous Falls', 
                              1, # Stage Number
                              10, # Time
                              10, # Number of Chests
                              0, # Void DLC
                              0, # Seeker DLC
                              'falls, erupting from the flora')

# Void DLC
siphoned_forest = Environment('Siphoned Forest', 
                              1, # Stage Number
                              10, # Time
                              10, # Number of Chests
                              1, # Void DLC
                              0, # Seeker DLC
                              'fire and ice')

#Seekers of the Storm DLC
shattered_adobes = Environment('Shattered Adobes', 
                              1, # Stage Number
                              10, # Time
                              10, # Number of Chests
                              0, # Void DLC
                              0, # Seeker DLC
                              'lost poetry')

# Shattered Adobe Variant 
disturbed_impact = Environment('Disturbed Impact', 
                              1, # Stage Number
                              10, # Time
                              10, # Number of Chests
                              0, # Void DLC
                              1, # Seeker DLC
                              'stabbing shards')

#Stage 2 Environments
abandoned_aquaduct = Environment('Abandoned Aquaduct', 
                                 2, # Stage Number
                                 10, # Time
                                 10, # Number of Chests
                                 0, # Void DLC
                                 0, # Seeker DLC
                                 'sand beneath your feet')
wetland_aspect = Environment('Wetland Aspect', 
                             2, # Stage Number
                             10, # Time
                             10, # Number of Chests
                             0, # Void DLC
                             0, # Seeker DLC
                             'twisting roots')

aphelian_sanctuary = Environment('Aphelian Sanctuary', 
                                 2, # Stage Number
                                 10, # Time
                                 10, # Number of Chests
                                 1, # Void DLC
                                 0, # Seeker DLC
                                 'clarity')

reformed_altar = Environment('Reformed Altar', 
                                 2, # Stage Number
                                 10, # Time
                                 10, # Number of Chests
                                 0, # Void DLC
                                 1, # Seeker DLC
                                 'clarity')

#Stage 3 Environments
rallypoint_delta = Environment('Rallypoint Delta', 
                               3, # Stage Number
                               10, # Time
                               10, # Number of Chests
                               0, # Void DLC
                               0, # Seeker DLC
                               'quiet snowfall')
scorched_acres = Environment('Scorched Acres', 
                             3, # Stage Number
                             10, # Time
                             10, # Number of Chests
                             0, # Void DLC
                             0, # Seeker DLC
                             'wind, blowing through trees')
sulfur_pools = Environment('Sulfur Pools', 
                           3, # Stage Number
                           10, # Time
                           10, # Number of Chests
                           1, # Void DLC
                           0, # Seeker DLC
                           'brimstone')

treeborn_colony = Environment('Treeborn Colony', 
                           3, # Stage Number
                           10, # Time
                           10, # Number of Chests
                           0, # Void DLC
                           1, # Seeker DLC
                           'vines, cutting through the sky')

golden_dieback = Environment('Golden Dieback', 
                           3, # Stage Number
                           10, # Time
                           10, # Number of Chests
                           0, # Void DLC
                           1, # Seeker DLC
                           'golden leaves')

#Stage 4 Environments
abyssal_depths = Environment('Abyssal Depths', 
                             4, # Stage Number
                             10, # Time
                             10, # Number of Chests
                             0, # Void DLC
                             0, # Seeker DLC
                             'fire')
sirens_call = Environment("Siren's Call", 
                          4, # Stage Number
                          10, # Time
                          10, # Number of Chests
                          0, # Void DLC
                          0, # Seeker DLC
                          'wind')
sundered_grove = Environment('Sundered Grove', 
                             4, # Stage Number
                             10, # Time
                             10, # Number of Chests
                             0, # Void DLC
                             0, # Seeker DLC
                             'violent growth')

prime_meridian = Environment('Prime Meridian', 
                             4, # Stage Number
                             10, # Time
                             10, # Number of Chests
                             0, # Void DLC
                             0, # Seeker DLC
                             '???') #TODO: Find if prime meridian is accessible via newt altar 

#Stage 5 Environments
sky_meadow = Environment('Sky Meadow', 
                         4, # Stage Number
                         10, # Time
                         10, # Number of Chests
                         0, # Void DLC
                         0, # Seeker DLC
                         'serenity')


#Final Stage

helminth_hatchery = Environment('Helminth Hatchery', 
                         4, # Stage Number
                         10, # Time
                         10, # Number of Chests
                         0, # Void DLC
                         1, # Seeker DLC
                         'wurms')

commencement = Environment('Commencement', 
                           6, #Stage Number
                           10, # Time
                           10, # Number of Chests
                           0, # Void DLC
                           0, # Seeker DLC
                           'glass and dirt')

planetarium = Environment('The Planetarium', 
                          7, # Stage Number 
                          10, # Time
                          10, # Number of Chests
                          1, # Void DLC
                          0, # Seeker DLC
                          'Cell V')

#Hidden Realms
a_moment_fractured = Environment('A Momement, Fractured', 1, 10, 10, 0, 0, '')
a_moment_whole = Environment('A Momement, Whole', 1, 10, 10, 0, 0, '') 
bazaar_between_time = Environment('Bazaar Between Time', 1, 10, 10, 0, 0, 'Null') #After every stage (Except commencement and planetarium)
bulwarks_ambry = Environment("Bulwark's Ambry", 7, 10, 10, 0, 0,'Null') #Only after Sky Meadow
gilded_coast = Environment("Gilded Coast", 1, 10, 10, 0, 0, 'wealth') #Random
void_fields = Environment("Void Fields", 1, 10, 10, 0, 0, 'Cosmic Prison') #Only occurs after Bazaar
void_locus = Environment('Void Locus', 1, 10, 10, 1, 0, 'potential')

# Base game set up
stage_1_environments = [distant_roost, titanic_plains, verdant_falls]
stage_2_environments = [abandoned_aquaduct, wetland_aspect]
stage_3_environments = [rallypoint_delta, scorched_acres]
stage_4_environments = [abyssal_depths, sirens_call, sundered_grove]
stage_5_environments = [sky_meadow]
stage_6_environments = [commencement]
stage_7_environments = [planetarium]


# this function adds maps to the each environment based on whether the player has looped,
# or depending on what DLC they own
def getDLCSetup(void_dlc_condition, seeker_dlc_condition, loop_condition):
    if (void_dlc_condition == 1):
        stage_1_environments.append(siphoned_forest)
        stage_2_environments.append(aphelian_sanctuary)
        stage_3_environments.append(sulfur_pools)

    if (seeker_dlc_condition == 1):
        stage_1_environments.append(shattered_adobes)
        stage_2_environments.append(reformed_altar)
        stage_3_environments.append(treeborn_colony)
        stage_5_environments.append(helminth_hatchery)
        
    #variant checker
    if (loop_condition == 1 and seeker_dlc_condition == 1):
        stage_1_environments.pop()
        stage_3_environments.pop()
        stage_1_environments.append(disturbed_impact)
        stage_3_environments.append(golden_dieback)

    if (loop_condition == 1):
        stage_1_environments.pop(2)
        stage_1_environments.append(viscous_falls)


def getEnvironmentFromStage(environment_stage):
    random_environment = random.choice(environment_stage)
    return random_environment

#Needs to account for trading items for greens and reds
#Needs to account for selecting lunar items 
def lunarSeer(stage_number):
    try:
        while True:
            if stage_number % 5 == 0:
                stage_number = 0
            stage_object = "stage_" + str(stage_number + 1) + "_environments"
            environments = globals()[stage_object]
            
            if len(environments) < 2:
                print("\033[3;2mYou dream of "+environments[0].bazaar_statement+"\033[0m")
                return environments[0]
            else:
                os.system('cls');
                os.system('clear');
                environment_display_case = random.sample(environments, k=2)
                print('Choose your next Stage (1,2)')
                print('(1) ' + environment_display_case[0].stage_name + ": \033[94m 2 Lunar Coins\033[0m")
                print('(2) ' + environment_display_case[1].stage_name + ": \033[94m 2 Lunar Coins\033[0m")
                stage_select = input('Choice: ')

                if stage_select in ['1', '2']:
                    print("\033[3;2mYou dream of "+environment_display_case[int(stage_select)-1].bazaar_statement+'.\033[0m')
                    return environment_display_case[int(stage_select)-1]
                else:
                    os.system('cls');
                    os.system('clear');
                    print("\033[3;2mInvalid input. Please input a value (1,2)\033[0m")
    except KeyboardInterrupt:
        print("\nThanks for playing!")
        return None




def onStart():
    os.system('cls');
    os.system('clear');
    try:
        while True:
            void_dlc_q = input("Do you have the Survivors of the Void DLC? (y, N)\n")
            if void_dlc_q in ['y', 'Y', '1']:
                void_dlc_condition = 1
                break
            elif void_dlc_q in ['n', 'N', '0']:
                void_dlc_condition = 0
                break
            else:
                os.system('cls');
                os.system('clear');
                print("\033[3;2mInvalid input. Please input either (y)es or (n)o\033[0m")
                    
                
        while True:
            seeker_dlc_q = input("Do you have the Seekers of the Storm DLC? (y, N)\n")
            if seeker_dlc_q in ['y', 'Y', '1']:
                seeker_dlc_condition = 1
                break
            elif seeker_dlc_q in ['n', 'N', '0']:
                seeker_dlc_condition = 0
                break
            else:
                os.system('cls');
                os.system('clear');
                print("\033[3;2mInvalid input. Please input either (y)es or (n)o\033[0m")

        os.system('cls');
        os.system('clear');
        getDLCSetup(void_dlc_condition, seeker_dlc_condition,0)
        print('Loading Environments')
        env = getEnvironmentFromStage(stage_1_environments)
        print("You are in: \n", env.stage_name)
        bazaar_condition = input("Would you like to go to the Bazaar Between Time? (\033[1mCost: 3 Lunar Coins\033[0m) (y,N)\n")
        stage_number = 1;
        while True:
            if bazaar_condition in ['y', 'Y', '1']:
                lunarSeer(stage_number)
                stage_number = stage_number + 1;
                break;
            elif bazaar_condition in ['n', 'N', '0']:
                print("Thanks for you playing!\n")
                break;
            else:
                os.system('cls');
                os.system('clear');
                print("\033[3;2mInvalid input. Please input a yes or no(y,n)\033[0m")
    except KeyboardInterrupt:
        print("\nThanks for playing!")
        return None

onStart()
# test = lunarSeer(0)
