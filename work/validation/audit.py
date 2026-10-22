from pathlib import Path
import re, hashlib, json
root=Path('outputs/Willow-Mist/shaders')
settings=(root/'lib/settings.glsl').read_text()
options={}
for match in re.finditer(r'^#define (\w+)\s+([^\n]+?)\s*//\s*\[([^]]+)\]',settings,re.M):
    name,default,choices=match.groups();options[name]=choices.split();assert default in options[name]
for match in re.finditer(r'const float (\w+)\s*=\s*([^;]+);\s*//\s*\[([^]]+)\]',settings):
    name,default,choices=match.groups();options[name]=choices.split();assert default in options[name]
assert len(options)==25
props=(root/'shaders.properties').read_text()
allowed_quality={'CLOUD_QUALITY','FOG_QUALITY','REFLECTION_QUALITY'}
for line in props.splitlines():
    if line.startswith('profile.'):
        assignments=line.split('=',1)[1].split()
        assert {a.split(':')[0] for a in assignments}==allowed_quality
        for token in assignments:
            name,value=token.split(':');assert value in options[name]
    if re.match(r'screen\.\w+=',line) and not line.startswith('screen.columns='):
        for name in line.split('=',1)[1].split():assert name in options,name
for name in options:
    assert f'option.{name}=' in (root/'lang/en_us.lang').read_text(),name
for path in root.rglob('*'):
    if not path.is_file():continue
    if path.suffix in {'.vsh','.fsh','.glsl'}:
        for ref in re.findall(r'^#include "([^"]+)"',path.read_text(),re.M):
            assert (root/ref.lstrip('/')).is_file(),(path,ref)
        if path.suffix=='.vsh' and path.parent.name!='lib':
            assert path.with_suffix('.fsh').is_file()
    assert path.suffix not in {'.csh','.gsh','.tcs','.tes'},path
    assert not path.name.startswith('shadow'),path
assert not list(root.rglob('gbuffers_line.*'))
assert 'block.1001=minecraft:water' in (root/'block.properties').read_text()
assert 'materialID == 1001' in (root/'lib/geometry.fsh').read_text()
assert '#define WM_WATER\n' in (root/'gbuffers_water.fsh').read_text()
for name in ('gbuffers_terrain','gbuffers_block','gbuffers_entities','gbuffers_hand'):
    assert '#define WM_WATER\n' not in (root/f'{name}.fsh').read_text()
assert 'Validated 342 program pairs; 0 failures.' in Path('work/validation/native-validation.log').read_text()
# Check actual shader declarations, ignoring comments.
for path in root.rglob('*.glsl'):
    code=re.sub(r'//[^\n]*|/\*.*?\*/','',path.read_text(),flags=re.S)
    assert not re.search(r'\b(?:buffer|imageStore|imageLoad|atomicAdd|shared)\b',code),path
# The final pack shader bytes correspond to the variants used by the compiler.
from prepare import expand, override, adapt, profiles, option_extremes
variants={'default':{},**{f'profile-{k}':v for k,v in profiles(root).items()},**option_extremes(root)}
for variant,values in variants.items():
    for vertex in list(root.glob('*.vsh'))+list(root.glob('world*/*.vsh')):
        for path in (vertex,vertex.with_suffix('.fsh')):
            expanded=adapt(override(expand(path,root),values),path.suffix)
            assert (Path('work/validation/expanded')/variant/path.relative_to(root)).read_text()==expanded,path
# Compare rendered water in the same small fixture. P6 header has three lines.
def pixels(name):
    payload=Path(f'work/validation/{name}-fixture.ppm').read_bytes()
    header,data=payload.split(b'\n255\n',1)
    width,height=map(int,header.splitlines()[1].split())
    assert len(data)==width*height*3
    return width,height,data
w,h,reference=pixels('reference');_,_,fast=pixels('fast');_,_,high=pixels('high')
roi=[(y*w+x)*3 for y in range(410,600) for x in range(460,690)]
change=sum(abs(reference[i+c]-fast[i+c]) for i in roi for c in range(3))/(len(roi)*3)
assert change>0.5,change
assert all(max(reference[i:i+3])>5 for i in roi)
summary={'shader_pairs':57,'configurations':6,'native_compile_link_checks':342,'failures':0,
         'controls':len(options),'standalone_presets_rendered':['Fast','Reference','High'],
         'water_roi_mean_byte_change_reference_vs_fast':round(change,3),
         'actual_iris_tested':False,'in_game_visual_tested':False,'game_performance_measured':False}
Path('work/validation/audit-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
