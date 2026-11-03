# 戒指用更薄锂电池调研 (2026-11-01)

## 基准：020815
- 2.0 x 8 x 15 mm，**9 mAh（最小）/ 10 mAh（典型）**，裸电芯约 0.4 g
- 规格书: https://www.honcell.com/Public/Uploads/uploadfile/files/20241104/DATASHEETHCP2008153.7V9mAhCELL2024.pdf （已验证 200）。注意：循环后厚度最大可到 2.16 mm；长度 15 不含极耳，顶封约 3 mm、极耳约 6 mm。
- 带保护板版本：鸿昊升 020815 "T2.0*W08*H15mm with PCM"，10 mAh，DW01+8205 https://www.hhsbattery.cn/lithium-polymer-battery/9mah-30mah/309.html （海外访问超时，未验证）
- JZFY 版标 2.0x8.0x**17** mm（含封边），MOQ 1000，$0.39–0.48 https://www.lipopolymerbattery.com/sale-14042025-iso14001-020815-3-7-v-li-polymer-battery-6mah-to-9mah.html

## 结论
**没有找到任何公开、有规格的 ≤1.5 mm x ≤8 mm x ≤15 mm 现货电芯**（搜索 150815/120815/010815/1.5*8*15/1.2*8*15 均无有效结果）。
能找到的 ≤1.5 mm 电芯都更长或更宽。按体积估算，1.5x8x15 约 5–7 mAh，1.0–1.2x8x15 约 3–5 mAh（**估算，未验证**），且超薄电芯封边占比更大、能量密度更差。
淘宝/立创：没能直接验证具体商品页（淘宝需登录、立创未见此尺寸 LiPo）。建议朋友在淘宝搜 "超薄聚合物锂电池 1.5mm" "戒指电池 弧形" "151020" "150830"，或找小厂定制（定制一般有 MOQ）。

## 候选（均为厂家页，非淘宝/立创；链接已 curl 验证 200）
| 型号 | T x W x L (mm) | 容量 | PCM | 价格 | 来源 | 是否符合 |
|---|---|---|---|---|---|---|
| LP151020 | 1.5 x 10 x 20 | 12 min / 22 typ | 裸芯无；带保护板版本 1.5x10x21 + 50mm 线 | 未标 | https://polybattery.com/product/1-5mm-thin-12mah-lp151020-3-7-v-lithium-battery-slim-battery-pack ; https://www.lipobatteries.net/hot-selling-lipo-battery/small-rechargeable-lipo-batteries-lp151020-12mah/ | 宽10、长20 超标 |
| 150830（弧形，戒指/手环用） | 1.5 x 8 x 30 | 15 | 有（尺寸增量未标） | 未标 | https://cestpower.com/product/lithium-battery/lipo-battery/3-7v-lipo-battery/150830-15mah/ | 宽OK，长30 超标 |
| 120732 戒指弧形 (ASOL) | 1.25 x 7.1 x 31 | 17–19 | 未标 | 未标 | https://asolbattery.com/product/smart-ring-lithium-polymer-battery-cells/ | 长超标（搜索摘要，未逐字核对页面） |
| 120732 (LithoTop) | 1.25 x 6.9 x 25 | 13–15 | 未标 | 未标 | https://lithotop.com/wearable-devices/smart-ring-battery | 长超标（同上，未逐字核对） |
| GRP150725 (Grepow 戒指) | 1.5 x 7 x 25 | 19 | 未标 | 未标 | https://www.grepow.com/wearables/smart-ring.html | 长超标（同上） |
| LP101414 | 1.0 x 14 x 14 | 15 | 未标 | 未标 | https://www.lithium-polymer-battery.net/8mah-200mah-3-7v-lithium-polymer-battery/ (返回202) | 宽14 超标 |
| 081518 | 0.8 x 15 x 18 | 5 | 无 | 询价 | https://www.ufinebattery.com/special-battery/ | 超标 |
| 151530 | 1.5 x 15 x 30 | 20 | 无 | 询价 | 同上 | 超标 |
| 012323 | 1.0 x 23 x 23 | 30 | 无 | 询价 | 同上 | 超标 |

## 设计建议
- 若坚持 8x15 侧装：只能定制 1.5x8x15（~5–7 mAh/颗，估算）。两颗约 10–14 mAh，比现有 2x020815（18–20 mAh）少 ~30%；脸宽仅省 2x0.5=1 mm。
- 戒指弧形电芯（120732/150725 类）沿戒圈放置，容量 13–19 mAh/颗，可能比两侧立装更合适。
- 一天续航：0.66" OLED 常亮通常数 mA 级，10–20 mAh 很难撑一整天，需要息屏/抬腕显示策略（未测，需实测电流）。
- 保护板：DW01+8205 小板一般会在极耳端增加约 2–4 mm 长、厚度≈电芯或 ~1 mm（经验值，**未验证**）；可考虑把保护做在主板上用裸芯。
