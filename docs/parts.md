# Parts, BOM and Dimensions

> All dimensions in mm. **The CAD script (`cad/ring_v10.py`) and `hardware/*/v10_*_checks.json` in this repo are the source of truth.** Marketplace seller drawings are reference only: many were phone screenshots with inaccurate scale and loose tolerances. See "Issues with seller data" for each item.

## 1. BOM (current prototype plan)

| # | Part | Spec / model | Qty | Source | Notes |
|---|---|---|---|---|---|
| 1 | Metal shell (one piece) | v10 shell, M or L (`hardware/M|L/v10_*_shell.step`) | 1 | Metal 3D printing service | Minimum metal wall 0.5 |
| 2 | Metal cover strip | 0.5 thick, 2.9 wide; M 14.31×2.9, L 16.01×2.9 (flat pattern, see `*_strip_flat.dxf`) | 1 | Same / cut steel shim | Bend to the bore radius, glue into the 3.0×0.5 groove |
| 3 | Cover glass | 0.4 thick; M 17.25×12.8; L 18.8×13.9 (sits on a 0.3 step) | 1 | Custom (Taobao) | Clear = white display; green printed layer = green display (see `*_glass_outline.dxf`) |
| 4 | OLED panel | M: standard 0.66" 64×48 (16.5×16.2); L: large 0.66" 18.46 (Y) × 18.1 (X) × 1.25 | 1 | Taobao | See reference/crops |
| 5 | MCU | ATtiny1616-MNR (VQFN-20 3×3) | 1 | LCSC C507118 | Thin alternative CH32V003F4U6 (C5299908) |
| 6 | Accelerometer (tap to wake) | SC7A20HTR (LGA-12 2×2) | 1 | LCSC C19274408 | Thin alternative LIS2DW12TR (C189624) |
| 7 | Charger IC | TP4054 / thin BQ24040DSQR (C81080) | 1 | LCSC | |
| 8 | Protection / LDO | AP6683 (C2849565); TPS7A0530PDQNR (C2871471) | 1 each | LCSC | |
| 9 | Battery | 020815 LiPo (2×8×15), two cells standing upright against the head top | 2 | Taobao | Spec per model number 020815 = 2×8×15 |
| 10 | Magnetic charging socket | WIRE 4 mm round magnetic receptacle Φ4×2 | 1 | Pinduoduo / WIRE magnetic | At the bottom of the inner bore |
| 11 | FPC cable | ≤0.2 thick, ≤2.2 wide | 1 | Custom | Head → charging socket |
| 12 | PCB | 0.4 thick FR4 / flex, component layer ≤0.85 | 1 | JLCPCB | |
| 13 | Epoxy | Clear / metal-tone 2-part epoxy | — | | Fills the 0.25-deep groove and the seam beside the socket |

Thin part comparison: [thin_bom.md](thin_bom.md). Battery options: [thin_battery.md](thin_battery.md).

## 2. Exact dimensions used (v10)

| Item | M | L |
|---|---|---|
| Inner diameter (ID) | 19.4 | 21.0 |
| Outer radius / band | 11.2 / 1.5 solid metal | 12.0 / 1.5 solid metal |
| Head W×L×T | 22.4×17.5×4.15 | 24.0×18.8×4.15 |
| Window | 16.8×12.2 | 18.2×13.3 (bezel 2.9 left/right, 2.75 top/bottom) |
| Glass | 17.25×12.8×0.4 | 18.8×13.9×0.4, 0.3 step |
| OLED | standard 0.66" 16.5×16.2 | large 0.66" 18.46×18.1×1.25 |
| Z stack (M, from bottom of bore) | parts 10.70–11.55, PCB 11.55–11.95, OLED 11.95–13.40, adhesive 0.05, glass 13.45–13.85, top 14.35 | same structure |
| Battery | 2× 020815 upright (2×8×15) against the head top | same |
| Cover strip (flat) | 14.31×2.9×0.5, 35.3°–117.7° | 16.01×2.9×0.5, 35.3°–120.6° |
| Epoxy zone A (0.25-deep groove at battery corner) | 118°–135° | 120.9°–133.4° |
| Epoxy zone B (beside socket) | 11.6°–35° | 10.7°–35° |
| Cable pass-through (head floor) | y=−7.5 | y=−8.3 |
| Charging pad | full-width inner bump, 1.0 peak, 35° transition each side, 0.4 fillet | same |
| Charging socket | Φ4×2, bottom of bore | same |

Angles are measured from the bottom (−Z) toward −Y. Minimum walls (from the checks JSON): battery corner to bore M 0.78 / L 1.10; battery to cable slot 0.53 / 0.85; socket back wall 0.50 / 0.50.

## 3. Seller drawings, redrawn (reference/crops)

The original seller screenshots were not in English, so the key dimensions were redrawn as clean English drawings with the same numbers.

| Drawing | Content | Issues with seller data |
|---|---|---|
| ![](../reference/crops/oled066_std_16.42_structure.png) `oled066_std_16.42_structure.png` | 0.66" 64×48 OLED outline (panel 16.42±0.2 × 16.2±0.2, AA 13.42×9.46 per this vendor) | Source was a low-res phone screenshot; panel tolerance ±0.2; FPC length after bending not given. We model 16.5×16.2 (upper bound). |
| ![](../reference/crops/oled066_16.5_structure.png) `oled066_16.5_structure.png` | Second vendor's 0.66" outline (panel 16.5±0.2, cap 16.5±0.2, polarizer 15.9±0.3, thickness 1.23±0.1, AA 13.42×10.06) | The two vendors disagree (16.42 vs 16.5); 1.23 thickness excludes adhesive. The large 18.46×18.1 panel used for L has no full drawing; data came from the seller verbally. |
| ![](../reference/crops/magnet_4mm_socket_dims.png) `magnet_4mm_socket_dims.png` | 4 mm magnetic receptacle (Φ4 outer diameter) | Height and pad sizes were unclear; we model Φ4×2 with a 0.5 back wall. **Measure on delivery.** |
