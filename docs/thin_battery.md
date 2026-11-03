# Research: thinner LiPo cells for the ring (2026-11-01)

## Baseline: 020815
- 2.0 x 8 x 15 mm, **9 mAh (min) / 10 mAh (typ)**, bare cell about 0.4 g
- Datasheet: https://www.honcell.com/Public/Uploads/uploadfile/files/20241104/DATASHEETHCP2008153.7V9mAhCELL2024.pdf (verified 200). Note: thickness can reach 2.16 mm after cycling; the 15 mm length excludes tabs; top seal ~3 mm, tabs ~6 mm.
- Version with protection board: HHS Battery 020815 "T2.0*W08*H15mm with PCM", 10 mAh, DW01+8205 https://www.hhsbattery.cn/lithium-polymer-battery/9mah-30mah/309.html (timed out from overseas, unverified)
- JZFY version lists 2.0x8.0x**17** mm (including seal), MOQ 1000, $0.39–0.48 https://www.lipopolymerbattery.com/sale-14042025-iso14001-020815-3-7-v-li-polymer-battery-6mah-to-9mah.html

## Conclusion
**No public, specified off-the-shelf cell of ≤1.5 mm x ≤8 mm x ≤15 mm was found** (searches for 150815/120815/010815/1.5*8*15/1.2*8*15 gave nothing useful).
The ≤1.5 mm cells that exist are all longer or wider. By volume, 1.5x8x15 would be about 5–7 mAh and 1.0–1.2x8x15 about 3–5 mAh (**estimate, unverified**); ultra-thin cells also lose more to the seal and have worse energy density.
Taobao/LCSC: no specific listing could be verified (Taobao needs login; LCSC lists no LiPo in this size). Suggest searching Taobao for "ultra-thin polymer lithium battery 1.5mm", "ring battery curved", "151020", "150830", or asking a small factory for a custom cell (usually with an MOQ).

## Candidates (all manufacturer pages, not Taobao/LCSC; links curl-verified 200)
| Model | T x W x L (mm) | Capacity | PCM | Price | Source | Fits? |
|---|---|---|---|---|---|---|
| LP151020 | 1.5 x 10 x 20 | 12 min / 22 typ | bare cell none; PCM version 1.5x10x21 + 50 mm leads | not listed | https://polybattery.com/product/1-5mm-thin-12mah-lp151020-3-7-v-lithium-battery-slim-battery-pack ; https://www.lipobatteries.net/hot-selling-lipo-battery/small-rechargeable-lipo-batteries-lp151020-12mah/ | width 10 and length 20 too big |
| 150830 (curved, for rings/bands) | 1.5 x 8 x 30 | 15 | yes (added size not listed) | not listed | https://cestpower.com/product/lithium-battery/lipo-battery/3-7v-lipo-battery/150830-15mah/ | width OK, length 30 too long |
| 120732 curved ring cell (ASOL) | 1.25 x 7.1 x 31 | 17–19 | not listed | not listed | https://asolbattery.com/product/smart-ring-lithium-polymer-battery-cells/ | too long (from search snippet, page not checked word for word) |
| 120732 (LithoTop) | 1.25 x 6.9 x 25 | 13–15 | not listed | not listed | https://lithotop.com/wearable-devices/smart-ring-battery | too long (same caveat) |
| GRP150725 (Grepow ring) | 1.5 x 7 x 25 | 19 | not listed | not listed | https://www.grepow.com/wearables/smart-ring.html | too long (same caveat) |
| LP101414 | 1.0 x 14 x 14 | 15 | not listed | not listed | https://www.lithium-polymer-battery.net/8mah-200mah-3-7v-lithium-polymer-battery/ (returned 202) | width 14 too big |
| 081518 | 0.8 x 15 x 18 | 5 | none | on request | https://www.ufinebattery.com/special-battery/ | too big |
| 151530 | 1.5 x 15 x 30 | 20 | none | on request | same | too big |
| 012323 | 1.0 x 23 x 23 | 30 | none | on request | same | too big |

## Design suggestions
- To keep the 8x15 side-mounted cells: only a custom 1.5x8x15 works (~5–7 mAh each, estimate). Two give ~10–14 mAh, ~30% less than the current 2x020815 (18–20 mAh), and the face only gets 2x0.5 = 1 mm narrower.
- Curved ring cells (120732/150725 type) laid along the band give 13–19 mAh each and may suit better than two upright side cells.
- All-day runtime: a 0.66" OLED always on usually draws a few mA, so 10–20 mAh can hardly last a day; a screen-off / raise-to-show strategy is needed (not measured; measure the current).
- Protection board: a small DW01+8205 board typically adds ~2–4 mm of length at the tab end and is about as thick as the cell or ~1 mm (rule of thumb, **unverified**); consider putting protection on the main board and using bare cells.
