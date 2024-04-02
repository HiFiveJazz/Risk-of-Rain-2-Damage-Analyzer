#This file defines all the stats for items in Risk of Rain 2 up to the Void DLC
import numpy as np
class Proc_Coeffecient_Item:
    def __init__(self, 
                 chance,
                 proc_coefficient,
                 damage):

        self.chance = chance
        self.proc_coefficient = proc_coefficient  
        self.damage = damage
#Creating Items
atg_missile_mk = Proc_Coeffecient_Item(0.1, 1.0, 3.0)
ukulele = Proc_Coeffecient_Item(0.2, 2.0, 6.0)
dang = Proc_Coeffecient_Item(0.3, 3.0, 9.0)

