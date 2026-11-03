# Code Rain Ring v6 / Product v1: Frozen Design Notes

## 1. Project split
- Dev kit (desk debugging, already bought): ESP32-C3 + 0.42" OLED dev board, TP4056 USB-C charger board, TTP223 module, 400909 35 mAh (9x9x4) battery. Only for writing code and tuning the animation; not going into the ring.
- Product v1: this file + BOM_v1_final.csv.

## 2. Exterior (identical to v4/v5)
Straight-wall U signet, parallel vertical sides in side view, no taper; length 17 x width 24.6 x height 27.1; head 4.5 mm above the finger; no button hole, no USB hole. The only opening is the Φ4 magnetic charging port at the top of the inner bore (facing the finger; take the ring off to charge).
With a 4.5 mm head there is only 4.5 mm above the finger at the rear face; a Φ4 hole plus the cover recess / fillet leaves ~0.25 mm, not feasible, so it goes in the inner bore (bottom lid).

## 3. Internal layout (z upward from the finger axis, bore radius 10.3)
| Layer | z |
|---|---|
| Bottom lid (with Φ4.1 hole) | 10.3–10.9 |
| Magnetic receptacle Φ4x2.0 (face recessed 0.1) | 10.4–12.4 |
| PCB bottom-side parts (MCU / accelerometer / charger / protection / LDO) | 10.9–12.4 |
| PCB 0.4 mm, 15.0x14.4 R0.8 | 12.4–12.8 |
| Panel FPC fold layer | 12.8–13.1 |
| 0.49" OLED 14.5x11.6x1.28 (adhesive-backed under the cover) | 13.1–14.4 |
| Cover glass 19x13 t0.4 | 14.4–14.8 |

One 2x8x15 cell in each side battery cavity, placed against the outer wall (y=±9.5~11.5, z=5.65~13.65).

## 4. v6 geometry fixes
- In v5 the lower part of the battery cavities opened into the finger bore at |y|=7.4~9.2 (the lid did not cover it, leaving a gap showing the battery). v6 keeps a 0.7 mm wall between the cavities and the bore; an SDF point-by-point check confirms no openings in the bore.
- Battery cavity top raised to 13.9. OLED pocket changed to 14.8x11.9 for the 0.49" panel.

## 5. Part choices
- MCU: ATtiny1616 (no radio). Runs directly from the battery from 1.8 V, 0.1 µA sleep, Arduino via megaTinyCore, single-wire UPDI programming. CH32V003 is cheaper but needs ≥2.7 V and has higher standby current; kept as an alternative.
- Wake: accelerometer tap (SC7A20 / LIS2DH12) single/double-tap interrupt. The metal shell sits against the finger, so capacitive touch (TTP223 / MCU touch) would trigger constantly or be shielded, and would need a hole / non-metal area. Not used.
- Charging: TP4054 ~15 mA (1C of 2x9 mAh ≈ 18 mA; 20–40 mA is too much); one XB5353A per cell.
- Display: 0.49" 64x32, active area 11.18x5.58, larger than the 0.42" (9.2x5.2), fits under the 19x13 cover, so 0.49" is frozen. The 0.42" (12x11) also fits as an alternative. FPC soldered directly to the PCB (no connector; not enough height).

## 6. Battery
- 2 mm-thick 200815 cells are available in China (~CNY 12 each on 1688); confirm tab length with samples.
- 400909 (9x9x4) does not fit: the side cavity is only 4.5 wide x ~8.3 tall (limited by the bore arc), and only ~2 mm of height is usable in the head cavity. Fitting a 400909 would need ~5 mm more head height or a wider body, breaking the v4 exterior, so it is dev-kit only.

## 7. PCB prototype (JLCPCB)
0.4 mm board, ENIG, 15.0x14.4 with R0.8 corners; single-sided (bottom) assembly, 0402 + QFN-20 + LGA-12 + SOT-23; JLC SMT can place these (choose "Economic" / "Standard" per their rules for LGA/QFN). Receptacle, panel FPC and batteries are hand-soldered. Leave UPDI/GND/VCC test points.
