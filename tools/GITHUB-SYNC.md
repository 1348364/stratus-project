# Automatic Stratus GitHub sync

The macOS LaunchAgent `au.stratus.project.github-sync` checks every five minutes while this Mac is awake and logged in. It runs `tools/github_sync.py run` directly, uses the existing authenticated GitHub CLI and makes no model calls or ChatGPT automation requests. GitHub auth must remain valid.

## What gets pushed

- Website source from committed HEAD in the public and developer Site repositories. Uncommitted website edits are excluded.
- Final packaged shader contents from the latest completed CHANGE-LOG.md release heading with a matching install receipt SHA. Editable shader changes in progress never replace a final packaged runtime in GitHub.
- Standalone Studio/tools source and project documents after the same complete snapshot is observed on two checks at least 60 seconds apart. CHANGES.md may contain pending requests as records; this does not publish unfinished shader implementation.
- A new `shader-vVERSION` GitHub Release with the final shader ZIP and labelled visual-report ZIP. Existing historical project-backup downloads are retained and are not re-uploaded every five minutes.

The script scans text/structured data for likely credentials, excludes private feedback and delivery state, and checks the authorised repository visibility. It follows the repository's stable numeric ID, so GitHub username changes can be resolved automatically. It refuses unexpected remotes, a dirty export checkout, non-fast-forward changes or mismatched release assets. It never force-pushes. Failures leave files/commits for review and are logged; authentication/network failures can retry on the next run when safe.

The first poll records a candidate; an unchanged later poll publishes it. A Mac that is asleep or offline catches up after waking and reconnecting. Published files remain on GitHub while this Mac is offline.

## Files and commands

- Configuration, no secrets: `tools/github-sync.json`.
- Export checkout: `work/stratus-github/`.
- Local state: `work/stratus-studio/.github-sync-state.json`.
- Logs: `work/stratus-studio/.github-sync.log` and `.github-sync-error.log`.
- Status: `python3 tools/github_sync.py status`.
- Run once: `python3 tools/github_sync.py run`.
- Install/reinstall service: `python3 tools/github_sync.py install`.

GitHub source and release archives are now authorised to be public. Credentials and visitor feedback stay local/private. Do not add them to the export checkout. If the script stops for local checkout changes or remote conflicts, review those changes before resuming; do not reset or force-push blindly.
