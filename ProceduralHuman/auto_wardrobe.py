"""Auto wardrobe

Step:
1.eye color
2.eyebrow
3.eyelash
4.hair
5.hat
6.glass
7.shirt
8.pant
9.shoe

"""


import bpy

## 2.eyebrow
bpy.context.view_layer.objects.active =  bpy.data.objects["Human.rig"]
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
bpy.ops.object.shade_smooth()
bpy.ops.mpfb.load_library_clothes(filepath="C:\\Users\\user\\AppData\\Roaming\\Blender Foundation\\Blender\\3.4\\mpfb\\data\\eyebrows\\eyebrow001\\eyebrow001.mhclo", object_type="Eyebrows", material_type="MAKESKIN")

## 3.eyelash
#bpy.context.view_layer.objects.active =  bpy.data.objects["Human.rig"]
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
bpy.ops.object.shade_smooth()
bpy.ops.mpfb.load_library_clothes(filepath="C:\\Users\\user\\AppData\\Roaming\\Blender Foundation\\Blender\\3.4\\mpfb\\data\\eyelashes\\eyelashes01\\eyelashes01.mhclo", object_type="Eyelashes", material_type="MAKESKIN")


## 4.hair assign
#bpy.context.view_layer.objects.active =  bpy.data.objects["Human.rig"]
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
bpy.ops.object.shade_smooth()
bpy.ops.mpfb.load_library_clothes(filepath="C:\\Users\\user\\AppData\\Roaming\\Blender Foundation\\Blender\\3.4\\mpfb\\data\\hair\\afro01\\afro01.mhclo", object_type="Hair", material_type="MAKESKIN")


## 5.hat
#bpy.context.view_layer.objects.active =  bpy.data.objects["Human.rig"]
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
bpy.ops.object.shade_smooth()
bpy.ops.mpfb.load_library_clothes(filepath="C:\\Users\\user\\AppData\\Roaming\\Blender Foundation\\Blender\\3.4\\mpfb\\data\\clothes\\toigo_maga_hat\\toigo_maga_hat.mhclo", object_type="Clothes", material_type="MAKESKIN")


## 6.glass 
#bpy.context.view_layer.objects.active =  bpy.data.objects["Human.rig"]
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
bpy.ops.object.shade_smooth()
bpy.ops.mpfb.load_library_clothes(filepath="C:\\Users\\user\\AppData\\Roaming\\Blender Foundation\\Blender\\3.4\\mpfb\\data\\clothes\\spamrakuen_tbm_glasses_frames_01\\spamrakuen_tbm_glasses_frames_01.mhclo", object_type="Clothes", material_type="MAKESKIN")


## 7.shirt
#bpy.context.view_layer.objects.active =  bpy.data.objects["Human.rig"]
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
bpy.ops.object.shade_smooth()
bpy.ops.mpfb.load_library_clothes(filepath="C:\\Users\\user\\AppData\\Roaming\\Blender Foundation\\Blender\\3.4\\mpfb\\data\\clothes\\elvs_lara_tank1\\elvs_lara_tank1.mhclo", object_type="Clothes", material_type="MAKESKIN")

## 8.pant
#bpy.context.view_layer.objects.active =  bpy.data.objects["Human.rig"]
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
bpy.ops.object.shade_smooth()
bpy.ops.mpfb.load_library_clothes(filepath="C:\\Users\\user\\AppData\\Roaming\\Blender Foundation\\Blender\\3.4\\mpfb\\data\\clothes\\mindfront_male_swimming_trunks_01\\mindfront_male_swimming_trunks_01.mhclo", object_type="Clothes", material_type="MAKESKIN")


## 9.shoe
#bpy.context.view_layer.objects.active =  bpy.data.objects["Human.rig"]
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
bpy.ops.object.shade_smooth()
bpy.ops.mpfb.load_library_clothes(filepath="C:\\Users\\user\\AppData\\Roaming\\Blender Foundation\\Blender\\3.4\\mpfb\\data\\clothes\\elvs_male_flip_flop_sandals1\\elvs_male_flip_flop_sandals1.mhclo", object_type="Clothes", material_type="MAKESKIN")

