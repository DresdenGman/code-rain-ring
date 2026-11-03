# Code Rain Ring v4: Design Notes (U-shape, straight walls)

## Changes (responding to v3 feedback)
- **No tapers at all:** viewed along the finger, the outline is a U (flat top, two vertical parallel sides, an arc below wrapping the finger), matching the sketch. Front, back and side profiles are straight lines; the band is the same width top to bottom, **17 mm**.
- **Wider, thicker band:** 17 mm wide, 2.0 mm at the thinnest. The straight upper walls blend tangentially into the arc below; R0.6 soft chamfer on the bore edge.
- **Thinner:** screen top **5.5 mm** above the finger (v3: 8.3 mm). Overall width 24.6 mm, height 28.1 mm (size M).
- Finish: matte sandblast, flush lens, top edge R1.0 / edges R0.7.

## Stack (centre, from finger upward, mm)
Lid 0.6 → PCB 0.6 + parts ≤0.8 → OLED 1.2 → lens 0.4 = 5.5
- What actually limits height is the **USB-C receptacle** (sunk-board 3.16 mm): it sits at the rear of the PCB, opening toward the back (−X end face).
- With magnetic pogo charging instead it could drop to about **4.5 mm** (estimate).
- Batteries: two 2×8×15 mm cells (9 mAh) standing in the left and right "shoulders", the cavities on either side of the finger, using the extra space of the U shape.

## Battery life (estimate)
- 2×9 = 18 mAh; tap-to-wake ~1 mAh/day, about 2 weeks.
- Always-on about 3–5 h.
- Two cells in parallel need matching from the same batch; or use only one for about 1 week.

## Sizes
A 17 mm closed band is not suited to an adjustable opening (the gap would be obvious and spring is insufficient), so make **S / M / L sizes**:

| Size | ID | US size |
|---|---|---|
| S | 19.4 mm | US 9.5 |
| M | 20.6 mm | US 11 |
| L | 21.8 mm | US 12.5 |

- Only the exterior scales with ID; the internal cavity is shared.
- Alternative: a 0.5–1 mm silicone sizing insert inside to cover half a size.

## Risks / TBD
- **Weight:** volume ~2.49 cm³. 925 silver ~26 g, 316L ~20 g, titanium ~11 g (estimates); on the heavy side. The shoulders can be hollowed to save weight.
- **Comfort:** 17 mm width will press on neighbouring fingers and the knuckle bend; 3D-print test rings and try them on before production.
- The lid currently has no screws (v3 had M1 screws): either glue + snap fit, or add two M1 screws.
- STL is not strictly watertight; the STEP is a triangulated conversion from the mesh. Rebuild a parametric model before CNC programming.
