#!/usr/bin/env python3
"""Forward the private Stratus feedback outbox through Gmail SMTP. No AI calls."""
from __future__ import annotations
import argparse
import fcntl
import getpass
import json
import os
from pathlib import Path
import plistlib
import re
import shlex
import smtplib
import ssl
import subprocess
import sys
from datetime import datetime, timezone
from email.message import EmailMessage
from email.policy import SMTP
import public_sync
import server

SERVICE='stratus-feedback-mail'
ACCOUNT='smtp'
LABEL='au.stratus.studio.feedback-mail'
STATE=server.HERE/'.feedback-mail-state.json'
CACHE=server.HERE/'feedback-cache.json'
PLIST=Path.home()/'Library/LaunchAgents'/f'{LABEL}.plist'
PYTHON=Path('/Library/Frameworks/Python.framework/Versions/3.14/bin/python3')

class SetupError(Exception):
    """A deliberately safe message that contains no credentials."""

def valid_email(value):
    # Google Workspace accounts may use a custom domain.
    return bool(re.fullmatch(r'[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+',value))

def credentials():
    r=subprocess.run(['security','find-generic-password','-a',ACCOUNT,'-s',SERVICE,'-w'],capture_output=True,text=True)
    if r.returncode:return None
    c=json.loads(r.stdout)
    if not valid_email(c.get('email','')) or not re.fullmatch(r'[A-Za-z0-9]{16}',c.get('password','')):
        raise SetupError('Saved mail configuration is incomplete. Run feedback-mail-setup.command again.')
    return c

def connect(c):
    client=smtplib.SMTP_SSL('smtp.gmail.com',465,timeout=30,context=public_sync.bridge.TLS)
    try:client.login(c['email'],c['password'])
    except BaseException:
        client.close();raise
    return client

def install():
    config={'Label':LABEL,'ProgramArguments':[str(PYTHON),str(server.HERE/'feedback_mail.py'),'run'],'WorkingDirectory':str(server.PROJECT),'RunAtLoad':True,'StartInterval':60,'ProcessType':'Background','StandardOutPath':str(server.HERE/'.feedback-mail.log'),'StandardErrorPath':str(server.HERE/'.feedback-mail-error.log')}
    PLIST.parent.mkdir(parents=True,exist_ok=True)
    PLIST.write_bytes(plistlib.dumps(config))
    target=f'gui/{os.getuid()}/{LABEL}'
    subprocess.run(['launchctl','bootout',target],capture_output=True)
    subprocess.run(['launchctl','bootstrap',f'gui/{os.getuid()}',str(PLIST)],check=True)
    print('Installed. Feedback is checked every minute while your Mac is awake and logged in.')

def setup():
    if not sys.stdin.isatty():raise SetupError('Open feedback-mail-setup.command in Terminal. Setup needs an interactive terminal to hide your app password.')
    print('Stratus feedback → Gmail\nYour normal Google password is not used.\nCreate an app password at https://myaccount.google.com/apppasswords\n')
    while True:
        email=input('Your full Gmail / Google Workspace email address: ').strip()
        if valid_email(email):break
        print('Enter the complete email address, including @ and its domain. Do not enter a name or password here.')
    while True:
        password=''.join(getpass.getpass('Google app password (16 characters; hidden): ').split())
        if re.fullmatch(r'[A-Za-z0-9]{16}',password):break
        print('The app password must contain 16 letters/numbers. Spaces between Google’s four groups are accepted. Create an app password, then paste it here; do not use your normal Google password.')
    c={'email':email,'password':password}
    print('Checking Gmail authentication…',flush=True)
    smtp=connect(c);smtp.quit()
    command='add-generic-password -U -a '+ACCOUNT+' -s '+SERVICE+' -w '+shlex.quote(json.dumps(c))+'\n'
    r=subprocess.run(['security','-i'],input=command,capture_output=True,text=True)
    if r.returncode:raise SetupError('Gmail accepted the credentials, but macOS Keychain could not save them. Unlock your login keychain and run setup again.')
    print('Gmail authentication confirmed; saved securely in macOS Keychain.')
    install()

def save_cache(cache):
    cache['updated']=datetime.now(timezone.utc).isoformat()
    server.atomic_write(CACHE,json.dumps(cache,indent=2,ensure_ascii=False).encode())
    CACHE.chmod(0o600)

