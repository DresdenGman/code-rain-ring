# v10 M: CadQuery unibody U-signet. X=along finger, Y=width, Z=up, finger axis = X axis.
import cadquery as cq, math, json, ezdxf
O='/workspace/coderain_ring/v10_M/'
ID=19.4; ri=ID/2; t_lin=0.5; t_out=1.0; rr=ri+t_lin; R=rr+t_out       # 9.7 / 10.2 / 11.2
HW=22.4; HL=17.5; assert abs(HW/2-R)<1e-9   # straight sides tangent to band -> no step
g_w=2.2; g_d=0.18
z_floor=rr+0.5            # bottom wall 0.5 above outer-band inner surface
stack=[('chips',0.85),('pcb',0.4),('oled',1.45),('glue',0.05),('glass',0.4),('lip',0.5)]
z=z_floor; Z={}
for n,t in stack: Z[n]=(z,z+t); z+=t
z_top=z; wall=0.5
win_y,win_x=16.8,12.2; gl_y,gl_x=17.4,win_x+0.6
bat_t,bat_h,bat_l=2.0,8.0,15.0
bat_yo=HW/2-wall; bat_yi=bat_yo-bat_t; bat_z1=Z['glass'][1]; bat_z0=bat_z1-bat_h
pad_d=1.0; z_pad=-(ri-pad_d); sock_d=4.1; sock_L=2.0; pad_x=3.0
def box(x0,x1,y0,y1,z0,z1): return cq.Workplane().box(x1-x0,y1-y0,z1-z0,centered=False).translate((x0,y0,z0))
def cylX(r,x0,x1): return cq.Workplane('YZ').circle(r).extrude(x1-x0).translate((x0,0,0))
L=HL/2
prof=cq.Workplane('YZ').circle(R).extrude(HL).translate((-L,0,0)).union(box(-L,L,-R,R,0,z_top))
try: prof=prof.edges('|X and >Z').fillet(0.6)
except Exception as e: print('fillet top',e)
shell=prof.cut(cylX(ri,-L-1,L+1)).cut(cylX(rr,-L+1,L-1))            # bore + liner recess (1.0 rims)
# socket pad (integral flat on inside bottom)
pad=cylX(rr,-pad_x,pad_x).intersect(box(-pad_x,pad_x,-5.6,5.6,-R,-7.5)).cut(cylX(ri,-5,5).intersect(box(-5,5,-6,6,z_pad,0)))
def wedgeYZ(a,x0,x1):  # sector |angle from -Z|<=a deg
    import math
    pts=[(0,0)]+[(15*math.sin(math.radians(t)),-15*math.cos(math.radians(t))) for t in [-a+i*(2*a)/20 for i in range(21)]]
    return cq.Workplane('YZ').polyline(pts).close().extrude(x1-x0).translate((x0,0,0))
liner_gap_a=35.0; filler_a=liner_gap_a-math.degrees(0.1/ri)
filler=cylX(rr,-L+1,L-1).cut(cylX(ri,-L,L)).intersect(wedgeYZ(filler_a,-L,L))   # metal fills recess at socket zone, full width
pad=pad.intersect(wedgeYZ(filler_a,-L,L))
shell=shell.union(pad).union(filler)
# cavities
cav=box(-8.25,8.25,-bat_yi,bat_yi,z_floor,Z['oled'][1]+0.05)\
   .union(box(-gl_x/2,gl_x/2,-gl_y/2,gl_y/2,Z['glue'][0],Z['glass'][1]))\
   .union(box(-win_x/2,win_x/2,-win_y/2,win_y/2,Z['glass'][1]-0.01,z_top+1))
for s in (1,-1):
    cav=cav.union(box(-bat_l/2,bat_l/2,min(s*bat_yi,s*bat_yo),max(s*bat_yi,s*bat_yo),bat_z0,bat_z1))
shell=shell.cut(cav)
hole_y=-7.5
shell=shell.cut(box(-g_w/2,g_w/2,hole_y-0.5,hole_y+0.5,6.0,z_floor+0.1))
a_end=135
pts=[(0,0)]+[(-15*math.sin(math.radians(a)),-15*math.cos(math.radians(a))) for a in range(0,a_end+1,5)]
wedge=cq.Workplane('YZ').polyline(pts).close().extrude(g_w).translate((-g_w/2,0,0))
groove=cylX(rr+g_d,-g_w/2,g_w/2).cut(cylX(rr-0.01,-2,2)).intersect(wedge)
shell=shell.cut(groove)
sock=cq.Workplane('XY').circle(sock_d/2).extrude(sock_L).translate((0,0,z_pad-sock_L))
shell=shell.cut(sock.union(cq.Workplane('XY').circle(sock_d/2).extrude(1).translate((0,0,z_pad-0.01))))
liner=cylX(rr,-L+1.05,L-1.05).cut(cylX(ri,-L,L)).cut(wedgeYZ(liner_gap_a,-L,L))   # OPEN strip, ends butt at socket cut-out
glass=box(-gl_x/2,gl_x/2,-gl_y/2,gl_y/2,*Z['glass'])
oled=box(-8.1,8.1,-8.25,8.25,*Z['oled']); pcb=box(-8.1,8.1,-8.25,8.25,*Z['pcb'])
bats=[box(-bat_l/2,bat_l/2,min(s*bat_yi,s*bat_yo),max(s*bat_yi,s*bat_yo),bat_z0,bat_z1) for s in (1,-1)]
socket=cq.Workplane('XY').circle(2.0).extrude(sock_L).translate((0,0,z_pad-sock_L))
parts=dict(shell=shell,liner=liner,glass=glass,oled=oled,pcb=pcb,bat_L=bats[1],bat_R=bats[0],socket=socket)
for n,p in parts.items():
    if n in('shell','liner','glass'): cq.exporters.export(p,O+f'v10_M_{n}.step')
    cq.exporters.export(p,O+f'v10_M_{n}.stl',tolerance=0.01,angularTolerance=0.1)
