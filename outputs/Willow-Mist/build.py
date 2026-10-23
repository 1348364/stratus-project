#!/usr/bin/env python3
"""Rebuild Willow-Mist-2.0.zip using only the Python standard library."""
from hashlib import sha256
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


def main():
    root = Path(__file__).resolve().parent
    shader_files = sorted(p for p in (root / "shaders").rglob("*") if p.is_file())
    manifest = "".join(f"{sha256(p.read_bytes()).hexdigest()}  {p.relative_to(root).as_posix()}\n" for p in shader_files)
    (root / "SOURCE-SHA256.txt").write_text(manifest)
    files = shader_files + [root / name for name in
        ("README.txt", "VALIDATION.txt", "LICENSE.txt", "SOURCE-SHA256.txt", "build.py")]
    for path in files:
        if not path.is_file():
            raise FileNotFoundError(path)
    target = root.parent / "Willow-Mist-2.0.zip"
    with ZipFile(target, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(files):
            entry = ZipInfo(path.relative_to(root).as_posix(), (2026, 10, 16, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            entry.external_attr = 0o644 << 16
            archive.writestr(entry, path.read_bytes())
    with ZipFile(target) as archive:
        if archive.testzip() is not None:
            raise RuntimeError("Archive integrity check failed")
        for path in files:
            if archive.read(path.relative_to(root).as_posix()) != path.read_bytes():
                raise RuntimeError(f"Archive/source mismatch: {path}")
    print(f"Built {target.name}: {len(files)} files, {target.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
