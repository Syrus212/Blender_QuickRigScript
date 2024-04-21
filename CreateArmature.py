import bpy

def sort_objects_custom(objects, name_getter):
    priority_order = {
        "Root": -1,  # Set "Root" to have the lowest priority
        "Body": 0,
        "ArmL": 1,
        "ArmR": 2,
        "HandL": 3,
        "HandR": 4,
        "LegL": 5,
        "LegR": 6,
        "FootL": 7,
        "FootR": 8
    }

    def sort_key(obj):
        # Get the name of the object using the provided name_getter function
        name = name_getter(obj)

        # Handle "Root" separately
        if name == "Root":
            return -1, '', 0  # Ensure "Root" always comes first

        # Extract prefix and potential number
        prefix, number = '', ''
        for i in range(len(name)):
            if name[i:].isdigit():
                prefix, number = name[:i], name[i:]
                break
        else:  # If no number found, set number to default
            prefix, number = name, '00'

        # Check if prefix is in the priority order, otherwise set it to highest priority
        priority = priority_order.get(prefix, len(priority_order))

        return priority, prefix, int(number)

    # Sort the objects using the custom key function
    return sorted(objects, key=sort_key)

# Function to get the name attribute from an object
def get_name(obj):
    return obj.name

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
    
    # Create mesh list and bone hierarchy
    mesh_names = []
    for mesh in bpy.data.objects:
        if mesh.type == "MESH":
            mesh_names.append(mesh.name)
            bone = armature.edit_bones.new(mesh.name)
    mesh_names.append("Root")

    # Adjust bones and link to meshes
    for mesh in sort_objects_custom(bpy.data.objects, get_name):
        if mesh.type == "MESH":
            
            bone_name = mesh.name[:-2]
    
            try:
                n = int(mesh.name[-2:])
            except:
                n = 1
                bone_name = mesh.name
            else:
                n = int(mesh.name[-2:])
            
            parent_name = ''
            while (n > 1):

                n -= 1
                pot_parent = bone_name + (str(n).zfill(2))

                if pot_parent in mesh_names:
                    parent_name = pot_parent

            if not(parent_name):
                n = 10
                parent_name = "Body"

                while n > 1:
                    n -= 1
                    try:
                        bone_parents.get(bone_name) + str(n).zfill(2)
                    except:
                        pass
                    else:
                        if (bone_parents.get(bone_name) + str(n).zfill(2)) in mesh_names:
                            parent_name = (bone_parents.get(bone_name) + str(n).zfill(2))
                            break
            
            print(f'mesh : {mesh} | bone_name : {bone_name} | parent_name : {parent_name}')
            
            bone_name = mesh.name
            
            bone = armature.edit_bones.get(bone_name)
            bone.tail = (mesh.location.x, mesh.location.y, mesh.location.z)  # Adjust tail position
            
            parent_bone = armature.edit_bones.get(parent_name)
            print(parent_bone.tail)
            
            if parent_bone:
                bone.parent = parent_bone
                bone.head = parent_bone.tail
            else:
                bone.head = (0, 0,0)
            
            # Iterate over all vertex groups and remove them
            for group in mesh.vertex_groups:
                mesh.vertex_groups.remove(group)
            
            # Create vertex group and assign vertices
            vertex_group = mesh.vertex_groups.new(name=bone_name)
            vertex_group.add(range(len(mesh.data.vertices)), 1.0, "REPLACE")
            
            # Link mesh to bone
            # Delete existing armature modifiers
            for mod in mesh.modifiers:
                # Check if the modifier is an armature modifier
                if mod.type == 'ARMATURE':
                    # Remove the armature modifier
                    mesh.modifiers.remove(mod)
                    # break
            # Add new armature modifier and link it
            modifier = mesh.modifiers.new(name="Armature", type="ARMATURE")
            modifier.object = obj

    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action='DESELECT')
