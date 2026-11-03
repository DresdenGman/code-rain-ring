# v3 unibody: SDF smooth-union of tapered head + flat open band, meshed by marching cubes
import numpy as np, sdf, trimesh, json
from sdf import sdf3
P=dict(ri=10.3, band_t=1.6, band_w=6.0, band_r=0.6, gap=8.0,
  top_x=18.6, top_y=18.0, top_r=3.6, z_top=18.6, z_bot=7.6, taper_deg=17, edge_r=0.5, blend=2.6,
  lens_x=15.4, lens_y=12.2, lens_r=1.5, lens_t=0.55,
  oled_x=12.3, oled_y=11.3, oled_t=1.35,
  cav_x=13.0, cav_y=12.8, cav_r=1.0, cav_bot=10.4, cav_top=16.75,
  lid_t=0.6, usb_w=9.2, usb_h=3.4, usb_zc=14.4)
def rr2(px,py,hx,hy,r):
    qx=np.abs(px)-hx+r; qy=np.abs(py)-hy+r
    return np.hypot(np.maximum(qx,0),np.maximum(qy,0))+np.minimum(np.maximum(qx,qy),0)-r
@sdf3
def head():
    t=np.tan(np.radians(P['taper_deg'])); e=P['edge_r']
    def f(p):
        x,y,z=p[:,0],p[:,1],p[:,2]
        dz=np.clip(P['z_top']-z,0,None)
        hx=P['top_x']/2-dz*t-e; hy=P['top_y']/2-dz*t-e; r=np.maximum(P['top_r']-dz*t*0.5-e,0.3)
        d2=rr2(x,y,hx,hy,r)*np.cos(np.radians(P['taper_deg']))
        dzs=np.maximum(z-(P['z_top']-e), P['z_bot']-z)
        return np.hypot(np.maximum(d2,0),np.maximum(dzs,0))+np.minimum(np.maximum(d2,dzs),0)-e
    return f
@sdf3
def band():
    ro=P['ri']+P['band_t']; rc=(P['ri']+ro)/2; r=P['band_r']
    def f(p):
        x,y,z=p[:,0],p[:,1],p[:,2]
        rad=np.hypot(y,z)
        d=rr2(rad-rc,x,P['band_t']/2,P['band_w']/2,r)
        # open gap at bottom
        ang=np.abs(np.arctan2(y,-z)); half=np.arcsin(P['gap']/2/ro)
        cut=(half-ang)*rad
        return np.maximum(d,cut)
    return f
@sdf3
def tapered_cav(hx,hy,r,z0,z1,t=0.0):
    def f(p):
        x,y,z=p[:,0],p[:,1],p[:,2]
        s=np.clip(P['z_top']-z,0,None)*t
        d2=rr2(x,y,hx-s,hy-s,r)
        return np.maximum(d2,np.maximum(z-z1,z0-z))
    return f
@sdf3
def finger():
    def f(p): return np.hypot(p[:,1],p[:,2])-P['ri']
    return f
@sdf3
def usb():
    def f(p):
        x,y,z=p[:,0],p[:,1],p[:,2]
        d2=rr2(y,z-P['usb_zc'],P['usb_w']/2,P['usb_h']/2,1.3)
        return np.maximum(d2, np.maximum(x-(-P['cav_x']/2+0.5),-12-x))
    return f
@sdf3
def clip_below(): 
    def f(p): return (P['cav_bot'])-p[:,2]  # used for head-only region
    return f
outer=head() | band().k(P['blend'])
solid=outer
inner=solid.dilate(-0.8)
outer=outer - finger()
body=outer-(tapered_cav(P['cav_x']/2,P['cav_y']/2,P['cav_r'],6.5,P['cav_top']) & inner)
body=body-tapered_cav(P['oled_x']/2,P['oled_y']/2,0.4,P['cav_top']-0.1,P['z_top']-P['lens_t']+0.01)
body=body-tapered_cav(P['lens_x']/2,P['lens_y']/2,P['lens_r'],P['z_top']-P['lens_t'],P['z_top']+1)
body=body-usb()
# lid: plate in cavity bottom, conforming to finger, 2 screw holes
@sdf3
def screws():
    def f(p):
        x,y,z=p[:,0],p[:,1],p[:,2]
        return np.minimum(np.hypot(x-5.2,y-5.2),np.hypot(x+5.2,y+5.2))-0.55
    return f
lid=((tapered_cav(P['cav_x']/2-0.05,P['cav_y']/2-0.05,P['cav_r'],7.0,P['cav_bot']+P['lid_t']) & inner) - finger()) - screws()
lens=tapered_cav(P['lens_x']/2-0.02,P['lens_y']/2-0.02,P['lens_r'],P['z_top']-P['lens_t']+0.02,P['z_top']-0.01)
if __name__=="__main__":
    import sys
    st=float(sys.argv[1]) if len(sys.argv)>1 else 0.08
    @sdf3
    def half():
        def f(p): return p[:,1]
        return f
    for n,s,b in [("v3_section_body",body & half(),((-12,-14,-14),(12,1,19.5))),("v3_section_lid",lid & half(),((-8,-8,6),(8,1,11.5))),("v3_unibody",body,((-12,-14,-14),(12,14,19.5))),("v3_bottom_lid",lid,((-8,-8,6),(8,8,11.5))),("v3_lens",lens,((-9,-8,17.5),(9,8,19)))]:
        s.save(f"cad/{n}_raw.stl",step=st,bounds=b,verbose=False)
        m=trimesh.load(f"cad/{n}_raw.stl"); m.merge_vertices(); m.update_faces(m.unique_faces()); m.remove_unreferenced_vertices()
        m.export(f"cad/{n}.stl"); print(n,m.is_watertight,np.round(m.bounds,2).tolist(),len(m.faces),"vol",round(m.volume,1))
    json.dump(P,open("cad/v3_params.json","w"),indent=1)
