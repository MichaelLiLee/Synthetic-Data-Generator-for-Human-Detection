""" HumanRotationRandomizer

"""

import bpy 
import math
import random
from mathutils import Euler

class HumanRotationRandomizer:
    def __init__(self):
        self.__collection_for_human_rotation_randomize = bpy.data.collections["HumanCollection"]

    def __get_random_rotation(self):
        """ 
        """ 
        random_rot = (
                random.uniform(-30/360, 30/360) * 2 * math.pi, # x axis rotation range -30~30
                random.uniform(0/360, 360/360) * 2 * math.pi, # y axis rotation range 0~360
                random.uniform(-30/360, 30/360) * 2 * math.pi  # z axis rotation range -30~30
                ) 
        return random_rot

    def human_rotation_randomize(self):
        """ 
        """ 
        for obj in self.__collection_for_human_rotation_randomize.objects:
                if obj.type == "ARMATURE": # select armature object only
                    random_rot = self.__get_random_rotation()
                    obj.rotation_euler = Euler(random_rot, 'XYZ')
        
        print("Human Rotation Randomize COMPLERED !!!")

if __name__ == '__main__':
    randomizer = HumanRotationRandomizer()
    randomizer.human_rotation_randomize()