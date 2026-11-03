import trimesh, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
D="cad/"; R="renders/"
L=lambda n: trimesh.load(D+n+".stl")
head,lid,band=L("v2_head"),L("v2_lid_shoulder"),L("v2_metal_band_REFERENCE")
parts={k:L("v2_part_"+k) for k in ["lens","oled","pcb","usbc","battery"]}
metal=(0.78,0.79,0.81); col={"lens":(0.05,0.12,0.07),"oled":(0.1,0.1,0.1),"pcb":(0.1,0.45,0.2),"usbc":(0.7,0.7,0.72),"battery":(0.85,0.7,0.25)}
Ld=np.array([0.4,-0.5,0.8]);Ld/=np.linalg.norm(Ld)
def draw(ax,m,c,a=1.0,off=(0,0,0),matte=True):
    v=m.vertices+np.array(off); n=m.face_normals
    lam=np.clip(n@Ld,0,1); h=(n@ (Ld+np.array([0,0,1]))/np.linalg.norm(Ld+np.array([0,0,1])))
    spec=np.clip(h,0,1)**(6 if matte else 30)*0.25
    fc=np.clip(np.outer(0.35+0.6*lam,c)+spec[:,None],0,1)
    ax.add_collection3d(Poly3DCollection(v[m.faces],facecolors=np.c_[fc,np.full(len(fc),a)],edgecolors="none"))
def fig(items,elev,azim,name,title,lim=16,zc=6):
    f=plt.figure(figsize=(7,7),facecolor="#1b1d20"); ax=f.add_subplot(111,projection="3d"); ax.set_facecolor("#1b1d20")
    for it in items: draw(ax,*it)
    ax.set_xlim(-lim,lim);ax.set_ylim(-lim,lim);ax.set_zlim(zc-lim,zc+lim);ax.set_box_aspect((1,1,1))
    ax.view_init(elev,azim);ax.set_axis_off();ax.set_title(title,color="w");f.tight_layout();f.savefig(R+name,dpi=140,facecolor=f.get_facecolor());plt.close(f)
# code-rain texture: fake glowing green dots on lens
rng=np.random.default_rng(3); pts=[]
z_top=lid.bounds[1][2] if False else head.bounds[1][2]
asm=[(band,metal),(lid,metal),(head,metal),(parts["lens"],col["lens"],1.0)]
def rain(ax):
    pass
fig(asm,28,-55,"v2_iso_front.png","Code Rain v2 - matte metal (iso)")
fig(asm,8,-90,"v2_side.png","v2 side (tapered head, flowing shoulder)")
fig(asm,8,180,"v2_back_usb.png","v2 back: hidden USB-C on rear slope")
fig(asm,85,-90,"v2_top.png","v2 top (flush lens)")
ex=[(band,metal,1,(0,0,-6)),(lid,metal,1,(0,0,-2)),(parts["battery"],col["battery"],1,(0,0,3)),(parts["pcb"],col["pcb"],1,(0,0,7)),
    (parts["usbc"],col["usbc"],1,(0,0,7)),(parts["oled"],col["oled"],1,(0,0,11)),(head,metal,0.35,(0,0,14)),(parts["lens"],(0.2,0.8,0.35),1,(0,0,19))]
fig(ex,15,-55,"v2_exploded.png","v2 exploded: band / lid-shoulder / battery / PCB+USB-C / OLED / head / lens",lim=22,zc=14)
cols={"head":metal,"lid":(0.6,0.62,0.66),"band":(0.5,0.5,0.55)}
for ax_n,normal,name,xi in [("x",[1,0,0],"v2_section_x0.png",(1,2)),("y",[0,1,0],"v2_section_y0.png",(0,2))]:
    f,ax=plt.subplots(figsize=(7,7))
    for k,m in [("head",head),("lid",lid),("band",band)]+list(parts.items()):
        s=m.section(plane_origin=[0.01,0.01,0],plane_normal=normal)
        if s is None: continue
        for e in s.discrete: ax.fill(e[:,xi[0]],e[:,xi[1]],color=cols.get(k,col.get(k)),alpha=0.9,lw=0.5,ec="k")
    ax.set_aspect("equal");ax.grid(alpha=.3);ax.set_xlabel("mm");ax.set_title(f"v2 section {ax_n}=0 (finger centre at 0,0)")
    f.savefig(R+name,dpi=130);plt.close(f)
