import random
class Environment:
    def __init__(self, 
                 stage_name,
                 stage_number,
                 time,
                 number_of_chests,
                 dlc,
                 bazaar_statement):
        self.stage_name = stage_name
        self.stage_number = stage_number 
        self.time = time 
        self.number_of_chests = number_of_chests 
        self.dlc = dlc
        self.bazaar_statement = bazaar_statement

#Stage 1 Environments
distant_roost = Environment('Distant Roost', 
                            1, 
                            10, 
                            10, 
                            0, 
                            'waves, crashing on cliffsides')
titanic_plains = Environment('Titanic Plains', 
                             1, 
                             10, 
                             10, 
                             0,
                             'rollings hills')
siphoned_forest = Environment('Siphoned Forest', 
                              1, 
                              10, 
                              10, 
                              1,
                              'fire and ice')

#Stage 2 Environments
abandoned_aquaduct = Environment('Abandoned Aquaduct', 
                                 2, 
                                 10, 
                                 10, 
                                 0,
                                 'sand beneath your feet')
wetland_aspect = Environment('Wetland Aspect', 
                             2, 
                             10, 
                             10, 
                             0,
                             'twisting roots')
aphelian_sanctuary = Environment('Aphelian Sanctuary', 
                                 2, 
                                 10, 
                                 10, 
                                 1,
                                 'clarity')

#Stage 3 Environments
rallypoint_delta = Environment('Rallypoint Delta', 
                               3, 
                               10, 
                               10, 
                               0,
                               'quiet snowfall')
scorched_acres = Environment('Scorched Acres', 
                             3, 
                             10, 
                             10, 
                             0,
                             'wind, blowing through trees')
sulfur_pools = Environment('Sulfur Pools', 
                           3, 
                           10, 
                           10, 
                           1,
                           'brimstone')

#Stage 4 Environments
abyssal_depths = Environment('Abyssal Depths', 
                             4, 
                             10, 
                             10, 
                             0,
                             'fire')
sirens_call = Environment("Siren's Call", 
                          4, 
                          10, 
                          10, 
                          0,
                          'wind')
sundered_grove = Environment('Sundered Grove', 
                             4, 
                             10, 
                             10, 
                             0,
                             'violent growth')

#Stage 5 Environments
sky_meadow = Environment('Sky Meadow', 
                         5, 
                         10, 
                         10, 
                         0,
                         'serenity')

#Final Stage
commencement = Environment('Commencement', 
                           6, 
                           10, 
                           10, 
                           0,
                           'glass and dirt')
planetarium = Environment('Commencement', 
                          7, 
                          10, 
                          10, 
                          0,
                          'Cell V')

stage_1_environments = [distant_roost, titanic_plains, siphoned_forest]
stage_2_environments = [abandoned_aquaduct, wetland_aspect, aphelian_sanctuary]
stage_3_environments = [rallypoint_delta, scorched_acres, sulfur_pools]
stage_4_environments = [abyssal_depths, sirens_call, sundered_grove]
stage_5_environments = [sky_meadow]
stage_6_environments = [commencement]
stage_7_environments = [planetarium]

def getEnvironmentFromStage(environment_stage):
    random_environment = random.choice(environment_stage)
    return random_environment

#Needs to account for trading items for greens and reds
#Needs to account for selecting lunar items 
def LunarSeer(stage_number):
    try:
        while True:
            if stage_number == 5:
                stage_number = 0
            stage_object = "stage_" + str(stage_number + 1) + "_environments"
            environments = globals()[stage_object]
            
            if len(environments) < 2:
                print("\033[3;2mYou dream of "+environments[0].bazaar_statement+"\033[0m")
                return environments[0]
            else:
                environment_display_case = random.sample(environments, 2)
                print('Choose your next Stage (1,2)')
                print('(1) ' + environment_display_case[0].stage_name + ": \033[94m 2 Lunar Coins\033[0m")
                print('(2) ' + environment_display_case[1].stage_name + ": \033[94m 2 Lunar Coins\033[0m")
                stage_select = input('Choice: ')

                if stage_select in ['1', '2']:
                    print("\033[3;2mYou dream of "+environment_display_case[int(stage_select)-1].bazaar_statement+'\033[0m')
                    return environment_display_case[int(stage_select)-1]
                    break  
                else:
                    print("\033[3;2mInvalid input. Please input a value (1,2)\033[0m")
    except KeyboardInterrupt:
        print("\nThanks for playing!")
        return None

test = LunarSeer(2)



def onStart():
    try:
        while True:
            print('Loading Environments')
            env = getEnvironmentFromStage(stage_1_environments)
            print("You are in: \n", env.stage_name)
            bazaar_condition = input("Would you like to go to the Bazaar Between Time? (\033[1mCost: 3 Lunar Coins\033[0m) (y,N)\n")
            try:
                if bazaar_condition in ['y', 'Y']:
                    print("False\n")
                    break
                elif bazaar_condition in ['n', 'N']:
                    print("False\n")
                    break
            except ValueError:
                print("Invalid Input. Please input either y(es) or n(o)")
    except KeyboardInterrupt:
        print("\nThanks for playing!")
        return None

    

#Hidden Realms
# a_moment_fractured = Environment('A Momement, Fractured', 1, 10, 10, 0)
# a_moment_whole = Environment('A Momement, Whole', 1, 10, 10, 0) 
bazaar_between_time = Environment('Bazaar Between Time', 1, 10, 10, 0, 'Null') #After every stage (Except commencement and planetarium)
bulwarks_ambry = Environment("Bulwark's Ambry", 7, 10, 10, 0,'Null') #Only after Sky Meadow
gilded_coast = Environment("Gilded Coast", 1, 10, 10, 0, 'wealth') #Random
void_fields = Environment("Void Fields", 1, 10, 10, 0, 'Cosmic Prison') #Only occurs after Bazaar
void_locus = Environment('Void Locus', 1, 10, 10, 1, 'potential')
