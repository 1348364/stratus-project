STRATUS 1.7.0-rc1 — NATIVE WATER AND TRANSPARENT OPTICS CANDIDATE

A standalone original Iris shader pack, MIT licensed. This is a development
candidate with incomplete live acceptance, not the completed1.7 water milestone.
The stable previous1.6.12 archive and saved preferences are preserved.

Changes:
- Water style: Vanilla default in every preset, or the retained Stratus physical
  colour/extinction mode. Native mode samples the active animated water atlas,
  vertex biome colour, native lightmap and game environmental underwater fog.
  Full-resolution native surface detail survives reduced-resolution optics.
- Stronger exposed film on top, side and underside faces, retaining shelter,
  roughness, drainage, weather choices and independent true-zero controls.
- Original nearest-interface thin-solid optics for mapped glass/panes, ice,
  slime and honey; independent reflection/refraction strengths. Related material
  render-path and visual acceptance is still pending.
-65 reachable options; all previous62 IDs/defaults/ranges and preset quality
  assignments preserved. No new fullscreen pass; one additional metadata buffer.

Install manually by copying the versioned ZIP into shaderpacks and selecting it
in Iris. Manual copying does not migrate settings. install.py --profile PATH
--previous-settings OLD.zip.txt performs selective migration without selecting
or loading the candidate. --dry-run previews the result. Old preferences and
existing new-version files always win over replacement. Related WATER_TEXTURE
uses approved defaults unless changed manually after the captured baseline;
new controls use source defaults unless a prior explicit manual value exists.
All unrelated current overrides carry forward.

Water controls remain accessible in both modes. Visibility, extinction,
turbidity and the biome override govern Stratus mode; native mode follows the
actual game colour/fog instead. WATER_TEXTURE scales the native alpha layer in
Vanilla mode, and retains whole-surface patterned tint in Stratus mode.

Transparent optics use flat block face normals and bounded screen-space
sampling, not water waves or full-volume ray tracing. Off-screen/hidden scenery
cannot be reconstructed. Multiple overlapping transparent layers and particles
have limited nearest-interface information. Both new optics controls at zero
bypass the effect. No third-party shader implementation was copied.

IMPORTANT LIMITS: known rectangular waterline band remains. Wet-face and glass
live acceptance, biome/status/resource-pack fog coverage and final ZIP loading
remain pending after the user skipped further live checks. Native underwater
mode keeps the prior straight-through exit: it deliberately omits vanilla's
back-face texture overlay, and enabled Stratus optics/atmosphere also differ.
No FPS was measured; no speedup or60FPS claim. See VALIDATION.txt,
IN-GAME-TEST.txt and CHECKS.json for exact evidence boundaries.
