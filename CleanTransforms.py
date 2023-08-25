import bpy

# Clean meshes transform
def clean_meshes():
    for mesh in bpy.data.objects:
        if mesh.type == "MESH":
            
            # Reset mesh origin
            bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = mesh
            mesh.select_set(True)
            
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_all(action="SELECT")
            
            bpy.context.area.type = "VIEW_3D"
            bpy.ops.view3d.snap_cursor_to_selected()
            bpy.context.area.type = "TEXT_EDITOR"
            
            bpy.ops.object.mode_set(mode="OBJECT")
            
            bpy.context.area.type = "VIEW_3D"
            bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
            bpy.context.area.type = "TEXT_EDITOR"
            
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_all(action='SELECT')
            
            bpy.ops.object.mode_set(mode="OBJECT")
            bpy.context.area.type = "VIEW_3D"
            bpy.ops.view3d.snap_cursor_to_active()
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)
            bpy.context.area.type = "TEXT_EDITOR"
            
    bpy.ops.object.mode_set(mode="OBJECT")
