# v4: straight-walled U-signet. End view (along finger, YZ): flat top, vertical parallel sides, round bottom.
import numpy as np, sdf, trimesh, json, sys
from sdf import sdf3
P=dict(ri=10.3, band_t=2.0, z_top=15.8, top_r=1.0, edge_r=0.7,
  hx_top=8.5, hx_bot=8.5,            # constant 17mm width: no taper in any view
  lens_y=19.0, lens_x=13.0, lens_r=1.2, lens_t=0.4,
  oled_y=12.3, oled_x=11.3, oled_t=1.2,
  cav_y=7.4, cav_x=7.7, cav_top=14.2, wall=0.8,
  sh_y0=7.0, sh_z0=4.6, sh_z1=13.6,
  usb_w=9.2, usb_h=3.4, usb_zc=12.53, lid_t=0.6)
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
cav=(center|shoulders) & inner
window=boxz(P['cav_x'],P['cav_y'],1.0,5.0,P['cav_top'])
lid=window & annulus(P['ri'],P['ri']+P['lid_t'])
body=ring - (cav - annulus(0,P['ri']+P['lid_t']).dilate(0) if False else cav)
body=body - boxz(P['oled_x']/2,P['oled_y']/2,0.4,P['cav_top']-0.1,P['z_top']-P['lens_t']+0.01)
body=body - boxz(P['lens_x']/2,P['lens_y']/2,P['lens_r'],P['z_top']-P['lens_t'],P['z_top']+1)
body=body - usb_hole()
lens=boxz(P['lens_x']/2-0.02,P['lens_y']/2-0.02,P['lens_r'],P['z_top']-P['lens_t']+0.02,P['z_top']-0.01)
@sdf3
def half():
    def f(p): return p[:,0]   # keep x<0 half -> section across finger (shows U profile)
    return f
if __name__=="__main__":
    st=float(sys.argv[1]) if len(sys.argv)>1 else 0.08
    B=((-10,-13.5,-13.5),(10,13.5,16.5))
    for n,s,b in [("v4_unibody",body,B),("v4_bottom_lid",lid,((-9,-9,5),(9,9,11.5))),("v4_lens",lens,((-8,-11,15),(8,11,16))),
                  ("v4_section_body",body & half(),((-10,-13.5,-13.5),(0.5,13.5,16.5)))]:
        s.save(f"cad/{n}.stl",step=st,bounds=b,verbose=False)
        m=trimesh.load(f"cad/{n}.stl"); print(n,np.round(m.bounds,2).tolist(),len(m.faces),"vol",round(m.volume,1),"wt",m.is_watertight)
    json.dump(P,open("cad/v4_params.json","w"),indent=1)
    print("top above finger",P['z_top']-P['ri'],"outer width",2*R)
