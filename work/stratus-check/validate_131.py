"""Verify exact compiled/tested shader source and focused optical invariants."""
from pathlib import Path
import hashlib,json,math,re,zipfile
from prepare import expand,override,adapt,profiles,option_extremes
pack=Path('outputs/Stratus');root=pack/'shaders';work=Path('work/stratus-check');game=Path('work/minecraft-smoke')
settings=(root/'core/options.glsl').read_text();choices={}
for name,value,allowed in re.findall(r'^#define (\w+)\s+([^\n]+?)\s*//\s*\[([^]]+)\]',settings,re.M):
 choices[name]=allowed.split();assert value in choices[name],name
for name,value,allowed in re.findall(r'const float (\w+)\s*=\s*([^;]+);\s*//\s*\[([^]]+)\]',settings):
 choices[name]=allowed.split();assert value in choices[name],name
assert len(choices)==39 and choices['WATER_VISIBILITY'][-1]=='4.00'
assert 'const float ambientOcclusionLevel = 1.00;' in settings
props=(root/'shaders.properties').read_text();language=(root/'lang/en_us.lang').read_text()
for name in choices:assert f'option.{name}=' in language,name
for row in props.splitlines():
 if re.match(r'screen\.\w+=',row):
  for token in row.split('=',1)[1].split():assert token in choices,token
for values in profiles(root).values():assert set(values)=={'CLOUD_LAYERS','MIST_DETAIL','REFLECTION_MODE'}
assert len(profiles(root))==4
vertices=list(root.glob('*.vsh'))+list(root.glob('world*/*.vsh'));assert len(vertices)==90
variants={'default':{},**{f'profile-{k}':v for k,v in profiles(root).items()},**option_extremes(root)}
for label,values in variants.items():
 for vertex in vertices:
  for p in [vertex,vertex.with_suffix('.fsh')]:
   assert (work/'expanded'/label/p.relative_to(root)).read_text()==adapt(override(expand(p,root),values),p.suffix),str(p)
assert 'Validated 630 program pairs; 0 failures.' in (work/'compile-1.3.1.log').read_text()
assert not list(root.rglob('*.csh')) and not list(root.rglob('shadow*'))
assert 'oldLighting=false' in props
assert 'size.buffer.colortex7=0.5 0.5' in props
for i in [5,6]:assert f'size.buffer.colortex{i}=0.25 0.25' in props
passes=['water-reflection','lake','atmosphere','atmosphere-resolve','bloom-horizontal','bloom-vertical']
for d in [root,root/'world-1',root/'world1']:
 for i,lib in enumerate(passes):assert f'/core/{lib}.frag.glsl' in (d/('composite'+(str(i) if i else '')+'.fsh')).read_text()
diffuse=(root/'core/diffuse.glsl').read_text();moisture=diffuse.split('float outdoorMoisture(',1)[1].split('vec3 absorbedWetAlbedo',1)[0]
assert not re.search(r'\b(?:smoothField|smoothVolume|simplexVolume|noise|random|fract)\s*\(',moisture)
assert 'kind > 0.95 ? formIrradiance' in diffuse
ids={}
for row in (root/'block.properties').read_text().splitlines():
 if row.startswith('block.'):
  key,values=row.split('=',1)
  for value in values.split():assert value not in ids,value;ids[value]=key
assert ids['minecraft:stone']==ids['minecraft:iron_ore']==ids['minecraft:deepslate_iron_ore']
probe=json.loads((work/'probe-1.3.0.json').read_text());cases=probe['cases'];assert probe['opengl_errors']==0 and len(cases)==34
cur=lambda n:cases[n]['current'][:3];old=lambda n:cases[n]['previous'][:3]
for name,row in cases.items():
 for key in ['previous','current']:assert all(math.isfinite(x) and x>=-1e-6 for x in row[key]),name
for n in ['covered_moisture','entity_moisture','entity_in_darkness','billboard_orientation','cloud_occlusion','mist_near_clear','mist_covered']:assert max(cur(n))<1e-6,n
assert min(cur('emissive_in_darkness'))>.5
assert sum(cur('entity_top'))>sum(cur('entity_side'))>sum(cur('entity_bottom'))
assert max(cur('water_split_path'))<1e-6
for n in ['water_two_blocks','water_eight_blocks','water_twenty_blocks']:assert all(a>b for a,b in zip(old(n),cur(n))),n
face=[sum(cur('face_'+n)) for n in ['top','east','west','south','north','bottom']]
assert len(set(round(x,5) for x in face))==6 and face[0]==max(face) and face[-1]==min(face)
assert cur('ground_warmth')[0]>old('ground_warmth')[0] and cur('ground_warmth')[2]<old('ground_warmth')[2]
assert cur('ground_night')==old('ground_night')
assert max(cur('simplex_xyz'))-min(cur('simplex_xyz'))>.05
assert all(0<a<=1 for a in cur('cloud_view_alpha')) and cur('cirrus_alpha')[0]>.02
assert max(cur('mist_xyz'))-min(cur('mist_xyz'))>.001 and cur('mist_far')[0]>.1
assert cur('sun_colour')[0]>cur('sun_colour')[1]>cur('sun_colour')[2]
assert all(a>b for a,b in zip(cur('sun_day'),old('sun_day')))
assert cur('sun_night')==old('sun_night') and cur('sky_away_from_sun')==old('sky_away_from_sun')
bloom=json.loads((work/'bloom-probe-1.3.0.json').read_text());assert bloom['opengl_errors']==0 and bloom['larger_radius_spreads_further']
sources={}
with zipfile.ZipFile(game/'shaderpacks/Stratus-1.3.1.zip') as tested:
 for p in sorted(root.rglob('*')):
  if p.is_file() and p.suffix in {'.vsh','.fsh','.glsl','.properties','.lang'}:
   name='shaders/'+p.relative_to(root).as_posix();assert tested.read(name)==p.read_bytes(),name;sources[name]=hashlib.sha256(p.read_bytes()).hexdigest()
result={'pack':'Stratus 1.3.1','date':'2026-10-17','controls':len(choices),'native_compile_link':{'passed':630,'failed':0,'program_pairs':90,'variants':7,'renderer':'Apple M1 OpenGL 4.1','method':'Offline compatibility shim; actual Iris checks recorded separately'},'gpu_appearance_probes':probe,'bloom_radius_probe':bloom,'source_hashes':sources,'checks':{'ao_default_maximum_1':True,'water_default_less_clear_035':True,'six_distinct_cube_faces':True,'daylight_ground_warmer_night_unchanged':True,'dry_entities_and_covered_blocks':True,'emission_separate_from_entity_light':True,'water_path_consistent':True,'cloud_density_3d_and_cirrus_present':True,'mist_world_height_xyz_and_clear_foreground':True,'night_sun_disabled':True,'postwater_atmosphere_order':True,'halfres_reflections_and_atmosphere':True,'quarterres_bloom':True,'sources_match_compiled_and_tested_zip':True}}
(work/'validation-1.3.1.json').write_text(json.dumps(result,indent=2)+'\n')
print('Verified 39 controls, 630 native pairs, 34 GPU cases, bloom spread and',len(sources),'tested source identities.')
