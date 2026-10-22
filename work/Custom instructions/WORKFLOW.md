# Efficient shader workflow

This workflow reduces repeated AI work. Existing shader scope, quality, controls, verification and batch protection remain mandatory.

## Choose the smallest appropriate action

- **Run pending changes** for an ordinary implementation batch. Combine closely related requests in one batch to share setup and verification.
- **Stage & send** when TASK.md requirements were added, modified or removed. Stage and implement in the same coding pass; a separate AI refinement pass is only useful for an ambiguous brief.
- **Run Changes + TASK.md** only for an explicitly wanted full target review. Do not expand routine changes into a whole-project audit.
- Saving, delivery, copying files, release feeds, feedback mail and GitHub sync are handled by code; do not ask a model to repeat those jobs.

## Start and resume

1. Studio generates `CONTEXT.md` and an initial `PROGRESS.md` for each run batch using local Python, without AI calls. The context has hashes, TASK section locations, filename navigation hints and the latest recorded release summary.
2. Read the active brief, applicable instructions and TASK.md. Use the section index for later lookups instead of repeatedly dumping entire documents. The generated summary never replaces the authoritative specification.
3. On resuming, read the batch's PROGRESS.md and refresh its context with `python3 work/stratus-studio/workflow.py --batch "work/Custom instructions/IN-PROGRESS/<request-id>"`. Compare fingerprints and relevant working files; refresh runtime state before relying on previous live evidence.
4. Search the current source and exact issue/release paths first. Do not scan historical releases, generated builds, node_modules, screenshots or the full change log unless the task requires them. Filename hints are navigation aids, not proof of where a bug lives.
5. Inspect the necessary source/dependency paths, make a focused change, then inspect its diff. Avoid separate speculative design, review and handoff loops for a clear request.

## Verification without repeated setup

- Follow project verification requirements and any explicit user deferral. Never call a source edit a visual, runtime or FPS success.
- Use existing packaging, installer and QA tools; do not rebuild their machinery for each batch. Confirm supported commands before invoking them.
- Run the relevant required checks on the final candidate. Repeat only checks invalidated by source, configuration, environment or scene changes; preserve evidence identifying the exact input/build and result.
- One candidate can cover related changes when doing so preserves clear attribution. Keep performance comparisons at matched quality and actual chunk readiness.
- Do not repeatedly sample FPS when the user has deferred FPS, when chunk readiness/focus prevents valid evidence, or when the same unresolved prerequisite makes another attempt uninformative. Record the blocker and exact next action. Deferred checks remain unverified.
- Update PROGRESS.md at meaningful milestones and before stopping: changed files, current fingerprints, evidence paths, unfinished items and the next concrete action. Keep it concise; do not duplicate the complete chat or TASK.md.
- Reconcile the active batch, TASK.md and change log once for the final result, preserving newer edits. Required documentation and incomplete work must not be skipped to save usage.

## Existing unattended services

The Studio bridge delivers saved batches. Public release notes/showcases, Gmail feedback and GitHub uploads use their existing standalone services. They require the Mac/service prerequisites already documented; they do not require an AI conversation per update. Do not create a ChatGPT automation or a second delivery path for these jobs.

No model setting is changed by this workflow. Do not spawn extra agents or run a second model review unless explicitly requested or required by an applicable instruction.
