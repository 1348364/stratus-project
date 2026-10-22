#!/usr/bin/env python3
"""Publish verified release captures and manage the private feedback outbox."""
import argparse,hashlib,json,re,ssl,subprocess,sys,termios,urllib.request
from pathlib import Path
import cloud_bridge as bridge
import server
STATE=server.HERE/'.public-sync-state.json'
UPDATES_STATE=server.HERE/'.public-updates-state.json'

def public_text(text):
 # Export release summaries as plain text, never local file links or HTML.
 text=re.sub(r'!?\[([^\]]+)\]\([^)]*\)',r'\1',text)
 text=re.sub(r'<[^>]+>','',text)
 text=re.sub(r'(?:/Users/|/private/|/var/folders/)[^\s]+','[local file]',text)
 text=re.sub(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}','[email omitted]',text)
 return re.sub(r'[*`_]','',text).strip()

def sync_updates():
 text=(server.DOCS/'CHANGE-LOG.md').read_text()
 sections=list(re.finditer(r'^## (.+?)\s+[—–-]\s+Stratus\s+(\d+\.\d+\.\d+)([^\n]*)$',text,re.M))
 releases=[]
 for i,match in enumerate(sections):
  # Do not publish candidates or QA builds as finished releases.
  if match.group(3).strip():continue
  v=match.group(2)
  try:
   receipt=json.loads((server.PROJECT/'outputs'/f'Stratus-{v}-install.json').read_text())
   package=server.PROJECT/'outputs'/f'Stratus-{v}.zip'
   if receipt.get('version')!=v or hashlib.sha256(package.read_bytes()).hexdigest()!=receipt.get('sha256'):continue
  except (OSError,ValueError):continue
  body=text[match.end():sections[i+1].start() if i+1<len(sections) else len(text)]
  glance=re.search(r'^### At a glance\s*\n(.*?)(?=^### |\Z)',body,re.M|re.S)
  if not glance:continue
  bullets=re.split(r'^- ',glance.group(1),flags=re.M)[1:]
  notes=[public_text(' '.join(item.split())) for item in bullets]
  if not notes or any(len(n)>4000 for n in notes):continue
  releases.append({'version':v,'date':public_text(match.group(1)),'items':notes[:12]})
 releases.sort(key=lambda r:tuple(map(int,r['version'].split('.'))),reverse=True)
 if not releases:return {'status':'waiting','detail':'No documented packaged releases.'}
 payload={'releases':releases[:100]}
 fingerprint=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
 old=json.loads(UPDATES_STATE.read_text()) if UPDATES_STATE.exists() else {}
 if old.get('fingerprint')==fingerprint:return {'status':'unchanged','version':releases[0]['version']}
 api('/api/manage/updates','PUT',payload)
 read=api('/api/updates')
 if read.get('releases')!=payload['releases']:raise ValueError('Published release notes readback mismatch.')
 server.atomic_write(UPDATES_STATE,json.dumps({'fingerprint':fingerprint,'version':releases[0]['version']}).encode())
 return {'status':'published','version':releases[0]['version'],'releases':len(releases)}

def api(path,method='GET',body=None,raw=None):
 c=bridge.load_config()['public'];data=raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
 headers={'User-Agent':'StratusStudio/1.0','X-Stratus-Update':c['key'],'Content-Type':'image/png' if raw is not None else 'application/json'}
 req=urllib.request.Request(c['url']+path,data=data,method=method,headers=headers)
 with urllib.request.urlopen(req,timeout=40,context=bridge.TLS) as r:return json.load(r)

def candidates():
 for receipt in (server.PROJECT/'outputs').glob('Stratus-*-install.json'):
  try:
   r=json.loads(receipt.read_text());v=r['version']
   if not re.fullmatch(r'\d+\.\d+\.\d+',v):continue
   # Showcase refreshes follow feature releases (x.y.0), not patch releases.
   if int(v.split('.')[2])!=0:continue
   if not r.get('release_loaded') or r.get('runtime_pack')!='Stratus-'+v+'.zip':continue
   package=server.PROJECT/'outputs'/('Stratus-'+v+'.zip')
   if not package.is_file() or hashlib.sha256(package.read_bytes()).hexdigest()!=r.get('sha256'):continue
   folder=server.PROJECT/'outputs'/('Stratus-'+v+'-showcase')
   images=sorted(folder.glob('*.png')) if folder.is_dir() else []
   if not images and r.get('runtime_evidence'):
    evidence=(server.PROJECT/r['runtime_evidence']).resolve()
    if not evidence.is_relative_to(server.PROJECT) or not evidence.is_file():continue
    folder=evidence.parent/'screenshots';prefix='s'+v.replace('.','')+'-release-'
    images=sorted(x for x in folder.glob(prefix+'*.png') if not any(word in x.stem for word in ['menu','restored']))
   if images:yield tuple(map(int,v.split('.'))),v,r,images[:8]
  except (OSError,ValueError,KeyError):continue

