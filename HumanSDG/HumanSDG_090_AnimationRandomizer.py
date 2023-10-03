import bpy
import os
import glob
import sys
import random


class AnimationRandomizer:
    """ 
    A randomizer class which randomizes the pose applied to the virtual human character. 
    The pose is a randomly chosen frame from a randomly chosen animation from the asset database of human animations.

    Attributes
    ----------
    asset_animation_folder_path (str): The path to the animation assets directory.
    __collection_need_to_assign_animation (bpy.types.Collection): The blender collection which need to apply animation.
    __armatures_need_to_assign_animation_list (list of bpy.types.Armature): A list of the blender armatures which need to apply animation.
    __animation_list (list of bpy.types.Action): All animation data in current blender file.
    __animation_name_list (list of str): All animation names in current blender file.
    __animation_num (int): Number of animation data in current blender file.

    Methods
    -------
    __error_check(): Check assigned animation assets folder path isn't empty.
    __load_animation(): Load animation asset from other blendfile to the current blendfile.
    __get_armatures_need_to_assign_animation(): Get all armature objects which need assign animation.
    __import_animation_asset(): Import all animation data from the animation dataset into the current blender file.
    __assign_animation_to_armature(): Assign animation data to all armature objects in the __armatures_need_to_assign_animation_list.
    __random_frame(): Randomly select currect blender scene frame number.
    animation_randomize(): Randomly apply animation to armatures.

    References
    link animation to armature obj, https://gist.github.com/PauloBarbeiro/a302229d10faaa32ba065e195748b66f.
    random frame, https://blender.stackexchange.com/questions/17839/python-render-specific-frames.
    ----------


    """ 

    def __init__(self, asset_animation_folder_path = "C:/Users/user/Documents/project/PeopleSansPeople/Asset/Animation/WIP/Frame250"):
        self.asset_animation_folder_path = asset_animation_folder_path
        self.__collection_need_to_assign_animation = bpy.data.collections["HumanCollection"]
        self.__armatures_need_to_assign_animation_list = list()
        self.__animation_list = list()
        self.__animation_name_list = list()
        self.__animation_num = 0


    def __error_check(self,asset_path_list):
        """Check assigned animation assets folder path isn't empty."""
        num_asset_in_folder = len(asset_path_list)
        if num_asset_in_folder < 1:
            print(f'ERROR!!! can not find any animation asset in {self.asset_animation_folder_path}')
            input("Press Enter to continue...")
            sys.exit()


    def __load_animation(self, filepath):
        """Load animation asset from other blendfile to the current blendfile.""" 
        # Append animation from .blend file
        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            data_to.actions = data_from.actions

    def __get_armatures_need_to_assign_animation(self):
        """Get all armature objects which need assign animation.""" 
        for obj in self.__collection_need_to_assign_animation.objects:
            if obj.type == "ARMATURE":
                armature = obj
                self.__armatures_need_to_assign_animation_list.append(armature)


    def __import_animation_asset(self):
        """Import all animation data from the animation dataset into the current blender file.""" 
        # Get animation asset path
        animation_path_list = glob.glob(os.path.join(self.asset_animation_folder_path, "*.blend"))
        self.__error_check(asset_path_list = animation_path_list)

        # Load all animation data into current blend file
        for animation_file_path in animation_path_list:
            self.__load_animation(animation_file_path)

        # Count animation num
        for action in bpy.data.actions:
            self.__animation_list.append(action)
        self.__animation_num = len(self.__animation_list)
        print(f'load animation num: {self.__animation_num}')

        # Show all animation name
        for animation in self.__animation_list:
            self.__animation_name_list.append(animation.name)
        print(f'all loaded animation name: {self.__animation_name_list}')


    def __assign_animation_to_armature(self):
        """Assign animation data to all armature objects in the __armatures_need_to_assign_animation_list."""
        for armature in self.__armatures_need_to_assign_animation_list:
            # Create empty action
            armature.animation_data_create()
            # Random select one animation from animation_list
            animation_selected = random.sample(self.__animation_list, 1)
            # Assign animation to armature
            armature.animation_data.action  = animation_selected[0]


    def __random_frame(self):
        """Randomly select currect blender scene frame number.""" 
        random_frame = random.randint(1,250)
        print(f'random_frame: {random_frame}')

        bpy.data.scenes['Scene'].frame_set(random_frame)


    def animation_randomize(self):
        """Randomly apply animation to armatures."""
        self.__get_armatures_need_to_assign_animation()
        self.__import_animation_asset()
        self.__assign_animation_to_armature()
        self.__random_frame()

        print("Animation Randomize COMPLERED !!!")
    

if __name__ == '__main__':
    randomizer = AnimationRandomizer()
    randomizer.animation_randomize()