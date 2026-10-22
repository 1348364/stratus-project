# Stratus Studio

A local website for editing the Stratus shader's specification and next-pass brief.

## Open

Double-click `start.command` in Finder. It starts the local server, waits until it is ready, then opens your default browser. If Studio is already running, it opens the existing instance.

The usual address is **http://127.0.0.1:8765/**. Keep the launcher terminal open while editing. Control-C stops the server.

From a terminal, you can also run:

```sh
cd '/Users/william.lei/Documents/ChatGPT/MC Shader Making/work/stratus-studio'
python3 server.py --port 8765
```

Python 3.10 or later is needed. No npm install or internet connection is needed to run the finished site; Monaco Editor is bundled locally. `package-lock.json` pins the editor version for future development.

## Documents

| Site page | Actual project file | Purpose |
| --- | --- | --- |
| Changes | `work/Custom instructions/CHANGES.md` | Pending requests for the next coding pass. |
| Specification / TASK.md tab | `work/Custom instructions/TASK.md` | The complete long-term shader target. |
| Activity | `work/Custom instructions/CHANGE-LOG.md` | Read-only release and verification history. |

These are the real project files, not exported copies. TASK.md describes the complete absolute shader target for a clean rebuild, including intended appearance, behaviour, construction and verification. CHANGES.md contains only the next relevant coding pass. In-game defaults and choice lists remain in shader source. Saving either file does not start work.

## Coding Stratus (2) connection

Use **Chat** in the editor toolbar or **Connect to chat** on the overview. Requests go to the existing **Coding Stratus (2)** chat using the installed Codex CLI and its existing sign-in.

- **Stage & send** in the editor toolbar opens **Stage and send for running**. This captures the saved TASK.md additions, edits and removals, asks Coding Stratus (2) to stage them in CHANGES.md, then run the pending work. A frozen target, change brief and diff are kept with the receipt. The comparison starts from the target when this action was installed and advances on successful queue delivery; delivery does not mean implementation is finished. Existing pending CHANGES.md items remain included.
- **Stage changes:** review and refine the saved CHANGES.md brief, without shader implementation.
- **Run Changes + TASK.md:** save both editors, then run pending incremental changes and audit the full target for unfinished requirements. Stage concrete gaps before implementing, preserve working features and newer edits, and keep unverified work pending. This is broader than Stage & send, which stages only the specification delta.
- **Run pending changes:** explicitly request implementation of pending CHANGES.md items in that chat. The full TASK.md target remains in force; completed changes must be reconciled into it and evidence recorded in CHANGE-LOG.md.
- **Related shader work:** send a specific request with relevant project-file references directly to the coding chat; unrelated pending items do not start automatically.
- **Modify TASK.md:** describe how to change the complete shader target. This requests a specification edit, without starting implementation.

Stage & send saves editor changes automatically. Recover or dismiss stored browser drafts and resolve file conflicts first. The server checks saved document revisions before sending. The final action button sends the selected request; there is no automatic send on save. Delivery receipts are stored locally in `.bridge/`. “Queued” confirms delivery to Codex, not task completion; read the chat for progress, approvals, questions and results. A timeout is reported as uncertain and never automatically retried. Repeated requests with the same request ID reuse the receipt. The archived broken coding chat is not used.

The connection needs the Codex app/CLI installed and signed in, plus internet access for model work. Editor/file saving works offline. The bridge does not change models, approval policy or sandbox settings. **Copy coding brief** remains available as a manual alternative.

## Editing

The editing pages use Microsoft Monaco Editor 0.57.0, with Markdown syntax highlighting, line numbers, folding, minimap, file tabs, an explorer, native undo/redo, multiple cursors, find/replace and a command palette. Editors always open in full-screen focus mode with plain file tabs, dark-grey/white/blue editor colours and a Save control. Code is the default view; Split preview and Preview are available. Home returns to the shader-themed overview.

