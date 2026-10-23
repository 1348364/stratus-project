#!/usr/bin/env python3
"""Publish settled Stratus source and final releases to GitHub; no model calls."""
from __future__ import annotations
import argparse,fcntl,hashlib,io,json,os,plistlib,re,shutil,subprocess,sys,tarfile,tempfile,time,zipfile
from datetime import datetime,timezone
from pathlib import Path
import github_backups
import sys as _sys
ROOT=Path(__file__).resolve().parents[1]
CHECKOUT=ROOT/'work/stratus-github'
STATE=ROOT/'work/stratus-studio/.github-sync-state.json'
CONFIG=ROOT/'tools/github-sync.json'
LABEL='au.stratus.project.github-sync'
GH='/opt/homebrew/bin/gh'
PYTHON='/Library/Frameworks/Python.framework/Versions/3.14/bin/python3'
TEXT={'.py','.java','.c','.h','.glsl','.md','.html','.js','.mjs','.css','.ts','.tsx','.json','.jsonl','.mcmeta','.mf','.txt','.yml','.yaml','.toml','.sql','.sh','.command','.plist','.properties','.lang','.svg','.xml','.fsh','.vsh','.gsh','.comp','.patch','.diff'}
OMIT={'.git','node_modules','.wrangler','.sites-runtime','.history','.bridge','__pycache__','.next','.vinext','.agents','.codex','.cache','.venv','venv','coverage','minecraft-smoke','stratus-github','.aws','.ssh'}
PATTERNS=[rb'gh[pousr]_[A-Za-z0-9_]{25,}',rb'github_pat_[A-Za-z0-9_]{30,}',rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',rb'AIza[0-9A-Za-z_-]{30,}',rb'\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}']
class SyncCommandError(RuntimeError):pass

SENSITIVE={'access_token','accesstoken','refresh_token','id_token','client_secret','api_key','app_password','password'}

def command(args,cwd=ROOT,timeout=90):
 r=subprocess.run(args,cwd=cwd,capture_output=True,timeout=timeout)
 if r.returncode:raise SyncCommandError('Command failed: '+Path(args[0]).name+' '+(args[1] if len(args)>1 else '')+' (exit '+str(r.returncode)+').')
 return r.stdout

def gh(*args):return command([GH,*args],timeout=120)
def git(*args):return command(['git',*args],CHECKOUT)
def digest(data):return hashlib.sha256(data).hexdigest()
def atomic(path,value):
 path.parent.mkdir(parents=True,exist_ok=True)
 fd,name=tempfile.mkstemp(dir=path.parent)
 try:
  with os.fdopen(fd,'wb') as f:f.write(value);f.flush();os.fsync(f.fileno())
  os.replace(name,path)
 finally:
  if os.path.exists(name):os.unlink(name)
def state_save(state):atomic(STATE,json.dumps(state,indent=2).encode())
def allowed(name):
 p=Path(name)
 return not any(part in OMIT for part in p.parts) and p.name not in {'feedback-cache.json','resourceful-config-web.json','.DS_Store'} and not p.name.startswith(('.env','.dev.vars','.feedback-','.cloud-','.public-','.github-sync')) and p.suffix not in {'.log','.class','.lock','.pem','.key'}

def inspect_bytes(name,data):
 if Path(name).suffix.lower() not in TEXT:return
 if any(re.search(pattern,data) for pattern in PATTERNS):raise ValueError('Possible credential in '+name)
 if Path(name).suffix.lower() in {'.json','.mcmeta','.jsonl'}:
  try:value=[json.loads(line) for line in data.splitlines() if line.strip()] if Path(name).suffix.lower()=='.jsonl' else json.loads(data)
  except (ValueError,UnicodeError):return
  def visit(v):
   if isinstance(v,dict):
    for key,item in v.items():
     if key.lower() in SENSITIVE and isinstance(item,str) and len(item)>12 and item.lower() not in {'not configured','not provided'}:raise ValueError('Credential field in '+name)
     visit(item)
   elif isinstance(v,list):
    for item in v:visit(item)
  visit(value)

