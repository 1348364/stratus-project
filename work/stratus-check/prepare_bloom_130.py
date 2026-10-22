from pathlib import Path
from prepare import expand,override,adapt
root=Path('outputs/Stratus/shaders');out=Path('work/stratus-check/bloom-probe-130');out.mkdir(exist_ok=True)
(out/'screen.vsh').write_text('#version 330 core\nout vec2 rasterUV;\nvoid main(){vec2 p=vec2((gl_VertexID<<1)&2,gl_VertexID&2);rasterUV=p;gl_Position=vec4(p*2.0-1.0,0,1);}\n')
for radius in ['small','normal']:
 for axis in ['horizontal','vertical']:
  s='#version 330 compatibility\n'+expand(root/'core'/f'bloom-{axis}.frag.glsl',root)
  (out/f'{radius}-{axis}.fsh').write_text(adapt(override(s,{'BLOOM_RADIUS':'0.50' if radius=='small' else '3.00'}),'.fsh'))
c=Path('work/stratus-check/bloom_probe_120.c').read_text()
c=c.replace('256','128').replace('127.5','63.5').replace('rms_radius_halfres_pixels','rms_radius_quarterres_pixels')
c=c.replace('static void draw(', 'static GLuint emissionMask,depthMask;\nstatic void draw(')
c=c.replace('glUniform1i(glGetUniformLocation(p,"colortex5"),0);','glUniform1i(glGetUniformLocation(p,"colortex5"),0);\n glActiveTexture(GL_TEXTURE1);glBindTexture(GL_TEXTURE_2D,emissionMask);glUniform1i(glGetUniformLocation(p,"colortex0"),1);\n glActiveTexture(GL_TEXTURE2);glBindTexture(GL_TEXTURE_2D,depthMask);glUniform1i(glGetUniformLocation(p,"depthtex0"),2);')
c=c.replace('for(int y=254;', 'for(int y=254;')
# source impulse must span a quarter-res pixel; symmetric 8x8 at centre.
c=c.replace('for(int y=254;y<258;y++)for(int x=254;x<258;x++)','for(int y=252;y<260;y++)for(int x=252;x<260;x++)')
c=c.replace('free(source);','free(source);\n float *mask=calloc(512*512*4,sizeof(float));for(int i=0;i<512*512;i++)mask[i*4+1]=1;emissionMask=image_texture(512,512,mask);memset(mask,0,512*512*4*sizeof(float));depthMask=image_texture(512,512,mask);free(mask);')
Path('work/stratus-check/bloom_probe_130.c').write_text(c)
print('Prepared quarter-resolution bloom probe, radius .50 versus default 3.00')