- **Command-S:** save the active document to the project.
- **Command-F:** editor search; use the search widget for replace, case sensitivity and regular expressions.
- **F1 / command icon:** editor command palette.
- **Command-B / Command-I:** Markdown bold / italic.
- **Alt-click:** add another cursor on macOS.
- **Escape:** close a popup. Editors remain in focus mode.

The outline jumps to a section. Add a change / Add a section inserts an editable starting point. All text remains freely editable. Imports enter the editor as unsaved drafts; exports download the current editor text. Raw HTML is displayed as text in preview for safety. The preview supports headings, ordinary lists, checkboxes, code blocks, quotes, tables and links; it is a lightweight Markdown preview, not a complete CommonMark implementation.

## Saving and recovery

Manual saving is the default. Auto-save is opt-in under editor preferences. Unsaved drafts are also kept in browser storage, with recovery offered after a reload. Browser storage can be cleared by the browser, so use Save to project for durable work.

Before each changed save, Studio backs up the previous file under `.history/changes/` or `.history/spec/`. Revision history can load a backup into the editor as a draft; saving applies it. Backups are local and are not automatically pruned.

The site polls for external edits every ten seconds. If the file changes in VS Code or another chat, an untouched editor reloads it. A dirty editor retains its draft and requires a conflict comparison before saving. The server also checks the revision during every save, so it catches changes between polls. Conflict comparison highlights lines missing from the other version; it does not perform an automatic merge.

The Python server listens only on `127.0.0.1`. The two editable paths are fixed; the release log is read-only. Saves use a per-process request token, same-origin checks and atomic replacement. This local setup lets Studio edit files on this Mac; it is not a hosted or publicly accessible website.

## Imagery

The home page and gallery use actual Stratus 1.6.7 Minecraft captures copied from `outputs/Stratus-1.6.7-visual-checks/screenshots/`. They are saved references, not live renders or generated mockups.

## Verification

`python3 verify.py` checks HTTP saves, backups, revision conflicts, history, allowed document paths, origin/host restrictions and static assets using disposable documents. It does not write the actual project spec or brief.

`python3 verify.py --serve-fixture` runs a disposable copy on port 8766 for browser checks. Stop it with Control-C.

See `verification/REPORT.md` for the checks performed during creation. Monaco's licence is in `dist/vendor/MONACO-LICENSE.txt`.

## Private cloud access

Hosted editor: https://stratus-studio-developer0406.chuyang-lei-2557.chatgpt.site

Sign in with the owning ChatGPT account on your phone or another computer. Cloud saves and queued work persist while this Mac is offline. The Mac must be awake and signed in to Codex to sync files and deliver jobs. A per-user LaunchAgent (`au.stratus.studio.cloud-bridge`) now starts the private connection at login and restarts it after failures, using macOS Keychain. The local Studio server and an open terminal are no longer needed for cloud delivery. `start.command` remains available for the optional local editor. No public inbound connection is exposed.

The bridge keeps a revision record in `.cloud-sync-state.json`. Concurrent edits on both cloud and Mac stop sync and job delivery instead of overwriting either copy. Reconcile both versions before continuing. Cloud delivery receipts distinguish waiting for the Mac, delivery to Codex, failure and uncertain delivery; they do not imply shader completion.

Stage & send automatically saves unsaved CHANGES.md and TASK.md edits before queueing. It waits for an in-progress save and uses the resulting saved revisions. Failed saves, unresolved file conflicts, unrecovered browser drafts or edits arriving during the save stop delivery. A successfully saved document stays saved if a later document fails; no request is queued until both are ready. Other chat actions retain their existing explicit-save workflow.

### Delivery recovery — 22 October 2026

The stopped Mac bridge and diverged cloud/local briefs blocked two identical water-fog submissions. Both original versions were backed up under `.bridge/delivery-recovery-20261022/`. The water-fog request was merged with the newer 1.6.8 documentation without dropping the existing performance/verification work. One request was delivered to Instructions midway node; the duplicate was retained as superseded. The background bridge now writes incoming documents with revision guards and backups directly, removing its dependency on the local web server.

