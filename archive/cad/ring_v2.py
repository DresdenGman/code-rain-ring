"""Code Rain ring v2 - smooth tapered metal head on a flat adjustable 304/316L stainless open band.
Form: soft-rounded-rect top 20x18 (R4), flush lens, sides taper inward 20deg from vertical (no vertical wall),
continuous taper continues through the adapter lid down onto the band (shoulder), lid underside saddles the band.
Axes: X finger axis, Y across, Z up. Finger centre at origin. mm."""
import cadquery as cq, math, os
OUT = os.path.join(os.path.dirname(__file__), "..")
P = dict(
  ring_id=20.6, band_w=6.0, band_t=1.6, band_gap=8.0,      # flat band (open, adjustable)
  top_x=20.0, top_y=19.5, top_r=4.0, taper=15.0, top_fillet=0.5,
  lens_t=0.55, lens_x=14.6, lens_y=10.6, lens_r=1.6,       # flush glass, bezel ~2.5-3.5mm
  win_x=10.6, win_y=6.6,
  oled_x=12.3, oled_y=11.3, oled_t=1.30,
  zone_t=3.2,                                              # PCB 0.6 + mid-mount USB-C 3.16 zone
  bat_x=12.2, bat_y=12.2, bat_t=2.1,                       # GEB201212 10mAh 2.0x12x12
  lid_t=0.6, shoulder=2.2,                                 # lid plate + tapered skirt down to band
  screw_x=6.7, screw_pilot=0.8, screw_clear=1.1, screw_head=1.9,   # 2x M1.0 x 2.5 self-tap (proto)
  usb_w=9.2, usb_h=3.4,
)
def rrect(x, y, r, z):
    return cq.Workplane("XY").workplane(offset=z).rect(x, y).val()
def _rw(x, y, r, z):
    sk = cq.Sketch().rect(x, y).vertices().fillet(r)
    return sk._faces.Faces()[0].outerWire().translate(cq.Vector(0,0,z))
def frustum(x0, y0, r0, z0, h, taper):
    """bottom smaller (inverted), top = x0,y0,r0 at z0+h"""
    d = h*math.tan(math.radians(taper))
    return cq.Workplane("XY").add(cq.Solid.makeLoft([_rw(x0-2*d, y0-2*d, max(r0-d,0.5), z0), _rw(x0, y0, r0, z0+h)], True))
