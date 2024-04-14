import random
class Environment:
    def __init__(self, 
                 stage_name,
                 stage_number,
                 time,
                 number_of_chests,
                 dlc):
        self.stage_name = stage_name
        self.stage_number = stage_number 
        self.time = time 
        self.number_of_chests = number_of_chests 
        self.dlc = dlc

#Stage 1 Environments
distant_roost = Environment('Distant Roost', 1, 10, 10, 0)
titanic_plains = Environment('Titanic Plains', 1, 10, 10, 0)
siphoned_forest = Environment('Siphoned Forest', 1, 10, 10, 1)

#Stage 2 Environments
abandoned_aquaduct = Environment('Abandoned Aquaduct', 2, 10, 10, 0)
wetland_aspect = Environment('Wetland Aspect', 2, 10, 10, 0)
aphelian_sanctuary = Environment('Aphelian Sanctuary', 2, 10, 10, 1)

#Stage 3 Environments
rallypoint_delta = Environment('Rallypoint Delta', 3, 10, 10, 0)
scorched_acres = Environment('Scorched Acres', 3, 10, 10, 0)
sulfur_pools = Environment('Sulfur Pools', 3, 10, 10, 1)

#Stage 4 Environments
abyssal_depths = Environment('Abyssal Depths', 4, 10, 10, 0)
sirens_call = Environment("Siren's Call", 4, 10, 10, 0)
sundered_grove = Environment('Sundered Grove', 4, 10, 10, 0)

#Stage 5 Environments
sky_meadow = Environment('Sky Meadow', 5, 10, 10, 0)

#Final Stage
commencement = Environment('Commencement', 6, 10, 10, 0)
planetarium = Environment('Commencement', 7, 10, 10, 0)

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

def BazaarCondition(stage_number): 
    if stage_number == 5:
        stage_number = 0
    stage_object = "stage_" + str(stage_number+1) + "_environments"
    environments = globals()[stage_object]
    if len(environments) < 2:
        environment_display_case = environments[0].stage_name
        print(environment_display_case)
    else:
        environment_display_case = random.sample(environments, 2)
        for environment in environment_display_case:
            print(environment.stage_name+'\n')
        print('Choose your next Stage (1,2)\n')
        print('(1) '+environment_display_case[0].stage_name+'\n')
        stage_select = input('(2) '+environment_display_case[1].stage_name+'\n')
BazaarCondition(2)



def onStart():
    try:
        while True:
            print('Loading Environments')
            env = getEnvironmentFromStage(stage_1_environments)
            print("You are in: \n", env.stage_name)
            bazaar_condition = input("Would you like to go to the Bazaar Between Time? (y,N)\n")
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
bazaar_between_time = Environment('Bazaar Between Time', 1, 10, 10, 0) #After every stage (Except commencement and planetarium)
bulwarks_ambry = Environment("Bulwark's Ambry", 7, 10, 10, 0) #Only after Sky Meadow
gilded_coast = Environment("Gilded Coast", 1, 10, 10, 0) #Random
void_fields = Environment("Void Fields", 1, 10, 10, 0) #Only occurs after Bazaar
void_locus = Environment('Void Locus', 1, 10, 10, 1)
the_planetarium = Environment('The Planetarium', 1, 10, 10, 1)
