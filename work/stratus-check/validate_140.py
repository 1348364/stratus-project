from pathlib import Path
import json,re,hashlib,zipfile,math
w=Path('work/stratus-check');p=Path('outputs/Stratus');root=p/'shaders'
options=(root/'core/options.glsl').read_text();props=(root/'shaders.properties').read_text();lang=(root/'lang/en_us.lang').read_text()
controls=set(re.findall(r'^#define (\w+) [^\n]+// \[',options,re.M))|set(re.findall(r'^const float (\w+) =.*// \[',options,re.M))
menus={}
for line in props.splitlines():
 m=re.match(r'screen(?:\.(\w+))?=(.*)',line)
 if m:menus[m[1] or 'root']=m[2].split()
seen=set();reachable=set()
def visit(n):
 if n in seen:return
 seen.add(n)
 for token in menus[n]:
  if token.startswith('['):visit(token[1:-1])
  elif token in controls:reachable.add(token)
visit('root');assert controls==reachable,(controls-reachable)
for c in controls:assert 'option.'+c+'=' in lang,c
assert '#define FACE_BLEND 1.00' in options and '#define WATER_VISIBILITY 1.70' in options and '#define SURFACE_SATURATION 1.00' in options
log=(w/'compile-140.log').read_text();assert 'Validated 744 program pairs; 0 failures.' in log
probe=json.loads((w/'probe-140.json').read_text());assert probe['opengl_errors']==0
v={n:r['current'][:3] for n,r in probe['cases'].items()}
assert abs(v['normal_fresnel'][0]-((1.333-1)/(1.333+1))**2)<1e-6
assert v['grazing_fresnel'][0]>.85 and v['underwater_TIR'][0]==1 and v['underwater_window'][0]<.03
assert abs(v['snell_direction'][0]-.70710678/1.333)<1e-6
assert max(abs(x) for x in v['normal_tir_direction'])<1e-7
assert v['trapped_wet'][0]>v['flat_wet'][0]*4>v['wall_wet'][0]
assert v['sheltered_wet'][0]==0 and v['soil_wet'][0]>v['smooth_wet'][0]
assert max(v['split_path_error'])<1e-6
assert sum(v['water_2m'])>sum(v['water_8m'])>sum(v['water_24m'])
assert sum(v['lit_cave_body'])>sum(v['cave_body']) and sum(v['outdoor_body'])>sum(v['cave_body'])
assert v['cloud_below'][0]>.2 and v['cloud_inside'][0]>.2 and v['cloud_above'][0]>.2
assert v['cloud_wrong_side'][0]==v['cloud_depth_clip'][0]==0
assert sum(v['face_top'])>sum(v['face_side']) and max(v['entity_dark'])==0
for n,values in v.items():assert all(math.isfinite(x) for x in values),n
source={str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest() for f in root.rglob('*') if f.is_file() and f.suffix in {'.glsl','.vsh','.fsh','.properties','.lang'}}
result={'version':'1.4.0','native_compile_pairs':744,'native_variants':8,'program_pairs':93,'controls':len(controls),'menu_reachable_controls':len(reachable),'gpu_invariant_cases':len(v),'gpu_errors':0,'gpu_invariants_passed':True,'source_hashes':source}
(w/'validation-1.4.0.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS:',len(controls),'reachable controls;',len(source),'source files;744 native checks;',len(v),'GLSL optical cases')
