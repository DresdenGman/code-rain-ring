# v9 (from v8): closed metal top plate w/ window 13.6x10.3, glass recessed 0.5 under plate; separate top bezel cap.
# v4: straight-walled U-signet. End view (along finger, YZ): flat top, vertical parallel sides, round bottom.
import numpy as np, sdf, trimesh, json, sys
from sdf import sdf3
P=dict(ri=10.3, band_t=2.0, z_top=14.8, top_r=1.0, edge_r=0.7,
  hx_top=10.3, hx_bot=10.3,            # constant 17mm width: no taper in any view
  lens_y=21.2, lens_x=17.6, lens_r=1.2, lens_t=0.4,
  oled_y=16.8, oled_x=17.4, oled_t=1.3,
  cav_y=7.4, cav_x=9.5, cav_top=13.2, wall=0.8,
  sh_y0=7.0, sh_z0=4.6, sh_z1=13.9,
  lid_t=0.6,
  sock_d=4.0, sock_hole=4.1, sock_L=2.0, sock_x=0.0, sock_recess=0.1)  # WIRE cx-4mm-jz female: OD4, L2 (step to D3.7), face ring D2.2, center pin D1
R=P['ri']+P['band_t']
def box2(px,py,hx,hy,r):
    qx=np.abs(px)-hx+r; qy=np.abs(py)-hy+r
    return np.hypot(np.maximum(qx,0),np.maximum(qy,0))+np.minimum(np.maximum(qx,qy),0)-r
@sdf3
def shell_outer():
    e=P['edge_r']
    def f(p):
        x,y,z=p[:,0],p[:,1],p[:,2]
        # U profile in YZ: circle radius R  U  rect |y|<=R, 0<=z<=z_top (top corners rounded)
        zc=P['z_top']/2
        drect=box2(y,z-zc,R,zc,P['top_r'])
        dcirc=np.hypot(y,z)-R
        d2=np.minimum(drect,dcirc)
        t=np.clip((z+R)/R,0,1); hx=P['hx_bot']+(P['hx_top']-P['hx_bot'])*(t*t*(3-2*t))
        dx=np.abs(x)-hx
        a=d2+e; b=dx+e
        return np.hypot(np.maximum(a,0),np.maximum(b,0))+np.minimum(np.maximum(a,b),0)-e
    return f
@sdf3
def finger():
    def f(p): return np.hypot(p[:,1],p[:,2])-P['ri']
    return f
@sdf3
def boxz(hx,hy,r,z0,z1,cx=0.0,cy=0.0):
    def f(p):
        return np.maximum(box2(p[:,0]-cx,p[:,1]-cy,hx,hy,r),np.maximum(p[:,2]-z1,z0-p[:,2]))
    return f
@sdf3
def annulus(r0,r1):
    def f(p):
        r=np.hypot(p[:,1],p[:,2]); return np.maximum(r0-r,r-r1)
    return f
@sdf3
def usb_hole():
    def f(p):
        x,y,z=p[:,0],p[:,1],p[:,2]
        return np.maximum(box2(y,z-P['usb_zc'],P['usb_w']/2,P['usb_h']/2,1.4),np.maximum(-12-x,x+5))
    return f
outer=shell_outer()
inner=outer.dilate(-P['wall'])
ring=outer.difference(finger(),k=0.6)   # soft inner edge
center=boxz(P['cav_x'],P['cav_y'],1.0,5.0,P['cav_top'])
shoulders=boxz(P['cav_x'],(R-P['sh_y0'])/2+0.5,0.8,P['sh_z0'],P['sh_z1'],0,(R+P['sh_y0'])/2) | boxz(P['cav_x'],(R-P['sh_y0'])/2+0.5,0.8,P['sh_z0'],P['sh_z1'],0,-(R+P['sh_y0'])/2)
P['sh_z1']=13.9
shoulders=boxz(P['cav_x'],(R-P['sh_y0'])/2+0.5,0.8,P['sh_z0'],P['sh_z1'],0,(R+P['sh_y0'])/2) | boxz(P['cav_x'],(R-P['sh_y0'])/2+0.5,0.8,P['sh_z0'],P['sh_z1'],0,-(R+P['sh_y0'])/2)
cav=(center|(shoulders - annulus(0,P['ri']+0.7))) & inner   # v8: 0.7 wall between battery pockets and finger
window=boxz(P['cav_x'],P['cav_y'],1.0,5.0,P['cav_top'])
@sdf3
def cylz(r,z0,z1,cx=0.0,cy=0.0):
    def f(p): return np.maximum(np.hypot(p[:,0]-cx,p[:,1]-cy)-r,np.maximum(p[:,2]-z1,z0-p[:,2]))
    return f
