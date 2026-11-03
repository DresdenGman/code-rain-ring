# Bigger screen options for the ring (researched 2026-11-01)

Baseline: 0.66" 64x48 ST7315, panel 16.5x16.2 mm, AA 13.42x10.06 mm = **135 mm²**.
Constraint: panel <= ~17.4 mm across finger, other axis <= ~20 mm.
All specs below come from the datasheets/pages linked. Anything I couldn't confirm is marked UNVERIFIED. I didn't find Taobao prices (not checked).

## Ranked table

| # | Part | Diag | Res | Type / IC | AA (mm) | AA mm² | Outline WxHxT (mm) | Interface / FPC | Power | Fit? |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | YDP085B001-V2 (Osptek) / N085-1212TBWIG41-H12 (Wisevision) / YDP LCD I 85 S | 0.85" | 128x128 RGB | IPS **TFT** (not OLED), GC9107, 1 white LED backlight | 15.21 x 15.21 (1:1) | **231** (+71%) | 17.58 x 20.82 x 1.5 (glass 17.26 x 19.55) | 4-wire SPI, 12-pin 0.7 mm-pitch solder FPC (from drawing) | VDD abs max 4.6 V (3.3 V logic); LED backlight needs its own current (~20 mA typ, UNVERIFIED) | Marginal: 17.58 is 0.18 mm over 17.4 (glass itself 17.26). Height 20.82 ~ the limit |
| 2 | Winstar WEO004864A (COG) | 0.71" | 48x64 | Mono PMOLED, SSD1306BZ | 10.54 x 14.70 (≈3:4) | **155** (+15%) | 13.90 x 22.0 x 1.26 | I2C, FPC | 3 V class (SSD1306: VDD 1.65–3.3 V, VCC ~7–15 V via internal charge pump; per IC datasheet) | Width fits easily; 22 mm is 2 mm over the 20 mm limit |
| 3 | 0.78" 80x128 (BuyDisplay ER-OLED0.78-1, GoldenMorning GME80128-01, 中景园-type zjydisplay page) | 0.78" | 80x128 | Mono PMOLED, SH1107 | 9.68 x 17.26 (≈1:1.78) | 167 (+24%) | 12.13 x 23.6 x 1.2 | 4-wire SPI, 13-pin 0.7 mm solder FPC | 3.3 V | Too long (23.6) and too skinny |
| 4 | 0.77" 64x128 (创力信, GoldenMorning E077XI-W-C10-02) | 0.77" | 64x128 | Mono PMOLED, SSD1312 | 9.26 x 17.26 | 160 (+18%) | 12.13 x 23.6 x 1.2 | I2C, 10-pin 0.5 mm | 3.3 V | Too long, skinny |
| – | 0.96" 64x128 (Multi-Inno MI64128CO/EO, SSD1312/SH1107) | 0.96" | 64x128 | PMOLED | 10.86 x 21.74 | 236 | 14.0 x 28.0 x 1.2 | SPI/I2C | 3.3 V | Too long (28 mm) |
| – | 0.95" 96x64 (GME9664-01, SH1106G) | 0.95" | 96x64 | PMOLED | 23.8 x 17.32 | – | 24.8 x 32.2 | SPI/I2C 26P | – | Way too big |
| – | 1.1" 96x96 / 1.12" 128x128 OLED | – | – | SSD1327/SH1107 | ~20 x 20 | – | ≥25 x 27 | – | – | Too big |

Not found: 0.76" 64x64, or any 0.71" 96x96 / 0.85" OLED that fits. As far as I could find, every 128x128 OLED is 1.12" or larger. I didn't find a 4:3 mono OLED bigger than 0.66" with a panel under 17.4 mm.

## Takeaways
- **Biggest lit area that (nearly) fits:** the 0.85" 128x128 GC9107 TFT. Its AA is 71% larger and it's full color. Downsides: it's 0.18 mm too wide (or 0.32 mm with tolerance), it needs a backlight LED so blacks aren't truly black and it draws more power, and it's 1.5 mm thick vs ~1.2–1.45 mm. It's sold widely as "0.85寸 128x128 GC9107" on Taobao (prices not checked).
- **Best OLED:** the 0.71" 48x64 SSD1306 rotated with 13.9 mm across the finger. AA grows only 15% (14.7 x 10.54 landscape vs 13.42 x 10.06) and the panel is 22 mm long.
- 0.77"/0.78" give slightly more area but are skinny strips (12 x 23.6 mm).

## Sources
- https://admin.osptek.com/uploads/YDP_085_B001_V2_c65b60c808.pdf
- https://www.jx-wisevision.com/uploads/SPEC-N085-1212TBWIG41-H12-VER-A-.pdf
- https://knitter-switch.com/wp-content/media/pms/Display/TFT/YDP%20LCD%20I%2085%20S.pdf
- https://www.winstar.com.tw/products/oled-module/graphic-oled-display/smallest-oled.html ; https://cdn.soselectronic.com/productdata/fb/ee/7ae9374a/weo004864awpp3n00000.pdf
- https://www.buydisplay.com/download/manual/ER-OLED0.78-1_Datasheet.pdf ; http://www.zjydisplay.com/product/83.html
- http://www.chinalcdclx.com/Products_detail/122.html
- https://goldenmorninglcd.com/ja/ (OLED table) ; https://www.multi-inno.com/OLED.asp