def final_release():
 log=(ROOT/'work/Custom instructions/CHANGE-LOG.md').read_text()
 versions=re.findall(r'^## .+?\s+[—–-]\s+Stratus (\d+\.\d+\.\d+)\s*$',log,re.M)
 for v in sorted(set(versions),key=lambda x:tuple(map(int,x.split('.'))),reverse=True):
  try:
   receipt=json.loads((ROOT/'outputs'/f'Stratus-{v}-install.json').read_text());pack=ROOT/'outputs'/f'Stratus-{v}.zip'
   if receipt.get('version')==v and digest(pack.read_bytes())==receipt.get('sha256'):return v,pack,receipt
  except (OSError,ValueError):pass
 raise ValueError('No final documented package with a matching receipt.')

def snapshot():
 files={};heads={}
 # Website edits are included only after they have been committed.
 for site in ['stratus-public','stratus-studio-cloud']:
  folder=ROOT/'work'/site;heads[site]=command(['git','rev-parse','HEAD'],folder).decode().strip()
  archive=command(['git','archive','HEAD'],folder)
  with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
   for member in tar:
    if member.isfile() and allowed(member.name):files['work/'+site+'/'+member.name]=tar.extractfile(member).read()
 # Local standalone services and project records must be unchanged across polls.
 for relative in ['work/stratus-studio','work/Custom instructions','tools']:
  folder=ROOT/relative
  for directory,dirs,names in os.walk(folder):
   dirs[:]=[d for d in dirs if d not in OMIT]
   for name in names:
    p=Path(directory)/name;rel=str(p.relative_to(ROOT))
    if p.is_file() and not p.is_symlink() and allowed(str(p.relative_to(folder))):files[rel]=p.read_bytes()
 for name in ['AGENTS.md']:
  files[name]=(ROOT/name).read_bytes()
 v,pack,receipt=final_release()
 # Use the final packaged shader, never an editable shader in progress.
 with zipfile.ZipFile(pack) as archive:
  for entry in archive.infolist():
   rel=Path(entry.filename)
   if entry.is_dir() or rel.is_absolute() or '..' in rel.parts:continue
   files['outputs/Stratus/'+entry.filename]=archive.read(entry)
  # Packaging helpers can advance only while editable runtime equals the final pack.
  entries=[entry for entry in archive.infolist() if entry.filename.startswith('shaders/') and not entry.is_dir()]
  matches=all((ROOT/'outputs/Stratus'/e.filename).is_file() and (ROOT/'outputs/Stratus'/e.filename).read_bytes()==archive.read(e) for e in entries)
  if matches:
   for p in (ROOT/'outputs/Stratus').iterdir():
    if p.is_file() and allowed(p.name):files['outputs/Stratus/'+p.name]=p.read_bytes()
 files[f'outputs/Stratus-{v}-install.json']=json.dumps(receipt,indent=2).encode()+b'\n'
 github_backups.augment_sources(_sys.modules[__name__],files)
 files['README.md']=b'''# Stratus shader project

Source, websites, development work, showcase images and verification evidence.

- `outputs/Stratus/`: latest final documented shader package contents.
- `development/Stratus/`: settled editable shader, including unfinished/candidate work.
- `work/`: authored QA tools, reports, project documents and websites.
- `outputs/*-showcase/`: curated showcase images and their provenance.
- `WORK-BACKUP-INDEX.json`: exact paths/checksums and GitHub Release asset locations for historical and new binary work. Large images, QA packs and release archives live in Releases rather than ordinary Git files.
- `tools/GITHUB-SYNC.md`: automatic sync coverage and operation.

Final shader downloads use `shader-vVERSION` releases. `project-work-snapshots` contains explicitly unfinished development backups; it does not certify those builds. The historical project backup is retained.

Standalone macOS code syncs without model calls. Private credentials, feedback, app logs, third-party Minecraft runtime and regenerable build caches are excluded.
'''
 for name,data in files.items():inspect_bytes(name,data)
 fingerprint=digest(json.dumps({name:digest(data) for name,data in sorted(files.items())},sort_keys=True).encode())
 return files,heads,v,pack,fingerprint

