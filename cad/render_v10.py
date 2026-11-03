import trimesh, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import sys, json
SZ=sys.argv[1] if len(sys.argv)>1 else 'M'
O=f'/workspace/coderain_ring/v10_{SZ}/'; R=f'/workspace/coderain_ring/renders/v10_{SZ}_'
J=json.load(open(O+f'v10_{SZ}_checks.json')); G=J['geo']
ri=G['ri']; gy,gx=G['glass']; wy,wx=G['window']; HWd={'M':(19.4,22.4,17.5),'L':(21.0,24.0,18.8)}[SZ]
a0s,a1s=G['strip_a0'],G['strip_a1']; zA=G['epoxy_zone_A_deg']; zB=G['epoxy_zone_B_deg']; SL=G['strip_flat_L_midline']
f2=lambda v:('%.2f'%v) if v is not None else 'n/a'
C=dict(shell='#b8bcc4',strip='#d4a050',glass='#7fc8ff',oled='#202020',pcb='#2e8b3a',bat_L='#c03030',bat_R='#c03030',socket='#e0c020')
M={n:trimesh.load(O+f'v10_{SZ}_{n}.stl') for n in C}
M={n:trimesh.Trimesh(*trimesh.remesh.subdivide_to_size(m.vertices,m.faces,0.7)) for n,m in M.items()}
def view(names,off,el,az,fn,title,alpha=None):
    f=plt.figure(figsize=(9,8)); ax=f.add_subplot(111,projection='3d'); L=np.array([0.3,-0.5,0.8]);L/=np.linalg.norm(L)
    allv=[]
    for n in names:
        m=M[n].copy(); m.apply_translation(off.get(n,(0,0,0))); allv.append(m.vertices)
        sh=0.45+0.55*np.clip(m.face_normals@L,0,1); base=np.array(matplotlib.colors.to_rgb(C[n]))
        pc=Poly3DCollection(m.triangles,facecolors=np.clip(base[None]*sh[:,None],0,1),linewidths=0,alpha=(alpha or {}).get(n,1)); ax.add_collection3d(pc)
    v=np.vstack(allv); c=(v.max(0)+v.min(0))/2; r=(v.max(0)-v.min(0)).max()/2
    ax.set_xlim(c[0]-r,c[0]+r);ax.set_ylim(c[1]-r,c[1]+r);ax.set_zlim(c[2]-r,c[2]+r); ax.set_box_aspect((1,1,1))
    ax.view_init(el,az); ax.set_axis_off(); ax.set_title(title); f.savefig(R+fn,dpi=130,bbox_inches='tight'); plt.close(f)
view(['shell','glass'],{},25,-55,'iso.png',f'v10 {SZ} iso (ID{HWd[0]}, head {HWd[1]}x{HWd[2]}x4.15)')
view(['shell','glass','oled'],{},90,-90,'top.png',f'v10 {SZ} top view')
CY=-min(abs(M['bat_L'].bounds[0][1]),abs(M['bat_L'].bounds[1][1])) if M['bat_L'].bounds[1][1]<0 else -abs(M['bat_R'].bounds[0][1]); CZ=M['bat_L'].bounds[0][2]
view(['shell','strip','socket','bat_L','bat_R','glass','oled','pcb'],
     {'strip':(0,-14,-22),'socket':(0,0,-36),'glass':(0,0,14),'oled':(0,0,9),'pcb':(0,0,5),'bat_L':(0,-12,4),'bat_R':(0,12,4)},
     -30,-60,'exploded.png',f'v10 {SZ} exploded (cover strip below, flex channel on -Y band inner, socket)')
# section at x=0 (YZ) and x=+? through groove (x=0 crosses groove & socket)
f,ax=plt.subplots(figsize=(8,9))
for n in C:
    s=M[n].section(plane_origin=[0,0,0],plane_normal=[1,0,0])
    if s is None: continue
    p,_=s.to_planar(to_2D=np.array([[0,1,0,0],[0,0,1,0],[1,0,0,0],[0,0,0,1]]))
    for poly in p.polygons_full:
        xs,ys=poly.exterior.xy; ax.fill(xs,ys,color=C[n],ec='k',lw=0.4)
        for h in poly.interiors: ax.fill(*h.xy,color='white',ec='k',lw=0.4)
ax.set_aspect('equal'); ax.grid(alpha=.3); ax.set_xlabel('Y mm'); ax.set_ylabel('Z mm')
ax.set_title(f'v10 {SZ} section X=0: grey shell, gold cover strip, red batteries, blue glass,\nblack OLED, green PCB, yellow Φ4x2 socket; flex groove on left (-Y)')
ax.annotate(f"bat corner: {f2(G['wall_batL_to_channel'])} to channel\n{f2(G['wall_batL_to_bore'])} to bore",(CY,CZ),(-6,0),arrowprops=dict(arrowstyle='->'),fontsize=8)
f.savefig(R+'section.png',dpi=140,bbox_inches='tight')
# glass outline png
f,ax=plt.subplots(figsize=(6,5)); ax.add_patch(plt.Rectangle((-gy/2,-gx/2),gy,gx,fc='#7fc8ff',ec='k'))
ax.add_patch(plt.Rectangle((-wy/2,-wx/2),wy,wx,fill=False,ls='--',ec='r')); ax.set_xlim(-10,10);ax.set_ylim(-8,8);ax.set_aspect('equal')
ax.set_title(f'Cover glass {gy:.2f} x {gx:.1f} x 0.4 (dashed: window {wy}x{wx})'); f.savefig(O+f'v10_{SZ}_glass_outline.png',dpi=120,bbox_inches='tight')
C['shell_ghost']=C['shell']; M['shell_ghost']=M['shell']
view(['strip','socket','shell_ghost'],{},-20,-150,'liner.png',f'v10 {SZ} cover strip {SL:.2f} x 2.9 x 0.5 over flex channel (-Y side)',alpha={'shell_ghost':0.12})

