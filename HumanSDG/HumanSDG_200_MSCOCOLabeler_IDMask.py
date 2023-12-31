import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
import numpy as np
from collections import OrderedDict
import copy
import datetime
import os
import json


class MSCOCOLabeler:
    """ 
    A class that renders the current Blender scene, outputs the synthetic image in PNG format, 
    and generates annotation/labeling data for virtual human bounding boxes and skeleton keypoints in MSCOCO format JSON file.

    Attributes
    ----------
    output_img_path (str): The path where rendered images will be saved.
    output_annotation_path (str): The path where MSCOCO format bounding box and skeleton keypoints annotations will be saved.
    __scene (bpy.types.Scene): The blender scene data-block of current virtual environment.
    __camera (bpy.types.Camera): The blender camera data-block.
    __clip_start (float): Camera near clipping distance.
    __clip_end (float): Camera far clipping distance.
    __target_obj_collections (list of bpy.types.Collection): The collection that needs extract bounding box and skeleton keypoints annotation from its containing virtual human objects.
    __armature_object_list (list of bpy.types.Armature): List of armature objects in current blender scene.
    __armature_can_see_list (list of bpy.types.Armature): List of armature objects visible in the camera view in the current Blender scene.
    __keypoint_can_see_list (list of bpy.types.Armature & bpy.types.PoseBone & str): List of armature bone joints visible in the camera view in the current Blender scene.
    __armature_annotation_list (list of bpy.types.Armature & dict): List of virtual human objects and their corresponding annotation data.
    __rig_obj_and_id_dict (dict of bpy.types.Armature: int): List of virtual human objects and their corresponding ID number.
    __rig_obj_and_parent_mesh_obj_dict (dict of bpy.types.Armature: list of bpy.types.Mesh): List of armature objects and their corresponding mesh objects.
    __minimum_armature_pixel (int): Filter armature objects based on the minimum number of pixels.
    __minimum_keypoint_num (int): Filter armature objects based on the minimum number of keypoints in camera view.
    __gen_img_id (str): ID of generated synthetic image data.
    __render_machine_id (str): ID of rendering PC.
    __keypoint_bone_mapping_dict (dict of str: list fo str): Mapping between mscoco 17 keypoints name and their corresponding blender bone joint name.
    __reference_bbox_value_dict (dict of str: int): Reference of mscoco object detection task annotation "bbox" format.
    __default_keypoint_value_dict (dict of str: list fo int): Default keypoint names[str] and value[x1,y1,v1,...] of mscoco keypoint annotation.
    __reference_mscoco_json_format (dict): Reference of mscoco data format https://cocodataset.org/#format-data
    __default_mscoco_json_format (dict): Default mscoco data format.
    __default_mscoco_annotations_part_dict (dict): Default mscoco data "annotations" format.
    __output_mscoco_json_dict (dict): Dict to store generated annotation data.

    Methods
    -------
    __create_gen_img_id(): Create a unique ID for generated synthetic image data.
    __get_all_armature_object_in_target_obj_collections(): Retrieve all armature objects from the Blender collection named "__target_obj_collections".
    __create_and_switch_annotation_scene(): Copy current Blender scene for annotation/labeling purpose and switch to the copy scene.
    __create_id_mask_nodes(): Create ID Mask Node for annotation/labeling purpose.
    __add_pass_index(): Add index number for the "Object Index" render pass.
    __annotation_render(): Render image for annotation/labeling purpose.
    __get_all_armature_can_see(): Retrieve all armature objects from the Blender scene that are visible in the camera view.
    __get_all_keypoint_can_see(): Retrieve the names of all armature bone joints from the Blender scene that are visible in the camera view.
    __get_keypoint_global_coordinate(): Get armature bone joint global coordinates in current Blender scene.
    __check_keypoint_in_cam_view(): Check if the armature bone joint is visible in the camera view.
    __get_bbox_image_coordinates(): Retrieve data for the image coordinates of the bounding box of the virtual human object.
    __get_keypoint_image_coordinates(): Retrieve data for the image coordinates of the skeleton keypoint of the virtual human object.
    __get_key_from_value(): Find dictionary key name based on its corresponding value.
    __get_all_armature_annotation(): Retrieve all annotation data from virtual human objects that are visible in the camera view.
    __convert_to_mscoco_format(): Convert all annotation data to MSCOCO format.
    __render_img_and_save_annotation(): Render the image and generate the corresponding annotation/labeling data.
    auto_labeling(): Main process for rendering and labeling data.

    References
    ----------
    1.https://blender.stackexchange.com/questions/35982/how-to-get-posebone-global-location
    2.https://blender.stackexchange.com/questions/284163/how-can-i-get-the-global-location-of-a-pose-bones-tail-using-only-the-bones-he
    3.https://stackoverflow.com/questions/3061/calling-a-function-of-a-module-by-using-its-name-a-string
    4.https://blender.stackexchange.com/questions/882/how-to-find-image-coordinates-of-the-rendered-vertex/1008#1008
    5.https://blender.stackexchange.com/questions/264385/object-index-blender-3-0/264394#264394
    6.https://blender.stackexchange.com/questions/39969/any-idea-how-to-get-the-location-and-bounds-of-object-in-the-image/39983#39983
    7.https://splunktool.com/bounding-box-from-2d-numpy-array-duplicate
    8.https://github.com/DIYer22/bpycv/blob/master/bpycv/render_utils.py
    9.https://blender.stackexchange.com/questions/167134/how-to-get-all-of-the-meshes-that-are-attached-to-an-armature-via-python

    """ 

    def __init__(self,
                 output_img_path = "C:/Users/user/Documents/project/PeopleSansPeople/gen_data/images",
                 output_annotation_path = "C:/Users/user/Documents/project/PeopleSansPeople/gen_data/annotations_single"
                 ):

        self.output_img_path = output_img_path
        self.output_annotation_path = output_annotation_path
        self.__scene = bpy.data.scenes["Scene"]
        self.__camera = bpy.data.objects['Camera']
        self.__clip_start = bpy.data.objects['Camera'].data.clip_start
        self.__clip_end = bpy.data.objects['Camera'].data.clip_end
        self.__target_obj_collections = [bpy.data.collections["HumanCollection"]]
        self.__armature_object_list = list() # Data format : [armature object1,armature object2,...]
        self.__armature_can_see_list = list() # Data format : [armature object1,armature object2,...]
        self.__keypoint_can_see_list = list() # Data format : [armature object,[[pose_bones_name1,joint_name1],[pose_bones_name2,joint_name2]]]
        self.__armature_annotation_list = list() # Data format : [[armature_obj_1, bbox_value_dict, keypoint_value_dict],[armature_obj_2, ...]]
        self.__rig_obj_and_id_dict = dict() # Data format : {'rig_obj': 1, ...}
        self.__rig_obj_and_parent_mesh_obj_dict = dict() # Data format : {'rig_obj': [mesh_obj01, mesh_obj02], ....}
        self.__minimum_armature_pixel = 100
        self.__minimum_keypoint_num = 3
        self.__gen_img_id = None
        self.__render_machine_id = "a"
        self.__keypoint_bone_mapping_dict = OrderedDict({
            "nose" : ["nose","head"],
            "left_eye" : ["eye_l","head"],"right_eye" : ["eye_r","head"],
            "left_ear" : ["ear_l","head"],"right_ear" : ["ear_r","head"],
            "left_shoulder" : ["upperarm_l","head"],"right_shoulder" : ["upperarm_r","head"],
            "left_elbow" : ["lowerarm_l","head"],"right_elbow" : ["lowerarm_r","head"],
            "left_wrist" : ["hand_l","head"],"right_wrist" : ["hand_r","head"],
            "left_hip" : ["thigh_l","head"],"right_hip" : ["thigh_r","head"],
            "left_knee" : ["calf_l","head"],"right_knee" : ["calf_r","head"],
            "left_ankle" : ["foot_l","head"],"right_ankle" : ["foot_r","head"],
            })
        # No use, reference only
        self.__reference_bbox_value_dict = OrderedDict({
            "x": 0,
            "y": 0,
            "width": 0,
            "height": 0
            })
        self.__default_keypoint_value_dict = OrderedDict({
            "nose" : [0,0,0],
            "left_eye" : [0,0,0],"right_eye" :[0,0,0],
            "left_ear" : [0,0,0],"right_ear" :[0,0,0],
            "left_shoulder" : [0,0,0],"right_shoulder" :[0,0,0],
            "left_elbow" : [0,0,0],"right_elbow" :[0,0,0],
            "left_wrist" : [0,0,0],"right_wrist" :[0,0,0],
            "left_hip" : [0,0,0],"right_hip" :[0,0,0],
            "left_knee" : [0,0,0],"right_knee" :[0,0,0],
            "left_ankle" : [0,0,0],"right_ankle" :[0,0,0],
            })
        # No use, reference only
        self.__reference_mscoco_json_format = dict({
            "categories": [{"id": 0, "name": "person"}],
            "images":[{"id" : "a0201", "file_name":"a0201.jpg", "height": 480, "width": 640}],
            "annotations":[{"id": "a0201_1", "image_id": "a0201", "category_id": 0, "bbox": ['x','y','width','height'],
                            "area":'width*height', "iscrowd": 0, "keypoints": [], "num_keypoints":17}]
        })
        self.__default_mscoco_json_format = dict({
            "categories": [{"id": 0, "name": "person"}],
            "images":[{"id" : None, "file_name": None, "height": None, "width": None}],
            "annotations":[]
        })
        self.__default_mscoco_annotations_part_dict = {"id": None, "image_id": None, "category_id": 0,
                                                     "bbox": [], "area": 0, "iscrowd": 0, "keypoints": [],
                                                      "num_keypoints": 0}
        self.__output_mscoco_json_dict = None


    def __create_gen_img_id(self):
        """Create a unique ID for generated synthetic image data."""
        now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))
        time_id = now.strftime("%Y%m%d%H%M%S").zfill(15)
        render_machine_id = self.__render_machine_id
        self.__gen_img_id = render_machine_id + time_id


    def __get_all_armature_object_in_target_obj_collections(self):
        """Retrieve all armature objects from the Blender collection named "__target_obj_collections".""" 
        for collection in self.__target_obj_collections:
            for target_obj in collection.objects:
                if target_obj.type == "ARMATURE":
                    self.__armature_object_list.append(target_obj)


    def __create_and_switch_annotation_scene(self):
        """Copy current Blender scene for annotation/labeling purpose and switch to the copy scene."""
        scene_list = []
        for scene in bpy.data.scenes:
            scene_list.append(scene.name)

        if ("Scene_Annot" not in scene_list):
            bpy.data.scenes['Scene'].copy()
            bpy.data.scenes["Scene.001"].name = "Scene_Annot"

        bpy.context.window.scene = bpy.data.scenes["Scene_Annot"]


    def  __create_id_mask_nodes(self):
        """Create ID Mask Node for annotation/labeling purpose."""
        # Active compositing nodes
        bpy.data.scenes['Scene_Annot'].use_nodes = True

        # Clear all nodes
        bpy.data.scenes['Scene_Annot'].node_tree.nodes.clear()

        # Activate object index pass
        bpy.data.scenes['Scene_Annot'].view_layers["ViewLayer"].use_pass_object_index = True

        # Add new nodes
        node_RenderLayers = bpy.data.scenes['Scene_Annot'].node_tree.nodes.new("CompositorNodeRLayers")
        node_Composite = bpy.data.scenes['Scene_Annot'].node_tree.nodes.new("CompositorNodeComposite")
        node_Viewer = bpy.data.scenes['Scene_Annot'].node_tree.nodes.new("CompositorNodeViewer")
  
        node_RenderLayers.location = (-100,0)
        node_Composite.location = (250,0)
        node_Viewer.location = (600,-200)

        # Link nodes
        links = bpy.data.scenes['Scene_Annot'].node_tree.links
        links.new(node_RenderLayers.outputs["Image"], node_Composite.inputs["Image"])
        links.new(node_RenderLayers.outputs["IndexOB"], node_Viewer.inputs["Image"])

        print("Create ID Mask Nodes Completed!")


    def __add_pass_index(self):
        """Add index number for the "Object Index" render pass.""" 
        bpy.data.scenes['Scene_Annot'].view_layers["ViewLayer"].use_pass_object_index = True
      
        for index, rig_obj in enumerate(self.__armature_object_list, start=1):
            mesh_obj_list = list()
            for collection in self.__target_obj_collections:
                for obj in collection.objects:
                    if (obj.type == "MESH" and obj.parent == rig_obj):
                        obj.pass_index = index
                        mesh_obj_list.append(obj)
            self.__rig_obj_and_id_dict[rig_obj] = index
            self.__rig_obj_and_parent_mesh_obj_dict[rig_obj] = mesh_obj_list

        print("Add Obj Index Completed!")


    def __annotation_render(self):
        """Render image for annotation/labeling purpose."""
        # Render using Cycle
        bpy.data.scenes['Scene_Annot'].render.engine = "CYCLES"
        bpy.data.scenes['Scene_Annot'].cycles.device = "GPU"
        bpy.data.scenes['Scene_Annot'].cycles.samples = 1
        bpy.data.scenes['Scene_Annot'].cycles.use_denoising = False
        print("Start Render Annot")
        bpy.ops.render.render(scene='Scene_Annot')
        print("End Render Annot")


    def __get_all_armature_can_see(self):
        """Retrieve all armature objects from the Blender scene that are visible in the camera view.""" 
        self.__annotation_render()
        for armature_obj, id in self.__rig_obj_and_id_dict.items():
            print(f'armature_obj, id : {armature_obj}, {id}')
            S = bpy.data.scenes['Scene_Annot']
            width  = int(S.render.resolution_x * S.render.resolution_percentage / 100)
            height = int(S.render.resolution_y * S.render.resolution_percentage / 100)
            depth  = 4

            img = np.array( bpy.data.images['Viewer Node'].pixels[:] ).reshape( [height, width, depth] )
            img = np.array( [ [ img[0] for img in row ] for row in img] )

            img = (img == id).astype(int) # https://stackoverflow.com/questions/19766757/replacing-numpy-elements-if-condition-is-met

            if img.max() == 0: # No armature object in view
                continue
            if (img > 0).sum() <= self.__minimum_armature_pixel: # Armature object too small in view
                continue

            self.__armature_can_see_list.append(armature_obj)
            print(f"armature_can_see: {armature_obj.name}")


    def __get_all_keypoint_can_see(self):
        """Retrieve the names of all armature bone joints from the Blender scene that are visible in the camera view. 

        This function will update attribute named "__self.keypoint_can_see_list".

        Update format : [[armature object,[[pose_bone_name1,joint_name1],[pose_bone_name2,joint_name2]]],
                        [armature object2,[[pose_bone_name1,joint_name1],[pose_bone_name2,joint_name2]]],...]

        """ 
        for armature in self.__armature_can_see_list:

            pose_bone_name_and_joint_name_list = list()

            for keypoint_name, bone_and_joint in self.__keypoint_bone_mapping_dict.items():
                pose_bone_name = bone_and_joint[0]
                pose_bone = armature.pose.bones[pose_bone_name]
                bone_joint = bone_and_joint[1]
                keypoint_global_coordinate = self.__get_keypoint_global_coordinate(armature, pose_bone, bone_joint)

                if self.__check_keypoint_in_cam_view(keypoint_global_coordinate):
                    pose_bone_name_and_joint_name_list.append([pose_bone_name, bone_joint])

            if len(pose_bone_name_and_joint_name_list) >= self.__minimum_keypoint_num:
                self.__keypoint_can_see_list.append([armature,pose_bone_name_and_joint_name_list])
                print(f"keypoint_can_see : {armature.name} {pose_bone_name_and_joint_name_list}")
            else:
                print("Not Any Keypoint cant see!!!")


    def __get_keypoint_global_coordinate(self, armature_object, pose_bone, bone_joint):
        """Get armature bone joint global coordinates in current Blender scene.

        Args:
            armature_object (bpy.types.Armature): Armature object that require coordinate conversion.
            pose_bone (bpy.types.PoseBone): Armature Bone that require coordinate conversion.
            bone_joint (str): Armature bone joint names that require coordinate conversion.

        Return:
            global_coordinate_list (list of float): Armature bone joint global coordinates.

        """
        #print(f'Armature name : {armature_object.name} / ', f'Pose Bone name : {pose_bone.name} / ', f'Bone Joint : {bone_joint}')
        global_coordinate_vector = armature_object.matrix_world @ getattr(pose_bone, bone_joint)
        global_coordinate_list = global_coordinate_vector[:] # Convert vector to list
        #print(f'Keypoint Global Coordinate : {global_coordinate_list}')
        return list(global_coordinate_list)


    def __check_keypoint_in_cam_view(self, keypoint_global_coordinate: list):
        """Check if the armature bone joint is visible in the camera view.

        Args:
            keypoint_global_coordinate (list of float): Armature bone joint global coordinates.

        """
        # World space to ndc space
        vector_p = Vector(keypoint_global_coordinate)
        co_ndc = world_to_camera_view(self.__scene, self.__camera, vector_p)
        # Check wether point is inside frustum
        if (0.0 < co_ndc.x < 1.0 and 0.0 < co_ndc.y < 1.0 and self.__clip_start < co_ndc.z < self.__clip_end):
            return True
        else:
            return False


    def __get_bbox_image_coordinates(self, armature_object):
        """Retrieve data for the image coordinates of the bounding box of the virtual human object.

        Args:
            armature_object (bpy.types.Armature): Armature object need to retrieve bounding box annotation data.

        Return:
        bbox_value_dict (dict of str: int): Bounding box top left image coordinate and box width、height information.

        """ 
        print(f"find {armature_object.name} bbox") 

        S = bpy.data.scenes['Scene_Annot']
        width  = int(S.render.resolution_x * S.render.resolution_percentage / 100)
        height = int(S.render.resolution_y * S.render.resolution_percentage / 100)
        depth  = 4

        img = np.array( bpy.data.images['Viewer Node'].pixels[:] ).reshape( [height, width, depth] )
        img = np.array( [ [ img[0] for img in row ] for row in img] )

        id = self.__rig_obj_and_id_dict[armature_object]
        img = (img == id).astype(int) # https://stackoverflow.com/questions/19766757/replacing-numpy-elements-if-condition-is-met

        img_flip = np.flip(img,0)
        y, x = np.where(img_flip)

        bbox_x = int(x.min())
        bbox_y =  int(y.min())
        bbox_width = int(x.max() - x.min()) + 1
        bbox_height = int(y.max() - y.min()) + 1

        bbox_value_dict = dict({"x": bbox_x,"y": bbox_y,"width": bbox_width,"height": bbox_height})

        return bbox_value_dict


    def __get_keypoint_image_coordinates(self, armature_object, pose_bone, bone_joint):
        """Retrieve data for the image coordinates of the skeleton keypoint of the virtual human object.""" 
        # World space to ndc space
        keypoint_global_coordinate = self.__get_keypoint_global_coordinate(armature_object, pose_bone, bone_joint)
        vector_p = Vector(keypoint_global_coordinate)
        co_ndc = world_to_camera_view(self.__scene, self.__camera, vector_p)
        
        # Ndc space to image space
        render_scale = self.__scene.render.resolution_percentage / 100
        image_width = int(self.__scene.render.resolution_x * render_scale)
        image_hight = int(self.__scene.render.resolution_y * render_scale)

        keypoint_image_coordinates = [round(co_ndc.x * image_width),round((1 - co_ndc.y) * image_hight)]

        return keypoint_image_coordinates


    def __get_key_from_value(self, dict, value):
        """Find dictionary key name based on its corresponding value.""" 
        return[k for k, v in dict.items() if v == value] 


    def __get_all_armature_annotation(self):
        """Retrieve all annotation data from virtual human objects that are visible in the camera view. 

        This function will loop through all armature objects and their pose joints in attribute named "self.__keypoint_can_see_list", 
        then calculate armature object's bounding box and pose joint's keypoint annotation information, then update 
        those information to attribute named "self.__armature_annotation_list".
        
        Update format : [[armature_obj_1, bbox_value_dict, keypoint_value_dict],[armature_obj_2, ...]]

        """ 
        
        for data in self.__keypoint_can_see_list:
            armature_object = data[0]
            # Get bbox_value_dict
            bbox_value_dict = self.__get_bbox_image_coordinates(armature_object)

            # Get keypoint_value_dict
            pose_bone_and_joint_list = data[1] # Data type: [[pose_bones_name1,joint_name1],[pose_bones_name2,joint_name2], ...]
            keypoint_value_dict = copy.deepcopy(self.__default_keypoint_value_dict)

            for pose_bone_name, bone_joint in pose_bone_and_joint_list:
                pose_bone = armature_object.pose.bones[pose_bone_name]
                keypoint_img_coord = self.__get_keypoint_image_coordinates(armature_object, pose_bone, bone_joint) # Return [x,y]
                # Find keypoint name from self.__keypoint_bone_mapping_dict
                bone = [pose_bone_name, bone_joint]
                keypoint_name = self.__get_key_from_value(self.__keypoint_bone_mapping_dict, bone)[0]
                # Update_keypoint_value_dict 
                keypoint_value_dict[keypoint_name][0] = keypoint_img_coord[0]
                keypoint_value_dict[keypoint_name][1] = keypoint_img_coord[1]
                keypoint_value_dict[keypoint_name][2] = 2

            self.__armature_annotation_list.append([armature_object,bbox_value_dict,keypoint_value_dict])


    def __convert_to_mscoco_format(self):
        """ Convert all annotation data to MSCOCO format."""
        self.__output_mscoco_json_dict = copy.deepcopy(self.__default_mscoco_json_format)


        self.__output_mscoco_json_dict["images"][0]["id"] = self.__gen_img_id
        self.__output_mscoco_json_dict["images"][0]["file_name"] = self.__gen_img_id+".png"

        render_scale = self.__scene.render.resolution_percentage / 100
        image_width = int(self.__scene.render.resolution_x * render_scale)
        image_hight = int(self.__scene.render.resolution_y * render_scale)
        self.__output_mscoco_json_dict["images"][0]["height"] = image_hight
        self.__output_mscoco_json_dict["images"][0]["width"] = image_width

        for i, anno in enumerate(self.__armature_annotation_list):
            anno_part_dict =  copy.deepcopy(self.__default_mscoco_annotations_part_dict)

            anno_part_dict["id"] = self.__gen_img_id+'_'+str(i+1)
            anno_part_dict["image_id"] = self.__gen_img_id

            bbox_value_dict = anno[1]
            anno_part_dict["bbox"] = [bbox_value_dict["x"],bbox_value_dict["y"],
                                     bbox_value_dict["width"],bbox_value_dict["height"]]
            anno_part_dict["area"] = int(bbox_value_dict["width"]*bbox_value_dict["height"])

            keypoint_value_dict = anno[2]
            keypoint_list = list()
            for keypoint in keypoint_value_dict.values():
                for value in keypoint:
                    keypoint_list.append(value)
            anno_part_dict["keypoints"] = keypoint_list
            
            num_keypoints = 0
            for keypoint in keypoint_value_dict.values():
                if keypoint[2] != 0:
                    num_keypoints += 1
            anno_part_dict["num_keypoints"] = num_keypoints

            self.__output_mscoco_json_dict["annotations"].append(anno_part_dict)


    def __render_img_and_save_annotation(self):
        """Render the image and generate the corresponding annotation/labeling data.""" 
        img_file_path = os.path.join(self.output_img_path,  self.__gen_img_id+".png")
        annotation_file_path = os.path.join(self.output_annotation_path,  self.__gen_img_id+".json")

        # Render imgand save
        self.__scene.render.filepath = img_file_path 
        print("Start Render Image") 
        bpy.ops.render.render(write_still=True, scene=self.__scene.name)
        print("End Render Image")
        # Save mscoco annotation to json
        with open(annotation_file_path, "w") as output_json_file:
                json.dump(self.__output_mscoco_json_dict, output_json_file)

        print("SAVE IMG AT {}".format(img_file_path))
        print("SAVE LABLE AT {}".format(annotation_file_path))


    def auto_labeling(self):
        """Main process for rendering and labeling data."""
        self.__create_gen_img_id()
        self.__get_all_armature_object_in_target_obj_collections()
        self.__create_and_switch_annotation_scene()
        self.__create_id_mask_nodes()
        self.__add_pass_index()
        self.__get_all_armature_can_see()
        self.__get_all_keypoint_can_see()
        self.__get_all_armature_annotation()
        self.__convert_to_mscoco_format()
        self.__render_img_and_save_annotation()
        print("Auto Labeling COMPLERED !!!")


if __name__ == "__main__":

    mscoco_labeler = MSCOCOLabeler()
    mscoco_labeler.auto_labeling()