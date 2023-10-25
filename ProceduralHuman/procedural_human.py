"""ProceduralHuman 

"""

import bpy
import random
import os
import subprocess
import datetime
import sys

class ProceduralHuman:

    def __init__(self):
        self.__procedural_human_id = None
        self.__eye_color_values = \
            {"brown": {"IrisMajorColor": [0.135633, 0.0578054, 0.043735, 1], "IrisMinorColor": [0.0352707, 0.0166579, 0.0131311, 1], "IrisSection4Color": [0.0352707, 0.0166579, 0.0131311, 1]},
            "blue":{"IrisMajorColor": [0.0032023, 0.0352672, 0.127302, 1], "IrisMinorColor": [0.0326636, 0.160456, 0.571125, 1], "IrisSection4Color": [0.00464031, 0.0674259, 0.258907, 1]},
            "hazel":{"IrisMajorColor": [0.114435, 0.0722718, 0.0262412, 1], "IrisMinorColor": [0.158961, 0.116971, 0.0331048, 1], "IrisSection4Color": [0.0569951, 0.036909, 0.0144305, 1]},
            "green":{"IrisMajorColor": [0.000910516, 0.0822827, 0.00121413, 1], "IrisMinorColor": [0.000303397, 0.165132, 0.000303574, 1], "IrisSection4Color": [0, 0.0251869, 0, 1]},
            }
        self.blender_exe_path = "C:/Program Files/Blender Foundation/Blender 3.4/blender"
        self.ProceduralHuman_module_path = "C:/Users/user/Documents/project/PeopleSansPeople/Asset/Human/procedural_human.py"
        self.base_human_model_folder_path = "C:/Users/user/Documents/project/PeopleSansPeople/Asset/Human/COCOrig"
        self.procedural_human_save_folder_path = "F:/ProceduralHuman500"
        self.skin_asset_folder_path = "C:/Users/user/Documents/project/PeopleSansPeople/Asset/Human/mpfb_asset/skin"
        self.eye_brow_asset_folder_path = "C:/Users/user/Documents/project/PeopleSansPeople/Asset/Human/mpfb_asset/eyebrows"
        self.eye_lash_asset_folder_path = "C:/Users/user/Documents/project/PeopleSansPeople/Asset/Human/mpfb_asset/eyelashes"
        self.hair_asset_folder_path = {"hair_male" : "C:/Users/user/Documents/project/PeopleSansPeople/Asset/Human/mpfb_asset/hair_male",
                                       "hair_female" : "C:/Users/user/Documents/project/PeopleSansPeople/Asset/Human/mpfb_asset/hair_female"}
        self.hair_male_asset_folder_path = "C:/Users/user/Documents/project/PeopleSansPeople/Asset/Human/mpfb_asset/eyelashes"
        self.hat_asset_folder_path = "C:/Users/user/Documents/project/PeopleSansPeople/Asset/Human/mpfb_asset/hat"
        self.glass_asset_folder_path = "C:/Users/user/Documents/project/PeopleSansPeople/Asset/Human/mpfb_asset/glass"
        self.glove_asset_folder_path = "C:/Users/user/Documents/project/PeopleSansPeople/Asset/Human/mpfb_asset/glove"
        self.shirt_asset_folder_path = "C:/Users/user/Documents/project/PeopleSansPeople/Asset/Human/mpfb_asset/shirt"
        self.pant_asset_folder_path = "C:/Users/user/Documents/project/PeopleSansPeople/Asset/Human/mpfb_asset/pant"
        self.skirt_asset_folder_path = "C:/Users/user/Documents/project/PeopleSansPeople/Asset/Human/mpfb_asset/skirt"
        self.suit_asset_folder_path = "C:/Users/user/Documents/project/PeopleSansPeople/Asset/Human/mpfb_asset/suit"
        self.dress_asset_folder_path = "C:/Users/user/Documents/project/PeopleSansPeople/Asset/Human/mpfb_asset/dress"
        self.shoe_asset_folder_path = "C:/Users/user/Documents/project/PeopleSansPeople/Asset/Human/mpfb_asset/shoe"

        self.eye_color_distribution = {"brown": 0.46, "blue": 0.27, "hazel": 0.18, "green": 0.09}
        self.hair_style_distribution = {"hair_male": 0.5, "hair_female": 0.5}
        self.hair_hat_distribution = {"hair": 0.9, "hat": 0.1}
        self.glass_probability = 0.1
        self.glove_probability = 0.1
        self.cloth_style_distribution = {"shirt_pant": 0.6, "shirt_skirt": 0.1, "suit": 0.2, "dress": 0.1}
        self.shoe_probability = 0.9

    def __create_procedural_human_id(self):
        """ 
        """
        now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))
        time_id = now.strftime("%Y%m%d%H%M%S").zfill(15)
        self.__procedural_human_id = time_id

    def random_open_base_model_then_randomize(self):
        """
        """
        human_base_model_blend_file_path_list = list()

        for blend_file in os.listdir(self.base_human_model_folder_path):
            if blend_file.endswith("blend"):
                human_base_model_blend_file_path_list.append(blend_file)

        print(f"Find {len(human_base_model_blend_file_path_list)} model")

        random_human_model_path = random.choice(human_base_model_blend_file_path_list)

        blend_file_path = os.path.join(self.base_human_model_folder_path, random_human_model_path)

        args = [
                self.blender_exe_path,
                blend_file_path,
                "--python",
                self.ProceduralHuman_module_path
                ]

        subprocess.run(args)


    def skin_randomize(self):
        """ 
        """ 
        skin_name_list = list()

        for filename in os.listdir(self.skin_asset_folder_path):
            skin_name_list.append(filename)

        random_skin = random.choice(skin_name_list)
        
        ## apply random_skin to human
        skin_filepath = os.path.join(self.skin_asset_folder_path, random_skin, random_skin+".mhmat")
        bpy.context.view_layer.objects.active =  bpy.data.objects["Human"]
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_set_active(group='nipple')
        bpy.ops.object.vertex_group_select()
        bpy.ops.object.material_slot_assign()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_set_active(group='lips')
        bpy.ops.object.vertex_group_select()
        bpy.ops.object.material_slot_assign()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_set_active(group='fingernails')
        bpy.ops.object.vertex_group_select()
        bpy.ops.object.material_slot_assign()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_set_active(group='toenails')
        bpy.ops.object.vertex_group_select()
        bpy.ops.object.material_slot_assign()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_set_active(group='ears')
        bpy.ops.object.vertex_group_select()
        bpy.ops.object.material_slot_assign()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_set_active(group='genitals')
        bpy.ops.object.vertex_group_select()
        bpy.ops.object.editmode_toggle()
        bpy.ops.mpfb.load_library_skin(filepath=skin_filepath)

        print(f"Skin {random_skin} Randomize Completed !!!")

    def eye_color_randomize(self):
        """
        """

        # eye_color_list = list()
        # eye_color_distribution_list = list()

        # for color, distribution in self.eye_color_distribution.items():
        #     eye_color_list.append(color)
        #     eye_color_distribution_list.append(distribution)

        #random_eye_color = random.choices(eye_color_list, weights = eye_color_distribution_list, k=1)[0]
        ## https://stackoverflow.com/questions/40927221/how-to-choose-keys-from-a-python-dictionary-based-on-weighted-probability
        random_eye_color = random.choices(list(self.eye_color_distribution.keys()), weights = self.eye_color_distribution.values(), k=1)[0]

        bpy.data.materials["Human.high-poly"].node_tree.nodes["EnhancedEye"].inputs["IrisMajorColor"].default_value = \
        self.__eye_color_values[random_eye_color]["IrisMajorColor"]

        bpy.data.materials["Human.high-poly"].node_tree.nodes["EnhancedEye"].inputs["IrisMinorColor"].default_value = \
        self.__eye_color_values[random_eye_color]["IrisMinorColor"]

        bpy.data.materials["Human.high-poly"].node_tree.nodes["EnhancedEye"].inputs["IrisSection4Color"].default_value = \
        self.__eye_color_values[random_eye_color]["IrisSection4Color"]

        print(f"Eye Color {random_eye_color} Randomize Completed !!!")

    def eye_brow_randomize(self):
        """ 
        """

        eye_brow_name_list = list()

        for filename in os.listdir(self.eye_brow_asset_folder_path):
            eye_brow_name_list.append(filename)

        random_eye_brow = random.choice(eye_brow_name_list)

        ## apply random_eye_brow to human
        eye_brow_filepath = os.path.join(self.eye_brow_asset_folder_path, random_eye_brow, random_eye_brow+".mhclo")
        bpy.context.view_layer.objects.active =  bpy.data.objects["Human.rig"]
        #bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        #bpy.ops.object.shade_smooth()
        bpy.ops.mpfb.load_library_clothes(filepath=eye_brow_filepath, object_type="Eyebrows", material_type="MAKESKIN")

        print(f"Eye Brow {random_eye_brow} Randomize Completed !!!")

    def eye_lash_randomize(self):
        """ 
        """ 

        eye_lash_name_list = list()

        for filename in os.listdir(self.eye_lash_asset_folder_path):
            eye_lash_name_list.append(filename)

        random_eye_lash = random.choice(eye_lash_name_list)

        ## apply random_eye_lash to human
        eye_lash_filepath = os.path.join(self.eye_lash_asset_folder_path, random_eye_lash, random_eye_lash+".mhclo")
        bpy.context.view_layer.objects.active =  bpy.data.objects["Human.rig"]
        #bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        #bpy.ops.object.shade_smooth()
        bpy.ops.mpfb.load_library_clothes(filepath=eye_lash_filepath, object_type="Eyelashes", material_type="MAKESKIN")

        print(f"Eye Lash {random_eye_lash} Randomize Completed !!!")

    def hair_randomize(self):
        """ 
        """

        hair_name_list = list()
        selected_hair_style = None
        selected_hair_style_folder_path = None

        selected_hair_style = random.choices(list(self.hair_style_distribution.keys()), weights = self.hair_style_distribution.values(), k=1)[0]
        selected_hair_style_folder_path = self.hair_asset_folder_path[selected_hair_style]
            
        for filename in os.listdir(selected_hair_style_folder_path):
            hair_name_list.append(filename)

        random_hair = random.choice(hair_name_list)

        ## apply random_hair to human
        hair_filepath = os.path.join(selected_hair_style_folder_path, random_hair, random_hair+".mhclo")
        bpy.context.view_layer.objects.active =  bpy.data.objects["Human.rig"]
        #bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        #bpy.ops.object.shade_smooth()
        bpy.ops.mpfb.load_library_clothes(filepath=hair_filepath, object_type="Hair", material_type="MAKESKIN")

        print(f"Hair {random_hair} Randomize Completed !!!")

    def hat_randomize(self):
        """ 
        """ 

        hat_name_list = list()

        for filename in os.listdir(self.hat_asset_folder_path):
            hat_name_list.append(filename)

        random_hat = random.choice(hat_name_list)
        
        ## apply random_hat to human
        hat_filepath = os.path.join(self.hat_asset_folder_path, random_hat, random_hat+".mhclo")
        bpy.context.view_layer.objects.active =  bpy.data.objects["Human.rig"]
        #bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        #bpy.ops.object.shade_smooth()
        bpy.ops.mpfb.load_library_clothes(filepath=hat_filepath, object_type="Clothes", material_type="MAKESKIN")

        print(f"Hat {random_hat} Randomize Completed !!!")

    def glass_randomize(self):
        """ 
        """ 

        glass_name_list = list()

        for filename in os.listdir(self.glass_asset_folder_path):
            glass_name_list.append(filename)

        random_glass = random.choice(glass_name_list)
        
        ## apply random_glass to human
        glass_filepath = os.path.join(self.glass_asset_folder_path, random_glass, random_glass+".mhclo")
        bpy.context.view_layer.objects.active =  bpy.data.objects["Human.rig"]
        #bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        #bpy.ops.object.shade_smooth()
        bpy.ops.mpfb.load_library_clothes(filepath=glass_filepath, object_type="Clothes", material_type="MAKESKIN")

        print(f"Glass {random_glass} Randomize Completed !!!") 

    def glove_randomize(self):
        """ 
        """ 

        glove_name_list = list()

        for filename in os.listdir(self.glove_asset_folder_path):
            glove_name_list.append(filename)

        random_glove = random.choice(glove_name_list)
        
        ## apply random_glove to human
        glove_filepath = os.path.join(self.glove_asset_folder_path, random_glove, random_glove+".mhclo")
        bpy.context.view_layer.objects.active =  bpy.data.objects["Human.rig"]
        #bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        #bpy.ops.object.shade_smooth()
        bpy.ops.mpfb.load_library_clothes(filepath=glove_filepath, object_type="Clothes", material_type="MAKESKIN")

        print(f"Glove {random_glove} Randomize Completed !!!")

    def shirt_randomize(self):
        """ 
        """ 

        shirt_name_list = list()

        for filename in os.listdir(self.shirt_asset_folder_path):
           shirt_name_list.append(filename)

        random_shirt = random.choice(shirt_name_list)
        
        ## apply random_shirt to human
        shirt_filepath = os.path.join(self.shirt_asset_folder_path, random_shirt, random_shirt+".mhclo")
        bpy.context.view_layer.objects.active =  bpy.data.objects["Human.rig"]
        #bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        #bpy.ops.object.shade_smooth()
        bpy.ops.mpfb.load_library_clothes(filepath=shirt_filepath, object_type="Clothes", material_type="MAKESKIN")

        print(f"Shirt {random_shirt} Randomize Completed !!!")

    def pant_randomize(self):
        """ 
        """ 

        pant_name_list = list()

        for filename in os.listdir(self.pant_asset_folder_path):
           pant_name_list.append(filename)

        random_pant = random.choice(pant_name_list)
        
        ## apply random_pant to human
        pant_filepath = os.path.join(self.pant_asset_folder_path, random_pant, random_pant+".mhclo")
        bpy.context.view_layer.objects.active =  bpy.data.objects["Human.rig"]
        #bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        #bpy.ops.object.shade_smooth()
        bpy.ops.mpfb.load_library_clothes(filepath=pant_filepath, object_type="Clothes", material_type="MAKESKIN")

        print(f"Pant {random_pant} Randomize Completed !!!")

    def skirt_randomize(self):
        """ 
        """ 

        skirt_name_list = list()

        for filename in os.listdir(self.skirt_asset_folder_path):
           skirt_name_list.append(filename)

        random_skirt = random.choice(skirt_name_list)
        
        ## apply random_skirt to human
        skirt_filepath = os.path.join(self.skirt_asset_folder_path, random_skirt, random_skirt+".mhclo")
        bpy.context.view_layer.objects.active =  bpy.data.objects["Human.rig"]
        #bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        #bpy.ops.object.shade_smooth()
        bpy.ops.mpfb.load_library_clothes(filepath=skirt_filepath, object_type="Clothes", material_type="MAKESKIN")

        print(f"Skirt {random_skirt} Randomize Completed !!!")

    def suit_randomize(self):
        """ 
        """ 

        suit_name_list = list()

        for filename in os.listdir(self.suit_asset_folder_path):
           suit_name_list.append(filename)

        random_suit = random.choice(suit_name_list)
        
        ## apply random_suit to human
        suit_filepath = os.path.join(self.suit_asset_folder_path, random_suit, random_suit+".mhclo")
        bpy.context.view_layer.objects.active =  bpy.data.objects["Human.rig"]
        #bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        #bpy.ops.object.shade_smooth()
        bpy.ops.mpfb.load_library_clothes(filepath=suit_filepath, object_type="Clothes", material_type="MAKESKIN")

        print(f"Suit {random_suit} Randomize Completed !!!")

    def dress_randomize(self):
        """ 
        """ 

        dress_name_list = list()

        for filename in os.listdir(self.dress_asset_folder_path):
           dress_name_list.append(filename)

        random_dress = random.choice(dress_name_list)
        
        ## apply random_dress to human
        dress_filepath = os.path.join(self.dress_asset_folder_path, random_dress, random_dress+".mhclo")
        bpy.context.view_layer.objects.active =  bpy.data.objects["Human.rig"]
        #bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        #bpy.ops.object.shade_smooth()
        bpy.ops.mpfb.load_library_clothes(filepath=dress_filepath, object_type="Clothes", material_type="MAKESKIN")

        print(f"Dress {random_dress} Randomize Completed !!!")

    def shoe_randomize(self):
        """ 
        """ 

        shoe_name_list = list()

        for filename in os.listdir(self.shoe_asset_folder_path):
           shoe_name_list.append(filename)

        random_shoe = random.choice(shoe_name_list)
        
        ## apply random_shoe to human
        shoe_filepath = os.path.join(self.shoe_asset_folder_path, random_shoe, random_shoe+".mhclo")
        bpy.context.view_layer.objects.active =  bpy.data.objects["Human.rig"]
        #bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        #bpy.ops.object.shade_smooth()
        bpy.ops.mpfb.load_library_clothes(filepath=shoe_filepath, object_type="Clothes", material_type="MAKESKIN")

        print(f"Shoe {random_shoe} Randomize Completed !!!")

    def mass_location_rotatin_adjust(self):
        """
        """
        bpy.context.scene.cursor.location = bpy.data.armatures["Human.rig"].bones["pelvis"].head_local
        bpy.data.objects["Human.rig"].select_set(True) # select obj
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        ## set location to 0
        bpy.context.object.location[0] = 0
        bpy.context.object.location[1] = 0
        bpy.context.object.location[2] = 0
        ## z axis rotate - 90 deg
        bpy.context.object.rotation_euler[0] = -1.5708
        ## applt rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

        print("Mass Location Rotatin Adjust Completed !!!")

    def mark_as_asset(self):
        """ 
        """
        for obj in bpy.data.collections["Collection"].objects:
            if obj.type == "ARMATURE":
                armature = obj
                armature.data.asset_mark()
            obj.asset_mark()

        print("Mark Asset Completed !!!")

    def save_completed_file(self):
        """
        """
        self.__create_procedural_human_id()
        save_completed_file_name = os.path.basename(bpy.data.filepath).split(".")[0] +"_"+self.__procedural_human_id+".blend"
        save_completed_file_path = os.path.join(self.procedural_human_save_folder_path, save_completed_file_name)

        bpy.ops.wm.save_as_mainfile(filepath = save_completed_file_path)

        print(f"Save blend file at {save_completed_file_path}")

    def gen_one_human(self):
        """ 
        """
        self.skin_randomize()
        self.eye_color_randomize()
        self.eye_lash_randomize()
        self.eye_brow_randomize()

        hair_or_hat = random.choices(list(self.hair_hat_distribution.keys()), weights = self.hair_hat_distribution.values(), k=1)[0]
        if hair_or_hat == "hair":
            self.hair_randomize()
        elif hair_or_hat == "hat":
            self.hat_randomize()

        have_glass = random.choices([True, False], weights = [self.glass_probability, 1 - self.glass_probability], k=1)[0]
        if have_glass:
            self.glass_randomize()

        have_glove = random.choices([True, False], weights = [self.glove_probability, 1 - self.glove_probability], k=1)[0]
        if have_glove:
            self.glass_randomize()

        cloth_style = random.choices(list(self.cloth_style_distribution.keys()), weights = self.cloth_style_distribution.values(), k=1)[0]
        if cloth_style == "shirt_pant":
            self.shirt_randomize()
            self.pant_randomize()
        if cloth_style == "shirt_skirt":
            self.shirt_randomize()
            self.skirt_randomize()
        if cloth_style == "suit":
            self.suit_randomize()
        if cloth_style == "dress":
            self.dress_randomize()

        have_shoe = random.choices([True, False], weights = [self.shoe_probability, 1 - self.shoe_probability], k=1)[0]
        if have_shoe:
            self.shoe_randomize()

        self.mark_as_asset()
        #self.mass_location_rotatin_adjust()
        self.save_completed_file()
        sys.exit()

    def test(self):
        """ 
        """ 
        have_shoe = random.choices([True, False], weights = [self.shoe_probability, 1 - self.shoe_probability], k=1)[0]
        if have_shoe:
            self.shoe_randomize()

if __name__ == "__main__":

    procedural_human = ProceduralHuman()
    procedural_human.gen_one_human()