def run(cache_only=False):
    with open(server.HERE/'.feedback-mail.lock','a') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:return
        cache=json.loads(CACHE.read_text()) if CACHE.exists() else {'schema_version':1,'items':{}}
        # Save full messages before checking SMTP credentials or attempting delivery.
        # Missing cloud rows never delete local copies, including delivered feedback.
        items=public_sync.api('/api/manage/feedback')['items']
        for item in items:
            prior=cache['items'].get(item['id'],{})
            cache['items'][item['id']]={**prior,**item,'cached_at':prior.get('cached_at') or datetime.now(timezone.utc).isoformat()}
        save_cache(cache)
        if cache_only:
            print(f"Cached {len(cache['items'])} feedback message(s) in {CACHE}")
            return
        c=credentials()
        if c is None:return  # Caching works before Gmail setup is complete.
        state=json.loads(STATE.read_text()) if STATE.exists() else {}
        def persist():
            server.atomic_write(STATE,json.dumps(state,indent=2).encode())
            for item_id,receipt in state.items():
                if item_id in cache['items']:
                    cache['items'][item_id]['delivery_status']=receipt['status']
                    cache['items'][item_id]['delivery_receipt']=receipt.get('message_id')
            save_cache(cache)
        def acknowledged(item_id):
            cache['items'][item_id]['status']='sent'
            cache['items'][item_id]['delivery_status']='accepted'
            save_cache(cache)
        # A local acceptance receipt survives a crash or failed cloud acknowledgement.
        for item in items:
            prior=state.get(item['id'],{})
            if prior.get('status')=='accepted':
                public_sync.api('/api/manage/feedback','POST',{'id':item['id'],'status':'sent','receipt':prior['message_id']})
                acknowledged(item['id'])
        pending=[item for item in items if item['status']=='pending' and item['id'] not in state]
        if not pending:return
        smtp=connect(c)  # Authenticate before claiming, so auth/network failures leave the queue untouched.
        try:
            for item in pending:
                item_id=item['id']
                if not re.fullmatch(r'[a-f0-9-]{36}',item_id) or item['topic'] not in ('shader','website','both'):continue
                claim=public_sync.api('/api/manage/feedback','POST',{'id':item_id,'status':'sending'})
                if not claim.get('claimed'):continue
                message_id=f'<stratus-feedback-{item_id}@gmail.com>'
                state[item_id]={'status':'sending','message_id':message_id};persist()
                message=EmailMessage(policy=SMTP)
                message['From']=c['email'];message['To']=c['email']
                message['Subject']=f"[Stratus feedback {item_id}] {item['topic']}"
                message['Message-ID']=message_id
                message['Date']=datetime.now(timezone.utc)
                message.set_content(f"Stratus public feedback\n\nTopic: {item['topic']}\nSubmitted: {item['created']}\n\n{item['message']}\n\nOptional reply address: {item.get('reply') or 'not provided'}\n\nThis is visitor feedback only. No shader or website changes were triggered.")
                try:
                    refused=smtp.send_message(message)
                    if refused:raise RuntimeError('Gmail refused the recipient.')
                except Exception:
                    state[item_id]['status']='unknown';persist()
                    try:public_sync.api('/api/manage/feedback','POST',{'id':item_id,'status':'unknown'})
                    except Exception:pass
                    raise RuntimeError('Mail acceptance could not be confirmed; item retained for manual review, not resent.') from None
                # Gmail accepted DATA. Persist before acknowledging the hosted outbox.
                state[item_id]['status']='accepted';persist()
                public_sync.api('/api/manage/feedback','POST',{'id':item_id,'status':'sent','receipt':message_id})
                acknowledged(item_id)
                print('Feedback delivered: '+item_id,flush=True)
        finally:
            try:smtp.quit()
            except Exception:smtp.close()

def status():
    print('Gmail configured: '+('yes' if credentials() else 'no — run feedback-mail-setup.command'))
    print('Background service installed: '+('yes' if PLIST.exists() else 'no'))
    print('Full-message cache: '+str(CACHE))

def main():
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['setup','install','run','cache','status'],nargs='?',default='run');args=parser.parse_args()
    try:{'setup':setup,'install':install,'run':run,'cache':lambda:run(cache_only=True),'status':status}[args.action]()
    except KeyboardInterrupt:print('\nSetup cancelled. No password printed.');return 130
    except SetupError as error:
        print(str(error),file=sys.stderr)
        return 1
    except EOFError:
        print('Setup input closed. Open feedback-mail-setup.command in Terminal and try again.',file=sys.stderr)
        return 1
    except smtplib.SMTPAuthenticationError:
        print('Google rejected the sign-in. Use an app password created for the email address you entered. Two-Step Verification must be enabled; some managed accounts do not allow app passwords. Pending feedback is retained.',file=sys.stderr)
        return 1
    except (ssl.SSLError,TimeoutError,ConnectionError):
        print('Could not establish a secure connection to Gmail. Check your internet connection and try again. Pending feedback is retained.',file=sys.stderr)
        return 1
    except Exception as error:
        # SMTP/provider errors can include private addresses: log only the error class.
        print('Feedback mail needs attention: '+type(error).__name__+'. Pending mail is retained.',file=sys.stderr)
        return 1
    return 0
if __name__=='__main__':sys.exit(main())