def build(P):
    r = P["ring_id"]/2; ro = r + P["band_t"]
    tn = math.tan(math.radians(P["taper"]))
    Hh = P["lens_t"] + P["oled_t"] + 0.1 + P["zone_t"] + P["bat_t"]       # head shell height
    zb = ro + P["lid_t"] + 0.0           # head bottom (lid top) ; lid plate bottom touches band top
    zt = zb + Hh
    head = frustum(P["top_x"], P["top_y"], P["top_r"], zb, Hh, P["taper"])
    try: head = head.faces(">Z").edges().fillet(P["top_fillet"])
    except Exception as e: print("top fillet skipped", e)
    # flush lens pocket + window
    lens = (cq.Workplane("XY").sketch().rect(P["lens_x"],P["lens_y"]).vertices().fillet(P["lens_r"]).finalize()
            .extrude(P["lens_t"]).translate((0,0,zt-P["lens_t"])))
    head = head.cut(lens)
    z = zt-P["lens_t"]
    head = head.cut(cq.Workplane("XY").rect(P["oled_x"],P["oled_y"]).extrude(P["oled_t"]+0.1).translate((0,0,z-P["oled_t"]-0.1)))
    z -= P["oled_t"]+0.1
    # internal cavity follows the taper (wall ~1.0mm normal)
    wall = 1.0/math.cos(math.radians(P["taper"]))
    cav = frustum(P["top_x"]-2*wall, P["top_y"]-2*wall, max(P["top_r"]-wall,0.8), zb-0.01, z-zb+0.01+0.0, P["taper"])
    # cavity top is at z with width = outer at z minus walls -> recompute by scaling: simpler intersect box
    cav = cav.intersect(cq.Workplane("XY").box(40,40,z-zb+0.02).translate((0,0,(z+zb)/2)))
    head = head.cut(cav)
    # FPC fold slot at +X
    head = head.cut(cq.Workplane("XY").center(P["oled_x"]/2+0.3,0).rect(1.2,9).extrude(P["oled_t"]+0.6).translate((0,0,z-0.5)))
    # USB-C on the BACK sloped face (-X, faces the hand) at PCB level
    z_pcb_top = z - 0.05 - 1.6 + 1.6 - 0.0 - 1.56   # USB top just under OLED: pcb_top = z-1.56-0.05
    z_pcb_top = z - 1.61
    usb = (cq.Workplane("YZ").center(0, z_pcb_top).rect(P["usb_w"],P["usb_h"]).extrude(6.5).edges("|X").fillet(1.3)
           .translate((-P["top_x"]/2-2,0,0)))
    head = head.cut(usb)
    # screw pilots in thick lower corners of the end walls
    for sx in (-1,1):
        head = head.cut(cq.Workplane("XY").center(sx*P["screw_x"],0).circle(P["screw_pilot"]/2).extrude(1.8).translate((0,0,zb-0.01)))
    # bosses: add material back around pilots inside cavity
    for sx in (-1,1):
        boss = cq.Workplane("XY").center(sx*(P["screw_x"]+0.5),0).rect(2.0,2.6).extrude(1.9).translate((0,0,zb))
        boss = boss.intersect(frustum(P["top_x"], P["top_y"], P["top_r"], zb, Hh, P["taper"]))
        boss = boss.cut(cq.Workplane("XY").center(sx*P["screw_x"],0).circle(P["screw_pilot"]/2).extrude(3).translate((0,0,zb-0.01)))
        head = head.union(boss)
    # tap zone: hidden copper electrode behind +Y wall; tiny engraved dot marks it
    head = head.cut(cq.Workplane("XY").sphere(0.35).translate((0, P["top_y"]/2-(zt-zb-1.2)*tn-0.0, zt-1.2)))
    # ---- lid / shoulder: continues the head taper down onto the band, saddle underside ----
    hb_x = P["top_x"]-2*Hh*tn; hb_y = P["top_y"]-2*Hh*tn; hb_r = max(P["top_r"]-Hh*tn,0.8)
    hs = P["lid_t"] + P["shoulder"]
    lid = frustum(hb_x, hb_y, hb_r, zb-hs, hs, P["taper"])
    lid = lid.cut(cq.Workplane("YZ").circle(ro).extrude(40).translate((-20,0,0)))       # saddle onto band OD
    # but keep a band channel so the band seats 0.4 deep and is captured sideways
    lid = lid.cut(cq.Workplane("YZ").circle(ro+0.4).extrude(P["band_w"]+0.2).translate((-(P["band_w"]+0.2)/2,0,0)))
    lid = lid.cut(cq.Workplane("YZ").circle(r).extrude(40).translate((-20,0,0)))
    lid = lid.cut(cq.Workplane("XY").rect(4,0.8).extrude(0.4).translate((0,-3,zb-0.4)))  # wire relief
    for sx in (-1,1):
        lid = lid.cut(cq.Workplane("XY").center(sx*P["screw_x"],0).circle(P["screw_clear"]/2).extrude(10).translate((0,0,zb-8)))
        lid = lid.cut(cq.Workplane("XY").center(sx*P["screw_x"],0).circle(P["screw_head"]/2).extrude(8).translate((0,0,zb-P["lid_t"]-8+0.0)))
    # metal band reference (flat rectangular section, open at bottom)
    band = cq.Workplane("YZ").circle(ro).circle(r).extrude(P["band_w"]).translate((-P["band_w"]/2,0,0))
    band = band.cut(cq.Workplane("XY").box(10, P["band_gap"], 5).translate((0,0,-r)))
    try: band = band.edges().fillet(0.5)
    except Exception: pass
    zo = zt-P["lens_t"]
    parts = {
     "lens": lens,
     "oled": cq.Workplane("XY").box(12,11,1.227).translate((0,0,zo-0.65)),
     "pcb": cq.Workplane("XY").box(12.8,10.8,0.6).translate((0,0,z_pcb_top-0.3)),
     "usbc": cq.Workplane("XY").box(6.8,8.94,3.16).translate((-P["top_x"]/2+Hh*tn*0.55+3.4+0.6,0,z_pcb_top-0.02)),
     "battery": cq.Workplane("XY").box(P["bat_x"]-0.2,P["bat_y"]-0.2,2.0).translate((0,0,zb+1.05)),
    }
    info = dict(finger_top=r, band_top=ro, head_bottom=round(zb,2), top=round(zt,2), head_height=round(Hh,2),
                top_above_finger=round(zt-r,2), head_bottom_size=(round(hb_x,2),round(hb_y,2)), pcb_top=round(z_pcb_top,2))
    return head, lid, band, parts, info
if __name__ == "__main__":
    head, lid, band, parts, info = build(P); print(info)
    for n,o in [("v2_head",head),("v2_lid_shoulder",lid),("v2_metal_band_REFERENCE",band)]:
        cq.exporters.export(o, f"{OUT}/cad/{n}.stl", tolerance=0.01, angularTolerance=0.1)
        cq.exporters.export(o, f"{OUT}/cad/{n}.step")
        bb=o.val().BoundingBox(); print(n, o.val().isValid(), round(bb.xlen,2),round(bb.ylen,2),round(bb.zlen,2))
    for k,v in parts.items(): cq.exporters.export(v, f"{OUT}/cad/v2_part_{k}.stl")
    # interference check
    import itertools
    for k,v in parts.items():
        if k=="lens": continue
        for n,o in [("head",head),("lid",lid)]:
            vol = o.intersect(v).val().Volume() if o.intersect(v).vals() else 0
            if vol>0.05: print("INTERFERENCE", k, n, round(vol,2))
