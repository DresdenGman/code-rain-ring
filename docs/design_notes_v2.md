# Code Rain Ring: Design Notes v2 (one-piece metal look / production-oriented)

> Labels: **[measured/sourced]** from a datasheet or product page; **[est]** estimate; **[assumption]** unverified.

## 1. Reference and differentiation
- Read https://danielidle.com/#digitalrainring. The public page has only a blurb ("Mini OLED display signet ring, playing 'Digital Rain'. Sterling Silver plated. [2026]") and links to Designboom / Yanko Design coverage. **There are no downloadable files (no STL, schematic or assembly guide)**, so the only takeaways are: (1) silver plated, which suggests a printed or resin/brass part plated in silver rather than solid silver; (2) the signet-ring form language.
- Our differences: near-square soft-rounded top 20×19.5 R4 (not hard square corners), 15° reverse taper (reference ~30–35°), flat open metal band, flush lens, hidden USB-C on the rear slope, hidden screws underneath. The look is not copied.

## 2. Band choice and attachment
- **Prototype:** Everful 316L polished open blank band, 5 mm wide, USD 1.94 (link in BOM); sandblast to matte ourselves.
- **Production:** HonHo, Dongguan (Gold Supplier) makes custom 304/316L ring blanks (width 3–8 mm, thickness 1.5/2.0/2.5 mm). Order spec: **6.0×1.6 mm flat band, ID about 20.6, opening about 8 mm**, hand-adjustable across US 9–13.
  - Note: stock adjustable bands are only listed up to US 12; US 13 relies on the opening and spring-back and is **unverified**.
- **Attachment:** the "shoulder lid" under the head (v2_lid_shoulder) has a saddle surface matching the band OD, with a 6.2×0.4 mm locating groove.
  - Prototype: snap the band into the groove and bond with structural adhesive (3M DP460); the lid fixes to the head with 2 hidden M1.0 screws from below.
  - **Production suggestion:** **laser-weld or cast the lid and band as one piece**, drop the glue, and add an R1.5–2 fillet at the shoulder. In CAD they are still separate parts without the large fillet.

## 3. Stack and height (top to bottom)
| Layer | Thickness mm |
|---|---|
| Flush lens | 0.55 |
| OLED 0.42" | 1.3 |
| PCB 0.6 + mid-mount USB-C zone | 3.2 |
| Battery GEB201212 (2.0 thick) | 2.1 (with clearance) |
| Lid/shoulder | 0.6, sitting on the 1.6 band |

- Head height 7.25 mm. **Top surface 9.45 mm above the finger** (reference ~8–10 mm).
- Top 20×19.5, bottom 16.1×15.6, wall about 1 mm.
- CAD interference check: only a 0.06 mm³ edge contact between USB-C and the shell; negligible, fix when laying out the board.
- Options to lower further:
  - Swap USB-C for a side-mount or sunk-board type, or use 4-pin magnetic pogo charging, saving about 1–1.5 mm.
  - USB-C is an explicit requirement, so it stays for now.

## 4. Battery life (10 mAh, about 8.5 mAh usable) [est]
- **Active:** OLED 72×40 with ~20–30% of pixels lit by code rain, plus MCU, about 3–5.5 mA.
- **Standby:** MCU standby ~10 µA, TTP223 ~1.5 µA, LDO ~1 µA, OLED sleep ≤10 µA; total ~20 µA.
- **Tap to wake:** 30×/day × 12 s ≈ 0.55 mAh; standby ≈ 0.48 mAh; total ≈ 1.0 mAh/day, **about 7–8 days**. Beats the "1 day" requirement.
- **Always on:** 8.5 / (3–5.5) ≈ **1.5–2.8 hours**. "A few hours always on" only just reaches the low end.
  - If 3+ hours always-on is required: switch to a 301012 30 mAh cell (height +1 mm, top ~10.4 mm above the finger), or drop brightness/contrast to minimum (~2–3 mA).
- **Charging:** TP4054 with RPROG ≈ 100 kΩ, ~10 mA (1C), full in ~1–1.5 h.

## 5. Wake method (the key issue with a metal shell)
- An all-metal shell shields and disturbs capacitive touch, and the band always touches the finger, so **the whole shell cannot be used as the electrode**.
- Options:
  - (a) Make the TTP223 electrode an ITO/FPC ring electrode under the lens and touch through the glass; or a small metal dot insulated from the shell (ceramic/adhesive insulation).
  - (b) **Recommended to evaluate:** tap-to-wake with a 3-axis accelerometer such as LIS2DH12 / SC7A20 (in stock at LCSC, part number TBD). Standby ~2–6 µA, no holes in the shell, best fits the "no visible seams" requirement.
