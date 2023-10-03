import bpy 
import math
import random
from mathutils import Euler


class HumanRotationRandomizer:
    """
    A randomizer class which assigns a random rotation to all foreground (virtual human) objects.
    The difference between this and RotationRandomizer is that here, the same rotation is applied to all target objects.

    Attributes
    ----------
    __collection_for_human_rotation_randomize (list of bpy.types.Collection): List of the blender collections which need to been rotated.

    Methods
    -------
    __get_random_rotation(): Generate a random rotation in radians.
    human_rotation_randomize(): Applies unified random rotation to all objects in foreground collections.

    """

    def __init__(self):
        self.__collection_for_human_rotation_randomize = bpy.data.collections["HumanCollection"]


    def __get_random_rotation(self):
        """ Generate a random rotation in radians.

        Return:
            random_rot (tuple of float): Random rotation in radians.

        """ 
        random_rot = (
                random.uniform(-30/360, 30/360) * 2 * math.pi, # X axis rotation range -30~30
                random.uniform(0/360, 360/360) * 2 * math.pi, # Y axis rotation range 0~360
                random.uniform(-30/360, 30/360) * 2 * math.pi  # Z axis rotation range -30~30
                ) 
        return random_rot


    def human_rotation_randomize(self):
        """ Applies unified random rotation to all objects (virtual human) in foreground collections."""  
        for obj in self.__collection_for_human_rotation_randomize.objects:
                if obj.type == "ARMATURE": # Select armature object only
                    random_rot = self.__get_random_rotation()
                    obj.rotation_euler = Euler(random_rot, 'XYZ')
        
        print("Human Rotation Randomize COMPLERED !!!")


if __name__ == '__main__':
    randomizer = HumanRotationRandomizer()
    randomizer.human_rotation_randomize()