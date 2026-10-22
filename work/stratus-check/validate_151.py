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
assert len(controls)==53
for default in ['FACE_BLEND 1.00','WATER_VISIBILITY 1.70','SURFACE_SATURATION 1.00','WATER_DISTORTION 1.00']:
    assert '#define '+default in options,default
assert 'Validated 768 program pairs; 0 failures.' in (w/'compile-151-final.log').read_text()
assert (root/'volumes/weather.rgba8').stat().st_size==128**3*4
assert 'TEXTURE_3D RGBA8 128 128 128 RGBA UNSIGNED_BYTE' in props
assert json.loads((root/'volumes/weather.rgba8.mcmeta').read_text())['texture']['clamp'] is False
probe=json.loads((w/'probe-151-final.json').read_text());v=probe['cases'];assert probe['opengl_errors']==0 and len(v)==44
for name,values in v.items():assert all(math.isfinite(x) for x in values),name
assert abs(v['normal_fresnel'][0]-((1.333-1)/(1.333+1))**2)<1e-6
assert v['grazing_fresnel'][0]>.85 and v['underwater_TIR'][0]==1 and v['underwater_window'][0]<.03
assert v['soil_darkening'][0]<v['wood_darkening'][0]<v['stone_darkening'][0]<v['polished_darkening'][0]<1
assert v['metal_no_darkening'][0]==v['sheltered_no_darkening'][0]==1
assert v['exposed_film'][0]>.5 and v['sheltered_no_film'][0]==0
assert max(v['split_path_error'][:3])<1e-6
assert sum(v['water_2m'][:3])>sum(v['water_8m'][:3])>sum(v['water_24m'][:3])
assert sum(v['lit_cave_body'][:3])>sum(v['cave_body'][:3]) and sum(v['outdoor_body'][:3])>sum(v['cave_body'][:3])
assert abs(v['cloud_below'][0]-v['cloud_above'][0])<1e-5
assert v['cloud_inside'][0]>.5
assert v['cloud_stationary_world_error'][0]<1e-5
assert v['cloud_wrong_side'][0]==v['cloud_depth_clip'][0]==0
assert v['fog_local_volume'][0]>.1 and v['fog_foreground_clear'][0]==v['fog_sheltered'][0]==v['fog_high'][0]==0
assert abs(v['fog_below'][0]-v['fog_offset'][0])>.0001
assert sum(v['face_top'][:3])>sum(v['face_side'][:3]) and max(v['entity_dark'][:3])==0
assert max(abs(v['legacy_refraction_zero'][i]-[.5,.35][i]) for i in range(2))<1e-6
assert abs(v['legacy_refraction_offset'][0]-.5225)<1e-6 and abs(v['legacy_refraction_offset'][1]-.347)<1e-6
assert max(abs(v['legacy_refraction_foreground_guard'][i]-[.5,.35][i]) for i in range(2))<1e-6
assert v['screen_visible_receiver'][0]>.99
assert v['screen_behind_eye_miss'][0]==v['screen_wrong_medium_rejected'][0]==0
assert not list(root.rglob('shadow.gsh')) and not list(root.glob('shadow.vsh'))
assert 'shadow.enabled=false' in props
suffixes={'.glsl','.vsh','.gsh','.fsh','.properties','.lang','.rgba8','.mcmeta'}
source={str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(root.rglob('*')) if f.is_file() and f.suffix in suffixes}
with zipfile.ZipFile('work/stratus-main-qa/experimental-shaders/Stratus-1.5.1-Refraction131.zip') as z:
    assert z.testzip() is None
    for name,digest in source.items():assert hashlib.sha256(z.read(name)).hexdigest()==digest,name
result={'version':'1.5.1','native_compile_pairs':768,'native_variants':8,'program_pairs':96,'controls':len(controls),'menu_reachable_controls':len(reachable),'gpu_invariant_cases':len(v),'gpu_errors':0,'gpu_invariants_passed':True,'weather_volume_size':[128,128,128,4],'source_hashes':source}
(w/'validation-1.5.1.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS:',len(controls),'reachable controls;',len(source),'matching shader/assets;768 native checks;',len(v),'actual GLSL cases.')
