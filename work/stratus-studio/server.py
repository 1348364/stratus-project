#!/usr/bin/env python3
"""Stratus Studio: a loopback-only editor for two project Markdown files."""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import mimetypes
import os
import re
import secrets
import shutil
import subprocess
import tempfile
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
DOCS = PROJECT / 'work' / 'Custom instructions'
DOCUMENTS = {'changes': DOCS / 'CHANGES.md', 'spec': DOCS / 'TASK.md'}
HISTORY = HERE / '.history'
DIST = HERE / 'dist'
TOKEN = secrets.token_urlsafe(32)
LOCK = threading.Lock()
MAX_BYTES = 2_000_000
CHAT_ID = '01a15d03-320f-7422-9005-6d7f85ce5aa9'
CHAT_NAME = 'Coding Stratus (2)'
BRIDGE = HERE / '.bridge'
BRIDGE_LOCK = threading.Lock()
SPEC_STAGE_BASE = BRIDGE / 'spec-stage-base.md'
RUN_ACTIONS = ('run', 'stage_run', 'run_both')
BATCHES = DOCS / 'IN-PROGRESS'


def empty_pending(text):
    """Keep document context; move only the unique Pending changes section."""
    headings = list(re.finditer(r'^##[ \t]+Pending changes[ \t]*\r?$', text, re.M | re.I))
    if len(headings) != 1:
        raise ValueError('CHANGES.md needs exactly one ## Pending changes heading before sending a run.')
    heading = headings[0]
    following = re.search(r'^#{1,2}[ \t]+', text[heading.end():], re.M)
    end = heading.end() + following.start() if following else len(text)
    return text[:heading.end()] + '\n\nNo pending changes.\n\n' + text[end:]


def batch_snapshot(request_id):
    return {key: {'text': (BRIDGE / (request_id + '-' + name)).read_text()}
            for key, name in (('changes', 'CHANGES.md'), ('spec', 'TASK.md'))}


def release_pending(snapshot, receipt):
    """Clear only the version sent, never subsequent user or coder edits."""
    with LOCK:
        current = document('changes')
        if current['revision'] != snapshot['revision']:
            receipt['detail'] += ' Newer CHANGES.md edits were preserved.'
            return
        text = empty_pending(snapshot['text'])
        folder = HISTORY / 'changes'
        folder.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        atomic_write(folder / (stamp + '-' + current['revision'][:12] + '.md'), current['text'].encode())
        if document('changes')['revision'] != current['revision']:
            receipt['detail'] += ' Newer CHANGES.md edits were preserved.'
            return
        atomic_write(DOCUMENTS['changes'], text.encode())
        receipt['changesMoved'] = True


def codex_binary():
    bundled = Path('/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex')
    return str(bundled) if bundled.is_file() else shutil.which('codex')


def bridge_requests():
    entries = []
    for path in sorted(BRIDGE.glob('*.json'), key=lambda p: p.stat().st_mtime, reverse=True)[:10]:
        try:
            entries.append(json.loads(path.read_text()))
        except (OSError, ValueError):
            continue
    return entries


