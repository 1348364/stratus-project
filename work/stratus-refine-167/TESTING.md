# Stratus 1.6.7 verification notes

The existing Modrinth Main Java client was verified loading 1.6.6 before changes. A guarded project-local Java agent used Minecraft/Iris APIs to capture the running Stratus Terrain Lab world without restarting, modifying Main's mods, redefining classes or transforming bytecode. The normal game stayed open. The read-only first capture was paused; it is not sky acceptance evidence.

`agent/LiveRunAgent.java` adapts the previous project QA driver. It checks the exact Main directory and designated world, queues Minecraft tasks on the proper client/server executors, verifies the shader pipeline and camera, and uses Minecraft's screenshot API. Native window selection is not needed. No OS keyboard/mouse synthesis is used. Standard JVM dynamic-agent warnings are distinct from shader errors.

Commands are queued through `qa-request.txt`. `STOP` restores the captured HUD/pause/menu values and stops the polling worker. Restore the original camera before stopping. Do not attach duplicate pollers or launch another client against the same open world. The original 1.6.6 settings file is snapshotted and hash-checked; immutable QA ZIPs/settings stay in `packs/` for evidence, and their exact temporary Main copies are removed after release loading.

Native checks use `work/stratus-check/prepare.py` then `native_compile --manifest work/stratus-check/pairs.tsv`. They do not emulate every Iris transform. `prepare_gpu.py`, `probe.c` and `check_gpu.py` exercise the actual GLSL for component independence, legacy reproduction, rain-film gating and high-cloud density/independence. `water_probe.c` checks the actual water resolve under preferred defaults.

Actual captures and comparative contact sheets are preserved here and in `outputs/Stratus-1.6.7-visual-checks`. Two early menu frames showed the previous page because the framebuffer had not caught up; corrected menu captures wait four seconds and use new filenames. Do not count stale/paused images as acceptance.

The game initially reported unfocused. Do not present background FPS as performance evidence. Record the final read-only runtime state, Dynamic FPS, actual settings and framebuffer size. A focused matched terrain/forest/river benchmark remains necessary before claiming a speed gain or maximum performance. Do not reduce quality to obtain one.
