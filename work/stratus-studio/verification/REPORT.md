# Studio verification — 21 October 2026

## Scope

Website implementation only. No shader source or real TASK.md / CHANGES.md was saved by the verification workflow. Save and restore checks used disposable copies under the system temporary directory.

## Completed

- JavaScript syntax check and Python compilation checks passed.
- Fourteen focused HTTP checks passed: document load, writes, byte-preserving backup, stale revision rejection, history list/read, invalid token rejection, host/origin checks, fixed editable paths, invalid history names, home controls, actual shader image and no-op saves.
- Browser visual checks: real shader home image and navigation at desktop and narrow widths; upgraded Monaco editor and optional split preview at desktop width; mobile editor and revision controls.
- Browser interactions in a disposable workspace: add a pending change, type into Monaco, undo, redo, save, inspect history, load an earlier revision as a draft, save the restored version, and open the Specification document.
- The Specification editor saved the disposable `TASK.md`; its displayed filename, breadcrumb and absolute document path matched that file.
- Opened the native command palette with 128 available editor commands.
- External-edit check: changed the disposable TASK.md while its editor had an unsaved draft. Saving displayed the conflict comparison, retained the draft and allowed the project version to be loaded explicitly.
- Original plain-text editor search/replace and undo were checked before the Monaco upgrade. The final editor uses Monaco's native search/replace instead.

## Limits

- No shader compilation, Minecraft run or FPS benchmark was performed for this website task.
- No public or hosted deployment. Local server required for direct project-file editing.
- The lightweight Markdown preview is not a full CommonMark renderer; raw editing preserves all text.
- Not an exhaustive test of every Monaco command or third-party browser extension.
- Browser drafts depend on browser storage. Backups are created only by a successful changed save through Studio.

## Final focus-mode revision

- Both editing routes always apply focus mode. The tested editor occupies the entire 900 px desktop viewport; the decorative header, sidebar and formatting toolbar are hidden.
- Escape leaves the editor in focus mode. A plain Home link returns to the shader-themed overview.
- File tabs switch between CHANGES.md and TASK.md; a visible Save button and keyboard saving remain available.
- The real Specification view was checked against its displayed absolute project path, ending in `work/Custom instructions/TASK.md`.
- Saved editor previews: `editor-desktop.png` and `editor-mobile.png` (real project, read-only visual checks, final neutral colour palette).

- Final editor palette uses dark grey, white and blue. Checked that returning Home removes editor focus mode and retains the shader screenshot/design.
