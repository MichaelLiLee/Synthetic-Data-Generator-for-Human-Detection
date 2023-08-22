"""HumanSDGParameter 
"""

class HumanSDGParameter:
    def __init__(self):
        self.gen_num = 400
        self.blender_exe_path = "C:/program Files/Blender Foundation/Blender 3.3/blender"
        self.asset_background_object_folder_path = 'C:/Users/user/Documents/project/synthDet/Asset/background_object'
        self.asset_foreground_object_folder_path = "F:/ProceduralHuman1500"
        self.asset_occluder_folder_path = "C:/Users/user/Documents/project/synthDet/Asset/occluder"
        self.asset_ambientCGMaterial_folder_path = "C:/Users/user/Documents/project/synthDet/Asset/blenderproc_asset/cc_texture"
        self.asset_hdri_lighting_folder_path = "C:/Users/user/Documents/project/synthDet/Asset/Lighting/HDRI"
        self.asset_animation_folder_path = "C:/Users/user/Documents/project/PeopleSansPeople/Asset/Animation/WIP/Frame250"
        self.output_img_path = "F:/PeopleSansPeople_synth40000/images"
        self.output_annotation_path = "F:/PeopleSansPeople_synth40000/annotations_single"
        self.background_poisson_disk_sampling_radius = 0.5
        self.num_foreground_object_in_scene_range = {"min": 1, "max": 6}
        self.foreground_area = [9, 7, 4]
        self.foreground_poisson_disk_sampling_radius = 1.5
        self.num_occluder_in_scene_range = {"min": 5 , "max": 10}
        self.occluder_area = [2.5, 1.5, 0.5]
        self.occluder_poisson_disk_sampling_radius =  0.25
        self.bg_obj_scale_ratio_range = {"min": 6, "max": 6}
        self.fg_obj_scale_ratio_range = {"min": 0.8, "max": 1.5}
        self.occluder_scale_ratio_range = {"min": 0.5, "max": 1.2}
        self.hdri_lighting_strength_range = {"min": 0.1 , "max": 2}
        self.camera_focal_length = 35
        self.img_resolution_x = 640
        self.img_resolution_y = 480
        self.max_samples = 256
        self.chromatic_aberration_probability = 0.1
        self.blur_probability = 0.1
        self.motion_blur_probability = 0.1 
        self.exposure_probability = 0.15
        self.noise_probability = 0.1
        self.white_balance_probability = 0.15
        self.brightness_probability = 0.15
        self.contrast_probability = 0.15
        self.hue_probability = 0.15
        self.saturation_probability = 0.15
        self.chromatic_aberration_value_range = {"min": 0.1, "max": 1}
        self.blur_value_range = {"min": 2, "max": 4}
        self.motion_blur_value_range = {"min": 2, "max": 7}
        self.exposure_value_range = {"min": -0.5, "max": 2}
        self.noise_value_range = {"min": 1.6, "max": 1.8}
        self.white_balance_value_range = {"min": 3500, "max": 9500}
        self.brightness_value_range = {"min": -1, "max": 1}
        self.contrast_value_range = {"min": -1, "max": 5}
        self.hue_value_range =  {"min": 0.45, "max": 0.55}
        self.saturation_value_range = {"min": 0.75, "max": 1.25}