# checks (volumes of intersections)
def iv(a,b):
    try: return a.intersect(b).val().Volume()
    except Exception: return 0.0
fing=cylX(ri,-L,L)
chk={'bat_vs_finger_vol':sum(iv(b,fing) for b in bats),'bat_vs_shellmetal':sum(iv(b,shell) for b in bats),
 'glass_vs_bat':sum(iv(glass,b) for b in bats),'glass_vs_shell':iv(glass,shell),'socket_vs_liner':iv(socket,liner),
 'liner_vs_shell':iv(liner,shell),'oled_vs_shell':iv(oled,shell)}
cr=math.hypot(bat_yi,bat_z0)
geo=dict(R=R,ri=ri,rr=rr,z_top=z_top,head_thk=z_top-rr,stack=Z,bat_z=(bat_z0,bat_z1),bat_y=(bat_yi,bat_yo),
 glass_to_bat_gap=bat_yi-gl_y/2,
 metal_bat_corner_to_liner=cr-rr, total_bat_corner_to_finger=cr-ri,
 groove_wall_to_bat_corner=cr-(rr+g_d), groove_band_remaining=R-rr-g_d,
 socket_back_wall=R+z_pad-sock_L+ (0), pad_flat_halfchord=math.sqrt(ri**2-z_pad**2),
 head_floor_center=z_floor-rr, top_lip=z_top-Z['glass'][1], side_wall=HW/2-bat_yo,
 bat_raise_needed_for_0p5=math.sqrt((rr+g_d+0.5)**2-bat_yi**2)-bat_z0)
geo['socket_back_wall']=R-(-z_pad+sock_L)
geo['shell_vol']=shell.val().Volume(); geo['liner_vol']=liner.val().Volume(); geo['valid']=shell.val().isValid()
rm=(ri+rr)/2; flatL=rm*(2*math.pi-2*math.radians(liner_gap_a)); flatW=HL-2.1
geo.update(liner_open=True,liner_gap_deg=2*liner_gap_a,liner_flat_L_midline=flatL,liner_flat_W=flatW,liner_t=t_lin,
 liner_end_gap_to_filler=0.1,liner_inner_arc=ri*(2*math.pi-2*math.radians(liner_gap_a)),liner_outer_arc=rr*(2*math.pi-2*math.radians(liner_gap_a)),
 liner_is_open=len(liner.solids().vals())==1 and abs(liner.val().Volume()-flatL*flatW*t_lin)<2)
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
dd=ezdxf.new(); mm=dd.modelspace(); mm.add_lwpolyline([(0,0),(flatL,0),(flatL,flatW),(0,flatW)],close=True)
mm.add_text(f'LINER v10 M  {flatL:.2f} x {flatW:.2f} x 0.5 sheet (midline length; bend grain along L)',dxfattribs={'height':1}).set_placement((0,-3))
dd.saveas(O+'v10_M_liner_flat.dxf')
f,ax=plt.subplots(figsize=(11,4)); ax.add_patch(plt.Rectangle((0,0),flatL,flatW,fc='#d4a050',ec='k')); ax.set_xlim(-3,flatL+3); ax.set_ylim(-4,flatW+3); ax.set_aspect('equal')
ax.annotate('',(0,-2),(flatL,-2),arrowprops=dict(arrowstyle='<->')); ax.text(flatL/2,-3.5,f'L = {flatL:.2f} (midline r={rm:.2f}; inner arc {geo["liner_inner_arc"]:.2f}, outer {geo["liner_outer_arc"]:.2f})',ha='center')
ax.text(flatL+0.5,flatW/2,f'W={flatW:.2f}',rotation=90,va='center'); ax.set_title('v10 M liner flat pattern, 0.5 mm sheet (ends butt inside socket cut-out, 70 deg gap)')
f.savefig(O+'v10_M_liner_flat.png',dpi=120,bbox_inches='tight')
print(json.dumps(dict(chk=chk,geo=geo),indent=1,default=str))
json.dump(dict(chk=chk,geo=geo),open(O+'v10_M_checks.json','w'),indent=1,default=str)
# glass outline DXF
import ezdxf
d=ezdxf.new(); m=d.modelspace(); m.add_lwpolyline([(-gl_y/2,-gl_x/2),(gl_y/2,-gl_x/2),(gl_y/2,gl_x/2),(-gl_y/2,gl_x/2)],close=True)
m.add_lwpolyline([(-win_y/2,-win_x/2),(win_y/2,-win_x/2),(win_y/2,win_x/2),(-win_y/2,win_x/2)],close=True,dxfattribs={'linetype':'DASHED'})
d.saveas(O+'v10_M_glass_outline.dxf')
