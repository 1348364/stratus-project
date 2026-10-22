#!/usr/bin/env python3
"""Prepare bounded shader context locally. No model, network or shader changes."""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import tempfile
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]


def read(path):
    return path.read_text() if path.is_file() else ''


def fingerprint(path):
    if not path.is_file():
        return 'missing'
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix='.' + path.name)
    try:
        with os.fdopen(fd, 'w') as handle:
            handle.write(text)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def prepare_context(project=PROJECT, batch=None):
    project = Path(project)
    docs = project / 'work' / 'Custom instructions'
    output = Path(batch) if batch else docs
    target = output / 'TASK.md' if batch else docs / 'TASK.md'
    brief = output / 'CHANGES.md' if batch else docs / 'CHANGES.md'
    shaders = project / 'outputs' / 'Stratus' / 'shaders'
    paths = sorted(p for p in shaders.rglob('*') if p.is_file()) if shaders.exists() else []
    source_hash = hashlib.sha256()
    for path in paths:
        relative = path.relative_to(shaders).as_posix()
        source_hash.update(relative.encode() + b'\0' + bytes.fromhex(fingerprint(path)))
    lines = [
        '# Shader context — generated locally',
        '',
        'Navigation and fingerprints only; this file does not certify a release or authorise additional work.',
        f'Project: {project}',
        f'Active brief: {brief}',
        f'Target snapshot: {target}',
        f'Brief SHA256: {fingerprint(brief)}',
        f'Target SHA256: {fingerprint(target)}',
        f'Current shared TASK SHA256: {fingerprint(docs / "TASK.md")}',
        f'Current shader tree SHA256: {source_hash.hexdigest()} ({len(paths)} files)',
        '',
        '## Read first',
        '- Project AGENTS.md, work/Custom instructions/AGENTS.md, GOALS.md and WORKFLOW.md.',
        '- Active brief and applicable TASK.md. Read unchanged documents once per context; use hashes to detect changes.',
        '- PROGRESS.md, if resuming this batch. Recheck changed files and relevant runtime state before reusing evidence.',
        '- Relative links copied into a batch brief resolve from work/Custom instructions, their original location.',
        '',
        '## Target section index',
    ]
    headings = [(number, text) for number, text in enumerate(read(target).splitlines(), 1)
                if re.match(r'^#{1,3}\s+', text)]
    lines.extend(f'- Line {number}: {text.lstrip("# ")}' for number, text in headings[:36])
    if len(headings) > 36:
        lines.append('- Further sections remain in TASK.md; this index is intentionally bounded.')
    lines += ['', '## Current source navigation hints']
    words = set(re.findall(r'[a-z]{4,}', read(brief).lower()))
    candidates = [p for p in paths if p.suffix in ('.glsl', '.properties') and 'lang' not in p.parts]
    def score(path):
        name = path.stem.lower().replace('-', ' ')
        return sum(word in name or name in word for word in words)
    ranked = sorted(candidates, key=lambda p: (-score(p), p.as_posix()))
    selected = [p for p in ranked if score(p)][:10]
    for relative in ('core/options.glsl', 'shaders.properties'):
        path = shaders / relative
        if path.is_file() and path not in selected:
            selected.append(path)
    lines.extend(f'- {path.relative_to(project)}' for path in selected)
    lines += ['- outputs/Stratus/package.py and outputs/Stratus/install.py: existing release tooling.',
              'Hints are filename matches only, not a diagnosis or a complete dependency list.',
              '', '## Latest recorded release summary — reported evidence, not a live check']
    changelog = read(docs / 'CHANGE-LOG.md').splitlines()
    started = False
    summary = []
    for line in changelog:
        if line.startswith('## ') and not started:
            started = True
            summary.append(line)
        elif started:
            if line.startswith('## ') or (line.startswith('### ') and 'At a glance' not in line):
                break
            summary.append(line)
    lines.extend(summary[:16] or ['No recorded release summary found.'])
    lines += ['', 'For earlier evidence, search the exact version or issue in CHANGE-LOG.md; do not dump its entire history.', '']
    destination = output / ('CONTEXT.md' if batch else 'CURRENT-CONTEXT.md')
    atomic_text(destination, '\n'.join(lines))
    if batch and not (output / 'PROGRESS.md').exists():
        atomic_text(output / 'PROGRESS.md', '''# Batch progress

Status: not started

## Resume here
- Next action:
- Changed files:
- Current source/target fingerprints (refresh CONTEXT.md before resuming):

## Evidence and remaining work
- Checks completed (command, exact build/source, result, evidence path):
- Visual/FPS verification still required:
- Blockers:
- Unfinished requests remain in this batch's CHANGES.md.

Update this checkpoint at meaningful milestones and before stopping, not after every tool call.
''')
    return destination


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', type=Path, help='Existing IN-PROGRESS batch directory')
    args = parser.parse_args()
    if args.batch:
        batch = args.batch.resolve()
        if not batch.is_relative_to(PROJECT / 'work' / 'Custom instructions' / 'IN-PROGRESS') or not (batch / 'CHANGES.md').is_file():
            parser.error('--batch must name an existing project IN-PROGRESS batch')
    print(prepare_context(batch=args.batch))
