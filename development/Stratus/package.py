"""Create the standalone installable Stratus archive, checking every entry."""
import hashlib
import json
import tempfile
import zipfile
from pathlib import Path


def package():
    project = Path(__file__).resolve().parent
    suffixes = {'.vsh', '.gsh', '.fsh', '.glsl', '.properties', '.lang', '.rgba8', '.mcmeta'}
    sources = sorted(p for p in project.joinpath('shaders').rglob('*')
                     if p.is_file() and p.suffix in suffixes)
    checksums = [dict(path=p.relative_to(project).as_posix(),
                      bytes=p.stat().st_size,
                      sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sources]
    project.joinpath('SOURCE-MANIFEST.json').write_text(json.dumps(checksums, indent=2) + '\n')
    documents = ['README.txt', 'VALIDATION.txt', 'IN-GAME-TEST.txt', 'CHECKS.json', 'LICENSE.txt',
                 'SOURCE-MANIFEST.json', 'package.py', 'generate_volume.py', 'install.py', 'RELEASE-POLICY.json']
    contents = sources + [project / name for name in documents]
    for item in contents:
        if not item.is_file():
            raise FileNotFoundError(item)
    destination = project.parent / 'Stratus-1.7.0-rc2.zip'
    with tempfile.TemporaryDirectory(prefix='stratus-package-', dir=project.parent) as scratch:
        pending = Path(scratch) / destination.name
        with zipfile.ZipFile(pending, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for item in contents:
                archive.write(item, item.relative_to(project).as_posix())
        with zipfile.ZipFile(pending) as archive:
            if archive.testzip():
                raise RuntimeError('ZIP integrity failure')
            for item in contents:
                if archive.read(item.relative_to(project).as_posix()) != item.read_bytes():
                    raise RuntimeError(f'Packaged source mismatch: {item}')
        pending.replace(destination)
    print(f'{destination.name}: {len(contents)} files, {destination.stat().st_size:,} bytes; integrity verified')


if __name__ == '__main__':
    package()
