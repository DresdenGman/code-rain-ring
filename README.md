<p align="center"><img src="promo/hero_banner.jpg" alt="Code Rain Ring" width="100%"></p>

<h1 align="center">Code Rain Ring · 代码雨戒指</h1>
<p align="center">一枚在指尖下着 <b>Matrix 代码雨</b> 的金属戒指 —— 3D 打印金属外壳 · 0.66" OLED · 敲击唤醒 · 磁吸充电</p>
<p align="center"><a href="#english">English</a> · <a href="docs/parts.md">BOM / 零件尺寸</a> · <a href="#开放问题">开放问题</a></p>

---

## 项目初衷

灵感来自 **Daniel Idle 的 Digital Rain Ring**。我们想做一枚自己的版本：真正能戴的尺寸（M / L 两个码），金属质感，屏幕上跑《黑客帝国》式的绿色代码雨，轻敲即亮。

整个项目从零开始用参数化 CAD（Python + CadQuery）迭代了 10 个版本，外壳交给 **珠光金属3D打印**，电子零件来自 **淘宝 / 立创商城 (LCSC)**，由在中国的朋友手工组装。这个仓库公开了所有文件：模型、脚本、设计说明、零件图纸、渲染图，希望对想做类似可穿戴小物的人有帮助。

## 特性

- **一体金属外壳**：3D 打印金属，最小壁厚 0.5 mm，指圈 1.5 mm 实心金属
- **超薄头部**：仅约 **4.15 mm** 厚，两颗 020815 电池直立贴住头部顶面
- **隐藏排线**：一侧 0.5 mm 金属盖条（约 2.9 宽）盖住从头部到充电座的 FPC 槽；电池角处 0.25 深槽用环氧填平
- **磁吸充电**：WIRE 4 mm 圆形磁吸座，指圈底部全宽内凸充电垫（峰高 1.0，两侧各 35° 过渡，0.4 圆角）
- **敲击唤醒**：ATtiny1616 MCU + SC7A20 加速度计
- **两种显示颜色**：透明盖板 = 白色代码雨；带绿色印刷层的盖板 = 绿色代码雨
- **两个尺码**：M（内径 19.4）和 L（内径 21.0）

## 展示

| | |
|---|---|
| ![](promo/closeup_screen.jpg) | ![](promo/on_hand.jpg) |
| ![](promo/charging_stand.jpg) | ![](promo/exploded_concept.jpg) |

![M 与 L](promo/M_L_pair_green_white.jpg)

> 以上宣传图为基于 CAD 渲染生成的概念效果图；下方为 CAD 直接渲染。

### CAD 渲染

| M | L |
|---|---|
| ![](renders/hq/M_iso_hq.png) | ![](renders/hq/L_iso_hq.png) |
| ![](renders/hq/M_exploded_hq.png) | ![](renders/hq/L_exploded_hq.png) |
| ![](renders/hq/M_top_hq.png) | ![](renders/hq/L_top_hq.png) |
| ![](renders/hq/M_side_hq.png) | ![](renders/hq/L_side_hq.png) |

![M vs L](renders/hq/ML_compare_hq.png)

### 工程图

| | |
|---|---|
| ![](renders/side_M_final.png) | ![](renders/side_L_final.png) |
| ![](renders/v10_M_section.png) 截面 M | ![](renders/v10_L_section.png) 截面 L |
| ![](renders/v10_M_route.png) 排线走向 M | ![](renders/v10_L_route.png) 排线走向 L |
| ![](renders/v10_M_liner.png) 盖条 M | ![](renders/v10_L_liner.png) 盖条 L |

![](renders/topview_ML_final3.png)
![](renders/v10_M_pad.png)

## 规格

| 参数 | M | L |
|---|---|---|
| 内径 | 19.4 | 21.0 |
| 头部 宽×长×厚 | 22.4 × 17.5 × 4.15 | 24.0 × 18.8 × 4.15 |
| 显示窗口 | 16.8 × 12.2 | 18.2 × 13.3 |
| 盖板玻璃 | 17.25 × 12.8 × 0.4 | 18.8 × 13.9 × 0.4（0.3 台阶） |
| OLED | 0.66" 标准 (16.5×16.2) | 0.66" 大号 (18.46×18.1×1.25) |
| 盖条（展开） | 14.31 × 2.9 × 0.5 | 16.01 × 2.9 × 0.5 |
| 电池 | 2 × 020815 直立 | 2 × 020815 直立 |
| 充电 | Φ4 磁吸座 + 内凸充电垫 | 同 |
| 指圈 | 1.5 实心金属 | 1.5 实心金属 |
| 最小壁厚 | 0.5 | 0.5 |