def send_to_chat(body, frozen=None):
    operation = body.get('operation')
    instructions = body.get('instructions', '')
    request_id = body.get('id', '')
    if operation not in ('stage', 'run', 'spec', 'stage_run', 'related', 'run_both') or not isinstance(instructions, str) or len(instructions) > 12000:
        raise ValueError('Choose an action and keep instructions under 12,000 characters.')
    if not isinstance(request_id, str) or not re.fullmatch(r'[a-f0-9-]{36}', request_id):
        raise ValueError('A valid request ID is required.')
    if operation in ('spec', 'related') and not instructions.strip():
        raise ValueError('Describe the specification edit or related shader work you want.')
    binary = codex_binary()
    if not binary:
        raise ValueError('Codex CLI was not found. Open the Codex app, then restart Studio.')
    with BRIDGE_LOCK:
        BRIDGE.mkdir(exist_ok=True)
        receipt_path = BRIDGE / (request_id + '.json')
        if receipt_path.exists():
            return json.loads(receipt_path.read_text())
        with LOCK:
            snapshots = frozen if frozen is not None else {key: document(key) for key in DOCUMENTS}
            for key in DOCUMENTS:
                if body.get('revisions', {}).get(key) != snapshots[key]['revision'] or digest(snapshots[key]['text'].encode()) != snapshots[key]['revision']:
                    raise ValueError('Project files changed. Refresh the editor and review them before sending.')
        for key, name in (('changes', 'CHANGES.md'), ('spec', 'TASK.md')):
            atomic_write(BRIDGE / (request_id + '-' + name), snapshots[key]['text'].encode())
        staging_context = ''
        if operation in ('stage_run', 'run_both'):
            before = SPEC_STAGE_BASE.read_text() if SPEC_STAGE_BASE.exists() else snapshots['spec']['text']
            delta = ''.join(difflib.unified_diff(before.splitlines(keepends=True), snapshots['spec']['text'].splitlines(keepends=True), fromfile='TASK.md before staging', tofile='TASK.md requested target'))
            delta_path = BRIDGE / (request_id + '-spec.diff')
            target_path = BRIDGE / (request_id + '-TASK.md')
            changes_path = BRIDGE / (request_id + '-CHANGES.md')
            atomic_write(delta_path, delta.encode())
            atomic_write(target_path, snapshots['spec']['text'].encode())
            atomic_write(changes_path, snapshots['changes']['text'].encode())
            staging_context = f'\nFrozen specification delta: {delta_path}\nFrozen complete target: {target_path}\nFrozen change brief: {changes_path}\n'
        if operation in RUN_ACTIONS:
            empty_pending(snapshots['changes']['text'])
            batch = BATCHES / request_id
            batch.mkdir(parents=True, exist_ok=True)
            for key, name in (('changes', 'CHANGES.md'), ('spec', 'TASK.md')):
                if not (batch / name).exists():
                    atomic_write(batch / name, snapshots[key]['text'].encode())
            staging_context += f'\nActive batch brief: {batch / "CHANGES.md"}\nBatch target snapshot: {batch / "TASK.md"}\n'
        actions = {
            'run_both': 'The user explicitly requests RUN CHANGES + TASK.md. Read both frozen snapshots below and current project instructions, AGENTS.md and GOALS.md. This action authorises implementing pending CHANGES.md requests AND unfinished requirements in the complete TASK.md target, even when there is no new specification delta. Review actual source and recorded verification first; preserve already completed features, controls, preferences and newer edits. Stage concrete unmet TASK.md requirements in CHANGES.md alongside the existing pending requests, then implement and verify them in this chat. Do not rebuild working code merely because TASK.md describes a clean rebuild. Do not treat obsolete wording or missing evidence alone as proof that working features are absent; record verification-only gaps separately and pursue them as appropriate. Resolve genuine conflicts without silently discarding either file. Preserve the intended full target, reconcile only approved completed changes and record actual evidence in CHANGE-LOG.md. Keep unfinished or unverified requests pending. If both files have no actionable unfinished work, report that and stop. Do not message another chat or revive the archived broken coding chat.',
            'related': 'Carry out only the related Stratus shader work explicitly described by the user below, in this chat. Read the project instructions and relevant TASK.md, CHANGES.md and CHANGE-LOG.md context. Saving or attaching these files does not authorise implementing their entire contents or other pending work. Preserve newer user edits and unrelated shader settings. If the requested work changes shader code, follow the project verification, specification reconciliation and completed-change recording rules. Do not send a handoff to another chat.',
            'stage_run': 'The user explicitly requests STAGE AND RUN. Read the frozen specification delta and snapshots below. Stage meaningful added, changed and removed TASK.md requirements as pending items in CHANGES.md, preserving existing pending requests. A removed requirement is a request to remove the corresponding shader behaviour; preserve unrelated controls and clarify high-impact removals as required by project instructions. Ignore formatting-only differences. TASK.md remains the complete absolute target, not an instruction to rebuild everything. Then apply the staged pending requests in this chat, following AGENTS.md and GOALS.md. If the delta is empty, use only existing pending changes and explicit user instructions; do not invent work by comparing the whole target with shader source. If both are empty, report no new work and stop. Reconcile approved completed changes into TASK.md, record actual evidence in CHANGE-LOG.md and leave incomplete or unverified items pending. Preserve newer edits and report conflicts against the frozen snapshots. Do not message another chat or revive the archived broken coding chat.',
            'stage': 'Review the saved CHANGES.md against TASK.md and the project instructions. Refine and stage only the pending change brief in CHANGES.md, preserving user intent. Do not implement shader code or start a coding handoff. Report the staged brief and any unresolved questions.',
            'run': 'The user explicitly requests execution of the saved pending changes in CHANGES.md. Read TASK.md and follow the project AGENTS.md and GOALS.md. Implement only pending requests; preserve unchanged visuals, controls and preferences. If no requests are pending, report that and stop. Record actual verification evidence in CHANGE-LOG.md, reconcile TASK.md only for approved completed changes, and keep incomplete or unverified items pending. Work in this chat; do not message another chat or revive the archived broken coding chat.',
            'spec': 'Modify work/Custom instructions/TASK.md using the user instructions below. TASK.md is the complete absolute shader target and clean-rebuild specification, covering intended look, behaviour, construction and verification, with a quick-edit section for major design choices. It is not an incremental work queue or an inventory of in-game setting defaults. Preserve unrelated requirements and user intent. Follow the latest workflow established in this chat and the project instructions. This action edits the specification only: do not implement shader code or launch a coding handoff. Report exactly what changed.'
        }
        if operation in ('run', 'stage_run', 'run_both'):
            actions[operation] += (' After the required verification, move completed requests out of CHANGES.md Pending changes into the separate work/Custom instructions/COMPLETED-CHANGES.md archive with the release and CHANGE-LOG.md reference. Keep CHANGES.md pending-only; never append completed history to it. Do not leave checked-off completed items under Pending changes. Preserve partial, failed, unverified and newly added user requests. When none remain, leave only "No pending changes." under the heading. Queue delivery or a finished chat turn is never proof that requests are complete.')
            actions[operation] = re.sub(r'(?<![-\w])CHANGES\.md', 'the active batch CHANGES.md', actions[operation])
            staging_context += ('\nBATCH WORKFLOW: Process this saved batch before any later queued batch. '
                'All change staging, implementation and pending-item reconciliation in this request refer to the active batch brief above. '
                'The shared work/Custom instructions/CHANGES.md is now the user\'s NEXT unsent batch: never clear it, replace it, stage into it, or implement new requests from it during this run. '
                'Keep unfinished/unverified items in the active batch brief; move verified items to COMPLETED-CHANGES.md with evidence. '
                'Reconcile the current shared TASK.md carefully, preserving later edits. Frozen .bridge snapshots are immutable delivery evidence. '
                'Report the batch path and remaining work. A queued batch is not completed work.\n')
        prompt = (f'Stratus Studio request {request_id}\nAction: {operation}\nProject: {PROJECT}\n'
                  f'Documents: {DOCS / "CHANGES.md"} and {DOCS / "TASK.md"}\n'
                  f'{actions[operation]}{staging_context}\n\nUser instructions:\n{instructions.strip() or "Use the saved project files."}\n'
                  'Read the current files before editing. If they have changed since this request was queued, preserve later edits and report conflicts. Saving alone is never an execution trigger.')
        receipt = {'id': request_id, 'operation': operation, 'status': 'sending',
                   'created': datetime.now(timezone.utc).isoformat(), 'chat': CHAT_NAME}
        atomic_write(receipt_path, json.dumps(receipt).encode())
    try:
        result = subprocess.run([binary, 'queue', '--thread', CHAT_ID, '--message', prompt],
                                cwd=PROJECT, capture_output=True, text=True, timeout=25)
        match = re.search(r'Queued message ([a-f0-9-]+) for thread ' + CHAT_ID, result.stdout)
        if result.returncode == 0 and match:
            receipt.update(status='queued', queueId=match.group(1), detail='Delivered to the chat queue. Open the chat for progress and results.')
            if operation in ('stage_run', 'run_both'):
                with BRIDGE_LOCK:
                    atomic_write(SPEC_STAGE_BASE, snapshots['spec']['text'].encode())
            if operation in RUN_ACTIONS:
                receipt['batchPath'] = str(BATCHES / request_id / 'CHANGES.md')
                if frozen is None:
                    release_pending(snapshots['changes'], receipt)
        else:
            receipt.update(status='failed', detail=(result.stderr or result.stdout or 'Codex could not queue the request.')[-1800:])
    except subprocess.TimeoutExpired:
        receipt.update(status='unknown', detail='Delivery timed out. Check the chat before sending another request; it may already have arrived.')
    except OSError:
        if receipt.get('status') == 'queued':
            receipt['detail'] += ' Could not clear the pending editor; the saved batch is safe. Do not resend it.'
        else:
            receipt.update(status='failed', detail='Could not launch Codex. Open the Codex app and try again.')
    atomic_write(receipt_path, json.dumps(receipt).encode())
    return receipt


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def document(key: str) -> dict:
    path = DOCUMENTS[key]
    data = path.read_bytes()
    return {'id': key, 'filename': path.name, 'path': str(path),
            'text': data.decode('utf-8'), 'revision': digest(data),
            'modified': datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()}


