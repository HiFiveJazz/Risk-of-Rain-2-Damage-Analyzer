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

#Hidden Realms
# a_moment_fractured = Environment('A Momement, Fractured', 1, 10, 10, 0)
# a_moment_whole = Environment('A Momement, Whole', 1, 10, 10, 0) 
bazaar_between_time = Environment('Bazaar Between Time', 1, 10, 10, 0) #After every stage (Except commencement and planetarium)
bulwarks_ambry = Environment("Bulwark's Ambry", 7, 10, 10, 0) #Only after Sky Meadow
gilded_coast = Environment("Gilded Coast", 1, 10, 10, 0) #Random
void_fields = Environment("Void Fields", 1, 10, 10, 0) #Only occurs after Bazaar
void_locus = Environment('Void Locus', 1, 10, 10, 1)
the_planetarium = Environment('The Planetarium', 1, 10, 10, 1)
