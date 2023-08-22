""" AnimationRandomizer

reference:

link animation to armature obj
https://gist.github.com/PauloBarbeiro/a302229d10faaa32ba065e195748b66f
random frame
https://blender.stackexchange.com/questions/17839/python-render-specific-frames
""" 

import bpy
import os
import glob
import sys
import random

class AnimationRandomizer:
    def __init__(self, asset_animation_folder_path = "C:/Users/user/Documents/project/PeopleSansPeople/Asset/Animation/WIP/Frame250"):
        self.asset_animation_folder_path = asset_animation_folder_path
        self.__collection_need_to_assign_animation = bpy.data.collections["HumanCollection"]
        self.__armatures_need_to_assign_animation_list = list()
        self.__animation_list = list()
        self.__animation_name_list = list()
        self.__animation_num = 0

    def __error_check(self,asset_path_list):
        """
        """
        num_asset_in_folder = len(asset_path_list)
        if num_asset_in_folder < 1:
            print(f'ERROR!!! can not find any animation asset in {self.asset_animation_folder_path}')
            input("Press Enter to continue...")
            sys.exit()

    def __load_animation(self, filepath):
        """ 
        """ 
        ## append animation from .blend file
        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            data_to.actions = data_from.actions

    def __get_armatures_need_to_assign_animation(self):
        """ 
        """ 
        for obj in self.__collection_need_to_assign_animation.objects:
            if obj.type == "ARMATURE":
                armature = obj
                self.__armatures_need_to_assign_animation_list.append(armature)

    def __import_animation_asset(self):
        """ 
        """ 
        ## get animation asset path
        animation_path_list = glob.glob(os.path.join(self.asset_animation_folder_path, "*.blend"))
        self.__error_check(asset_path_list = animation_path_list)

        ## load all animation data into current blend file
        for animation_file_path in animation_path_list:
            self.__load_animation(animation_file_path)

        ## count animation num
        for action in bpy.data.actions:
            self.__animation_list.append(action)
        self.__animation_num = len(self.__animation_list)
        print(f'load animation num: {self.__animation_num}')

        ## show all animation name
        for animation in self.__animation_list:
            self.__animation_name_list.append(animation.name)
        print(f'all loaded animation name: {self.__animation_name_list}')

    def __assign_animation_to_armature(self):
        """ 
        """
        for armature in self.__armatures_need_to_assign_animation_list:
            ## create empty action
            armature.animation_data_create()
            ## random select one animation from animation_list
            animation_selected = random.sample(self.__animation_list, 1)
            ## assign animation to armature
            armature.animation_data.action  = animation_selected[0]

    def __random_frame(self):
        """ 
        """ 
        random_frame = random.randint(1,250)
        print(f'random_frame: {random_frame}')

        bpy.data.scenes['Scene'].frame_set(random_frame)

    def animation_randomize(self):
        """ 
        """
        self.__get_armatures_need_to_assign_animation()
        self.__import_animation_asset()
        self.__assign_animation_to_armature()
        self.__random_frame()

        print("Animation Randomize COMPLERED !!!")
    
if __name__ == '__main__':
    randomizer = AnimationRandomizer()
    randomizer.animation_randomize()