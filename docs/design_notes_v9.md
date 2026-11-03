# CodeRain v9: metal bezel covers the non-emitting border of the panel (based on v8 / v1 frozen; only the display window changed)
## What changed
- The top is now **one continuous metal plate** with a rectangular window **13.6 (across, Y) x 10.3 (along finger, X)**, corner R0.5, 0.15x45° inner chamfer on the top edge (opening 13.9x10.6 at the top surface)
- Panel active area AA 13.42x10.06 (64x48), long side across the finger (as in v8); the window is ~0.09 (Y) / 0.12 (X) larger than AA per side and smaller than the VA 14.42x11.06, so the whole non-emitting black border is hidden under metal and everything visible can light up
- The glass top is **0.50 below** the metal top (metal z14.80, glass z13.90–14.30); in side view the metal bezel stands above the glass
- Window centre x=+0.8 (aligned to AA centre); the panel moved −X by 0.5 vs v8 (centre x=−0.2), FPC bend allowance 1.2 on the −X side
- Bezel widths: 5.50 each side across; along the finger 5.95 on −X (FPC side) / 4.35 on +X (AA offset +1.0 from the panel centre is estimated from the drawing, **to be confirmed with the seller's datasheet**; only the aa_off parameter needs changing)
- Window / face area = 140.1 / 506.8 = 27.6% (AA/face 26.6%); v8 glass/face 73.6%
## Parts and assembly (loaded from the top)
- Unibody (z<13.9, top opening 19.0x23.0 R1 = inner wall) + **top_bezel** (z13.9–14.8, the whole face including outer fillets, with a 0.25 locating lip, lip broken on the −X side for the FPC) + bottom lid (unchanged) + glass 13.0x16.4 R0.8 t0.4 (bought in, no printed border needed)
- Parting line runs around the head sides, 0.9 below the top; top surface seamless
- Order: 2 batteries into the side cavities → socket into the lid / lid installed → PCB in from the top (z12.0–12.4), solder batteries / socket → solder panel FPC to the PCB top and fold down from the −X edge, seat the panel (z12.62–13.85, on 0.2 foam) → bond the glass with OCA/UV glue into the 13.1x16.5, 0.4-deep recess on the back of the bezel (bond margin ≥1.3) → fit the bezel, locate by the lip, seal with structural adhesive (DP460) or laser spot/seam weld, polish / sandblast the parting line
- Why not load from the bottom: the lid opening is only 14.8 in Y, smaller than the 16.5 panel / 18.6 PCB; sealing the top as one piece would make it impossible to fit the panel
## Internal changes to make room for the recess
- Head height 4.5, face 24.6x20.6, exterior 20.6x24.6x27.1 **unchanged**
- PCB down 0.4 (v8 z12.4–12.8 → v9 12.0–12.4); panel down 0.48; battery cavities / socket / lid / bore unchanged; the 0.5 metal shelf above the battery cavities removed (now open at the top, held by the bezel lip)
## Weight
- Body 2516.7 + bezel 290.1 + lid 177.8 = 2984.6 mm³ (v8 2857.0, +127.6)
- 316L ≈23.8 g (v8 22.8) / Ti ≈13.2 g (12.7) / 925 silver ≈31.0 g (29.7); glass 0.21 g (v8 0.37 g)
## Risks / to confirm
- AA offset relative to the panel (aa_off) and the real position of the 13.42x10.06 area: window alignment tolerance is only ±0.1; finalise the window after measuring a delivered panel; use an alignment jig in assembly
- The window is only 0.1 larger than the emitting area, so edges get clipped at oblique angles (0.5 recess + 0.4 glass)
- Thinnest bezel: 0.5 metal at the window edge, watch for warping when printing; bezel-to-body fit needs 0.05 clearance per side (lip 0.05 included in the model)
- PCB support step not modelled since v8
## Files
cad/ring_v9_sdf.py, cad/render_v9_blender.py, cad/fix_v9.py (repairs STL into a closed manifold), cad/v9_*.stl, cad/v9_params.json, renders/v9_*.png/jpg
