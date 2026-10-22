# Stratus project archive

Private source archive of the Stratus Minecraft Iris shader, public showcase, private Studio, release workflow, feedback sender and completed development tooling.

## Layout

- `outputs/Stratus/`: editable shader, packaging/installation tools, textures and licence.
- `work/Custom instructions/`: complete target, pending requests, completed archive and release evidence log.
- `work/stratus-public/`: public site and standalone visual effects.
- `work/stratus-studio-cloud/`: private editor/server source.
- `work/stratus-studio/`: local editor, cloud sync, automatic release posting, SMTP mail and cache.
- Remaining work folders: authored QA, research, verification reports and helper source.
- GitHub Release assets: historical shader builds, labelled visual reports and development imagery.

The archive preserves documented verification limits. Source, packaging, actual Minecraft visual checks and measured performance are separate states. Pending performance or scene acceptance is not marked complete by this backup.

## Running

Read the README beside the relevant component. Websites use their existing Sites hosting configuration; server credentials must be configured separately. Local Studio uses its documented start command. Standalone mail setup uses macOS Keychain. No secrets or private feedback are included.

## Refreshing this archive

In the original project, run `python3 tools/export_github.py`, inspect `EXPORT-MANIFEST.json`, then commit/push this checkout and upload the regenerated release asset ZIPs. Uploads require an authenticated GitHub CLI. This export uses no model calls or ChatGPT automation.
