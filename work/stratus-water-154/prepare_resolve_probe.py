"""Compare the actual full-resolution resolve shaders on identical GPU inputs."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path('work/stratus-check').resolve()))
from prepare import expand,adapt,override

w=Path(__file__).resolve().parent
root=Path('outputs/Stratus/shaders').resolve()
values={'WATER_RENDER_QUALITY':'2','REFLECTION_MODE':'2',
        'WATER_EXTINCTION':'3.00','WATER_TURBIDITY':'6.00'}
(w/'screen.vsh').write_text('''#version 330 core
out vec2 rasterUV;
void main(){vec2 p=vec2((gl_VertexID<<1)&2,gl_VertexID&2);rasterUV=p;gl_Position=vec4(p*2.-1.,0,1);}
''')
current=expand(root/'core/water-resolve.frag.glsl',root)
previous=(w/'baseline/water-resolve.frag.glsl').read_text()
# The include expansion is identical; only the resolve body differs.
previous=current[:current.index('in vec2 rasterUV;')]+previous[previous.index('in vec2 rasterUV;'):]
for name,source in [('previous',previous),('current',current)]:
    (w/f'{name}.fsh').write_text(adapt(override('#version 330 compatibility\n#define DIMENSION_TYPE 0\n'+source,values),'.fsh'))
print('Prepared original and optimized full-resolution water resolve shaders.')
support=Path('work/stratus-check/appearance_probe.c').read_text().split('static void sample(')[0]
(w/'probe-support.h').write_text(support.replace('#include "native_compile.c"','#include "../stratus-check/native_compile.c"'))