- **Undecided.**

## 6. Sourcing and assembly in China
- **LCSC:**
  - CH32V003F4U6 **C5299908** ($0.31)
  - TTP223-BA6 **C2757936** (old number C80757)
  - TP4054 **C382138**
  - XC6206P332MR-G **C5446**
  - USB-C 6P **C7507406**
- **Taobao:** 0.42" 72×40 bare OLED, 201212 LiPo, M1 screws, ESP32-C3 0.42" OLED dev board (to validate the effect first).
- **PCB:** JLCPCB 0.6 mm 2-layer + SMT assembly. CH32V003 is flashed over single-wire with WCH-LinkE; leave an SWIO test point.
- **Assembly steps for a friend:**
  1. Print a black border on the back of the lens and glue the lens into the head.
  2. Stick the OLED under the lens with double-sided tape.
  3. Solder the FPC to the PCB (or use a 0.5 mm hot-bar FPC).
  4. Insert the PCB with the USB-C aligned to the rear-slope opening.
  5. Stick the battery to the back of the PCB and solder the leads (the cell needs a protection board, or add a protection IC on the PCB).
  6. Fit lid + band and drive the 2 M1 screws.
- **Compliance:** no wireless, so in the US it is an FCC Part 15B unintentional radiator; SDoC testing is still required. Battery transport needs UN38.3.

## 7. Metalworking notes (for the factory)
- **CNC 6061/7075 aluminium:** cheapest and lightest (finished ~3–4 g [est]). Sandblast + clear/silver anodise. Tolerance ±0.02–0.05; inner cavity corner radius ≥0.5 (Φ1 tool). Good for 5–50 prototypes. Plenty of CNC shops in Chang'an (Dongguan) and Bao'an (Shenzhen).
- **CNC titanium TC4:** best feel, light, hypoallergenic. Slow to machine, unit price ~3–5× aluminium [est]; sandblast or brush.
- **316L stainless steel:**
  - Investment (lost-wax) casting or MIM; MIM suits 1k+ pcs, tooling about CNY 10–30k [est].
  - Post-processing: CNC finish the lens step and threads, then sandblast / PVD.
- **925 silver lost-wax casting:** jewellery shops in Panyu or Shuibei (Shenzhen): 3D-printed wax → cast → clean-up → sandblast.
  - The lens step and OLED cavity need post-cast CNC finishing.
  - Silver is soft and M1 threads are unreliable; use embedded steel nuts or adhesive.
  - Silver tarnishes; rhodium-plate or lacquer it.
- **General requirements:**
  - Wall ≥0.8 (cast ≥1.0).
  - Top edge fillet 0.5, shoulder transition R1.5–2.
  - Lens step depth 0.55±0.03 so the lens sits flush.
  - 0.2 chamfer on the USB opening edge.
  - Sandblast 120–180 grit for a matte silver finish.
  - The metal shell must be grounded or ESD-protected (USB shield pins to GND).

## 8. Files
- **CAD:** `cad/ring_v2.py` (parametric), `cad/render_v2.py`
- **STL/STEP:** `cad/v2_head.*`, `cad/v2_lid_shoulder.*`, `cad/v2_metal_band_REFERENCE.*` (band for rendering only), `cad/v2_part_*.stl`
- **Renders:** `renders/v2_iso_front.png`, `v2_exploded.png`, `v2_section_x0.png`, `v2_section_y0.png`, `v2_side.png`, `v2_back_usb.png`, `v2_top.png`
- **BOM:** `BOM_v2.csv`

## 9. Open issues
1. The large shoulder-to-band fillet is not modelled yet (separate parts + groove). Renders still look like "a box sitting on a ring"; the next version needs to be one piece.
2. Wake method under a metal shell: touch or accelerometer.
3. Actual size of the 201212 cell and whether it has a protection board need samples.
4. US 13 coverage is unverified.
5. There is no green 0.42" OLED; only a white panel + green lens, or a blue panel.
6. Whether similar products already exist on Chinese platforms (Taobao/Xianyu/Xiaohongshu): not logged in, **unconfirmed**.
7. M1 screws in a 1 mm wall are weak.
