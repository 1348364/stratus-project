from pathlib import Path
import re,json,hashlib,zipfile
root=Path(__file__).resolve().parents[2];w=Path(__file__).parent;p=root/'outputs/Stratus';s=p/'shaders'
props=(s/'shaders.properties').read_text();lang=(s/'lang/en_us.lang').read_text();screens={}
for row in props.splitlines():
 m=re.match(r'screen(?:\.(\w+))?=(.*)',row)
 if m:screens[m[1] or 'root']=m[2].split()
reachable=set();visited=set()
def visit(name):
 if name in visited:return
 visited.add(name)
 for token in screens[name]:
  if token.startswith('['):visit(token[1:-1])
  elif not token.startswith('<'):reachable.add(token)
visit('root')
missing=[n for n in reachable if not re.search(r'^option\.'+re.escape(n)+r'=',lang,re.M)]
assert not missing,missing
assert 'shadow.enabled=false' in props
assert all('profile.'+n+'=' in props for n in ['FAST','BALANCED','REFERENCE','HIGH'])
with zipfile.ZipFile(root/'outputs/Stratus-1.6.5.zip') as z:
 assert z.testzip() is None
 names=[n for n in z.namelist() if n.startswith('shaders/')]
 assert names and all(z.read(n)==(p/n).read_bytes() for n in names)
source={f.relative_to(p).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(s.rglob('*')) if f.is_file()}
result={'version':'1.6.5','reachable_options':len(reachable),'labeled_options':len(reachable),'screens':sorted(visited),'shadow_rendering_enabled':False,'shader_assets':len(names),'archive_matches_source':True,'source_hashes':source,'native_variants':json.loads((root/'work/stratus-check/variants.json').read_text())}
(w/'source-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(len(reachable),'reachable/labeled options;',len(names),'shader assets match candidate ZIP; shadows off.')
