import bpy

# Create armature
def create_armature():
    armature = bpy.data.armatures.new("Armature")
    obj = bpy.data.objects.new("Armature", armature)
    obj.show_in_front = True
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.context.object.data.display_type = "STICK"
    bpy.ops.object.mode_set(mode="EDIT")

    # Create root bone
    root_bone = armature.edit_bones.new("Root")
    root_bone.head = (0, 0, 0)
    root_bone.tail = (0, 0, 1)

    # List of bone parents
    bone_parents = {
        "Body": "Root",
        "Head": "Body",
        "ArmL": "Body",
        "HandL": "ArmL",
        "ArmR": "Body",
        "HandR": "ArmR",
        "LegL": "Body",
        "FootL": "LegL",
        "LegR": "Body",
        "FootR": "LegR"
    }

    mesh_names = []
    for mesh in bpy.data.objects:
        if mesh.type == "MESH":
            mesh_names.append(mesh.name)
    mesh_names.append("Root")

    # Create bones and link to meshes
    for mesh in bpy.data.objects:
        if mesh.type == "MESH":
            bone_name = mesh.name
            
            if bone_parents.get(bone_name) in mesh_names:
                parent_name = bone_parents.get(bone_name, "Body")
            else:
                parent_name = "Body"
            
            bone = armature.edit_bones.new(bone_name)
            bone.tail = (mesh.location.x, mesh.location.y, mesh.location.z)  # Adjust tail position
            
            parent_bone = armature.edit_bones.get(parent_name)
            if parent_bone:
                bone.parent = parent_bone
                bone.head = parent_bone.tail
            else:
                bone.head = (0, 0, 0)
            
            # Create vertex group and assign vertices
            vertex_group = mesh.vertex_groups.new(name=bone_name)
            vertex_group.add(range(len(mesh.data.vertices)), 1.0, "REPLACE")

            # Link mesh to bone
            modifier = mesh.modifiers.new(name="Armature", type="ARMATURE")
            modifier.object = obj

    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action='DESELECT')
