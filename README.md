<p align="center"><img src="promo/hero_banner.jpg" alt="Code Rain Ring" width="100%"></p>

<h1 align="center">Code Rain Ring</h1>
<p align="center">A metal ring with <b>Matrix-style code rain</b> falling across your fingertip: metal 3D-printed shell · 0.66" OLED · tap to wake · magnetic charging</p>
<p align="center"><a href="docs/parts.md">BOM / part dimensions</a> · <a href="#open-issues">Open issues</a></p>

---

## Why this project

Inspired by **Daniel Idle's Digital Rain Ring**, we wanted to build our own version: a size you can actually wear (M and L), a real metal feel, and green *Matrix*-style code rain on the screen that lights up with a light tap.

The design was built from scratch in parametric CAD (Python + CadQuery) over 10 iterations. The shell is made by a metal 3D printing service (Zhuguang Metal 3D Printing), the electronics come from **Taobao / LCSC**, and a friend in China assembles it by hand. This repository publishes everything (models, scripts, design notes, part drawings and renders) in the hope it helps anyone building a similar small wearable.

## Features

- **One-piece metal shell**: metal 3D printed, 0.5 mm minimum wall, solid 1.5 mm metal band
- **Ultra-thin head**: only about **4.15 mm** thick; two 020815 cells stand upright against the head top
- **Hidden flex cable**: a 0.5 mm metal cover strip (about 2.9 wide) on one side covers the FPC channel from the head to the charging socket; a 0.25 mm deep groove at the battery corner is filled flush with epoxy
- **Magnetic charging**: WIRE 4 mm round magnetic socket on a full-width inward charging pad at the bottom of the band (1.0 peak, 35° blends on each side, 0.4 fillets)
- **Tap to wake**: ATtiny1616 MCU + SC7A20 accelerometer
- **Two display colours**: clear cover glass = white code rain; green-printed cover glass = green code rain
- **Two sizes**: M (inner diameter 19.4) and L (inner diameter 21.0)

## Gallery

| | |
|---|---|
| ![](promo/closeup_screen.jpg) | ![](promo/on_hand.jpg) |
| ![](promo/charging_stand.jpg) | ![](promo/exploded_concept.jpg) |

![M and L](promo/M_L_pair_green_white.jpg)

> The promo images above are AI-assisted concept renders based on the CAD; the images below are direct CAD renders.

### CAD renders

| M | L |
|---|---|
| ![](renders/hq/M_iso_hq.png) | ![](renders/hq/L_iso_hq.png) |
| ![](renders/hq/M_exploded_hq.png) | ![](renders/hq/L_exploded_hq.png) |
| ![](renders/hq/M_top_hq.png) | ![](renders/hq/L_top_hq.png) |
| ![](renders/hq/M_side_hq.png) | ![](renders/hq/L_side_hq.png) |

![M vs L](renders/hq/ML_compare_hq.png)

### Engineering drawings

| | |
|---|---|
| ![](renders/side_M_final.png) | ![](renders/side_L_final.png) |
| ![](renders/v10_M_section.png) Section, M | ![](renders/v10_L_section.png) Section, L |
| ![](renders/v10_M_route.png) Cable route, M | ![](renders/v10_L_route.png) Cable route, L |
| ![](renders/v10_M_liner.png) Cover strip, M | ![](renders/v10_L_liner.png) Cover strip, L |

![](renders/topview_ML_final3.png)
![](renders/v10_M_pad.png)

## Specifications

All dimensions in mm.

| Parameter | M | L |
|---|---|---|
| Inner diameter | 19.4 | 21.0 |
| Head W × L × T | 22.4 × 17.5 × 4.15 | 24.0 × 18.8 × 4.15 |
| Display window | 16.8 × 12.2 | 18.2 × 13.3 |
| Cover glass | 17.25 × 12.8 × 0.4 | 18.8 × 13.9 × 0.4 (0.3 lip) |
| OLED | 0.66" standard (16.5 × 16.2) | 0.66" large (18.46 × 18.1 × 1.25) |
| Cover strip (flat) | 14.31 × 2.9 × 0.5 | 16.01 × 2.9 × 0.5 |
| Battery | 2 × 020815, upright | 2 × 020815, upright |
| Charging | Φ4 magnetic socket + inward charging pad | Same |
| Band | 1.5 solid metal | 1.5 solid metal |
| Minimum wall | 0.5 | 0.5 |

The full BOM, exact dimensions and redrawn vendor drawings are in **[docs/parts.md](docs/parts.md)**.

## Repository structure

```
hardware/M, hardware/L   Final v10 models: shell / cover strip / glass STEP+STL, part STLs, flat DXF, checks JSON
cad/                     Parametric scripts: ring_v10.py (M|L), render_v10.py, render_hq_vtk.py
renders/                 Engineering renders; renders/hq has high-resolution VTK renders
promo/                   Promo images (hero banner, etc.)
docs/                    parts.md (BOM), design_notes v1–v9, thin battery / BOM research
reference/crops          Key part dimensions redrawn as English drawings
archive/                 Earlier versions (v2–v9 scripts, models, BOMs, renders; old meshes >25 MB not included)
```

To rebuild: `pip install cadquery trimesh matplotlib ezdxf vtk`, then run `python cad/ring_v10.py M`, `python cad/render_v10.py M` and `python cad/render_hq_vtk.py`.

## Assembly

1. The FPC (≤ 0.2 thick) runs from the head cavity through the floor via hole (−Y side) and along the 2.2 × 0.18 channel in the inner band to the charging socket.
2. Bend the metal cover strip to the inner band radius and glue it into the 3.0 × 0.5 slot, flush with the inner surface.
3. Epoxy zone A: the 0.25 deep groove beside the battery corner. Lay the cable in it and fill flush with epoxy (there is no cover strip on this section).
4. Epoxy zone B: fill the gap between the charging socket and the end of the cover strip.
5. Stand the two cells upright against the head top; the glass sits on the 0.3 lip between the two cells.

<a id="open-issues"></a>
## Open issues

- **L OLED vs cavity clash**: the large OLED is 18.1 long (along the finger) but the cavity is only 17.8, so about 0.15 at each end overlaps the 0.5 end wall. **Proposal: lengthen the head by 0.3 mm along the finger.**
- **OLED / PCB insertion method TBD**: both the panel and the PCB are larger than the window. How they go in (from the top before the glass, tilted in, or through a slot in the end wall) is not decided yet.
- Part heights marked UNVERIFIED in the thin BOM must be confirmed against official drawings.
- Vendor drawings have limited accuracy; measure the magnetic socket and the large OLED when they arrive.

## Credits

- Inspiration: **Daniel Idle, Digital Rain Ring**. This project is an independent redesign and uses none of his files.
- Metal printing: Zhuguang Metal 3D Printing. Parts: Taobao and LCSC. Assembly: a friend in China.

## License

- Hardware design files (models, drawings, renders, docs): **CERN-OHL-S-2.0** (strongly reciprocal open hardware licence; modified versions must also be open)
- Code (`cad/*.py` and other scripts): **MIT**
- The drawings in `reference/crops` are redrawn from vendor data for reference only. See [LICENSE](LICENSE).
