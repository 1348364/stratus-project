# Stratus Studio cloud

Private owner-only deployment. Sign in with the same ChatGPT account on desktop or mobile.

The hosted API stores TASK.md, CHANGES.md, revision history and queued actions in D1. The original Mac files sync through `../stratus-studio/cloud_bridge.py`. The bridge stores its private connection in macOS Keychain, checks both file revisions, preserves backups and stops on conflicting edits. It does not expose a port on the Mac to the internet.

Cloud saves and queued requests remain available while the Mac is offline. Model work needs the Mac awake, signed in to Codex, and Studio's local server and cloud bridge running. Double-click the original `start.command` after restarting the Mac to reconnect. No system startup service is installed.

Queued receipts confirm delivery, not shader completion. Read Instructions midway node for execution results. Editing a queued document again before delivery invalidates that request; review and send again. Conflicting edits on both devices are preserved and require reconciliation before work runs.

Runtime secret `BRIDGE_KEY` lives in Sites. The platform service token and bridge key are kept out of source and browser code. The bootstrap config is passed on stdin and stored only in Keychain. Existing site audience must stay owner-only.

Stage & send automatically saves unsaved CHANGES.md and TASK.md edits before queueing. It waits for an in-progress save and uses the resulting saved revisions. Failed saves, unresolved file conflicts, unrecovered browser drafts or edits arriving during the save stop delivery. A successfully saved document stays saved if a later document fails; no request is queued until both are ready. Other chat actions retain their existing explicit-save workflow.
