"""Install a Stratus release and migrate only unrelated option overrides.

Old preferences and existing new-version preferences are never overwritten.
Run with --dry-run to inspect the exact migration before touching a profile.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile
import zipfile


def read_values(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    result = {}
    for line in path.read_text().splitlines():
        if '=' in line and not line.lstrip().startswith('#'):
            key, value = line.split('=', 1)
            result[key.strip()] = value.strip()
    return result


def migrate(values: dict[str, str], policy: dict) -> tuple[dict, dict]:
    related = set(policy['reset_related_overrides'])
    carried = {k: v for k, v in values.items() if k not in related}
    reset = {k: v for k, v in values.items() if k in related}
    if policy.get('preserve_newer_manual_overrides'):
        captured = policy['captured_previous_values']
        previous_defaults = policy['previous_source_defaults']
        for key in related:
            latest = values.get(key, previous_defaults[key])
            if latest != captured[key]:
                carried[key] = latest
                reset.pop(key, None)
    return carried, reset


def create_if_absent(path: Path, data: bytes) -> bool:
    """Atomically create, never replace a user's existing settings/archive."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(prefix='.stratus-', dir=path.parent, delete=False) as f:
        temporary = Path(f.name)
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    try:
        try:
            os.link(temporary, path)
            return True
        except FileExistsError:
            return False
    finally:
        temporary.unlink()


def install(archive: Path, profile: Path, previous_settings: Path | None = None,
            dry_run: bool = False) -> dict:
    archive = archive.resolve()
    profile = profile.resolve()
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None:
            raise ValueError('ZIP integrity failure')
        policy = json.loads(z.read('RELEASE-POLICY.json'))
    expected_name = f"Stratus-{policy['version']}.zip"
    if archive.name != expected_name:
        raise ValueError(f'Expected release archive {expected_name}')
    destination = profile / 'shaderpacks' / archive.name
    settings = destination.with_suffix('.zip.txt')
    if previous_settings is None:
        selected = read_values(profile / 'config/iris.properties').get('shaderPack')
        if selected:
            # Iris names packs by basename; do not accept paths outside shaderpacks.
            if Path(selected).name != selected:
                raise ValueError('Selected shader name is not a basename')
            previous_settings = profile / 'shaderpacks' / (selected + '.txt')
    if previous_settings is not None:
        previous_settings = previous_settings.resolve()
        if previous_settings == settings:
            previous_settings = None
    original = read_values(previous_settings) if previous_settings else {}
    preserved, reset = migrate(original, policy)
    data = archive.read_bytes()
    if destination.exists() and destination.read_bytes() != data:
        raise FileExistsError(f'Refusing to replace different archive: {destination}')
    settings_existed = settings.exists()
    result = {'version': policy['version'], 'source': str(archive),
              'installed': str(destination), 'sha256': hashlib.sha256(data).hexdigest(),
              'previous_settings': str(previous_settings) if previous_settings else None,
              'unrelated_overrides_carried': preserved, 'related_overrides_reset': reset,
              'related_visual_defaults': policy['visual_defaults'],
              'newer_manual_overrides_preserved': {k: v for k, v in preserved.items() if k in policy['reset_related_overrides']},
              'existing_new_version_preferences_preserved': settings_existed,
              'dry_run': dry_run, 'loaded': False}
    if not dry_run:
        result['archive_created'] = create_if_absent(destination, data)
        if not result['archive_created'] and destination.read_bytes() != data:
            raise FileExistsError(f'Refusing conflicting concurrently created archive: {destination}')
        contents = '# Stratus: unrelated overrides migrated; related controls use release/preset defaults.\n'
        contents += ''.join(f'{k}={v}\n' for k, v in sorted(preserved.items()))
        result['preferences_created'] = create_if_absent(settings, contents.encode())
        result['migration_applied'] = result['preferences_created']
        # A concurrent settings writer wins; never overwrite its data.
        result['existing_new_version_preferences_preserved'] |= not result['preferences_created']
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', type=Path, required=True)
    parser.add_argument('--archive', type=Path)
    parser.add_argument('--previous-settings', type=Path)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    policy = json.loads(Path(__file__).with_name('RELEASE-POLICY.json').read_text())
    archive = args.archive or Path(__file__).resolve().parent.parent / f"Stratus-{policy['version']}.zip"
    print(json.dumps(install(archive, args.profile, args.previous_settings, args.dry_run), indent=2))


if __name__ == '__main__':
    main()
