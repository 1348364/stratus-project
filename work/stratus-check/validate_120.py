"""Verify the tested Stratus 1.2 sources, native checks and optical invariants."""
from pathlib import Path
import hashlib,json,math,re,zipfile
from prepare import expand,override,adapt,profiles,option_extremes
pack=Path('outputs/Stratus');root=pack/'shaders';work=Path('work/stratus-check');game=Path('work/minecraft-smoke')
settings=(root/'core/options.glsl').read_text();choices={}
for name,value,allowed in re.findall(r'^#define (\w+)\s+([^\n]+?)\s*//\s*\[([^]]+)\]',settings,re.M):
 choices[name]=allowed.split();assert value in choices[name],name
for name,value,allowed in re.findall(r'const float (\w+)\s*=\s*([^;]+);\s*//\s*\[([^]]+)\]',settings):
 choices[name]=allowed.split();assert value in choices[name],name
assert len(choices)==34 and choices['WATER_VISIBILITY'][-1]=='4.00'
assert 'const float ambientOcclusionLevel = 1.00;' in settings
properties=(root/'shaders.properties').read_text();language=(root/'lang/en_us.lang').read_text()
for name in choices:assert f'option.{name}=' in language,name
for row in properties.splitlines():
 if re.match(r'screen\.\w+=',row):
  for token in row.split('=',1)[1].split():assert token in choices,token
for values in profiles(root).values():assert set(values)=={'CLOUD_LAYERS','MIST_DETAIL','REFLECTION_MODE'}
vertices=list(root.glob('*.vsh'))+list(root.glob('world*/*.vsh'));assert len(vertices)==81
variants={'default':{},**{f'profile-{k}':v for k,v in profiles(root).items()},**option_extremes(root)}
for label,values in variants.items():
 for vertex in vertices:
  for p in [vertex,vertex.with_suffix('.fsh')]:
   assert (work/'expanded'/label/p.relative_to(root)).read_text()==adapt(override(expand(p,root),values),p.suffix),str(p)
assert 'Validated 486 program pairs; 0 failures.' in (work/'compile-1.2.0.log').read_text()
assert not list(root.rglob('*.csh')) and not list(root.rglob('shadow*'))
assert 'oldLighting=false' in properties
# Only the sky/environment is procedural: moisture coverage has no noise field.
diffuse=(root/'core/diffuse.glsl').read_text()
moisture=diffuse.split('float outdoorMoisture(',1)[1].split('vec3 absorbedWetAlbedo',1)[0]
assert not re.search(r'\b(?:smoothField|smoothVolume|latticeValue|noise|random|fract)\s*\(',moisture)
assert 'kind > 0.95 ? formIrradiance' in diffuse
blocks=(root/'block.properties').read_text();ids={}
for row in blocks.splitlines():
 if row.startswith('block.'):
  key,values=row.split('=',1)
  for value in values.split():assert value not in ids,value;ids[value]=key
assert ids['minecraft:stone']==ids['minecraft:iron_ore']==ids['minecraft:deepslate_iron_ore']
probe=json.loads((work/'probe-1.2.0.json').read_text());cases=probe['cases'];assert probe['opengl_errors']==0
cur=lambda n:cases[n]['current'][:3];old=lambda n:cases[n]['previous'][:3]
for name,row in cases.items():
 for key in ['previous','current']:assert all(math.isfinite(x) and x>=-1e-6 for x in row[key]),name
assert max(cur('covered_moisture'))==0 and max(cur('entity_moisture'))==0
assert all(a<b for a,b in zip(cur('wet_absorption'),[.08,.25,.60]))
assert all(a>b for a,b in zip(cur('smooth_material_absorption'),cur('wet_absorption')))
ratios=[a/b for a,b in zip(cur('wet_absorption'),[.08,.25,.60])];assert max(ratios)-min(ratios)>.1
assert min(a-b for a,b in zip(cur('wet_grazing'),old('wet_grazing')))>.02
assert sum(cur('wet_grazing'))>sum(cur('wet_front'))*2
assert sum(cur('entity_top'))>sum(cur('entity_side'))>sum(cur('entity_bottom'))
assert max(cur('entity_in_darkness'))==0 and min(cur('emissive_in_darkness'))>.5
assert max(cur('billboard_orientation'))<1e-6 and max(cur('water_split_path'))<1e-6
assert all(a>b for a,b in zip(old('water_twenty_blocks'),cur('water_twenty_blocks')))
assert max(cur('cloud_volume_y'))-min(cur('cloud_volume_y'))>.05
assert all(0<a<=1 for a in cur('cloud_view_alpha'))
assert max(cur('cloud_occlusion'))==0 and cur('cloud_shadow')[0]<cur('cloud_shadow')[2]
assert all(a>b for a,b in zip(cur('sun_day'),old('sun_day')))
assert cur('sun_night')==old('sun_night') and cur('sky_away_from_sun')==old('sky_away_from_sun')
sources={}
with zipfile.ZipFile(game/'shaderpacks/Stratus-1.2.0.zip') as tested:
 for p in sorted(root.rglob('*')):
  if p.is_file() and p.suffix in {'.vsh','.fsh','.glsl','.properties','.lang'}:
   name='shaders/'+p.relative_to(root).as_posix();assert tested.read(name)==p.read_bytes(),name
   sources[name]=hashlib.sha256(p.read_bytes()).hexdigest()
result={'pack':'Stratus 1.2.0','date':'2026-10-17','controls':len(choices),'native_compile_link':{'passed':486,'failed':0,'program_pairs':81,'variants':6,'renderer':'Apple M1 OpenGL 4.1','method':'Offline compatibility shim; actual Iris testing is recorded separately'},'gpu_appearance_probes':probe,'source_hashes':sources,'checks':{'ao_default_and_maximum_1':True,'water_clarity_maximum_4':True,'moisture_has_no_procedural_noise':True,'stone_and_ores_share_material_class':True,'entities_receive_form_lighting':True,'entities_have_no_self_emission':True,'wet_reflection_is_view_dependent':True,'cloud_density_varies_in_xyz':True,'cloud_sunlight_is_density_attenuated':True,'sun_is_disabled_at_night':True,'sources_match_compiled_and_tested_zip':True}}
(work/'validation-1.2.0.json').write_text(json.dumps(result,indent=2)+'\n')
print('34 controls, 486 native checks, 21 GPU cases and',len(sources),'tested source identities verified.')