pogo_cut=cylz(P['sock_hole']/2,5.0,P['ri']+3.0,P['sock_x'])
lid=(window & annulus(P['ri'],P['ri']+P['lid_t'])) - pogo_cut
z0s=P['ri']+P['sock_recess']
pogo=cylz(P['sock_d']/2,z0s,z0s+1.8,P['sock_x']) | cylz(1.85,z0s+1.79,z0s+P['sock_L'],P['sock_x'])
# ---------------- v9: closed metal top plate + recessed glass/screen ----------------
P.update(z_split=13.9,                    # parting line: body z<13.9 / top bezel cap z>=13.9 (seam on head sides, 0.9 below top)
  plate_t=0.5,                           # metal above glass = recess depth
  win_x=10.3, win_y=13.6, win_r=0.5, win_ch=0.15,   # window (X along finger, Y across), inner chamfer
  aa_x=10.06, aa_y=13.42, aa_off=1.0,    # active area; AA offset from panel centre toward +X (away from FPC) -- CONFIRM with spec
  oled_cx=-0.2, oled_z0=12.62,           # panel moved -0.5 vs v8 so AA sits near face centre; panel z 12.62-13.85
  pcb_z0=12.0,                           # PCB lowered 0.4 (12.0-12.4) to make room for recess
  glass_x=13.0, glass_y=16.4, glass_r=0.8, glass_t=0.4,
  open_x=19.0, open_y=23.0, open_r=1.0)   # top assembly opening of body (= inner wall)
P['win_cx']=P['oled_cx']+P['aa_off']
zt=P['z_top']; zs=P['z_split']; zg1=zt-P['plate_t']; zg0=zg1-P['glass_t']
@sdf3
def slab(z0,z1):
    def f(p): return np.maximum(p[:,2]-z1,z0-p[:,2])
    return f
@sdf3
def win_cut():
    def f(p):
        x,y,z=p[:,0]-P['win_cx'],p[:,1],p[:,2]
        g=np.clip(z-(zt-P['win_ch']),0,None)          # 45deg chamfer at top edge
        d=box2(x,y,P['win_x']/2+g,P['win_y']/2+g,P['win_r']+g)
        return np.maximum(d,np.maximum(p[:,2]-(zt+1),zg1-0.3-p[:,2]))
    return f
opening=boxz(P['open_x']/2,P['open_y']/2,P['open_r'],P['pcb_z0']-0.3,zs+0.01) & inner
body=(ring - cav - opening) & slab(-20,zs)
glass_pocket=boxz(P['glass_x']/2+0.05,P['glass_y']/2+0.05,P['glass_r'],zs-0.1,zg1,P['win_cx'])
oled_pocket=boxz(8.4,8.4,0.4,zs-0.1,zg0+0.001,P['oled_cx'])   # tiny relief, cap underside flat elsewhere
lip=(boxz(P['open_x']/2-0.05,P['open_y']/2-0.05,P['open_r'],zs-0.25,zs+0.01) - boxz(P['open_x']/2-0.45,P['open_y']/2-0.45,0.6,zs-1,zs+1)) - boxz(2.5,13,0.1,zs-1,zs+0.02,-9.5)  # locating lip, no -X segment (FPC bend)
cap=((outer & slab(zs,30)) | lip) - win_cut() - glass_pocket
lens=boxz(P['glass_x']/2,P['glass_y']/2,P['glass_r'],zg0+0.005,zg1-0.005,P['win_cx'])
@sdf3
def half():
    def f(p): return p[:,0]-P['win_cx']   # keep x<0 half -> section across finger (shows U profile)
    return f
if __name__=="__main__":
    st=float(sys.argv[1]) if len(sys.argv)>1 else 0.08
    B=((-12,-14,-14),(12,14,15.5))
    for n,s,b in [("v9_unibody",body,((-12,-14,-14),(12,14,14.2))),("v9_top_bezel",cap,((-11.5,-13.5,13.4),(11.5,13.5,15.2))),("v9_bottom_lid",lid,((-11.5,-9,5),(11.5,9,11.5))),("v9_lens",lens,((-8,-9,13.5),(9,9,14.6))),("v9_pogo",pogo,((-3,-3,9.8),(3,3,13))),
                  ("v9_section_body",body & half(),((-12,-14,-14),(1.3,14,14.2))),("v9_section_cap",cap & half(),((-11.5,-13.5,13.4),(1.3,13.5,15.2))),("v9_section_lens",lens & half(),((-8,-9,13.5),(1.3,9,14.6))),("v9_section_lid",lid & half(),((-11.5,-9,5),(1.3,9,11.5))),("v9_section_pogo",pogo & half(),((-3,-3,9.8),(1.3,3,13)))]:
        s.save(f"cad/{n}.stl",step=st,bounds=b,verbose=False)
        m=trimesh.load(f"cad/{n}.stl"); print(n,np.round(m.bounds,2).tolist(),len(m.faces),"vol",round(m.volume,1),"wt",m.is_watertight)
    json.dump(P,open("cad/v9_params.json","w"),indent=1)
    print("top above finger",P['z_top']-P['ri'],"outer width",2*R)