The user service definition is `cloud-bridge-launchagent.plist`; the installed copy is in `~/Library/LaunchAgents/`. Logs remain in `.cloud-bridge.log` and `.cloud-bridge-error.log`. The cloud API's recent connection timestamp is the live availability signal.

## Automatic public showcase

The plain developer home contains only document links, coding actions and connection state. No release images or manual release content need updating here. The background bridge runs `public_sync.py sync` every minute to publish verified release captures to the separate public site. See `work/stratus-public/README.md` for the release artefact convention. Gmail feedback delivery uses the private outbox commands in `public_sync.py` and the standalone SMTP sender `feedback_mail.py`, scheduled by macOS launchd every minute. No ChatGPT automation is used.

## Standalone feedback email

Double-click `feedback-mail-setup.command` once. Enter your Gmail address and a Google app password into its hidden password prompt. Setup checks Gmail authentication, saves credentials in macOS Keychain (`stratus-feedback-mail` / `smtp`) and installs `au.stratus.studio.feedback-mail` in your user LaunchAgents. No password appears in source, shell arguments, logs or browser files. Google app passwords require 2-Step Verification and may not be offered for some accounts. Never enter your normal Google password.

The background sender checks every minute while the Mac is awake and logged in. It does not need Codex or the Studio editor open. The cloud form remains available while the Mac is offline and queues submissions. `python3 feedback_mail.py status` reports setup state. Logs are `.feedback-mail.log` and `.feedback-mail-error.log`; local delivery receipts are `.feedback-mail-state.json`. Transport acceptance is recorded, not proof that Gmail placed the message in Inbox. Uncertain sends remain for manual review to avoid duplicate messages.

### Local feedback cache

`feedback-cache.json` keeps full downloaded feedback messages, optional reply addresses, cloud status and local delivery receipts. It is updated before SMTP authentication or sending, so it works even before Gmail setup succeeds. The existing mail LaunchAgent refreshes it every minute while this Mac is awake and online. Unsent, uncertain and delivered messages stay in the cache; absent cloud records never remove local copies. The file is private to the current user (0600), excluded from Git, and contains no SMTP credentials. Run `python3 feedback_mail.py cache` to refresh without sending. Messages not yet downloaded remain in the hosted queue while the Mac is offline. Delivery still requires cloud claim checks to avoid duplicates.

## Automatic GitHub publishing

The standalone `tools/github_sync.py` LaunchAgent checks every five minutes. It publishes committed websites, settled local tools/documents and final packaged shaders, then uploads new shader release ZIPs and visual reports. It uses no ChatGPT automation. Configuration and recovery guidance are in `tools/GITHUB-SYNC.md`. Private feedback, credentials and runtime delivery state are excluded.

## Separate run batches

Run changes, Stage & send and Run Changes + TASK.md preserve the submitted CHANGES.md and TASK.md as a durable, independent batch. The shared Pending changes section is cleared for the next requests after the cloud transaction saves the job and snapshots (or after confirmed local CLI delivery). Saves and staging-only actions do not clear it. New edits never invalidate a detached batch or get silently included in its coding pass.

The Mac materialises each active brief under `work/Custom instructions/IN-PROGRESS/<request-id>/CHANGES.md`, with its TASK.md snapshot. The coder reconciles this active brief and moves only verified items into COMPLETED-CHANGES.md. Unfinished work stays in the active batch. `.bridge` snapshots and cloud job metadata retain the original submission, and revision history retains the previous editor text. Open Chat → Saved batches & delivery receipts → View saved batch to inspect an original submission. Delivery states are not implementation status. A failed/uncertain delivery retains its batch for recovery; inspect its receipt before resubmitting.

The cloud bridge dispatches frozen batches in queue order, independently of later document edits. Existing older jobs retain their original revision checks. Pending clearing uses revision checks so later edits are preserved. Sending while a batch is being coded queues the next batch; it does not start a parallel coder or interrupt the current one.