def atomic_write(path: Path, data: bytes) -> None:
    fd, name = tempfile.mkstemp(prefix='.' + path.name + '-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(name, path.stat().st_mode & 0o777 if path.exists() else 0o600)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


class Handler(BaseHTTPRequestHandler):
    server_version = 'StratusStudio/1.0'

    def log_message(self, fmt, *args):
        if str(args[1] if len(args) > 1 else '') not in ('200', '304'):
            super().log_message(fmt, *args)

    def trusted(self) -> bool:
        allowed = {f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}'}
        if self.headers.get('Host') not in allowed:
            return False
        origin = self.headers.get('Origin')
        return not origin or origin in {f'http://{host}' for host in allowed}

    def reply(self, status: int, value, content_type='application/json; charset=utf-8'):
        data = json.dumps(value, ensure_ascii=False).encode() if content_type.startswith('application/json') else value
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; worker-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if not self.trusted():
            return self.reply(403, {'error': 'Only this local workspace may connect.'})
        route = unquote(urlparse(self.path).path)
        try:
            if route == '/api/workspace':
                spec = document('spec')
                release = re.search(r'Stratus-(\d+\.\d+\.\d+)\.zip', spec['text'])
                return self.reply(200, {'name': 'Stratus Studio', 'project': str(PROJECT),
                    'release': release.group(1) if release else 'Unspecified', 'token': TOKEN,
                    'documents': {'spec': spec, 'changes': document('changes')}})
            if route == '/api/chat':
                return self.reply(200, {'name': CHAT_NAME, 'available': bool(codex_binary()), 'requests': bridge_requests()})
            batch_match = re.fullmatch(r'/api/chat/([a-f0-9-]{36})', route)
            if batch_match:
                return self.reply(200, batch_snapshot(batch_match.group(1)))
            if route == '/api/activity':
                return self.reply(200, {'text': (DOCS / 'CHANGE-LOG.md').read_text(), 'filename': 'CHANGE-LOG.md'})
            match = re.fullmatch(r'/api/history/(changes|spec)(?:/([a-zA-Z0-9.-]+))?', route)
            if match:
                key, name = match.groups()
                folder = HISTORY / key
                if name:
                    if not re.fullmatch(r'\d{8}T\d{12}Z-[a-f0-9]{12}\.md', name):
                        return self.reply(404, {'error': 'Revision not found.'})
                    return self.reply(200, {'text': (folder / name).read_text(), 'name': name})
                entries = sorted(folder.glob('*.md'), reverse=True) if folder.exists() else []
                return self.reply(200, {'entries': [{'name': p.name, 'bytes': p.stat().st_size,
                    'modified': datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat()} for p in entries]})
            if route.startswith('/api/'):
                return self.reply(404, {'error': 'Endpoint not found.'})
            path = (DIST / (route.lstrip('/') or 'index.html')).resolve()
            if not path.is_relative_to(DIST.resolve()) or not path.is_file():
                return self.reply(404, b'Not found', 'text/plain; charset=utf-8')
            mime = mimetypes.guess_type(path)[0] or 'application/octet-stream'
            return self.reply(200, path.read_bytes(), mime + ('; charset=utf-8' if mime.startswith('text/') else ''))
        except FileNotFoundError:
            return self.reply(404, {'error': 'File not found.'})
        except (OSError, UnicodeError):
            return self.reply(500, {'error': 'Could not read the workspace file.'})

    def do_POST(self):
        if not self.trusted() or not secrets.compare_digest(self.headers.get('X-Studio-Token', ''), TOKEN):
            return self.reply(403, {'error': 'Reconnect to the local workspace before sending.'})
        if urlparse(self.path).path != '/api/chat':
            return self.reply(404, {'error': 'Endpoint not found.'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 60000:
                return self.reply(413, {'error': 'Request is too large.'})
            body = json.loads(self.rfile.read(length))
            if not isinstance(body, dict):
                raise ValueError('Invalid request.')
            return self.reply(200, send_to_chat(body))
        except (ValueError, TypeError, AttributeError) as error:
            return self.reply(400, {'error': str(error)})
        except OSError:
            return self.reply(500, {'error': 'Could not record the request. Check the chat before retrying.'})

    def do_PUT(self):
        if not self.trusted() or not secrets.compare_digest(self.headers.get('X-Studio-Token', ''), TOKEN):
            return self.reply(403, {'error': 'Reconnect to the local workspace before saving.'})
        match = re.fullmatch(r'/api/documents/(changes|spec)', urlparse(self.path).path)
        if not match:
            return self.reply(404, {'error': 'This document is not editable.'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= MAX_BYTES:
                return self.reply(413, {'error': 'Document is too large (2 MB maximum).'})
            body = json.loads(self.rfile.read(length))
            if not isinstance(body.get('text'), str) or not isinstance(body.get('revision'), str):
                return self.reply(400, {'error': 'Text and the saved revision are required.'})
            key = match.group(1)
            with LOCK:
                current = document(key)
                if current['revision'] != body['revision']:
                    return self.reply(409, {'error': 'This file changed outside Studio. Compare both versions before saving.', 'document': current})
                new = body['text'].encode('utf-8')
                if digest(new) == current['revision']:
                    return self.reply(200, {'document': current, 'unchanged': True})
                folder = HISTORY / key
                folder.mkdir(parents=True, exist_ok=True)
                stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
                backup = folder / f'{stamp}-{current["revision"][:12]}.md'
                atomic_write(backup, current['text'].encode('utf-8'))
                if key == 'spec' and not SPEC_STAGE_BASE.exists():
                    BRIDGE.mkdir(exist_ok=True)
                    atomic_write(SPEC_STAGE_BASE, current['text'].encode('utf-8'))
                if digest(DOCUMENTS[key].read_bytes()) != body['revision']:
                    return self.reply(409, {'error': 'The file changed while saving. Your editor text is still intact.', 'document': document(key)})
                atomic_write(DOCUMENTS[key], new)
                return self.reply(200, {'document': document(key), 'backup': backup.name})
        except (ValueError, KeyError, TypeError):
            return self.reply(400, {'error': 'Invalid save request.'})
        except OSError:
            return self.reply(500, {'error': 'Could not save. Your editor text is still intact.'})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    for key in DOCUMENTS:
        if not DOCUMENTS[key].is_file():
            parser.error(f'Missing {DOCUMENTS[key]}')
    BRIDGE.mkdir(exist_ok=True)
    if not SPEC_STAGE_BASE.exists():
        atomic_write(SPEC_STAGE_BASE, DOCUMENTS['spec'].read_bytes())
    server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    print(f'Stratus Studio is ready at http://127.0.0.1:{server.server_port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nStudio stopped. Your saved documents are in the project.', flush=True)
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
