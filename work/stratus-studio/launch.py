#!/usr/bin/env python3
"""Start Studio, wait for readiness, and open it in the default browser."""
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path

HERE = Path(__file__).resolve().parent
URL = 'http://127.0.0.1:8765'


def ready():
    try:
        with urllib.request.urlopen(URL + '/api/workspace', timeout=1) as response:
            value = json.load(response)
            return value.get('name') == 'Stratus Studio' and value.get('project') == str(HERE.parents[1])
    except (OSError, ValueError):
        return False


def start_cloud_bridge():
    result = subprocess.run(['security', 'find-generic-password', '-a', 'bridge', '-s', 'stratus-studio-cloud'], capture_output=True)
    if result.returncode == 0:
        with (HERE / '.cloud-bridge.log').open('a') as log:
            subprocess.Popen([sys.executable, str(HERE / 'cloud_bridge.py')], cwd=HERE, stdout=log, stderr=log, start_new_session=True)


if ready():
    start_cloud_bridge()
    print('Stratus Studio is already running. Opening your workspace.')
    webbrowser.open(URL)
    sys.exit(0)

process = subprocess.Popen([sys.executable, str(HERE / 'server.py'), '--port', '8765'], cwd=HERE)
try:
    for _ in range(60):
        if process.poll() is not None:
            print('Studio could not start. Port 8765 may be in use. Check the message above.')
            input('Press Return to close.')
            sys.exit(1)
        if ready():
            start_cloud_bridge()
            webbrowser.open(URL)
            print('Keep this window open while editing. Press Control-C to stop Studio.')
            process.wait()
            break
        time.sleep(0.2)
    else:
        print('Studio did not become ready. Close this window and try again.')
        process.terminate()
except KeyboardInterrupt:
    process.terminate()
    process.wait()
