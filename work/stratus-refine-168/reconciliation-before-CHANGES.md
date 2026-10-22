# Stratus — changes for the next coding pass

Put only the changes you want worked on now under **Pending changes**. `TASK.md` is the complete shader target and remains in force for everything else. A saved file does not start work; tell the coding chat **“Apply the pending changes.”**

## Pending changes

- [ ] Finish the archived 1.6.7 brief's focused matched FPS/frame-time verification before implementing the four requests below. The 243-entry release/source/installed integrity recheck passed. Current benchmark access is waiting for explicit approval of temporary Java test-code attachment and Minecraft window focus; normal desktop selection failed. No new performance result is claimed. [Current check and blockers](../stratus-finish-167/status.json).
- When the realistic shading is turned off, all shading needs to look vanilla including face shading, colour, brightness, ambiant brightness, etc
- Allow wet sheem without being in weather conditions, so all time
- Optimise performance searching and using exsisting expert sources, while keeping 99% of visuals
- Clean up shader options pages, following the guidelines from other popular shaders

## Completed changes

Completed items can be moved here with a link to the corresponding `CHANGE-LOG.md` entry or release. Keep partially completed or unverified items pending.

Rechecked the explicitly requested `TASK-previous-brief.md` on 21 October 2026. Its historical “not implemented” progress is superseded by the source, archive and actual runtime evidence; the archive remains unchanged as history.

- [x] Main's recorded preferred values are source defaults; original saved options remain preserved and Reference remains separately selectable.
- [x] Polished square sun has a richer local halo/core with independent controls; native mode and global bloom remain preserved.
- [x] Vanilla and realistic face components have separate controls; their default combination reproduces the previous mix.
- [x] Independent high cirrus is visible in the preserved actual Main isolation comparisons, with existing amount/altitude controls retained.
- [x] Appropriate rainy materials have adjustable view-dependent sheen; dry/non-absorbing response and saved values are preserved, with the deliberate extension documented.

All five are already present in the current **1.6.7** source, released ZIP and installed pack. No missing shader code was found and no duplicate build was made. [Implementation, visual evidence and limitations](CHANGE-LOG.md), [fresh integrity recheck](../stratus-recheck-167/recheck.json), [fresh runtime state](../stratus-recheck-167/runtime-state.txt). Broader unverified scene coverage remains described in `TASK.md` and the change log; the performance item above remains pending.
