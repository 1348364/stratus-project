from pathlib import Path
import json,re,hashlib
w=Path(__file__).parent;before=w/'baseline/shaders';after=Path('outputs/Stratus/shaders');snap=json.loads((w/'settings-snapshot.json').read_text())
def inventory(r):
 s=(r/'core/options.glsl').read_text();opts={m[0]:{'default':m[1].strip(),'values':m[2].split()} for m in re.findall(r'^#define\s+(\w+)\s+(.*?)\s*//\s*\[([^\]]+)\]',s,re.M)};opts.update({m[0]:{'default':m[1].strip(),'values':m[2].split()} for m in re.findall(r'^const float (\w+)\s*=\s*([^;]+);\s*//\s*\[([^\]]+)\]',s,re.M)})
 props=(r/'shaders.properties').read_text();menu={};profiles={};lang=dict(l.split('=',1) for l in (r/'lang/en_us.lang').read_text().splitlines() if '=' in l and l.startswith(('option.','value.','screen.')))
 for l in props.splitlines():
  if l.startswith('screen') and '=' in l:menu[l.split('=',1)[0]]=l.split('=',1)[1].split()
  if l.startswith('profile.'):profiles[l.split('=',1)[0]]=l.split('=',1)[1]
 return {'options':opts,'menu':menu,'profiles':profiles,'language':lang}
a,b=inventory(before),inventory(after);assert set(a['options'])<=set(b['options']);changes={}
for k,old in a['options'].items():
 new=b['options'][k];assert old['values']==new['values'],k
 if old['default']!=new['default']:changes[k]={'before':old['default'],'after':new['default']};assert new['default']==snap['saved_overrides'][k]
assert set(changes)==set(snap['source_defaults_to_change'])
for k,value in snap['saved_overrides'].items():assert b['options'][k]['default']==value
assert a['profiles']==b['profiles'];assert 'profile.REFERENCE' in b['profiles'];assert set(a['language'])<=set(b['language'])
for k,tokens in a['menu'].items():assert all(t in b['menu'][k] for t in tokens),(k,tokens)
saved=Path(snap['saved_file']);assert hashlib.sha256(saved.read_bytes()).hexdigest()==snap['saved_sha256'],'Original 1.6.6 preferences changed'
result={'before_count':len(a['options']),'after_count':len(b['options']),'added_controls':sorted(set(b['options'])-set(a['options'])),'removed_or_narrowed_controls':[],'old_allowed_values_identical':True,'old_controls_reachable':True,'all_four_profiles_identical_and_Reference_selectable':True,'preferred_defaults_applied':changes,'saved_1_6_6_file_sha256_preserved':snap['saved_sha256'],'migrations':{'FACE_SHADING':'Combined master retained; new vanilla and realistic component multipliers at 1 reproduce the prior combined look.','WET_SHEEN':'Numeric values and sheltered matte retention retained; now also gates rain-driven view-dependent film on absorbent exposed surfaces.'},'before':a,'after':b}
(w/'option-inventory.json').write_text(json.dumps(result,indent=2)+'\n');print(len(a['options']),'retained;',len(b['options']),'total;',len(changes),'requested default changes; Reference and old saved file preserved.')
