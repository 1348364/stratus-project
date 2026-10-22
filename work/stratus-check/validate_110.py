"""Validate the 1.1 renderer and preserve actual tested-source identity."""
from pathlib import Path
import re,json,hashlib,zipfile
from prepare import expand,override,adapt,profiles,option_extremes
root=Path('outputs/Stratus/shaders');work=Path('work/stratus-check')
options=(root/'core/options.glsl').read_text();choices={}
for name,value,allowed in re.findall(r'^#define (\w+)\s+([^\n]+?)\s*//\s*\[([^]]+)\]',options,re.M):
 choices[name]=allowed.split();assert value in choices[name],name
for name,value,allowed in re.findall(r'const float (\w+)\s*=\s*([^;]+);\s*//\s*\[([^]]+)\]',options):
 choices[name]=allowed.split();assert value in choices[name],name
assert len(choices)==31
assert 'const float ambientOcclusionLevel = 1.00;' in options
assert choices['ambientOcclusionLevel'][-1]=='1.00'
properties=(root/'shaders.properties').read_text();language=(root/'lang/en_us.lang').read_text()
for name in choices:assert f'option.{name}=' in language,name
for row in properties.splitlines():
 if re.match(r'screen\.\w+=',row):
  for word in row.split('=',1)[1].split():assert word in choices,word
for values in profiles(root).values():assert set(values)=={'CLOUD_LAYERS','MIST_DETAIL','REFLECTION_MODE'}
vertices=list(root.glob('*.vsh'))+list(root.glob('world*/*.vsh'));assert len(vertices)==81
variants={'default':{},**{f'profile-{k}':v for k,v in profiles(root).items()},**option_extremes(root)}
for label,values in variants.items():
 for vertex in vertices:
  for p in [vertex,vertex.with_suffix('.fsh')]:
   expected=adapt(override(expand(p,root),values),p.suffix)
   assert (work/'expanded'/label/p.relative_to(root)).read_text()==expected,str(p)
assert 'Validated 486 program pairs; 0 failures.' in (work/'compile-1.1.0.log').read_text()
assert not list(root.rglob('*.csh')) and not list(root.rglob('shadow*'))
diffuse=(root/'core/diffuse.glsl').read_text()
assert not re.search(r'\b(?:smoothField|latticeValue|noise|random|fract)\s*\(',diffuse)
assert 'category = 1.3;' in (root/'core/raster.frag.glsl').read_text()
assert 'BLOCK_SURFACE 1' in (root/'gbuffers_block.fsh').read_text()
assert 'physicalCloudLayer(cameraPosition, direction, distanceLimit)' in (root/'core/resolve.frag.glsl').read_text()
assert 'blend.gbuffers_water.colortex3=SRC_ALPHA ONE_MINUS_SRC_ALPHA ONE ONE_MINUS_SRC_ALPHA' in properties
assert 'alphaTest.gbuffers_water=off' in properties
probe=json.loads((work/'appearance-probe-result.json').read_text());assert probe['opengl_errors']==0
cases=probe['cases'];current=lambda name:cases[name]['current'][:3]
assert current('wet_origin')==current('wet_far_away')
assert max(current('wet_origin'))<0.25
assert current('covered_dry')==[0.5]*3 and current('entity_dry')==[0.5]*3
assert max(current('all_materials_same'))<1e-7 and max(current('all_faces_same'))<1e-7
assert max(current('water_split_path'))<1e-6
assert all(a>b for a,b in zip(current('water_two_blocks'),current('water_eight_blocks')))
assert all(x>0.05 for x in current('cloud_below_inside_above'))
assert max(current('cloud_direction_and_occlusion'))==0
assert all(a>b for a,b in zip(current('sky_light_leak'),cases['sky_light_leak']['previous'][:3]))
assert current('face_shading')!=cases['face_shading']['previous'][:3]
assert max(abs(a-b) for a,b in zip(current('face_shading'),cases['face_shading']['previous'][:3]))<0.03
sources={}
with zipfile.ZipFile('work/minecraft-smoke/shaderpacks/Stratus-1.1.0-verified5.zip') as z:
 for p in sorted(root.rglob('*')):
  if p.is_file() and p.suffix in {'.vsh','.fsh','.glsl','.properties','.lang'}:
   name='shaders/'+p.relative_to(root).as_posix();assert z.read(name)==p.read_bytes(),name
   sources[name]=hashlib.sha256(p.read_bytes()).hexdigest()
result={'pack':'Stratus 1.1.0','date':'2026-10-16','options':len(choices),'native_compile_link':{'passed':486,'failed':0,'program_pairs':81,'variants':6,'renderer':'Apple M1 OpenGL 4.1','method':'Offline compatibility shim, separate from actual Iris test'},'gpu_appearance_probes':probe,'checks':{'ao_default_and_maximum_1':True,'dampness_world_position_independent':True,'all_block_classes_same_dampness':True,'covered_blocks_and_entities_dry':True,'water_absorption_shared_and_path_consistent':True,'finite_cloud_layer_below_inside_above':True,'clouds_occluded_by_nearer_geometry':True,'sky_light_leak_measurable':True,'face_shading_subtle':True,'preset_art_controls_unchanged':True,'expanded_sources_match_native_checks':True,'source_matches_tested_zip':True},'source_hashes':sources}
(work/'validation-1.1.0.json').write_text(json.dumps(result,indent=2)+'\n')
print('31 controls, 486 compile/link passes, 13 focused GPU cases, tested source identity verified')
