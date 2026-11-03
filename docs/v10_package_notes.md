# CodeRain ring — v10 final package (M + L)
Generated 2026-11-01 (PT). Units are mm. Coordinates: X runs along the finger, Y across the face, Z up.

## Folder
- M/, L/: shell, strip and glass as STEP + STL; part STLs (OLED, PCB, bat_L/R, socket); strip_flat DXF/PNG; glass_outline DXF/PNG; checks JSON (walls, interference)
- renders/: v10_M_* and v10_L_* (iso, top, section, exploded, liner, route, pad) plus side_M_final, side_L_final, topview_ML_final3
- cad/: ring_v10.py (parameterized, `python ring_v10.py M|L`), render_v10.py (`M|L`), and ring_v10_M.py / render_v10_M.py (the original approved M scripts). Needs cadquery, trimesh, matplotlib, ezdxf.
- docs/: design notes v1–v9, thin_battery.md, thin_bom.md, bigger_screen_options.md (historical context; v10 supersedes them)
- ref/: battery photos (a, c1, c2), 0.66" OLED drawings, Φ4 magnet drawing, section sketch

## Final spec
| | M | L |
|---|---|---|
| ID (bore) | 19.4 | 21.0 |
| Head (W×L×H) | 22.4×17.5×4.15 | 24.0×18.8×4.15 |
| Outer R / band | 11.2 / 1.5 solid | 12.0 / 1.5 solid |
| Window | 16.8×12.2 | 18.2×13.3 (border 2.9 L/R, 2.75 T/B), 0.3 lip |
| Cover glass | 17.25×12.8×0.4 | 18.8×13.9×0.4 (0.10 per side to the batteries) |
| OLED | 0.66" std (16.5×16.2) | large 0.66" 18.46(Y)×18.1(X)×1.25 |
| Batteries | 2× 020815 upright (2×8×15), touching head top | same |
| Charging pad | full-width cos² bump, 1.0 peak, ±35°, 0.4 bore-edge fillets | same |
| Socket | Φ4×2 at the bore bottom | same |
| Cover strip (flat) | 14.31×2.9×0.5, 35.3–117.7° | 16.01×2.9×0.5, 35.3–120.6° |
| Epoxy zone A (0.25-deep groove) | 118–135° | 120.9–133.4° |
| Epoxy zone B (slot beside socket) | 11.6–35° | 10.7–35° |
| Flex slot in head floor | y=−7.5 | y=−8.3 |
Angles are measured from the bottom (−Z) toward −Y.

## Minimum walls (from checks JSON)
| Wall | M | L |
|---|---|---|
| Battery corner to bore | 0.78 | 1.10 |
| Battery to flex channel / epoxy groove | 0.53 | 0.85 |
| Battery to strip recess | 0.99 | 1.01 |
| Battery to flex slot | 0.70 | 0.70 |
| Socket back wall | 0.50 | 0.50 |
| Band behind flex groove | 0.82 | 0.82 |

## Parts BOM (from docs/thin_bom.md)
## Recommended thin BOM
CH32V003F4U6 + LIS2DW12TR + BQ24040DSQR + AP6683 + TPS7A0530PDQNR + 0201/0402 passives.
Tallest part: CH32V003 at ~0.75 mm, or BQ24040 at 0.80 mm max. With ~0.03–0.05 mm of solder, the component layer is **≈0.80–0.85 mm**. That is right at the limit, so confirm the QFN and WSON drawings before layout. Without the CH32V003 and BQ24040 the tallest part is 0.70 mm (accel), which gives ≈0.75 mm.
Firmware impact: moving from ATtiny (AVR) to CH32V003 (RISC-V) means porting the code, and you need a WCH-LinkE programmer (1-wire SWIO).

Mechanical parts: unibody metal shell; cover strip, 0.5 metal or stiff sheet (cut from strip_flat DXF and form to the bore radius); cover glass 0.4 (cut from glass_outline DXF); 0.66" OLED (M std / L large); PCB; 2× 020815 LiPo; Φ4×2 magnet/pogo charging socket.

## Assembly notes
1. The flex must be ≤0.2 thick. It runs from the head cavity through the floor slot (−Y side) and down the 2.2×0.18 groove in the bore to the socket.
2. Glue the cover strip into the 3.0×0.5 recess over the groove so it sits flush with the bore.
3. Epoxy zone A: the 0.25-deep groove next to the battery corner. Fill flush with epoxy over the flex; there is no strip there.
4. Epoxy zone B: the open slot between the socket edge and the end of the strip. Fill flush.
5. Glass: M 17.25×12.8×0.4, L 18.8×13.9×0.4. It sits in a pocket on the 0.3 lip, between the batteries.

## Open issues
- **The OLED panel and PCB are larger than the window,** and on L also larger than the cavity length. The cavity is 17.8 along X, but the large OLED is 18.1 along X: 0.15 per end overlaps the 0.5 end walls (checks: oled_vs_shell > 0). Its 18.46 width leaves 0.27 per side to the batteries. How the module goes in (from the top before the glass, tilted, or a thinner end wall/notch) is **TBD**.
- Thin-BOM part heights marked UNVERIFIED in thin_bom.md need confirming against the drawings.
