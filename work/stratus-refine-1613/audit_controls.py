from pathlib import Path
import re,json,sys,hashlib,difflib
sys.path.insert(0,str(Path('work/stratus-check').resolve()));from prepare import profiles
w=Path(__file__).parent;p=Path('outputs/Stratus');b=w/'baseline'
def opts(root):
 s=(root/'shaders/core/options.glsl').read_text();d={}
 for m in re.finditer(r'^#define (\w+) ([^\s]+)\s*//\s*\[([^\]]+)\]',s,re.M):d[m[1]]={'default':m[2],'values':m[3].split()}
 for m in re.finditer(r'^const float (ambientOcclusionLevel)\s*=\s*([^;]+);\s*//\s*\[([^\]]+)\]',s,re.M):d[m[1]]={'default':m[2].strip(),'values':m[3].split()}
 return d
old,new=opts(b),opts(p);assert len(old)==62 and len(new)==65,(len(old),len(new));assert all(new[k]==v for k,v in old.items());assert set(new)-set(old)=={'WATER_STYLE','TRANSPARENT_REFLECTIONS','TRANSPARENT_REFRACTION'}
props=(p/'shaders/shaders.properties').read_text();lang=(p/'shaders/lang/en_us.lang').read_text();menus={}
for l in props.splitlines():
 if l.startswith('screen') and '=' in l and not '.columns=' in l:k,v=l.split('=',1);menus[k]=v.split()
def visit(name,seen):
 assert name not in seen;tokens=menus[name];out=set()
 for token in tokens:
  if token.startswith('['):out|=visit('screen.'+token[1:-1],seen|{name})
  elif token in new:out.add(token)
 return out
reachable=visit('screen',set());assert set(new)<=reachable,set(new)-reachable
assert all('option.'+k+'=' in lang and 'option.'+k+'.comment=' in lang for k in new if k!='ambientOcclusionLevel')
op,np=profiles((b/'shaders').resolve()),profiles((p/'shaders').resolve());assert len(np)==4
for tag,vals in op.items():assert all(np[tag][k]==v for k,v in vals.items()),tag
for vals in np.values():assert vals['WATER_STYLE']=='1' and len(vals)==65
# Block mappings must retain every original token exactly once.
def blocks(root):
 s='\n'.join(l for l in (root/'shaders/block.properties').read_text().splitlines() if l.startswith('block.'));return re.findall(r'minecraft:[a-z0-9_]+(?:\[[^\]]*\])?',s)
a,c=blocks(b),blocks(p)
from collections import Counter
assert not (Counter(a)-Counter(c)),Counter(a)-Counter(c)
assert set(c)-set(a)=={'minecraft:slime_block','minecraft:honey_block'}
assert Counter(c)-Counter(a)==Counter({'minecraft:slime_block':1,'minecraft:honey_block':1})
changed=[];diff=[]
for f in sorted((p/'shaders').rglob('*')):
 if not f.is_file():continue
 r=f.relative_to(p);oldf=b/r
 if not oldf.exists() or oldf.read_bytes()!=f.read_bytes():
  changed.append(str(r));
  if f.suffix not in ['.rgba8']:
   diff+=difflib.unified_diff(oldf.read_text().splitlines(True) if oldf.exists() else [],f.read_text().splitlines(True),fromfile='before/'+str(r),tofile='after/'+str(r))
(w/'changes.diff').write_text(''.join(diff));(w/'source-changes.json').write_text(json.dumps(changed,indent=2)+'\n')
result={'previous_controls':len(old),'current_controls':len(new),'previous_defaults_and_ranges_preserved':True,'reachable_controls':len(reachable),'tooltips_present':True,'all_four_original_preset_assignments_preserved':True,'all_presets_native_water_default':True,'block_tokens_preserved':len(a),'changed_shader_files':changed,'failures':0}
(w/'control-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
