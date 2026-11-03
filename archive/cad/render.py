import trimesh, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
D="cad/"; R="renders/"
shell=trimesh.load(D+"ring_shell.stl"); lid=trimesh.load(D+"ring_lid.stl")
print("shell watertight",shell.is_watertight,"vol",round(shell.volume,1),"lid",lid.is_watertight)
parts={k:trimesh.load(D+f"part_{k}.stl") for k in ["lens","oled","pcb","usbc","battery"]}
col={"shell":(0.18,0.2,0.22),"lid":(0.35,0.37,0.4),"lens":(0.3,1,0.4),"oled":(0.05,0.05,0.05),"pcb":(0.1,0.5,0.2),"usbc":(0.75,0.75,0.78),"battery":(0.85,0.7,0.2)}
def draw(ax,m,c,alpha=1.0,off=(0,0,0)):
    v=m.vertices+np.array(off); f=m.faces; n=m.face_normals
    shade=0.45+0.55*np.clip(n@np.array([0.3,-0.5,0.8])/np.linalg.norm([0.3,-0.5,0.8]),0,1)
    fc=np.clip(np.outer(shade,c),0,1); fc=np.c_[fc,np.full(len(fc),alpha)]
    ax.add_collection3d(Poly3DCollection(v[f],facecolors=fc,edgecolors="none"))
def fig(items,elev,azim,name,title,lim=17):
    f=plt.figure(figsize=(7,7)); ax=f.add_subplot(111,projection="3d")
    for m,c,a,o in items: draw(ax,m,c,a,o)
    ax.set_xlim(-lim,lim);ax.set_ylim(-lim,lim);ax.set_zlim(-lim+4,lim+4);ax.set_box_aspect((1,1,1))
    ax.view_init(elev,azim);ax.set_axis_off();ax.set_title(title);f.tight_layout();f.savefig(R+name,dpi=130);plt.close(f)
asm=[(shell,col["shell"],1,(0,0,0)),(lid,col["lid"],1,(0,0,0)),(parts["lens"],col["lens"],0.9,(0,0,0))]
fig(asm,25,-60,"iso_front.png","Code Rain v1 - iso")
fig(asm,10,-180,"usb_end.png","USB-C end (-X)")
fig(asm,80,-90,"top.png","Top / face")
fig(asm,5,-90,"side_y.png","Side (+Y tap zone)")
fig(asm,-35,-60,"underside.png","Underside / lid + open band")
# exploded
ex=[(shell,col["shell"],0.35,(0,0,0)),(lid,col["lid"],1,(0,0,-14)),(parts["battery"],col["battery"],1,(0,0,-8)),
    (parts["pcb"],col["pcb"],1,(0,0,4)),(parts["usbc"],col["usbc"],1,(0,0,4)),(parts["oled"],col["oled"],1,(0,0,9)),(parts["lens"],col["lens"],1,(0,0,13))]
fig(ex,15,-55,"exploded.png","Exploded: lens/OLED/PCB+USB-C/battery/lid",lim=22)
# section at x=0 (YZ) and y=0 (XZ) 2D
for ax_n,normal,name,xi in [("x",[1,0,0],"section_x0.png",(1,2)),("y",[0,1,0],"section_y0.png",(0,2))]:
    f,ax=plt.subplots(figsize=(7,7))
    for k,m in [("shell",shell),("lid",lid)]+list(parts.items()):
        s=m.section(plane_origin=[0,0,0] if ax_n=="x" else [0,0.01,0],plane_normal=normal)
        if s is None: continue
        for e in s.discrete:
            ax.fill(e[:,xi[0]],e[:,xi[1]],color=col[k],alpha=0.85 if k!="shell" else 0.6,lw=0.5,ec="k")
    ax.set_aspect("equal");ax.grid(alpha=.3);ax.set_xlabel("mm");ax.set_title(f"Section {ax_n}=0")
    f.savefig(R+name,dpi=130);plt.close(f)
