"""Code Rain ring v1 - parametric CadQuery model. Units mm.
Axes: X = finger axis, Y = across hand, Z = up (face on top). Finger centre at origin."""
import cadquery as cq, math, sys, os
OUT = os.path.join(os.path.dirname(__file__), "..")

# ---------------- parameters ----------------
P = dict(
  ID=20.6,          # nominal band inner dia (US ~11); open gap lets it flex ~18.9-22.2
  band_t=1.6,       # band radial thickness
  band_w=5.5,       # band width along finger
  band_facets=12,   # faceted cyber outer
  gap=7.0,          # opening at bottom of band (chord)
  face_x=17.0, face_y=15.5, chamf=2.2,   # octagonal face outline
  lens_x=12.6, lens_y=8.6, lens_d=0.7,   # cover lens recess (0.5mm lens + PSA)
  win_x=10.6, win_y=6.6,                 # through window (VA 10.196x6.18)
  oled_x=12.3, oled_y=11.3, oled_d=1.35, # OLED 12x11x1.227 + clearance
  fpc_slot=1.0,                          # FPC fold slot at +X end
  cav_x=13.2, cav_y=12.6, cav_d=6.55,    # PCB(0.8)+USB zone(3.2)+battery(3.0)+gaps
  lid_t=0.9, lid_lip=0.2,
  usb_w=9.2, usb_h=3.4,                  # Type-C receptacle 8.94x3.16 + clearance
  floor_gap=0.3,                         # lid underside above finger top
  btn=True, btn_w=2.4, btn_h=1.4,        # optional side tact-switch slot (+Y)
)
def build(P):
    ri = P["ID"]/2; ro = ri + P["band_t"]
    zb = ri + P["floor_gap"]                       # housing bottom
    H = P["lens_d"] + P["oled_d"] + P["cav_d"] + P["lid_t"]
    zt = zb + H
    fx, fy, c = P["face_x"], P["face_y"], P["chamf"]
    # octagon outline (YZ? no: XY plane) then extrude in Z
    def octo(x, y, ch):
        return (cq.Workplane("XY").polyline([(-x/2+ch,-y/2),(x/2-ch,-y/2),(x/2,-y/2+ch),(x/2,y/2-ch),
                 (x/2-ch,y/2),(-x/2+ch,y/2),(-x/2,y/2-ch),(-x/2,-y/2+ch)]).close())
    body = octo(fx, fy, c).extrude(H).translate((0,0,zb))
    # stepped angular bezel: chamfer the top edges
    body = body.faces(">Z").edges().chamfer(0.8)
    # second step: shallow raised frame groove
    groove = octo(fx-2.0, fy-2.0, c-0.6).extrude(0.25).translate((0,0,zt-0.25)).cut(
             octo(fx-2.6, fy-2.6, c-0.8).extrude(0.25).translate((0,0,zt-0.25)))
    body = body.cut(groove)
    # lens recess, window, OLED pocket, FPC slot
    z = zt
    body = body.cut(cq.Workplane("XY").rect(P["lens_x"],P["lens_y"]).extrude(P["lens_d"]).translate((0,0,z-P["lens_d"])))
    body = body.cut(cq.Workplane("XY").rect(P["win_x"],P["win_y"]).extrude(5).translate((0,0,z-5)))
    z -= P["lens_d"]
    body = body.cut(cq.Workplane("XY").rect(P["oled_x"],P["oled_y"]).extrude(P["oled_d"]).translate((0,0,z-P["oled_d"])))
    body = body.cut(cq.Workplane("XY").center(P["oled_x"]/2+P["fpc_slot"]/2-0.2,0).rect(P["fpc_slot"]+0.4,9.0)
                    .extrude(P["oled_d"]+0.5).translate((0,0,z-P["oled_d"]-0.5)))
    z -= P["oled_d"]
    # main cavity (PCB + USB + battery) and lid ledge
    body = body.cut(cq.Workplane("XY").rect(P["cav_x"],P["cav_y"]).extrude(P["cav_d"]+1).translate((0,0,zb)))
    body = body.cut(cq.Workplane("XY").rect(P["cav_x"]+2*P["lid_lip"],P["cav_y"]+2*P["lid_lip"]).extrude(P["lid_t"]).translate((0,0,zb)))
    # cable channel (battery leads / touch electrode wire) along -Y inner wall
    body = body.cut(cq.Workplane("XY").center(0,-P["cav_y"]/2-0.4).rect(9,0.9).extrude(P["cav_d"]).translate((0,0,zb+P["lid_t"])))
    # USB-C port on -X end; centre at PCB top level (mid-mount)
    z_pcb_top = zt - P["lens_d"] - P["oled_d"] - 0.25 - 1.6
    usb = (cq.Workplane("YZ").center(0, z_pcb_top).rect(P["usb_w"],P["usb_h"]).extrude(4)
           .edges("|X").fillet(1.3).translate((-fx/2-1,0,0)))
    body = body.cut(usb)
    if P["btn"]:
        body = body.cut(cq.Workplane("XZ").center(2.0, z_pcb_top+0.6).rect(P["btn_w"],P["btn_h"]).extrude(-3)
                        .translate((0,fy/2-1.8,0)))
    # tap-zone tactile ribs on +Y outer side (TTP223 electrode lives behind this wall)
    for i in range(3):
        body = body.cut(cq.Workplane("XZ").center(-4.5+i*1.1, zb+H/2-0.5).rect(0.4,3.2).extrude(-0.3).translate((0,fy/2+0.0001,0)).translate((0,0.0,0)))
    # ---- faceted open band ----
    n = P["band_facets"]; rop = ro/math.cos(math.pi/n)
    pts = [(rop*math.cos(2*math.pi*k/n+math.pi/n), rop*math.sin(2*math.pi*k/n+math.pi/n)) for k in range(n)]
    band = (cq.Workplane("YZ").polyline(pts).close().extrude(P["band_w"]).translate((-P["band_w"]/2,0,0)))
    band = band.cut(cq.Workplane("YZ").circle(ri).extrude(P["band_w"]+2).translate((-P["band_w"]/2-1,0,0)))
    band = band.cut(cq.Workplane("XY").box(P["band_w"]+2, P["gap"], 6).translate((0,0,-ro)))  # opening
    # keep lid area accessible: remove band under the lid opening
    band = band.cut(cq.Workplane("XY").box(P["band_w"]+2, P["cav_y"]+2*P["lid_lip"], 4).translate((0,0,zb+0.5)))
    # shoulders: blend band into housing sides
    sh = (cq.Workplane("YZ").polyline([(-fy/2+0.3, zb+2.5),(fy/2-0.3, zb+2.5),(ro*0.72, ri*0.55),(-ro*0.72, ri*0.55)]).close()
          .extrude(P["band_w"]+3).translate((-(P["band_w"]+3)/2,0,0)))
    sh = sh.cut(cq.Workplane("YZ").circle(ri).extrude(20).translate((-10,0,0)))
    sh = sh.cut(cq.Workplane("XY").box(P["face_x"], P["cav_y"]+2*P["lid_lip"], 6).translate((0,0,zb+0.5)))
    sh = sh.cut(cq.Workplane("XY").box(P["face_x"], 30, 30).translate((0,0,zb-15-0.0)).intersect(
         cq.Workplane("XY").box(P["face_x"], 30, 30).translate((0,0,0))) ) if False else sh
    ring = body.union(band).union(sh)
    ring = ring.cut(cq.Workplane("YZ").circle(ri).extrude(30).translate((-15,0,0)))
    # lid
    lid = (cq.Workplane("XY").rect(P["cav_x"]+2*P["lid_lip"]-0.1, P["cav_y"]+2*P["lid_lip"]-0.1).extrude(P["lid_t"])
           .translate((0,0,zb)))
    lid = lid.cut(cq.Workplane("YZ").circle(ri+0.05).extrude(30).translate((-15,0,0)))
    # internal part dummies for renders
    zo = zt-P["lens_d"]
    parts = {
     "lens":   cq.Workplane("XY").box(P["lens_x"]-0.2,P["lens_y"]-0.2,0.5).translate((0,0,zt-0.45)),
     "oled":   cq.Workplane("XY").box(12,11,1.227).translate((0,0,zo-0.62)),
     "pcb":    cq.Workplane("XY").box(13.0,12.4,0.8).translate((0,0,z_pcb_top-0.4)),
     "usbc":   cq.Workplane("XY").box(6.8,8.94,3.16).translate((-P["cav_x"]/2+3.3,0,z_pcb_top-0.04)),
     "battery":cq.Workplane("XY").box(12,10,3.0).translate((0.4,0,zb+P["lid_t"]+1.6)),
    }
    info = dict(zb=zb, zt=zt, H=H, ri=ri, ro=ro, z_pcb_top=z_pcb_top,
                total_y_outer=2*ro, top_above_finger_top=zt-ri)
    return ring, lid, parts, info

if __name__ == "__main__":
    ring, lid, parts, info = build(P)
    print(info)
    for name, obj in [("ring_shell", ring), ("ring_lid", lid)]:
        cq.exporters.export(obj, f"{OUT}/cad/{name}.stl", tolerance=0.02, angularTolerance=0.1)
        cq.exporters.export(obj, f"{OUT}/cad/{name}.step")
    for k,v in parts.items():
        cq.exporters.export(v, f"{OUT}/cad/part_{k}.stl")
    # size variants
    for idd in (18.9, 22.2):
        Q = dict(P); Q["ID"] = idd
        r,l,_,inf = build(Q)
        cq.exporters.export(r, f"{OUT}/cad/ring_shell_ID{idd}.stl", tolerance=0.02, angularTolerance=0.1)
    bb = ring.val().BoundingBox(); print("bbox", bb.xlen, bb.ylen, bb.zlen)
