STRATUS 1.7.0-rc2 — MATERIAL, ENTITY AND NATIVE WATER REPAIRS

Original Iris shader pack, MIT licensed. Release candidate; the full1.7 water
milestone and sustained gameplay performance have not passed acceptance.

Changes from rc1:
- Preserve valid dark native water colours instead of substituting a bright
  biome tint. This fixes the reproduced pale cave-water step faces/edge bands.
- Vanilla water mode now includes the active animated underside texture, tied
  to WATER_TEXTURE, with zero and intermediate strengths. Stratus physical mode
  retains its clear underwater interface. Fog still stops at the true water exit.
- Ordinary entities regain vanilla-style two-light face shading in vanilla
  lighting mode, with their actual lightmap, texture and model normals. The
  existing enhanced lighting path and emissive/spidereyes passes remain.
- Leaf/plant cutout surfaces stay matte; their interior planes do not receive
  film. Exposed solid film remains, with a substantially lower solar lobe gain.
- Missing-background water transmission respects local sky exposure. An exact
  zero-contribution underwater atmosphere resolve skips redundant depth/taps.

All65 controls, defaults/ranges and preset quality assignments are retained.
No added pass, reduced resolution, removed quality choice or forced preset.
Related WATER_TEXTURE uses approved defaults where appropriate; later manual
choices and every unrelated override carry forward. Old and existing new-
version settings/archives are never overwritten. Use install.py --profile PATH
--previous-settings OLD.zip.txt, or --dry-run to inspect migration. Manual ZIP
copying does not migrate settings; installation does not imply selection/load.

Deliverable archives belong in the intended Minecraft shaderpacks folder and
remain installed after QA cleanup. Exact final installation/loading evidence is
in the external versioned receipt. Preserve older deliverables/preferences.

LIMITS: no focused FPS sample or general speedup claim. Requested progressive
partial-frame display is owned by Minecraft's renderer, beyond a shader pack.
Submerged-only fog intentionally differs from vanilla's distance fog for air
beyond an exit. Foliage exclusion covers the whole cutout material, not only
neighbour-facing leaf planes. Known waterline defect and earlier pending checks
remain explicit; this is not exhaustive weather/mod/resource-pack certification.
See VALIDATION.txt, IN-GAME-TEST.txt, CHECKS.json and the project change log.