def settled_sources(files,state):
 """Publish stable files without waiting for the entire active project to stop."""
 candidates=state.setdefault('source_candidates',{});ready={};pending=0
 prior_file=CHECKOUT/'AUTO-SYNC-MANIFEST.json'
 prior=json.loads(prior_file.read_text()).get('files',[]) if prior_file.exists() else []
 now=time.time()
 for name in set(files)|set(prior):
  data=files.get(name);checksum=digest(data) if data is not None else 'deleted'
  target=CHECKOUT/name
  if data is not None and target.is_file() and not target.is_symlink() and target.read_bytes()==data:
   ready[name]=data;candidates.pop(name,None);continue
  candidate=candidates.get(name)
  if name=='WORK-BACKUP-INDEX.json':stable=True
  else:
   if not candidate or candidate['sha256']!=checksum:
    candidates[name]={'sha256':checksum,'since':now};candidate=candidates[name]
   stable=now-candidate['since']>=60
  if stable:
   if data is not None:ready[name]=data
  else:
   pending+=1
   if name in prior and target.is_file() and not target.is_symlink():ready[name]=target.read_bytes()
 state['pending_source_files']=pending
 return ready

def release_upload(repo,v,pack,state):
 if state.get('uploaded_releases',{}).get(v)==digest(pack.read_bytes()):return
 tag='shader-v'+v
 listed=json.loads(gh('api',f'repos/{repo}/releases?per_page=100'))
 release=next((r for r in listed if r['tag_name']==tag),None)
 if release is None:
  gh('release','create',tag,'--repo',repo,'--title','Stratus '+v,'--notes','Automatic backup of final documented Stratus '+v+'. See the project change log for verification evidence and remaining limitations.','--latest=false')
  release=json.loads(gh('api',f'repos/{repo}/releases/tags/{tag}'))
 existing={asset['name']:asset for asset in release.get('assets',[])}
 report=ROOT/'outputs'/f'Stratus-{v}-visual-checks'
 assets=[pack]
 if report.is_dir():
  out=ROOT/'backups/github-auto-assets'/f'Stratus-{v}-visual-checks.zip';out.parent.mkdir(parents=True,exist_ok=True)
  with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=1) as archive:
   for p in report.rglob('*'):
    if p.is_file() and not p.is_symlink() and allowed(str(p.relative_to(report))):
     inspect_bytes(str(p),p.read_bytes());archive.write(p,str(p.relative_to(report)))
  assets.append(out)
 for asset in assets:
  if asset.name in existing:
   remote=existing[asset.name]
   if remote.get('size')!=asset.stat().st_size or remote.get('state')!='uploaded':raise ValueError('Existing release asset differs; manual review required.')
   checksum=remote.get('digest')
   if checksum and checksum!='sha256:'+digest(asset.read_bytes()):raise ValueError('Release asset checksum differs; manual review required.')
  else:command([GH,'release','upload',tag,str(asset),'--repo',repo],timeout=1800)
 state.setdefault('uploaded_releases',{})[v]=digest(pack.read_bytes());state_save(state)