完整 BOM 与精确尺寸、商家图纸截取见 **[docs/parts.md](docs/parts.md)**。

## 仓库结构

```
hardware/M, hardware/L   最终 v10 模型：外壳/盖条/玻璃 STEP+STL，零件 STL，DXF 展开图，checks JSON
cad/                     参数化脚本 ring_v10.py (M|L)、render_v10.py、render_hq_vtk.py
renders/                 工程渲染；renders/hq 高清 VTK 渲染
promo/                   宣传图（hero 横幅等）
docs/                    parts.md (BOM)、设计说明 v1–v9、薄型电池/BOM 调研
reference/seller         淘宝/拼多多商家原图；reference/crops 截取的尺寸图
archive/                 早期版本（v2–v9 脚本、模型、BOM、渲染；>25MB 的旧网格未收录）
```

重新生成：`pip install cadquery trimesh matplotlib ezdxf vtk`，然后 `python cad/ring_v10.py M`、`python cad/render_v10.py M`、`python cad/render_hq_vtk.py`。

## 组装说明

1. FPC 厚度 ≤ 0.2，从头部腔体经底板过孔（−Y 侧）沿内圈 2.2×0.18 槽走到充电座。
2. 金属盖条弯成内圈半径，胶粘入 3.0×0.5 槽，与内圈齐平。
3. 环氧区 A：电池角旁 0.25 深槽，覆盖排线后用环氧填平（此段没有盖条）。
4. 环氧区 B：充电座与盖条末端之间的缝，填平。
5. 两颗电池直立贴住头部顶面；玻璃落在 0.3 台阶上，位于两电池之间。

## 开放问题

- **L 码 OLED 与腔体冲突**：大号 OLED 长 18.1（沿手指方向），腔体只有 17.8，每端约 0.15 压到 0.5 端壁。**建议：头部沿手指方向加长 0.3 mm。**
- **OLED / PCB 装配方式待定**：屏和 PCB 都大于窗口，如何装入（盖玻璃前从顶部放入、倾斜放入、或端壁开槽）尚未确定。
- 薄型 BOM 中标 UNVERIFIED 的器件高度需按官方图纸确认。
- 商家图纸精度有限，磁吸座和大号 OLED 到货后需实测。

## 致谢

- 灵感：**Daniel Idle — Digital Rain Ring**。本项目为独立重新设计，未使用其文件。
- 金属打印：珠光金属3D打印；零件：淘宝、立创商城 LCSC；组装：在中国的朋友。

## 许可证

- 硬件设计文件（模型、图纸、渲染、文档）：**CERN-OHL-S-2.0**（强互惠开源硬件许可，适合硬件，改版需同样开源）
- 代码（`cad/*.py` 等脚本）：**MIT**
- `reference/` 内商家图片版权归原商家，仅作参考。详见 [LICENSE](LICENSE)。

---

<a id="english"></a>
## English

**Code Rain Ring** is a wearable metal ring with a tiny OLED showing *Matrix*-style digital rain, inspired by Daniel Idle's Digital Rain Ring. The shell is metal 3D-printed (珠光金属3D打印), parts come from Taobao/LCSC, and a friend in China assembles it. Designed parametrically in Python/CadQuery over 10 iterations.

**Highlights:** ~4.15 mm thin head; two upright 020815 LiPo cells against the head top; solid 1.5 mm band; hidden ≤0.2 mm flex cable under a 0.5 mm metal cover strip (M 14.31×2.9, L 16.01×2.9) with a 0.25 mm epoxy-filled section at the battery corner; full-width inward charging pad (1.0 peak, 35° blends, 0.4 fillets) and a 4 mm WIRE magnetic socket; ATtiny1616 + SC7A20 tap-to-wake; clear cover glass = white rain, green-printed glass = green rain. Min metal wall 0.5 mm.

| | M | L |
|---|---|---|
| Inner diameter | 19.4 | 21.0 |
| Face | 22.4×17.5 | 24.0×18.8 |
| Window | 16.8×12.2 | 18.2×13.3 |
| Cover glass | 17.25×12.8×0.4 | 18.8×13.9×0.4, 0.3 lip |
| OLED | 0.66" std | 0.66" large (18.46×18.1) |

**Open issues:** L OLED length 18.1 vs cavity 17.8 (proposal: extend head +0.3 mm along the finger); OLED/PCB insertion method TBD.

See [docs/parts.md](docs/parts.md) for the BOM and exact dimensions. Licence: hardware CERN-OHL-S-2.0, code MIT. Promo images are AI-assisted concept renders based on the CAD; `renders/` are direct CAD renders.
