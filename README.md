# Blender_QuickRigScript

A quick and easy way to rig a humanoid character in Blender.

Your character must be composed of distinct mesh objects which follow this naming convention : "Body", "Head", "ArmL", "HandL", "ArmR", "HandR", "LegL", "FootL", "LegR", "FootR". Note : bones for arms or legs are not necessary if your character does not have these parts.

If you have multiple meshes that you want to attach other body parts (say, a pony tail or shoulder puffs) you just have to add an integer suffix to them in the "00" format and they'll be rigged in order accordingly.

Go to the scripting tab in Blender and create 3 new scripts named after each ```.py``` file in this repository. Paste the content of the files in the respective Blender scripts and run the one called ```SetupArmature``` to create the armature.
