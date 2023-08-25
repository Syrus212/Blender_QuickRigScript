import bpy

CleanTransforms = bpy.data.texts["CleanTransforms"].as_module()
CreateArmature = bpy.data.texts["CreateArmature"].as_module()

CleanTransforms.clean_meshes()
CreateArmature.create_armature()
