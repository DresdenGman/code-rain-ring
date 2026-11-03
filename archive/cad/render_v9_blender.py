import bpy, bmesh, math, sys, os
from mathutils import Vector
R="/workspace/coderain_ring/"; import json; PJ=json.load(open(R+"cad/v9_params.json")); WCX=PJ["win_cx"]; argv=sys.argv[sys.argv.index("--")+1:]; VIEW=argv[0]; SAMPLES=int(argv[1]) if len(argv)>1 else 96
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene; sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=SAMPLES; sc.cycles.use_denoising=True
sc.render.resolution_x=sc.render.resolution_y=1400; sc.render.film_transparent=False
sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Medium High Contrast'
def imp(n):
    bpy.ops.wm.stl_import(filepath=R+f"cad/{n}.stl"); o=bpy.context.selected_objects[0]
    bpy.ops.object.shade_smooth(); return o
def mat(name,base,metal,rough,emit_img=None):
    m=bpy.data.materials.new(name); m.use_nodes=True; nt=m.node_tree; b=nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value=(*base,1); b.inputs["Metallic"].default_value=metal; b.inputs["Roughness"].default_value=rough
    if emit_img:
        tx=nt.nodes.new("ShaderNodeTexImage"); tx.image=bpy.data.images.load(emit_img)
        tc=nt.nodes.new("ShaderNodeTexCoord"); mp=nt.nodes.new("ShaderNodeMapping")
        mp.inputs["Location"].default_value=(0.5-WCX/10.06,0.5,0); mp.inputs["Scale"].default_value=(1/10.06,1/13.42,1); tx.extension="CLIP"
        nt.links.new(tc.outputs["Object"],mp.inputs["Vector"]); nt.links.new(mp.outputs["Vector"],tx.inputs["Vector"])
        nt.links.new(tx.outputs["Color"],b.inputs["Emission Color"]); b.inputs["Emission Strength"].default_value=6.0
        b.inputs["Coat Weight"].default_value=1.0; b.inputs["Coat Roughness"].default_value=0.03
    return m
silver=mat("bead_silver",(0.86,0.86,0.88),1.0,0.34)
# subtle bead-blast micro-bump
nt=silver.node_tree; nz=nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value=900; bm_=nt.nodes.new("ShaderNodeBump"); bm_.inputs["Strength"].default_value=0.04
nt.links.new(nz.outputs["Fac"],bm_.inputs["Height"]); nt.links.new(bm_.outputs["Normal"],nt.nodes["Principled BSDF"].inputs["Normal"])
glass=mat("black_glass",(0.005,0.005,0.006),0.0,0.04,R+"renders/v9_rain_tex.png")
body=imp("v9_unibody"); body.data.materials.append(silver)
lens=imp("v9_lens"); lens.data.materials.append(glass)
lid=imp("v9_bottom_lid"); lid.data.materials.append(silver)
cap=imp("v9_top_bezel"); cap.data.materials.append(silver)
pogo=imp("v9_pogo"); pogo.data.materials.append(mat("nickel",(0.7,0.7,0.68),1,0.3))
def dots(px):
    out=[]
    for r,z,col,mt in [(1.1,10.45,(1.0,0.75,0.3),1),(0.75,10.43,(0.02,0.02,0.02),0),(0.5,10.41,(1.0,0.75,0.3),1)]:
        bpy.ops.mesh.primitive_cylinder_add(radius=r,depth=0.1,location=(px,0,z)); c=bpy.context.object; c.data.materials.append(mat("d",col,mt,0.25)); out.append(c)
    return out
pdots=dots(0.0)
def box(name,dims,loc,col,metal=0,rough=0.5):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=bpy.context.object; o.scale=dims; o.name=name
    bpy.ops.object.modifier_add(type='BEVEL'); o.modifiers[0].width=0.15; o.modifiers[0].segments=3
    o.data.materials.append(mat(name+"_m",col,metal,rough)); return o
parts=[]
if VIEW in("exploded","section","sidecut"):
    parts=[box("battery",(15,2,8),(0,10.5,9.6),(0.75,0.62,0.25),0.6,0.35),
           box("battery2",(15,2,8),(0,-10.5,9.6),(0.75,0.62,0.25),0.6,0.35),
           box("pcb",(18.6,18.6,0.4),(0,0,12.2),(0.05,0.25,0.12),0,0.4),
           
           
           box("oled",(16.2,16.5,1.23),(PJ["oled_cx"],0,13.235),(0.02,0.02,0.02),0,0.3)]
if VIEW=="exploded":
    off={"lid":-24,"battery":9,"battery2":9,"pcb":14,"pogo":-21,"oled":20,"lens":26,"cap":32}
    lid.location.z+=off["lid"]; pogo.location.z+=off["pogo"]; lens.location.z+=off["lens"]; cap.location.z+=off["cap"]
    for d_ in pdots: d_.location.z+=off["pogo"]
    for p in parts: p.location.z+=off[p.name]