import math
f,ax=plt.subplots(figsize=(9,8))
for n in ['shell','strip','bat_L','socket']:
    s=M[n].section(plane_origin=[0,0,0],plane_normal=[1,0,0])
    if s is None: continue
    p,_=s.to_planar(to_2D=np.array([[0,1,0,0],[0,0,1,0],[1,0,0,0],[0,0,0,1]]))
    for poly in p.polygons_full:
        ax.fill(*poly.exterior.xy,color=C[n],ec='k',lw=0.5)
        for h in poly.interiors: ax.fill(*h.xy,color='white',ec='k',lw=0.4)
def arc(a0,a1,r): t=np.radians(np.linspace(a0,a1,60)); return -r*np.sin(t),-r*np.cos(t)
zones=[(zB[0],zB[1],f'EPOXY zone B {zB[0]:.1f}-{zB[1]:.0f} deg\n(open slot beside socket, flush epoxy)',(-3,-6.5))]
if zA: zones.append((zA[0],zA[1],f'EPOXY zone A {zA[0]:.1f}-{zA[1]:.1f} deg\n(groove 2.2w x 0.25d, flush epoxy)',(-4,3)))
for (a0,a1,lab,xy) in zones:
    ys,zs=arc(a0,a1,ri+0.12); ax.plot(ys,zs,color='magenta',lw=5,alpha=.8)
    ax.annotate(lab,(ys[30],zs[30]),xy,color='m',fontsize=9,arrowprops=dict(arrowstyle='->',color='m'))
ys,zs=arc(a0s,a1s,ri+0.25); ax.annotate(f'cover strip {a0s:.1f}-{a1s:.1f} deg\n{SL:.2f} x 2.9 x 0.5 (over 3.0x0.5 recess\n+ 2.2x0.18 flex groove)',(ys[30],zs[30]),(-3,1),fontsize=9,arrowprops=dict(arrowstyle='->'))
ax.annotate(f"flex slot in head floor (y={G['hole_y']:.1f})\n{f2(G['wall_batL_to_flex_slot'])} to battery",(G['hole_y'],CZ+2),(-4,10.5),fontsize=9,arrowprops=dict(arrowstyle='->'))
ax.annotate(f"-Y battery 2x8x15\ncorner: {f2(G['wall_batL_to_channel'])} to channel/groove,\n{f2(G['wall_batL_to_strip_recess'])} to strip recess, {f2(G['wall_batL_to_bore'])} to bore",(CY,CZ),(-14.5,-2),fontsize=9,arrowprops=dict(arrowstyle='->'))
ax.annotate('Φ4x2 socket',(0,-ri),(2,-7),fontsize=9,arrowprops=dict(arrowstyle='->'))
ax.set_xlim(-16,6); ax.set_ylim(-13,13); ax.set_aspect('equal'); ax.grid(alpha=.3); ax.set_xlabel('Y mm'); ax.set_ylabel('Z mm')
ax.set_title(f'v10 {SZ} flex route, section X=0 (-Y side); angles from bottom toward -Y')
f.savefig(R+'route.png',dpi=140,bbox_inches='tight')
# pad render: bottom from inside + side profile
low=M['shell'].slice_plane([0,0,-4],[0,0,-1]); M['shell_low']=low; C['shell_low']=C['shell']
f=plt.figure(figsize=(15,6)); ax=f.add_subplot(121,projection='3d'); Lv=np.array([0.2,0.3,1.0]);Lv/=np.linalg.norm(Lv)
sh=0.35+0.65*np.clip(low.face_normals@Lv,0,1); base=np.array(matplotlib.colors.to_rgb(C['shell']))
ax.add_collection3d(Poly3DCollection(low.triangles,facecolors=np.clip(base[None]*sh[:,None],0,1),linewidths=0))
ax.set_xlim(-10,10);ax.set_ylim(-12,8);ax.set_zlim(-14,6);ax.set_box_aspect((1,1,1));ax.view_init(55,-60);ax.set_axis_off()
ax.set_title('bottom of band from inside (cut at Z=-4): full-width pad, socket hole, flex channel')
ax2=f.add_subplot(122)
for xs,col,lab in [(0,'k','X=0 (centre, through socket)'),(6.0,'b','X=6 (no socket)')]:
    s=M['shell'].section(plane_origin=[xs,0,0],plane_normal=[1,0,0])
    p,_=s.to_planar(to_2D=np.array([[0,1,0,0],[0,0,1,0],[1,0,0,xs],[0,0,0,1]]))
    for i,poly in enumerate(p.polygons_full):
        for ring in [poly.exterior]+list(poly.interiors): ax2.plot(*ring.xy,color=col,lw=1,label=lab if i==0 and ring is poly.exterior else None)
t=np.radians(np.linspace(-60,60,200)); ax2.plot(ri*np.sin(t),-ri*np.cos(t),'r--',lw=0.8,label=f'plain bore r{ri} (ref)')
ax2.set_xlim(-ri,ri);ax2.set_ylim(-ri-1.9,-ri+3.7);ax2.set_aspect('equal');ax2.grid(alpha=.3);ax2.legend(fontsize=8,loc='upper right')
ax2.set_title('side profile of pad: 1.0 peak, cos² blend to bore at ±35°, tangent, no crease'); ax2.set_xlabel('Y mm');ax2.set_ylabel('Z mm')
f.savefig(R+'pad.png',dpi=130,bbox_inches='tight')
