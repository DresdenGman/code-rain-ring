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
body=ring - (cav - annulus(0,P['ri']+P['lid_t']).dilate(0) if False else cav)
body=body - boxz(P['oled_x']/2,P['oled_y']/2,0.4,P['cav_top']-0.1,P['z_top']-P['lens_t']+0.01)
body=body - boxz(P['lens_x']/2,P['lens_y']/2,P['lens_r'],P['z_top']-P['lens_t'],P['z_top']+1)
lens=boxz(P['lens_x']/2-0.02,P['lens_y']/2-0.02,P['lens_r'],P['z_top']-P['lens_t']+0.02,P['z_top']-0.01)
@sdf3
def half():
    def f(p): return p[:,0]   # keep x<0 half -> section across finger (shows U profile)
    return f
if __name__=="__main__":
    st=float(sys.argv[1]) if len(sys.argv)>1 else 0.08
    B=((-12,-14,-14),(12,14,15.5))
    for n,s,b in [("v8_unibody",body,B),("v8_bottom_lid",lid,((-11.5,-9,5),(11.5,9,11.5))),("v8_lens",lens,((-11,-13,14),(11,13,15))),("v8_pogo",pogo,((-3,-3,9.8),(3,3,13))),
                  ("v8_section_body",body & half(),((-12,-14,-14),(0.5,14,15.5))),("v8_section_lid",lid & half(),((-11.5,-9,5),(0.5,9,11.5))),("v8_section_pogo",pogo & half(),((-3,-3,9.8),(0.5,3,13)))]:
        s.save(f"cad/{n}.stl",step=st,bounds=b,verbose=False)
        m=trimesh.load(f"cad/{n}.stl"); print(n,np.round(m.bounds,2).tolist(),len(m.faces),"vol",round(m.volume,1),"wt",m.is_watertight)
    json.dump(P,open("cad/v8_params.json","w"),indent=1)
    print("top above finger",P['z_top']-P['ri'],"outer width",2*R)