if VIEW in("section","sidecut"):
    for o in [body,lid,pogo,cap,lens]+pdots: bpy.data.objects.remove(o)
    lens=imp("v9_section_lens"); lens.data.materials.append(glass)
    cap=imp("v9_section_cap"); cap.data.materials.append(silver)
    pogo=imp("v9_section_pogo"); pogo.data.materials.append(mat("pb",(0.02,0.02,0.022),0,0.45))
    body=imp("v9_section_body"); body.data.materials.append(silver); lid=imp("v9_section_lid"); lid.data.materials.append(silver)
    for p in parts:
        lo=p.location.x-p.scale.x/2; hi=min(p.location.x+p.scale.x/2,WCX)
        if hi<=lo: bpy.data.objects.remove(p); continue
        p.scale.x=hi-lo; p.location.x=(hi+lo)/2
# world + studio lights
w=bpy.data.worlds.new("w"); sc.world=w; w.use_nodes=True; wn=w.node_tree.nodes; wl=w.node_tree.links; bg=wn["Background"]
sky=wn.new("ShaderNodeTexSky") if False else None
grad=wn.new("ShaderNodeTexGradient"); tc=wn.new("ShaderNodeTexCoord"); sep=wn.new("ShaderNodeSeparateXYZ"); ramp=wn.new("ShaderNodeValToRGB")
wl.new(tc.outputs["Generated"],sep.inputs[0]) ; wl.new(sep.outputs["Z"],ramp.inputs["Fac"])
ramp.color_ramp.elements[0].color=(0.08,0.08,0.09,1); ramp.color_ramp.elements[1].color=(1.0,1.0,1.0,1); ramp.color_ramp.elements[0].position=0.45
lp=wn.new("ShaderNodeLightPath"); mx=wn.new("ShaderNodeMixRGB"); wl.new(lp.outputs["Is Camera Ray"],mx.inputs["Fac"])
wl.new(ramp.outputs["Color"],mx.inputs[1]); mx.inputs[2].default_value=(0.035,0.037,0.04,1); wl.new(mx.outputs[0],bg.inputs[0]); bg.inputs[1].default_value=1.0
def light(loc,energy,size,col=(1,1,1)):
    bpy.ops.object.light_add(type='AREA',location=loc); l=bpy.context.object; l.data.energy=energy; l.data.size=size; l.data.color=col
    l.rotation_euler=(Vector((0,0,8))-Vector(loc)).to_track_quat('-Z','Y').to_euler()
light((-60,-50,80),9000,40); light((70,-20,40),5000,30,(0.95,0.97,1)); light((10,80,50),5000,40); light((0,-90,0),2000,60); light((90,15,25),3500,50); light((-90,-15,25),2500,50)
# floor
bpy.ops.mesh.primitive_plane_add(size=600,location=(0,0,-12.3)); fl=bpy.context.object; fl.data.materials.append(mat("floor",(0.09,0.095,0.1),0,0.6))
if VIEW=="exploded": fl.location.z=-30
if VIEW=="under": bpy.data.objects.remove(fl)
cams={"under":((-55,6,-4),(-1,0,9.5),14),"side":((90,0,2),(0,0,1.75),34),"front":((0,-90,2),(0,0,1.75),34),"back":((-90,0,2),(0,0,1.75),34),
 "top":((0,0,90),(0,0,0),28),"hero":((48,-40,36),(0,0,3),40),"section":((70,30,18),(0,0,2),34),"exploded":((80,-85,40),(0,0,8),92),"sidecut":((60,7.4,14.0),(0,7.4,14.0),4.4)}
_unused={"hero":((52,-38,40),(0,0,7),34),"side":((0,-80,6),(0,0,4),48),"top":((0,0,90),(0,0,10),34),
      "section":((25,75,22),(0,0,6),40),"exploded":((-45,-60,45),(0,0,14),55),"back":((-70,-25,25),(0,0,8),45)}
loc,tgt,ortho=cams[VIEW]
bpy.ops.object.camera_add(location=loc); cam=bpy.context.object; sc.camera=cam
cam.rotation_euler=(Vector(tgt)-Vector(loc)).to_track_quat('-Z','Y').to_euler(); cam.data.lens=100
d=(Vector(tgt)-Vector(loc)).length; cam.data.lens=100*d/ (ortho*2.8)
cam.data.dof.use_dof=False
if VIEW in('side','front','back','top','sidecut'): cam.data.type='ORTHO'; cam.data.ortho_scale=ortho
sc.render.filepath=R+f"renders/v9_{VIEW}.png"; bpy.ops.render.render(write_still=True)
