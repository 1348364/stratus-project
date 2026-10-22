from pathlib import Path
import sys
sys.path.insert(0,str(Path('work/stratus-check').resolve()))
from prepare import expand,adapt,override
w=Path('work/stratus-water-163'); root=Path('outputs/Stratus/shaders').resolve()
(w/'screen.vsh').write_text('#version 330 core\nout vec2 rasterUV;\nvoid main(){vec2 p=vec2((gl_VertexID<<1)&2,gl_VertexID&2);rasterUV=p;gl_Position=vec4(p*2.-1.,0,1);}\n')
s=expand(root/'core/water-resolve.frag.glsl',root)
(w/'current.fsh').write_text(adapt(override('#version 330 compatibility\n#define DIMENSION_TYPE 0\n'+s,{'WATER_EXTINCTION':'3.00','WATER_TURBIDITY':'6.00','WATER_VISIBILITY':'1.70'}),'.fsh'))
