# Risk of Rain 2 Damage Analyzer

Have you ever thought   

> *Why doesn't Risk of Rain 2 show how much damage an individual item does?*  

or  

> *I wish I could see the probability distribution of how proc-chains work with the items in my inventory?*  

Probably not, but regardless, this project aims to do just that! 


###### Goal

This project aims to create a standalone website that applies both <u>Probability Theory</u> and <u>Information Theory</u> to : 
- Visualize and Simulate Proc-Chains
- Determine Overall DPS
- Determine "Ideal" items for Characters and Character Abilities

## Backend Development Progress
### Survivors and their Abilities (survivor.py)   
##### Defines all the survivors based on their base stats alongside difficulty
Survivors
- [X] Define and Declare all Survivors
- [X] Define and Declare all Survivor Abilities
### Define and Declare Items (items)
##### Defines the all the items and their properties
Defined
- [X] White Items
- [X] Green Items
- [X] Red Items
- [ ] Yellow Items
- [ ] Equipment
- [ ] Void Items    

Item Interpreter
- [X] Interprets White Items useful for DPS calculations
- [ ] Interprets Green Items useful for DPS calculations
- [ ] Interprets Red Items useful for DPS calculations

### Item Simulation (item_simulation.py)
##### Simulates the probability of choosing an item from one of ROR2's many chests.  
- [X] Define and Declare all Chest Types
- [X] Implement randomly receiving an item based on Chest Type Probabilities
- [ ] Implement for all Chest Types
### Environments (environments.py)
##### Simulates moving through all the Stages in Risk of Rain and populating with chests
- [X] Define and Declare all Environemnts
- [ ] Implement Features inside the Bazaar Between Time
    - [X] Lunar Seer
    - [ ] Trading in items for Random Green and Red Items
    - [ ] Random Carousel of Lunar Items
- [ ] Implement all different *Directors* to populate items on different Environments
### Probability (probability.py)
#####  Anything relating to data analysis
- [X] Determine probability of all proc-chains given items of player 
- [ ] Visualize the probability as a distribution
- [ ] Implement Information Theory for determining ideal items
### Damage Per Second (dps.py)
- [X] Calculate the base DPS of the base character and their abilities
- [ ] Calculate the DPS of the items

### Enemies (enemies.py)
- [ ] Define and Declare all enemies
- [ ] Implement spawning of enemies based on environment and scaling
## Frontend Development Progress

Once backend progress nearly complete, Frontend Development Process will start!

### Collaborations
If you want to help with the project, feel free to send a pull request or reach out to me directly through GitHub! :>
