# v10 (M/L): usage: python ring_v10.py M|L.  CadQuery unibody U-signet. X=along finger, Y=width, Z=up, finger axis = X axis.
import cadquery as cq, math, json, ezdxf, sys, os
SZ=sys.argv[1] if len(sys.argv)>1 else 'M'
S=dict(M=dict(ID=19.4,HW=22.4,HL=17.5,win=(16.8,12.2),gl_y=17.25,oled=(16.2,16.5)),   # oled=(X along finger, Y)
       L=dict(ID=21.0,HW=24.0,HL=18.8,win=(18.2,13.3),gl_y=18.8,oled=(18.1,18.46)))[SZ]
O=f'/workspace/coderain_ring/v10_{SZ}/'; os.makedirs(O,exist_ok=True); P=f'v10_{SZ}_'
ID=S['ID']; ri=ID/2; t_lin=0.5; t_out=1.0; rr=ri+t_lin; R=rr+t_out
HW=S['HW']; HL=S['HL']; assert abs(HW/2-R)<1e-9   # straight sides tangent to band -> no step
g_w=2.2; g_d=0.18
z_floor=rr+0.5            # bottom wall 0.5 above outer-band inner surface
stack=[('chips',0.85),('pcb',0.4),('oled',1.45),('glue',0.05),('glass',0.4),('lip',0.5)]
z=z_floor; Z={}
for n,t in stack: Z[n]=(z,z+t); z+=t
z_top=z; wall=0.5
win_y,win_x=S['win']; gl_y=S['gl_y']; gl_x=win_x+0.6
bat_t,bat_h,bat_l=2.0,8.0,15.0
bat_yo=HW/2-wall; bat_yi=bat_yo-bat_t; bat_z1=Z['glass'][1]; bat_z0=bat_z1-bat_h
pocket_y=2*bat_yi
pad_d=1.0; z_pad=-(ri-pad_d); sock_d=4.1; sock_L=2.0; pad_x=3.0
def box(x0,x1,y0,y1,z0,z1): return cq.Workplane().box(x1-x0,y1-y0,z1-z0,centered=False).translate((x0,y0,z0))
def cylX(r,x0,x1): return cq.Workplane('YZ').circle(r).extrude(x1-x0).translate((x0,0,0))
L=HL/2
prof=cq.Workplane('YZ').circle(R).extrude(HL).translate((-L,0,0)).union(box(-L,L,-R,R,0,z_top))
try: prof=prof.edges('|X and >Z').fillet(0.6)
except Exception as e: print('fillet top',e)
# full-width charging pad: bore radius r(th)=ri-pad_d*cos^2(pi*th/(2*pad_w)) for |th|<pad_w (th from -Z), tangent blend, no crease
pad_w=35.0
def r_bore(th):
    a=abs(((th+180)%360)-180)
    return ri-pad_d*math.cos(math.pi*a/(2*pad_w))**2 if a<pad_w else ri
bpts=[(-r_bore(th)*math.sin(math.radians(th)),-r_bore(th)*math.cos(math.radians(th))) for th in [i*2.5 for i in range(144)]]
bore=cq.Workplane('YZ').spline(bpts,periodic=True).close().extrude(HL+2).translate((-L-1,0,0))
shell=prof.cut(bore)
ed=[e for e in shell.edges().vals() if e.geomType()=='BSPLINE' and abs(abs(e.Center().x)-L)<0.05]
try: shell=shell.newObject(ed).fillet(0.4); print('bore edge fillet ok',len(ed))
except Exception as ex: print('fillet fail',ex)
def sec(a0,a1,x0,x1):  # sector on -Y side, angle from -Z toward -Y
    pts=[(0,0)]+[(-15*math.sin(math.radians(a0+(a1-a0)*i/30)),-15*math.cos(math.radians(a0+(a1-a0)*i/30))) for i in range(31)]
    return cq.Workplane('YZ').polyline(pts).close().extrude(x1-x0).translate((x0,0,0))
ch_w=3.0; st_w=2.9; a_end=135
a_pad=pad_w                                   # pad blends back into bore here
a_sock=math.degrees(math.asin((sock_d/2)/rr))                       # socket hole edge
# cavities
cav=box(-(L-wall),L-wall,-bat_yi,bat_yi,z_floor,Z['oled'][1]+0.05)\
   .union(box(-gl_x/2,gl_x/2,-pocket_y/2,pocket_y/2,Z['glue'][0],Z['glass'][1]))\
   .union(box(-win_x/2,win_x/2,-win_y/2,win_y/2,Z['glass'][1]-0.01,z_top+1))
for s in (1,-1):
    cav=cav.union(box(-bat_l/2,bat_l/2,min(s*bat_yi,s*bat_yo),max(s*bat_yi,s*bat_yo),bat_z0,bat_z1))