def run():
 STATE.parent.mkdir(parents=True,exist_ok=True)
 with open(STATE.with_suffix('.lock'),'a') as lock:
  try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  except BlockingIOError:return
  config=json.loads(CONFIG.read_text());state=json.loads(STATE.read_text()) if STATE.exists() else {}
  repo=json.loads(gh('api','repositories/'+str(config['repository_id'])))
  if repo['visibility']!=config['visibility']:raise ValueError('Repository visibility differs from the authorised configuration.')
  repo_name=repo['full_name'];remote=git('remote','get-url','origin').decode().strip();expected='https://github.com/'+repo_name+'.git'
  if remote not in {expected,config['initial_remote'],state.get('remote')}:raise ValueError('Unexpected Git remote; stopped.')
  if git('status','--porcelain').strip():raise ValueError('The GitHub checkout has local edits; stopped without overwriting them.')
  if remote!=expected:git('remote','set-url','origin',expected)
  git('fetch','origin','main');git('merge','--ff-only','origin/main')
  files,heads,v,pack,_=snapshot()
  index,groups=github_backups.backup_inventory(_sys.modules[__name__],state,files)
  index=github_backups.upload_backups(_sys.modules[__name__],repo_name,state,index,groups)
  files['WORK-BACKUP-INDEX.json']=json.dumps({'files':index,'source_files':'See AUTO-SYNC-MANIFEST.json for Git-tracked source.','binary_release':github_backups.SNAPSHOT_TAG,'policy':'Exact original historical archives plus checksum-verified immutable new work assets. Development snapshots are not final releases.','excluded':['credentials and private feedback','raw app logs and compiled caches','third-party Minecraft runtime','regenerable website deployment bundles']},indent=2).encode()+b'\n'
  files=settled_sources(files,state)
  fingerprint=digest(json.dumps({name:digest(data) for name,data in sorted(files.items())},sort_keys=True).encode())
  state.update(candidate=fingerprint,remote=expected)
  state_save(state)
  if state.get('published')!=fingerprint:
   prior_file=CHECKOUT/'AUTO-SYNC-MANIFEST.json'
   prior=json.loads(prior_file.read_text()).get('files',[]) if prior_file.exists() else []
   for name,data in files.items():
    target=CHECKOUT/name
    if target.is_symlink() or not target.resolve().is_relative_to(CHECKOUT.resolve()):raise ValueError('Unsafe target path; stopped.')
    if not target.exists() or target.read_bytes()!=data:atomic(target,data)
   # Remove only files previously owned by this sync, never historical archive work.
   for name in set(prior)-set(files):
    target=CHECKOUT/name
    if not target.resolve().is_relative_to(CHECKOUT.resolve()):raise ValueError('Invalid manifest path.')
    if target.is_file():target.unlink()
   manifest={'files':sorted(files),'site_commits':heads,'shader_release':v,'fingerprint':fingerprint,'policy':'Per-file settled authored work, separately labelled development source, committed websites, final shader and indexed binary backups. No model calls.'}
   atomic(prior_file,json.dumps(manifest,indent=2).encode()+b'\n')
   git('add','--all')
   if git('diff','--cached','--name-only').strip():git('commit','-m','Sync completed Stratus project updates ('+v+')')
   git('push','origin','main')
   local=git('rev-parse','HEAD').decode().strip();remote_sha=git('ls-remote','origin','refs/heads/main').decode().split()[0]
   if local!=remote_sha:raise ValueError('Push could not be verified.')
   state.update(published=fingerprint,commit=local,remote=expected,last_pushed=datetime.now(timezone.utc).isoformat(),last_status='Source pushed and verified.')
   state_save(state);print('Source pushed: '+local,flush=True)
  release_upload(repo_name,v,pack,state)
  state['last_checked']=datetime.now(timezone.utc).isoformat()
  asset_waiting=sum(1 for name,item in state.get('asset_settling',{}).items() if state.get('work_backups',{}).get(name,{}).get('sha256')!=item['sha256'])
  state['pending_asset_files']=asset_waiting
  pending=state.get('pending_source_files',0)+asset_waiting
  state['last_status']=f'Synced; {pending} files waiting to settle.' if pending else 'Up to date, including authored work and binary backups.'
  state.pop('last_error',None);state_save(state);print(state['last_status'],flush=True)

def install():
 target=Path.home()/'Library/LaunchAgents'/f'{LABEL}.plist';target.parent.mkdir(parents=True,exist_ok=True)
 config={'Label':LABEL,'ProgramArguments':[PYTHON,str(Path(__file__).resolve()),'run'],'WorkingDirectory':str(ROOT),'RunAtLoad':True,'StartInterval':300,'ProcessType':'Background','StandardOutPath':str(STATE.parent/'.github-sync.log'),'StandardErrorPath':str(STATE.parent/'.github-sync-error.log'),'EnvironmentVariables':{'PATH':'/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin'}}
 target.write_bytes(plistlib.dumps(config));service=f'gui/{os.getuid()}/{LABEL}'
 subprocess.run(['launchctl','bootout',service],capture_output=True)
 command(['launchctl','bootstrap',f'gui/{os.getuid()}',str(target)])
 print('Installed: checks every five minutes while logged in and awake.')

def main():
 parser=argparse.ArgumentParser();parser.add_argument('action',choices=['run','install','status'],default='run',nargs='?');args=parser.parse_args()
 try:
  if args.action=='install':install()
  elif args.action=='status':print(STATE.read_text() if STATE.exists() else 'Not run yet.')
  else:run()
 except Exception as error:
  detail='GitHub sync stopped: '+type(error).__name__+'. '+(str(error) if isinstance(error,(ValueError,SyncCommandError)) else 'Check authentication, network and the checkout; no force push was used.')
  print(detail,file=sys.stderr)
  try:
   state=json.loads(STATE.read_text()) if STATE.exists() else {}
   state.update(last_status=detail,last_error=datetime.now(timezone.utc).isoformat());state_save(state)
  except (OSError,ValueError):pass
  return 1
 return 0
if __name__=='__main__':sys.exit(main())
