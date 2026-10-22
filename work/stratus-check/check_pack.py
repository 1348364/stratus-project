from pathlib import Path
import json,re,hashlib
from prepare import expand,override,adapt,profiles,option_extremes
pack=Path('outputs/Stratus'); root=pack/'shaders'
settings=(root/'core/options.glsl').read_text()
choices={}
for name,value,allowed in re.findall(r'^#define (\w+)\s+([^\n]+?)\s*//\s*\[([^]]+)\]',settings,re.M):
    choices[name]=allowed.split();assert value in choices[name]
for name,value,allowed in re.findall(r'const float (\w+)\s*=\s*([^;]+);\s*//\s*\[([^]]+)\]',settings):
    choices[name]=allowed.split();assert value in choices[name]
assert len(choices)==26
properties=(root/'shaders.properties').read_text()
for row in properties.splitlines():
    if row.startswith('profile.'):
        assignments=row.split('=',1)[1].split()
        assert {a.split(':')[0] for a in assignments}=={'CLOUD_LAYERS','MIST_DETAIL','REFLECTION_MODE'}
        for setting in assignments:
            name,value=setting.split(':');assert value in choices[name]
    if re.match(r'screen\.\w+=',row):
        for name in row.split('=',1)[1].split():assert name in choices
for name in choices:assert f'option.{name}=' in (root/'lang/en_us.lang').read_text()
assert not list(root.rglob('shadow*'))
assert not list(root.rglob('gbuffers_line.*'))
assert not [p for p in root.rglob('*') if p.suffix in {'.csh','.gsh','.tcs','.tes'}]
variants={'default':{},**{f'profile-{key}':value for key,value in profiles(root).items()},**option_extremes(root)}
vertices=list(root.glob('*.vsh'))+list(root.glob('world*/*.vsh'))
assert len(vertices)==72
for label,values in variants.items():
    for vertex in vertices:
        for source in (vertex,vertex.with_suffix('.fsh')):
            expected=adapt(override(expand(source,root),values),source.suffix)
            tested=Path('work/stratus-check/expanded')/label/source.relative_to(root)
            assert tested.read_text()==expected
log=Path('work/stratus-check/compile.log').read_text()
assert 'Validated 432 program pairs; 0 failures.' in log
# Successful diagnostic PPMs must contain finite non-black image data.
images={}
for name in ('fast','reference','high'):
    payload=Path(f'work/stratus-check/{name}.ppm').read_bytes()
    header,pixels=payload.split(b'\n255\n',1)
    w,h=map(int,header.splitlines()[1].split());assert len(pixels)==w*h*3
    images[name]=pixels
region=[(y*w+x)*3 for y in range(410,600) for x in range(460,690)]
difference=sum(abs(images['reference'][i+c]-images['fast'][i+c]) for i in region for c in range(3))/(len(region)*3)
assert difference>0.25,difference
assert all(max(images['reference'][i:i+3])>5 for i in region)
negative=Path('work/stratus-check/format-negative.log').read_text()
assert "Use of undeclared identifier 'RGBA8'" in negative
assert "Use of undeclared identifier 'RGBA16F'" in negative
assert "#define RGBA8" not in Path('work/stratus-check/expanded/default/deferred.fsh').read_text()
independence=json.loads(Path('work/stratus-check/independence.json').read_text())
dampness=json.loads(Path('work/stratus-check/dampness-result.json').read_text())
assert dampness['dock']['mean_byte_darkening']>20
assert dampness['soil_bank']['mean_byte_darkening']>20
assert dampness['sky']['absolute_difference']==0
assert dampness['lantern']['absolute_difference']==0
assert (root/'core/diffuse.glsl').read_bytes()==Path('work/stratus-check/prior-1.0.4/shaders/core/diffuse.glsl').read_bytes()
atmosphere=json.loads(Path('work/stratus-check/air-probe-result.json').read_text())
assert atmosphere['opengl_errors']==0
assert atmosphere['checks']['clear_through_80_blocks']
assert atmosphere['checks']['distant_mist_at_128_and_192']
assert atmosphere['checks']['fluid_status_fog_unchanged']
assert atmosphere['checks']['cave_lighting_unchanged']
assert abs(atmosphere['checks']['skylight_ratio_from_user_setting']-1.4/1.2)<1e-5
assert '#define SKY_AMBIENT 1.40' in settings
assert '#define MIST_CLEAR 80.0' in settings
assert 'const float ambientOcclusionLevel = 0.30;' in settings
evidence={
    'pack':'Stratus 1.0.6','date':'2026-10-16',
    'basis':'User-supplied reference images and visual brief; shader implementation authored anew.',
    'independence_audit':independence,
    'native_compile_link':{'passed':432,'failed':0,'program_pairs':72,'configurations':6,'renderer':'Apple M1 OpenGL 4.1','method':'Offline compatibility-to-core declarations, not the actual Iris transformer'},
    'standalone_gpu_diagnostic':{'presets':['Fast','Reference','High'],'opengl_errors':0,'water_region_mean_byte_difference_reference_fast':round(difference,3),'reference_visual_inspection':True,'minecraft_render':False},
    'static_checks':{'controls':26,'profile_art_controls_unchanged':True,'include_resolution':True,'source_matches_compiled_variants':True},
    'iris_directive_parser_regression':{'installed_version':'1.10.8','original_failure_reproduced':True,'corrected_clear_colours_accepted':3,'parser_bytecode_unmodified':True,'isolated_logging_stubs':True},
    'texture_format_regression':{'pack_declares_format_constants':True,'test_injects_format_constants':False,'negative_fixture_reproduces_identical_error':True,'installed_iris_accepts_symbolic_formats':5},
    'dampness_gpu_comparison':{'default_strength':1.00,'maximum_strength':2.00,'falling_rain_required':False,'scene_regions':dampness,'function_unchanged_from_1_0_4':True,'minecraft_visual_comparison':False},
    'atmosphere_and_light_gpu_probe':atmosphere,
    'actual_iris_compilation':False,'in_game_visual_test':False,'game_fps_measured':False}
runtime_result=Path('work/stratus-check/minecraft-smoke-result.json')
if runtime_result.exists():
    runtime=json.loads(runtime_result.read_text())
    assert runtime['passed'] and runtime['shader_errors']==0
    for name,digest in runtime['source_hashes'].items():
        assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name
    evidence['actual_iris_compilation']=True
    evidence['in_game_visual_test']=runtime.get('in_game_visual_test',False)
    evidence['minecraft_iris_smoke_test']={key:value for key,value in runtime.items() if key!='source_hashes'}
(pack/'CHECKS.json').write_text(json.dumps(evidence,indent=2)+'\n')
print(json.dumps(evidence,indent=2))
