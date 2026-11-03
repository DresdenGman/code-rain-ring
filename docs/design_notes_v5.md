# Code Rain Ring v5: Design Notes

## Changes (vs v4)
- Exterior keeps the v4 straight-wall U signet: parallel vertical sides in side view, no taper, constant 17 mm length, band OD 24.6 mm. The only change: head height above the finger 5.5→4.5 mm (z_top 15.8→14.8), overall height 27.1 mm.
- USB-C opening removed; replaced with 2-pin magnetic pogo charging. The receptacle (LCSC C5280828, 2.8 mm tall) sits in the bottom lid at the top of the inner bore, contacts facing the finger, aligned along the finger axis (surface sagitta ≈0.5 mm), centre x = −1.9. No openings on the top, sides or rear face.
- At 4.5 mm head height the rear face has only ~3 mm of material, too little for the ~11×6.5 mm receptacle, so the inner bore was chosen.

## Stack (from finger upward, mm)
Lid 10.3–10.9 / PCB 11.0–11.6 (parts up to ≈12.4; C-shaped board clears the pogo) / top of pogo body 13.1 / OLED 13.2–14.4 / cover 14.4–14.8

## Power
TP4054 (C382138) + R_PROG 68k ≈ 15 mA (estimate); one XB5353A (C80628) per cell. The requested 20–40 mA exceeds 1C of 2×9 mAh (≈18 mA) and is not recommended. Contacts go to VIN through a Schottky + ESD, gold-plated.
Battery LIP-020815 is available on 1688 and similar; the cavity is 15.4 mm long so the tabs must be bent; verify with samples.

## Files
cad/ring_v5_sdf.py, cad/v5_*.stl/.step, renders/v5_*.png, renders/v5_contact.jpg, BOM_v5.csv