def sync_showcase():
 choices=sorted(candidates(),reverse=True)
 if not choices:return {'status':'waiting','detail':'No loaded release with release captures.'}
 _,v,receipt,images=choices[0]
 scenes=[];uploads=[]
 for i,p in enumerate(images):
  if not p.resolve().is_relative_to(server.PROJECT):raise ValueError('Image is outside project.')
  raw=p.read_bytes()
  if not raw.startswith(b'\x89PNG\r\n\x1a\n') or len(raw)>10000000:continue
  digest=hashlib.sha256(raw).hexdigest()[:12];name=re.sub(r'^s\d+-release-','',p.stem);name=re.sub('[^a-z0-9-]','-',name.lower())[:40]
  key=f'{v}/{name}-{digest}.png';uploads.append((key,raw));scenes.append({'id':name,'title':name.replace('-',' ').capitalize()+'.','description':f'Actual Minecraft release capture from Stratus {v}.','alt':f'Stratus {v}: '+name.replace('-',' '),'image':'/api/images/'+key})
 if not scenes:return {'status':'waiting'}
 # Prefer a river/landscape over a material close-up for the home image.
 scenes.sort(key=lambda s:('river' not in s['id'],s['id']))
 summary=f'Stratus {v} is packaged and recorded as loaded in Minecraft. These are release captures. Visual checks and performance measurements are separate; no FPS improvement is implied.'
 manifest={'version':v,'date':receipt.get('verification_date',''),'summary':summary,'scenes':scenes}
 fingerprint=hashlib.sha256(json.dumps(manifest,sort_keys=True).encode()).hexdigest()
 old=json.loads(STATE.read_text()) if STATE.exists() else {}
 if old.get('fingerprint')==fingerprint:return {'status':'unchanged','version':v}
 for key,raw in uploads:api('/api/manage/images/'+key,'PUT',raw=raw)
 api('/api/manage/release','PUT',manifest)
 read=api('/api/release')
 if read.get('version')!=v or read.get('scenes')!=[{**s,'tag':'STRATUS '+v} for s in scenes]:raise ValueError('Published release readback mismatch.')
 server.atomic_write(STATE,json.dumps({'version':v,'fingerprint':fingerprint}).encode())
 return {'status':'published','version':v,'images':len(scenes)}

def sync():
 # Notes include every final release, independently of the x.y.0 gallery policy.
 updates=sync_updates()
 showcase=sync_showcase()
 return {'updates':updates,'showcase':showcase}

def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=['configure','sync','list','claim','ack','unknown']);p.add_argument('--id');p.add_argument('--receipt');a=p.parse_args()
 if a.action=='configure':
  if sys.stdin.isatty():
   attrs=termios.tcgetattr(sys.stdin.fileno());attrs[3]&=~termios.ECHO;termios.tcsetattr(sys.stdin.fileno(),termios.TCSANOW,attrs)
  print('Ready for public connection JSON (input hidden).',flush=True);value=json.loads(sys.stdin.readline());c=bridge.load_config();c['public']=value;bridge.configure(c);print('Saved to Keychain.');return
 if a.action=='sync':result=sync()
 elif a.action=='list':result=api('/api/manage/feedback')
 else:
  if not a.id:p.error('--id is required')
  if a.action=='ack' and not a.receipt:p.error('--receipt is required')
  result=api('/api/manage/feedback','POST',{'id':a.id,'status':{'claim':'sending','ack':'sent','unknown':'unknown'}[a.action],'receipt':a.receipt})
 print(json.dumps(result))
if __name__=='__main__':main()
