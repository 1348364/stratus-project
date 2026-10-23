# Automatic Stratus GitHub sync

The macOS LaunchAgent `au.stratus.project.github-sync` checks every five minutes while this Mac is awake and logged in. It runs `tools/github_sync.py run` directly, uses the existing authenticated GitHub CLI and makes no model calls or ChatGPT automation requests. GitHub auth must remain valid.

## What gets pushed

- Website source from committed HEAD in the public and developer Site repositories. Uncommitted source is additionally preserved under `development/<site>/`, clearly separate from deployed source; regenerable build caches are excluded.
- Final packaged shader contents from the latest completed CHANGE-LOG.md release heading with a matching install receipt SHA remain under `outputs/Stratus/`. Settled editable shader source, including work in progress, is backed up separately under `development/Stratus/`. Release candidates are never labelled as final releases.
- Standalone Studio/tools source, project documents, authored QA/helper/report source across work folders, release metadata and curated showcase images. New or changed files are observed independently across two checks at least 60 seconds apart; active editing in one folder no longer blocks settled files elsewhere.
- A new `shader-vVERSION` GitHub Release with the final shader ZIP and labelled visual-report ZIP. Existing historical project-backup downloads are retained and are not re-uploaded every five minutes.

The script scans text/structured data for likely credentials, excludes private feedback and delivery state, and checks the authorised repository visibility. It follows the repository's stable numeric ID, so GitHub username changes can be resolved automatically. It refuses unexpected remotes, a dirty export checkout, non-fast-forward changes or mismatched release assets. It never force-pushes. Failures leave files/commits for review and are logged; authentication/network failures can retry on the next run when safe.

Each new/changed file settles independently. The first poll records a candidate; an unchanged later poll publishes it. Source and asset failures update the status instead of leaving a stale “Up to date” message. A Mac that is asleep or offline catches up after waking and reconnecting. Published files remain on GitHub while this Mac is offline.

## Files and commands

- Configuration, no secrets: `tools/github-sync.json`.
- Export checkout: `work/stratus-github/`.
- Local state: `work/stratus-studio/.github-sync-state.json`.
- Logs: `work/stratus-studio/.github-sync.log` and `.github-sync-error.log`.
- Status: `python3 tools/github_sync.py status`.
- Run once: `python3 tools/github_sync.py run`.
- Install/reinstall service: `python3 tools/github_sync.py install`.

GitHub source and release archives are now authorised to be public. Credentials and visitor feedback stay local/private. Do not add them to the export checkout. If the script stops for local checkout changes or remote conflicts, review those changes before resuming; do not reset or force-push blindly.

## Comprehensive work backups

Large release archives, original captures, QA packs and other authored binary work are catalogued in `WORK-BACKUP-INDEX.json` in the GitHub repository. Each record identifies the original project-relative path, checksum and containing GitHub Release asset. Existing historical bundles are reused only after their archive hashes match GitHub; their original contents are indexed with SHA-256. New/changed assets are checked independently for stability, scanned for credentials in textual archive entries, grouped into bounded immutable ZIPs and uploaded to the prerelease `project-work-snapshots`. Uploaded archive hashes are verified before the index points at them. Work snapshots may be unfinished and must not be mistaken for final shader releases.

Private feedback, Keychain/credentials, raw app logs, compiled caches, third-party Minecraft runtime and regenerable website deployment bundles remain excluded. Settled source files are published in Git; large binary evidence is in Releases rather than being silently omitted. The generated root README and index explain both locations.