shell=shell.cut(cav)
hole_y=-(bat_yi-1.2); slot_z0=math.sqrt(ri**2-hole_y**2)-0.15
shell=shell.cut(box(-g_w/2,g_w/2,hole_y-0.5,hole_y+0.5,slot_z0,z_floor+0.1))
a_end=math.degrees(math.atan2(-hole_y,-math.sqrt(ri**2-hole_y**2)))+5.6
def md(r,a1):   # 2D min dist from arc r (0..a1) to -Y battery rect
    best=9
    for i in range(41):
        for j in range(81):
            y=-bat_yi-bat_t*i/40; zz=bat_z0+bat_h*j/80
            for k in range(int(a1*4)+1):
                th=math.radians(k/4); best=min(best,math.hypot(y+r*math.sin(th),zz+r*math.cos(th)))
    return best
a_strip_end=a_end
for a in [a_end-0.5*i for i in range(200)]:
    if md(rr+g_d,a)>=0.9: a_strip_end=a; break
if SZ=='M': a_end,a_strip_end=135.0,118.0   # keep approved M route exactly
print('a_end',a_end,'a_strip_end',a_strip_end)
ep_d=0.25          # deep channel 0..118 deg; shallow epoxy groove 118..135
recess=cylX(rr,-ch_w/2,ch_w/2).intersect(sec(0,a_strip_end,-2,2))
groove=cylX(rr+g_d,-g_w/2,g_w/2).cut(cylX(rr-0.01,-2,2)).intersect(sec(0,a_strip_end,-2,2))
chan=recess.union(groove)
epg=None
if a_end-a_strip_end>0.5:
    epg=cylX(ri+ep_d,-g_w/2,g_w/2).intersect(sec(a_strip_end-1,a_end+3,-2,2)); chan=chan.union(epg)
shell=shell.cut(chan)
sock=cq.Workplane('XY').circle(sock_d/2).extrude(sock_L).translate((0,0,z_pad-sock_L))
shell=shell.cut(sock.union(cq.Workplane('XY').circle(sock_d/2).extrude(1).translate((0,0,z_pad-0.01))))
gap_a=math.degrees(0.05/ri)
s_a0=a_pad+gap_a; s_a1=a_strip_end-gap_a
liner=cylX(rr,-st_w/2,st_w/2).cut(cylX(ri,-2,2)).intersect(sec(s_a0,s_a1,-2,2))   # narrow cover strip
glass=box(-gl_x/2,gl_x/2,-gl_y/2,gl_y/2,*Z['glass'])
ox,oy=S['oled']; oled=box(-ox/2,ox/2,-oy/2,oy/2,*Z['oled']); pcb=box(-ox/2,ox/2,-oy/2,oy/2,*Z['pcb'])
bats=[box(-bat_l/2,bat_l/2,min(s*bat_yi,s*bat_yo),max(s*bat_yi,s*bat_yo),bat_z0,bat_z1) for s in (1,-1)]
socket=cq.Workplane('XY').circle(2.0).extrude(sock_L).translate((0,0,z_pad-sock_L))
parts=dict(shell=shell,strip=liner,glass=glass,oled=oled,pcb=pcb,bat_L=bats[1],bat_R=bats[0],socket=socket)
for n,p in parts.items():
    if n in('shell','strip','glass'): cq.exporters.export(p,O+P+f'{n}.step')
    cq.exporters.export(p,O+P+f'{n}.stl',tolerance=0.01,angularTolerance=0.1)
# checks (volumes of intersections)
def iv(a,b):
    try: return a.intersect(b).val().Volume()
    except Exception: return 0.0
fing=cylX(ri,-L,L)
chk={'bat_vs_finger_vol':sum(iv(b,fing) for b in bats),'bat_vs_shellmetal':sum(iv(b,shell) for b in bats),
 'glass_vs_bat':sum(iv(glass,b) for b in bats),'glass_vs_shell':iv(glass,shell),'socket_vs_strip':iv(socket,liner),
 'strip_vs_shell':iv(liner,shell),'oled_vs_shell':iv(oled,shell),'pcb_vs_shell':iv(pcb,shell),'oled_vs_bat':sum(iv(oled,b) for b in bats)}
cr=math.hypot(bat_yi,bat_z0)
geo=dict(R=R,ri=ri,rr=rr,z_top=z_top,head_thk=z_top-rr,stack=Z,bat_z=(bat_z0,bat_z1),bat_y=(bat_yi,bat_yo),
 glass_to_bat_gap=bat_yi-gl_y/2,
 total_bat_corner_to_finger=cr-ri,
 groove_wall_to_bat_corner=cr-(rr+g_d), groove_band_remaining=R-rr-g_d,
 socket_back_wall=R+z_pad-sock_L+ (0), pad_flat_halfchord=math.sqrt(ri**2-z_pad**2),
 head_floor_center=z_floor-rr, top_lip=z_top-Z['glass'][1], side_wall=HW/2-bat_yo,
 bat_raise_needed_for_0p5=math.sqrt((rr+g_d+0.5)**2-bat_yi**2)-bat_z0)
