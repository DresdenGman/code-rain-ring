import trimesh, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
O='/workspace/coderain_ring/v10_M/'; R='/workspace/coderain_ring/renders/v10_M_'
C=dict(shell='#b8bcc4',strip='#d4a050',glass='#7fc8ff',oled='#202020',pcb='#2e8b3a',bat_L='#c03030',bat_R='#c03030',socket='#e0c020')
M={n:trimesh.load(O+f'v10_M_{n}.stl') for n in C}
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
view(['shell','glass'],{},25,-55,'iso.png','v10 M iso (ID19.4, head 22.4x17.5x4.15)')
view(['shell','glass','oled'],{},90,-90,'top.png','v10 M top view')
view(['shell','strip','socket','bat_L','bat_R','glass','oled','pcb'],
     {'strip':(0,-14,-22),'socket':(0,0,-36),'glass':(0,0,14),'oled':(0,0,9),'pcb':(0,0,5),'bat_L':(0,-12,4),'bat_R':(0,12,4)},
     -30,-60,'exploded.png','v10 M exploded (cover strip below, flex channel on -Y band inner, socket)')
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
ax.set_title('v10 M section X=0: grey shell, gold cover strip, red batteries, blue glass,\nblack OLED, green PCB, yellow Φ4x2 socket; flex groove on left (-Y)')
ax.annotate('bat corner: 0.53 to epoxy groove\n0.78 to bore',(-8.7,5.85),(-6,0),arrowprops=dict(arrowstyle='->'),fontsize=8)
f.savefig(R+'section.png',dpi=140,bbox_inches='tight')
# glass outline png
f,ax=plt.subplots(figsize=(6,5)); ax.add_patch(plt.Rectangle((-8.625,-6.4),17.25,12.8,fc='#7fc8ff',ec='k'))
ax.add_patch(plt.Rectangle((-8.4,-6.1),16.8,12.2,fill=False,ls='--',ec='r')); ax.set_xlim(-10,10);ax.set_ylim(-8,8);ax.set_aspect('equal')
ax.set_title('Cover glass 17.25 x 12.8 x 0.4 (dashed: window 16.8x12.2)'); f.savefig(O+'v10_M_glass_outline.png',dpi=120,bbox_inches='tight')
C['shell_ghost']=C['shell']; M['shell_ghost']=M['shell']
view(['strip','socket','shell_ghost'],{},-20,-150,'liner.png','v10 M cover strip 14.31 x 2.9 x 0.5 over flex channel (-Y side)',alpha={'shell_ghost':0.12})

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
for (a0,a1,lab,xy) in [(118,135,'EPOXY zone A 118-135 deg\n(groove 2.2w x 0.25d, flush epoxy)',(-4,3)),(11.6,35,'EPOXY zone B 11.6-35 deg\n(open slot beside socket, flush epoxy)',(-3,-6.5))]:
    ys,zs=arc(a0,a1,9.82); ax.plot(ys,zs,color='magenta',lw=5,alpha=.8)
    ax.annotate(lab,(ys[30],zs[30]),xy,color='m',fontsize=9,arrowprops=dict(arrowstyle='->',color='m'))
ys,zs=arc(35.3,117.7,9.95); ax.annotate('cover strip 35.3-117.7 deg\n14.31 x 2.9 x 0.5 (over 3.0x0.5 recess\n+ 2.2x0.18 flex groove)',(ys[30],zs[30]),(-3,1),fontsize=9,arrowprops=dict(arrowstyle='->'))
ax.annotate('flex slot in head floor (y=-7.5)\n0.70 to battery',(-7.5,8),(-4,10.5),fontsize=9,arrowprops=dict(arrowstyle='->'))
ax.annotate('-Y battery 2x8x15\ncorner: 0.53 to epoxy groove,\n1.06 to strip recess, 0.78 to bore',(-8.7,5.85),(-14.5,-2),fontsize=9,arrowprops=dict(arrowstyle='->'))
ax.annotate('Φ4x2 socket',(0,-9.7),(2,-7),fontsize=9,arrowprops=dict(arrowstyle='->'))
ax.set_xlim(-15,6); ax.set_ylim(-12,12); ax.set_aspect('equal'); ax.grid(alpha=.3); ax.set_xlabel('Y mm'); ax.set_ylabel('Z mm')
ax.set_title('v10 M flex route, section X=0 (-Y side); angles from bottom toward -Y')
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
t=np.radians(np.linspace(-60,60,200)); ax2.plot(9.7*np.sin(t),-9.7*np.cos(t),'r--',lw=0.8,label='plain bore r9.7 (ref)')
ax2.set_xlim(-9,9);ax2.set_ylim(-11.6,-6);ax2.set_aspect('equal');ax2.grid(alpha=.3);ax2.legend(fontsize=8,loc='upper right')
ax2.set_title('side profile of pad: 1.0 peak, cos² blend to bore at ±35°, tangent, no crease'); ax2.set_xlabel('Y mm');ax2.set_ylabel('Z mm')
f.savefig(R+'pad.png',dpi=130,bbox_inches='tight')
