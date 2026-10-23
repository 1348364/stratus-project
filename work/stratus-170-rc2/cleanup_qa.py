from pathlib import Path
import hashlib,json
w=Path(__file__).resolve().parent
root=Path.home()/'Library/Application Support/ModrinthApp/profiles/Minecraft (1)/shaderpacks'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def props(p):return dict(line.strip().split('=',1) for line in p.read_text().splitlines() if '=' in line and not line.lstrip().startswith('#'))
def norm(v):
 try:return float(v)
 except ValueError:return v
base=json.loads((w/'reference-defaults.json').read_text()); rows=[]
for d in ['packs-v1','packs-v2','packs']:
 for src in sorted((w/d).iterdir()):
  dest=root/src.name
  if not dest.exists():rows.append({'file':src.name,'status':'already absent'});continue
  same=sha(src)==sha(dest)
  if src.name.endswith('.txt'):
   expected=base|props(src);actual=base|props(dest)
   same=same or {k:norm(v) for k,v in expected.items()}=={k:norm(v) for k,v in actual.items()}
  if same:dest.unlink();status='removed own unchanged QA file'
  else:status='preserved changed file'
  rows.append({'file':src.name,'status':status})
(w/'qa-cleanup.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps({s:sum(r['status']==s for r in rows) for s in set(r['status'] for r in rows)}))