geo['socket_back_wall']=R-(-z_pad+sock_L)
geo['shell_vol']=shell.val().Volume(); geo['strip_vol']=liner.val().Volume(); geo['valid']=shell.val().isValid()
rm=(ri+rr)/2; flatL=rm*math.radians(s_a1-s_a0); flatW=st_w
def wall_pt(r_surf): return math.hypot(bat_yi,bat_z0)-r_surf
geo.update(strip_a0=s_a0,strip_a1=s_a1,strip_flat_L_midline=flatL,strip_flat_W=flatW,strip_t=t_lin,
 strip_inner_arc=ri*math.radians(s_a1-s_a0),strip_outer_arc=rr*math.radians(s_a1-s_a0),
 batR_corner_to_inner_surface=wall_pt(ri),batL_corner_to_strip_recess=wall_pt(rr),batL_corner_to_groove=wall_pt(rr+g_d),
 band_under_groove=R-rr-g_d,band_under_recess=R-rr,pad_slot_open_len_midline=rm*math.radians(a_pad-a_sock))
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
dd=ezdxf.new(); mm=dd.modelspace(); mm.add_lwpolyline([(0,0),(flatL,0),(flatL,flatW),(0,flatW)],close=True)
mm.add_text(f'COVER STRIP v10 '+SZ+'  {flatL:.2f} x {flatW:.2f} x 0.5 sheet (midline length; bend grain along L)',dxfattribs={'height':1}).set_placement((0,-3))
dd.saveas(O+P+'strip_flat.dxf')
f,ax=plt.subplots(figsize=(11,4)); ax.add_patch(plt.Rectangle((0,0),flatL,flatW,fc='#d4a050',ec='k')); ax.set_xlim(-3,flatL+3); ax.set_ylim(-4,flatW+3); ax.set_aspect('equal')
ax.annotate('',(0,-2),(flatL,-2),arrowprops=dict(arrowstyle='<->')); ax.text(flatL/2,-3.5,f'L = {flatL:.2f} (midline r={rm:.2f}; inner arc {geo["strip_inner_arc"]:.2f}, outer {geo["strip_outer_arc"]:.2f})',ha='center')
ax.text(flatL+0.5,flatW/2,f'W={flatW:.2f}',rotation=90,va='center'); ax.set_title(f'v10 {SZ} cover strip flat pattern, 0.5 mm sheet ')
f.savefig(O+P+'strip_flat.png',dpi=120,bbox_inches='tight')
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
def dist(a,b):
    d=BRepExtrema_DistShapeShape(a.val().wrapped,b.val().wrapped); d.Perform(); return d.Value()
slot=box(-g_w/2,g_w/2,hole_y-0.5,hole_y+0.5,slot_z0,z_floor+0.1)
fing=cylX(ri,-L-1,L+1)
geo.update(wall_batL_to_bore=dist(bats[1],fing),wall_batR_to_bore=dist(bats[0],fing),wall_batL_to_channel=dist(bats[1],chan),
 wall_batL_to_strip_recess=dist(bats[1],recess),wall_batL_to_epoxy_groove=(dist(bats[1],epg) if epg else None),wall_batL_to_flex_slot=dist(bats[1],slot),
 glass_gap_each_side=bat_yi-gl_y/2, epoxy_zone_A_deg=((a_strip_end,a_end) if epg else None), epoxy_zone_A_arc_mm=(ri*math.radians(a_end-a_strip_end) if epg else 0),
 epoxy_zone_B_deg=(a_sock,a_pad), epoxy_zone_B_arc_mm=ri*math.radians(a_pad-a_sock), band_under_epoxy_groove=R-ri-ep_d, hole_y=hole_y, glass=(gl_y,gl_x), window=(win_y,win_x), oled=S['oled'], cavity_x=2*(L-wall), oled_x_overhang_each_end=(S['oled'][0]-2*(L-wall))/2, oled_y_gap_to_bat=bat_yi-S['oled'][1]/2, border_LR=(HW-win_y)/2, border_TB=(HL-win_x)/2)
for k in ('groove_wall_to_bat_corner','batL_corner_to_strip_recess','batL_corner_to_groove','glass_to_bat_gap'): geo.pop(k,None)
print(json.dumps(dict(chk=chk,geo=geo),indent=1,default=str))
json.dump(dict(chk=chk,geo=geo),open(O+P+'checks.json','w'),indent=1,default=str)
# glass outline DXF
import ezdxf
d=ezdxf.new(); m=d.modelspace(); m.add_lwpolyline([(-gl_y/2,-gl_x/2),(gl_y/2,-gl_x/2),(gl_y/2,gl_x/2),(-gl_y/2,gl_x/2)],close=True)
m.add_lwpolyline([(-win_y/2,-win_x/2),(win_y/2,-win_x/2),(win_y/2,win_x/2),(-win_y/2,win_x/2)],close=True,dxfattribs={'linetype':'DASHED'})
d.saveas(O+P+'glass_outline.dxf')
