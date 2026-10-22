from pathlib import Path
from prepare import expand,override,adapt
root=Path('outputs/Stratus/shaders');out=Path('work/stratus-check/bloom-probe-120');out.mkdir(exist_ok=True)
(out/'screen.vsh').write_text('#version 330 core\nout vec2 rasterUV;\nvoid main(){vec2 p=vec2((gl_VertexID<<1)&2,gl_VertexID&2);rasterUV=p;gl_Position=vec4(p*2.0-1.0,0,1);}\n')
for radius in ['small','normal']:
 for axis in ['horizontal','vertical']:
  s='#version 330 compatibility\n'+expand(root/'core'/f'bloom-{axis}.frag.glsl',root)
  (out/f'{radius}-{axis}.fsh').write_text(adapt(override(s,{'BLOOM_RADIUS':'0.50' if radius=='small' else '1.50'}),'.fsh'))
