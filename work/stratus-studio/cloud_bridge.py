#!/usr/bin/env python3
"""Sync the private cloud Studio with this Mac; credentials stay in Keychain."""
import fcntl
import hashlib
import json
import shlex
import ssl
import subprocess
import sys
import termios
import time
import urllib.error
import urllib.request
from pathlib import Path
from datetime import datetime, timezone
import server

ACCOUNT='bridge'
SERVICE='stratus-studio-cloud'
STATE=server.HERE/'.cloud-sync-state.json'
TLS=ssl.create_default_context(cafile='/etc/ssl/cert.pem')

def sha(text):return hashlib.sha256(text.encode()).hexdigest()

def request(url,method='GET',body=None,headers=None):
    data=None if body is None else json.dumps(body).encode()
    req=urllib.request.Request(url,data=data,method=method,headers={'Content-Type':'application/json',**(headers or {})})
    with urllib.request.urlopen(req,timeout=40,context=TLS) as reply:return json.load(reply)

def configure(config):
    command='add-generic-password -U -a '+ACCOUNT+' -s '+SERVICE+' -w '+shlex.quote(json.dumps(config))+'\n'
    result=subprocess.run(['security','-i'],input=command,text=True,capture_output=True)
    if result.returncode:raise RuntimeError('Could not save the private connection in macOS Keychain.')

def load_config():
    result=subprocess.run(['security','find-generic-password','-a',ACCOUNT,'-s',SERVICE,'-w'],text=True,capture_output=True)
    if result.returncode:raise RuntimeError('Cloud connection is not configured in macOS Keychain.')
    return json.loads(result.stdout)

def save_cloud_document(key, other, expected_revision):
    """Preserve revision checks and backups without requiring the local web server."""
    current=server.document(key)
    if current['revision']!=expected_revision:return False
    folder=server.HISTORY/key
    folder.mkdir(parents=True,exist_ok=True)
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    server.atomic_write(folder/(stamp+'-'+current['revision'][:12]+'.md'),current['text'].encode())
    if server.document(key)['revision']!=expected_revision:return False
    if key=='spec' and not server.SPEC_STAGE_BASE.exists():
        server.BRIDGE.mkdir(exist_ok=True)
        server.atomic_write(server.SPEC_STAGE_BASE,current['text'].encode())
    server.atomic_write(server.DOCUMENTS[key],other['text'].encode())
    return server.document(key)['revision']==other['revision']

def main():
    lock=open(server.HERE/'.cloud-bridge.lock','w')
    try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:
        print('Cloud bridge is already running.',flush=True);return
    if '--configure' in sys.argv:
        if sys.stdin.isatty():
            attributes=termios.tcgetattr(sys.stdin.fileno())
            attributes[3] &= ~termios.ECHO
            termios.tcsetattr(sys.stdin.fileno(),termios.TCSANOW,attributes)
        print('Ready for private connection JSON on stdin (input is hidden).',flush=True)
        config=json.loads(sys.stdin.readline());configure(config)
    else:config=load_config()
    headers={'OAI-Sites-Authorization':'Bearer '+config['token'],'X-Stratus-Bridge':config['key']}
    base=config['url'].rstrip('/')
    cloud=lambda path,method='GET',body=None:request(base+path,method,body,headers)
    sync=json.loads(STATE.read_text()) if STATE.exists() else config['initial']
    print('Private cloud bridge connected. Credentials are stored in macOS Keychain.',flush=True)
    last_error=None
    public_checked=0
    while True:
        try:
            remote=cloud('/api/bridge/state')
            conflict=[]
            for key in server.DOCUMENTS:
                local=server.document(key);other=remote['documents'][key];previous=sync.get(key,local['revision'])
                if local['revision']==other['revision']:sync[key]=local['revision'];continue
                if local['revision']!=previous and other['revision']!=previous:
                    conflict.append(key);continue
                if other['revision']==previous:
                    cloud('/api/bridge/documents/'+key,'PUT',{'text':local['text'],'revision':other['revision']})
                    sync[key]=local['revision']
                else:
                    if not save_cloud_document(key,other,local['revision']):
                        conflict.append(key);continue
                    sync[key]=other['revision']
            server.atomic_write(STATE,json.dumps(sync).encode())
            activity=(server.DOCS/'CHANGE-LOG.md').read_text()
            cloud('/api/bridge/heartbeat','POST',{'status':'conflict' if conflict else 'online','detail':'Both cloud and Mac edited '+', '.join(conflict)+'. Resolve before running.' if conflict else 'Documents synced.','activity':activity})
            for job in remote['jobs']:
                claim=cloud('/api/bridge/job','POST',{'id':job['id'],'claim':True})
                if not claim['claimed']:continue
                snapshot=claim.get('snapshot')
                detached=bool(snapshot and snapshot.get('detached'))
                if conflict and not detached:
                    cloud('/api/bridge/job','POST',{'id':job['id'],'status':'waiting','detail':'Waiting for document conflicts to be resolved.'});continue
                current={key:server.document(key)['revision'] for key in server.DOCUMENTS}
                if not detached and current!=job['revisions']:
                    cloud('/api/bridge/job','POST',{'id':job['id'],'status':'failed','detail':'Files changed after this request was staged. Review the latest documents and send a new request.'});continue
                # Persistent local request IDs prevent duplicate Codex messages after reconnecting.
                body={'id':job['id'],'operation':job['operation'],'instructions':job['instructions'],'revisions':job['revisions'] if detached else current}
                result=server.send_to_chat(body,frozen=snapshot if detached else None)
                status=result['status'] if result['status'] in ('queued','failed','unknown') else 'unknown'
                cloud('/api/bridge/job','POST',{'id':job['id'],'status':status,'detail':result.get('detail','Check the chat before retrying.'),'queueId':result.get('queueId')})
            if time.monotonic()-public_checked>60:
                public_checked=time.monotonic()
                try:
                    import public_sync
                    if config.get('public'):public_sync.sync()
                except Exception as public_error:
                    print('Public release sync waiting: '+type(public_error).__name__+'. Existing images preserved.',flush=True)
            if last_error:print('Cloud connection restored.',flush=True)
            last_error=None
        except Exception as error:
            message=type(error).__name__+((': '+str(error.reason)) if isinstance(error,urllib.error.URLError) else '')
            if message!=last_error:print('Cloud sync waiting: '+message+'. Files and queued work are preserved.',flush=True)
            last_error=message
        time.sleep(5)

if __name__=='__main__':main()
