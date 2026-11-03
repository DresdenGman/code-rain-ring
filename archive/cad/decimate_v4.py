import bpy
R="/workspace/coderain_ring/cad/"
bpy.ops.wm.read_factory_settings(use_empty=True)
for n,t in [("v4_unibody",60000),("v4_bottom_lid",8000),("v4_lens",4000)]:
    bpy.ops.wm.stl_import(filepath=R+n+".stl"); o=bpy.context.selected_objects[0]
    m=o.modifiers.new("d","DECIMATE"); m.ratio=t/len(o.data.polygons)
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active=o
    bpy.ops.object.modifier_apply(modifier="d")
    bpy.ops.wm.stl_export(filepath=R+n+"_lowpoly.stl",export_selected_objects=True); bpy.data.objects.remove(o)
