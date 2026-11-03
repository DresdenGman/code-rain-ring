# Code Rain Ring: Design Notes v3 (one-piece metal body)

## 1. Key changes
- **Shell:** head and band merged into **one continuous shell** (SDF smooth-union, transition fillet ~R2.6, top edge fillet R0.5). No seams or screws on the top or sides.
- **Band:** flat 6.0×1.6 mm, edge R0.6, 8 mm opening at the bottom, metal spring adjusts US 9–13. ID 20.6.
- **Top:** near-square 18.6×18.0, corner R3.6, sides taper inward 17° going down.
  - Black glass lens 15.4×12.2×0.55, **flush with the top**.
  - Visible bezel: ~1.6 mm left/right, ~2.9 mm top/bottom.
- **Bottom lid:** removable, hidden on the inside of the ring (finger side), bottom follows the finger curve, 2 M1 screws. Not visible from top or sides.
- **USB-C:** on the rear slope (−X), not visible from front or sides.
- **Height:** **top 8.3 mm above the finger**, under the 8.5 mm target.
- **Internal stack** (top of lid z = 11.0):
  - battery 201212, z 11.0–13.0
  - PCB + mid-mount USB-C zone, z 13.1–16.75
  - OLED, z 16.75–18.05
  - lens, z 18.05–18.6
- **Volume and weight:** ~1.16 cm³. Estimated weight: 316L ~9 g, 925 silver ~12 g, titanium ~5 g, aluminium ~3 g.

## 2. Wake method: accelerometer tap
- **SC7A20HTR** (Silan), LCSC **C19274408**, LGA-12 2×2, USD 0.29, with single/double-tap interrupt.
- Alternative: **LIS2DH12TR** (ST), LCSC **C110926**.
- Wiring: INT1 to a CH32V003 EXTI pin to wake from standby; I2C shared with the OLED.
- Standby: ~2 µA in low-power mode (datasheet; depends on ODR, **not measured**).
- Benefit: no holes in the metal body; "double-tap to light for 10–15 s" is pure firmware.
- Risk: everyday motion may false-trigger. Tune threshold and time window; require double-tap if needed.

## 3. Battery life (estimate)
Same as v2: 10 mAh cell, 30 wakes/day ≈ 7–8 days; always-on ≈ 1.5–2.8 hours.

## 4. Manufacturing
- **925 silver lost-wax** (recommended first) or **316L MIM / investment casting**: CNC-finish the lens step (depth 0.55 ± 0.03), cavity and USB opening after casting, then sandblast.
- **Titanium / aluminium CNC:** freeform exterior needs 5-axis machining; cavity milled from the bottom.
- **Band spring:**
  - 925 silver is soft and fatigues with repeated opening. Thicken to 1.8 mm or use 316L / titanium.
  - A spring opening only adjusts a little. US 9–13 is a wide span (ID 18.9–22.2); **whether one size is comfortable is unverified**; S/L sizes may be needed.

## 5. Files
- **CAD source:** `cad/ring_v3_sdf.py` (SDF parametric), parameters in `cad/v3_params.json`
- **STL:** `cad/v3_unibody.stl`, `cad/v3_bottom_lid.stl`, `cad/v3_lens.stl`, sections `cad/v3_section_*.stl`, low-poly `*_lowpoly.stl`
- **STEP:** `cad/v3_unibody.step`, `cad/v3_bottom_lid.step`, `cad/v3_lens.step`
  - **Note:** these are triangulated STEP files stitched from the mesh (~149 MB), not NURBS surfaces. Fine for viewing, 3D printing and casting wax; if the factory needs editable surfaces, rebuild the form in Rhino/Fusion (next step).
- **Renders:** `cad/render_v3_blender.py` (Blender 4.2 Cycles), outputs:
  - `renders/v3_hero.png`, `renders/v3_side.png`, `renders/v3_top.png`, `renders/v3_back.png`, `renders/v3_section.png`, `renders/v3_exploded.png`
  - contact sheet: `renders/v3_contact.jpg`
- **BOM:** `BOM_v3.csv`

## 6. Open issues
1. STEP is a mesh STEP and must be rebuilt as a surface STEP.
2. The high-res STL is not strictly watertight in trimesh (marching-cubes artefacts); repair before printing (Blender 3D-Print toolbox or Netfabb).
3. No assembly clearance between lid and body yet; add 0.05–0.1 mm before tooling. M1 screw bosses not modelled.
4. Check the USB-C opening against the PCB after layout.
5. False-trigger rate of accelerometer tap needs prototype validation.
