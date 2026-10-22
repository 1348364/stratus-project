# Ready-to-use prompts

Use these from the MC Shader Making project root. Its `AGENTS.md` provides the standing instructions automatically.

## Apply pending changes

Read `work/Custom instructions/CHANGES.md` and the complete target in `work/Custom instructions/TASK.md`. Implement only unchecked Pending changes, preserve everything else, verify the result and document it in `CHANGE-LOG.md`. Reconcile `TASK.md` with the approved completed behaviour and actual source/release without overwriting newer edits or weakening unfulfilled requirements. After implementation and the required verification, move each completed request out of `CHANGES.md` → Pending changes into `COMPLETED-CHANGES.md` with its release/change-log reference. Do not leave checked-off completed items under Pending changes. Preserve partial, failed or unverified requests and newer user edits. When no requests remain, leave only “No pending changes.” under that heading. Never clear pending requests merely because a job was queued, delivered, or a chat turn ended. If the pending list is empty, report that there is no new task.

## Water task

Apply only the pending water-related items in `CHANGES.md`, using `TASK.md` as the full target and `.prompts/water.md` for the workflow; then verify affected scenes.

## Cloud task

Apply only the pending cloud-related items in `CHANGES.md`, using `TASK.md` as the full target and `.prompts/clouds.md` for the workflow; then inspect the rendered result.

## Performance task

Apply only the pending performance-related items in `CHANGES.md`, using `TASK.md` as the full target and `.prompts/performance.md` for the workflow. Measure a baseline and report comparable before/after results.

## Review only

Review the current shader using `work/Custom instructions/.prompts/visual-verification.md` and report evidence-backed findings. Do not edit shader code or install another build unless I ask.
