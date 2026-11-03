# Coderain ring — thin BOM (≤0.8 mm parts) — checked 2026-11-01 (PT)
Stock and price come from the LCSC product pages, fetched 2026-11-01 (USD, lowest price break). "Verified" means the C-number and package were read from LCSC this session.

## Current parts (all fail the 0.8 mm limit, except where noted)
| Part | C# | LCSC pkg | Height | Stock | Verdict |
|---|---|---|---|---|---|
| ATtiny1616-MNR | C507118 | VQFN-20 3x3 | 0.85 typ / **1.00 max** (Microchip) | 14 | FAIL (too tall, almost no stock) |
| SC7A20HTR | C19274408 | LGA-12 2x2 | ~1.0 (Silan 2x2x1.0, UNVERIFIED) | 98k | FAIL (likely) |
| LIS2DH12TR | C110926 | LGA-12 2x2 | 1.0 max (ST 2x2x1) | 297 | FAIL |
| TP4054 | C5381776 | SOT-23-5 | ~1.1–1.45 | 254k | FAIL |
| XB5353A | C80628 | SOT-23-5 | ~1.1–1.45 | 1.3k | FAIL |
| XC6206 | — | SOT-23 | ~1.1 | — | FAIL |

## Thin replacements
| Function | Part | C# | Package | Max height | Stock | Price | JLC SMT |
|---|---|---|---|---|---|---|---|
| MCU | WCH CH32V003F4U6 (16KB flash/2KB RAM, I2C, standby ~9 µA) | C5299908 ✔ | QFN-20 3x3, 0.4 pitch | **0.75** (generic QFN3x3-20 spec; WCH drawing is an image → CONFIRM) | 4,725 | $0.19–0.31 | Extended part (yes) |
| Accel (tap) | ST LIS2DW12TR (tap/double-tap, wake-up int, 50 nA standby) | C189624 ✔ | LGA-12 2x2 | **0.70 max** (ST datasheet) | 21,758 | $0.71–1.05 | Extended (yes) |
| Charger | TI BQ24040DSQR (ISET 10–800 mA, set ~15 mA via R) | C81080 ✔ | WSON-10 2x2 | 0.80 max (TI DSQ, CONFIRM in drawing) | 140,244 | $0.25–0.42 | Extended (yes) |
| Charger alt | TI BQ25100YFPR (1–250 mA, good for tiny cells) | C527572 ✔ | DSBGA-6 | ~0.625 max (UNVERIFIED) | **0** | $1.60 | 0.4 mm-pitch BGA, out of stock |
| Charger alt | LTC4065EDC (szlcsc 608608) / TP4066 DFN228 (szlcsc 43227265) | not checked | DFN 2x2 | 0.75 | not checked | — | — |
| Protection | ALLPOWER AP6683 (has its own MOSFETs, 1-cell) | C2849565 ✔ | DFN-4-EP 1x1 | ~0.4–0.55 (UNVERIFIED) | 101,770 | $0.05–0.06 | Extended (yes) |
| Protection alt | LOWPOWER LPB1010HQVF | C47345803 ✔ | DFN-4-EP 1x1 | UNVERIFIED | 13,665 | — | — |
| LDO 3.3V | MICRONE ME6211C33U4AG-N | C428904 ✔ | X2SON/FBP 1x1-4 | **0.37** (ME6211 datasheet) | 8,930 | $0.03–0.05 | Extended (yes) |
| LDO 3.0V (low Iq) | TI TPS7A0530PDQNR (Iq 1 µA) | C2871471 ✔ | X2SON-4 1x1 | ~0.4 (UNVERIFIED) | 2,685 | $0.16–0.28 | Extended (yes) |
| Passives | 0201 MLCC (≤0.33 max) or 0402 (0.5–0.55 max; 1 µF+ 0402 can be 0.55–0.6 → check) | — | — | ≤0.55 | — | — | Basic/Extended |

Notes: XB8089D0 (C2760005) is SOP-8-EP, 1.75 mm tall, so it is not a thin option. For the LDO, pick TPS7A05 (Iq 1 µA) for battery life. ME6211 draws 30 µA quiescent, which is bad for standby. CH32V003 standby is about 9 µA plus the LDO, and that is the dominant sleep current. If sleep current matters a lot, compare a PY32F002B (QFN/DFN) part; not checked here.

## Recommended thin BOM
CH32V003F4U6 + LIS2DW12TR + BQ24040DSQR + AP6683 + TPS7A0530PDQNR + 0201/0402 passives.
Tallest part: CH32V003 at ~0.75 mm, or BQ24040 at 0.80 mm max. With ~0.03–0.05 mm of solder, the component layer is **≈0.80–0.85 mm**. That is right at the limit, so confirm the QFN and WSON drawings before layout. Without the CH32V003 and BQ24040 the tallest part is 0.70 mm (accel), which gives ≈0.75 mm.
Firmware impact: moving from ATtiny (AVR) to CH32V003 (RISC-V) means porting the code, and you need a WCH-LinkE programmer (1-wire SWIO).
