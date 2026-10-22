#!/usr/bin/env python3
"""Export Stratus source and completed evidence without credentials or private mail."""
from pathlib import Path
import json,shutil,zipfile,hashlib,re,sys
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'work/stratus-github'
ASSETS=ROOT/'backups/github-release-assets'
SKIP_DIR={'.git','node_modules','.wrangler','.sites-runtime','.history','.bridge','__pycache__','.next','.vinext','.cache','coverage','minecraft-smoke','stratus-github'}
SKIP_FILE={'feedback-cache.json','.DS_Store','connector-grants.json','resourceful-config-web.json'}
CODE={'.py','.java','.c','.h','.glsl','.md','.html','.js','.mjs','.css','.ts','.tsx','.json','.txt','.yml','.yaml','.toml','.sql','.sh','.command','.plist','.properties','.lang','.svg','.xml','.fsh','.vsh','.gsh','.comp','.patch','.diff'}
MEDIA={'.png','.jpg','.jpeg','.webp','.gif','.zip','.jar','.bin'}
SITE={'stratus-public','stratus-studio-cloud','stratus-studio'}
SECRET=[re.compile(rb'gh[pousr]_[A-Za-z0-9_]{25,}'),re.compile(rb'github_pat_[A-Za-z0-9_]{30,}'),re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),re.compile(rb'AIza[0-9A-Za-z_-]{30,}')]

def safe(p):
 rel=p.relative_to(ROOT)
 if any(x in SKIP_DIR for x in rel.parts):return False
 if p.name in SKIP_FILE or p.name.startswith(('.env','.dev.vars','.feedback-','.cloud-','.public-','.github-sync')):return False
 if p.suffix.lower() in {'.log','.class','.lock'} and p.name not in {'package-lock.json'}:return False
 if any(x in {'dist','outputs'} for x in rel.parts[2:-1]) and rel.parts[1:2] in [('stratus-public',),('stratus-studio-cloud',)]:return False
 return True

def add_source(p):
 if p.is_symlink() or not safe(p):return False
 data=p.read_bytes()
 if p.suffix.lower() in CODE and any(pattern.search(data) for pattern in SECRET):raise RuntimeError('Credential-shaped data detected; export stopped: '+str(p.relative_to(ROOT)))
 out=DEST/p.relative_to(ROOT);out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,out);return True

def main():
 DEST.mkdir(parents=True,exist_ok=True);ASSETS.mkdir(parents=True,exist_ok=True)
 exported=[];evidence=[];releases=[]
 for p in ROOT.rglob('*'):
  if not p.is_file() or p.is_symlink():continue
  rel=p.relative_to(ROOT)
  if rel.parts[0] in {'backups','.git','.agents','.codex'} or not safe(p):continue
  if rel.parts[0]=='outputs':
   if len(rel.parts)>1 and rel.parts[1]=='Stratus':
    if add_source(p):exported.append(str(rel))
   elif p.suffix.lower() in CODE|MEDIA:releases.append(p)
  elif rel.parts[0]=='work':
   if len(rel.parts)<2:continue
   if rel.parts[1] in SITE or rel.parts[1]=='Custom instructions':
    if add_source(p):exported.append(str(rel))
   elif p.suffix.lower() in CODE:
    if add_source(p):exported.append(str(rel))
   elif p.suffix.lower() in MEDIA:evidence.append(p)
  elif p.suffix.lower() in CODE:
   if add_source(p):exported.append(str(rel))
 archives=[]
 for name,files in [('stratus-completed-releases.zip',releases),('stratus-development-evidence.zip',evidence)]:
  with zipfile.ZipFile(ASSETS/name,'w',zipfile.ZIP_DEFLATED,compresslevel=3) as archive:
   for p in files:archive.write(p,str(p.relative_to(ROOT)))
  q=ASSETS/name;archives.append({'file':name,'bytes':q.stat().st_size,'files':len(files),'sha256':hashlib.sha256(q.read_bytes()).hexdigest()})
 (DEST/'EXPORT-MANIFEST.json').write_text(json.dumps({'source_files':len(exported),'release_assets':archives,'excluded':['credentials and Keychain data','private feedback and delivery state','chat dispatch snapshots','third-party Minecraft runtime / smoke-test instance','dependencies, build caches and raw application logs'],'source_layout':'Original project-relative paths. Release bundles and visual evidence are GitHub Release assets.'},indent=2)+'\n')
 (DEST/'.gitignore').write_text('node_modules/\n.DS_Store\n.env*\n.dev.vars*\n.wrangler/\n.sites-runtime/\n__pycache__/\n*.log\nfeedback-cache.json\n.feedback-*\n.cloud-*\n.public-*\n.history/\n.bridge/\nwork/stratus-public/dist/\nwork/stratus-studio-cloud/dist/\n')
 (DEST/'README.md').write_text('''# Stratus project archive

Private source archive of the Stratus Minecraft Iris shader, public showcase, private Studio, release workflow, feedback sender and completed development tooling.

## Layout

- `outputs/Stratus/`: editable shader, packaging/installation tools, textures and licence.
- `work/Custom instructions/`: complete target, pending requests, completed archive and release evidence log.
- `work/stratus-public/`: public site and standalone visual effects.
- `work/stratus-studio-cloud/`: private editor/server source.
- `work/stratus-studio/`: local editor, cloud sync, automatic release posting, SMTP mail and cache.
- Remaining work folders: authored QA, research, verification reports and helper source.
- GitHub Release assets: historical shader builds, labelled visual reports and development imagery.

The archive preserves documented verification limits. Source, packaging, actual Minecraft visual checks and measured performance are separate states. Pending performance or scene acceptance is not marked complete by this backup.

## Running

Read the README beside the relevant component. Websites use their existing Sites hosting configuration; server credentials must be configured separately. Local Studio uses its documented start command. Standalone mail setup uses macOS Keychain. No secrets or private feedback are included.

## Refreshing this archive

In the original project, run `python3 tools/export_github.py`, inspect `EXPORT-MANIFEST.json`, then commit/push this checkout and upload the regenerated release asset ZIPs. Uploads require an authenticated GitHub CLI. This export uses no model calls or ChatGPT automation.
''')
 print(json.dumps({'checkout':str(DEST),'source_files':len(exported),'assets':archives}))
if __name__=='__main__':main()
