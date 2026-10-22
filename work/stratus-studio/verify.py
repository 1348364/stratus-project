#!/usr/bin/env python3
"""Focused HTTP checks against disposable documents; never edits real specs."""
import argparse
import importlib.util
import json
import tempfile
import threading
import urllib.error
import urllib.request
from pathlib import Path
from http.server import ThreadingHTTPServer

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('studio_server', HERE / 'server.py')
studio = importlib.util.module_from_spec(spec)
spec.loader.exec_module(studio)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--serve-fixture', action='store_true')
    args = parser.parse_args()
    originals = {key: path.read_bytes() for key, path in studio.DOCUMENTS.items()}
    with tempfile.TemporaryDirectory(prefix='stratus-studio-check-') as temp:
        root = Path(temp)
        studio.HISTORY = root / 'history'
        studio.DOCUMENTS = {key: root / path.name for key, path in studio.DOCUMENTS.items()}
        for key, value in originals.items():
            studio.DOCUMENTS[key].write_bytes(value)
        server = ThreadingHTTPServer(('127.0.0.1', 8766 if args.serve_fixture else 0), studio.Handler)
        if args.serve_fixture:
            print('Disposable browser-QA workspace ready at http://127.0.0.1:8766', flush=True)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass
            finally:
                server.server_close()
            return
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f'http://127.0.0.1:{server.server_port}'
        results = []

        def request(route, data=None, headers=None):
            request_headers = {'X-Studio-Token': studio.TOKEN, 'Content-Type': 'application/json', **(headers or {})}
            req = urllib.request.Request(base + route, data=json.dumps(data).encode() if data is not None else None,
                headers=request_headers, method='PUT' if data is not None else 'GET')
            try:
                with urllib.request.urlopen(req) as response:
                    raw = response.read()
                    return response.status, json.loads(raw) if response.headers['Content-Type'].startswith('application/json') else raw
            except urllib.error.HTTPError as error:
                return error.code, json.loads(error.read())

        def check(name, condition):
            assert condition, name
            results.append(name)

        try:
            status, workspace = request('/api/workspace')
            check('Both actual document formats load', status == 200 and set(workspace['documents']) == {'spec', 'changes'})
            old = workspace['documents']['changes']
            status, result = request('/api/documents/changes', {'text': old['text'] + '\n- [ ] Fixture test\n', 'revision': old['revision']})
            check('Saving writes the fixture document', status == 200 and studio.DOCUMENTS['changes'].read_text().endswith('Fixture test\n'))
            check('A byte-preserving backup exists', next((studio.HISTORY / 'changes').glob('*.md')).read_bytes() == originals['changes'])
            status, result = request('/api/documents/changes', {'text': 'stale overwrite', 'revision': old['revision']})
            check('Stale saves are blocked with current text', status == 409 and result['document']['text'].endswith('Fixture test\n'))
            status, history = request('/api/history/changes')
            check('History lists the previous version', status == 200 and len(history['entries']) == 1)
            status, result = request('/api/history/changes/' + history['entries'][0]['name'])
            check('History retrieves original text', status == 200 and result['text'] == old['text'])
            status, result = request('/api/documents/changes', {'text': 'bad token', 'revision': old['revision']}, {'X-Studio-Token': 'invalid'})
            check('Unauthorised writes are rejected', status == 403)
            status, result = request('/api/workspace', headers={'Host':'outside.example'})
            check('Untrusted hosts are rejected', status == 403)
            status, result = request('/api/workspace', headers={'Origin':'https://outside.example'})
            check('Cross-origin requests are rejected', status == 403)
            status, result = request('/api/documents/log', {'text':'never', 'revision':'never'})
            check('Only the two intended files are editable', status == 404)
            status, result = request('/api/history/changes/not-a-revision.md')
            check('Invalid revision filenames are rejected', status == 404)
            status, html = request('/')
            check('Home page and editor controls are served', status == 200 and b'editor-view' in html and b'hero-image' in html)
            status, image = request('/assets/river.png')
            check('Actual shader screenshot is served', status == 200 and image.startswith(b'\x89PNG'))
            current = studio.document('spec')
            status, result = request('/api/documents/spec', {'text': current['text'], 'revision': current['revision']})
            check('Saving unchanged text creates no revision', status == 200 and result['unchanged'] and not (studio.HISTORY / 'spec').exists())
            print(json.dumps({'passed':len(results),'checks':results,'scope':'Disposable fixtures only; actual project documents not written'}, indent=2))
        finally:
            server.shutdown()
            server.server_close()


if __name__ == '__main__':
    main()
