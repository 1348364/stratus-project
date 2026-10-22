"""Validate the final 1.5 source, controls, assets and actual GLSL probe results."""
from pathlib import Path
import hashlib,json,math,re,zipfile
w=Path('work/stratus-check');p=Path('outputs/Stratus');root=p/'shaders'
options=(root/'core/options.glsl').read_text();props=(root/'shaders.properties').read_text();lang=(root/'lang/en_us.lang').read_text()
controls=set(re.findall(r'^#define (\w+) [^\n]+// \[',options,re.M))|set(re.findall(r'^const float (\w+) =.*// \[',options,re.M))
menus={}
for line in props.splitlines():
    m=re.match(r'screen(?:\.(\w+))?=(.*)',line)
    if m:menus[m[1] or 'root']=m[2].split()
seen=set();reachable=set()
def visit(name):
    if name in seen:return
    seen.add(name)
    for token in menus[name]:
        if token.startswith('['):visit(token[1:-1])
        elif token in controls:reachable.add(token)
visit('root');assert controls==reachable,(controls-reachable)
for c in controls:assert 'option.'+c+'=' in lang,c
assert len(controls)==50
for default in ['FACE_BLEND 1.00','WATER_VISIBILITY 1.70','SURFACE_SATURATION 1.00','WATER_DISTORTION 1.00']:
    assert '#define '+default in options,default
assert 'Validated 744 program pairs; 0 failures.' in (w/'compile-150.log').read_text()
assert (root/'volumes/weather.rgba8').stat().st_size==128**3*4
assert 'TEXTURE_3D RGBA8 128 128 128 RGBA UNSIGNED_BYTE' in props
assert json.loads((root/'volumes/weather.rgba8.mcmeta').read_text())['texture']['clamp'] is False
probe=json.loads((w/'probe-150.json').read_text());v=probe['cases'];assert probe['opengl_errors']==0 and len(v)==41
for name,values in v.items():assert all(math.isfinite(x) for x in values),name
assert abs(v['normal_fresnel'][0]-((1.333-1)/(1.333+1))**2)<1e-6
assert v['grazing_fresnel'][0]>.85 and v['underwater_TIR'][0]==1 and v['underwater_window'][0]<.03
assert abs(v['snell_air_to_water'][0]-.70710678/1.333)<1e-6
assert abs(v['snell_water_to_air'][0]-.5*1.333)<1e-6
assert max(abs(x) for x in v['TIR_direction'][:3])<1e-7
assert v['soil_darkening'][0]<v['wood_darkening'][0]<v['stone_darkening'][0]<v['polished_darkening'][0]<1
assert v['metal_no_darkening'][0]==v['sheltered_no_darkening'][0]==1
assert v['exposed_film'][0]>.5 and v['sheltered_no_film'][0]==0
assert max(v['split_path_error'][:3])<1e-6
assert sum(v['water_2m'][:3])>sum(v['water_8m'][:3])>sum(v['water_24m'][:3])
assert sum(v['lit_cave_body'][:3])>sum(v['cave_body'][:3]) and sum(v['outdoor_body'][:3])>sum(v['cave_body'][:3])
assert all(v[n][0]>.5 for n in ['cloud_below','cloud_inside','cloud_above'])
assert v['cloud_wrong_side'][0]==v['cloud_depth_clip'][0]==0
assert v['fog_local_volume'][0]>.1 and v['fog_foreground_clear'][0]==v['fog_sheltered'][0]==v['fog_high'][0]==0
assert abs(v['fog_below'][0]-v['fog_offset'][0])>.0001
assert sum(v['face_top'][:3])>sum(v['face_side'][:3]) and max(v['entity_dark'][:3])==0
assert v['refracted_cube_top'][0]>.99 and v['refracted_cube_top'][2]>.8
assert v['unbent_floor'][0]>.99 and v['unbent_floor'][2]<.2
assert v['refracted_cube_top'][1]<v['unbent_floor'][1]
suffixes={'.glsl','.vsh','.fsh','.properties','.lang','.rgba8','.mcmeta'}
source={str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(root.rglob('*')) if f.is_file() and f.suffix in suffixes}
with zipfile.ZipFile('work/minecraft-smoke/shaderpacks/Stratus-1.5.0.zip') as z:
    assert z.testzip() is None
    for name,digest in source.items():assert hashlib.sha256(z.read(name)).hexdigest()==digest,name
result={'version':'1.5.0','native_compile_pairs':744,'native_variants':8,'program_pairs':93,'controls':len(controls),'menu_reachable_controls':len(reachable),'gpu_invariant_cases':len(v),'gpu_errors':0,'gpu_invariants_passed':True,'weather_volume_size':[128,128,128,4],'source_hashes':source}
(w/'validation-1.5.0.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS:',len(controls),'reachable controls;',len(source),'matching shader/assets;744 native checks;',len(v),'actual GLSL cases.')
