from pathlib import Path
root=Path('outputs/Stratus/shaders')
p=root/'core/lake.frag.glsl';s=p.read_text();start=s.index('vec3 lakeNormal(');end=s.index('void main()',start)
normal=s[start:end]
(root/'core/lake-normal.glsl').write_text('#ifndef STRATUS_LAKE_NORMAL_INCLUDED\n#define STRATUS_LAKE_NORMAL_INCLUDED\n'+normal+'#endif\n')
s=s[:start]+s[end:]
s=s.replace('#include "/core/trace.glsl"','#include "/core/lake-normal.glsl"\nuniform sampler2D colortex4;\nuniform sampler2D depthtex1;\nuniform sampler2D colortex7;')
s=s.replace('        vec4 traced=sceneryReflection(waterView+nView*0.075,reflectedRay);','''        // Reconstruct premultiplied half-resolution screen reflections.
        vec2 grid=rasterUV*vec2(textureSize(colortex7,0))-0.5;
        ivec2 cell=ivec2(floor(grid)),size=textureSize(colortex7,0);vec2 fraction=fract(grid);
        vec4 traced=vec4(0.0);float total=0.0;
        for(int y=0;y<2;y++)for(int x=0;x<2;x++){
            ivec2 sampleCell=clamp(cell+ivec2(x,y),ivec2(0),size-ivec2(1));
            vec2 uv=(vec2(sampleCell)+0.5)/vec2(size);
            vec4 neighbourDepth=texture(colortex2,uv),neighbourNormal=texture(colortex1,uv);
            float weight=(x==0?1.0-fraction.x:fraction.x)*(y==0?1.0-fraction.y:fraction.y);
            weight*=step(0.5,neighbourDepth.a)*step(0.8,dot(neighbourNormal.xyz,markedNormal.xyz));
            weight*=exp(-abs(neighbourDepth.x-markedDepth.x)/max(0.25,markedDepth.x*0.02));
            traced+=texelFetch(colortex7,sampleCell,0)*weight;total+=weight;
        }
        if(total>0.0001)traced/=total;
        traced.rgb/=max(traced.a,0.0001);''')
p.write_text(s)
(root/'core/water-reflection.frag.glsl').write_text('''#include "/core/options.glsl"
#include "/core/frame.glsl"
#include "/core/lake-normal.glsl"
#include "/core/trace.glsl"
uniform sampler2D colortex0;
uniform sampler2D colortex1;
uniform sampler2D colortex2;
in vec2 rasterUV;
/* RENDERTARGETS: 7 */
layout(location=0)out vec4 waterReflection;
void main(){
    waterReflection=vec4(0.0);
#if REFLECTION_MODE != 0
    vec4 colour=texture(colortex0,rasterUV),normal=texture(colortex1,rasterUV),depth=texture(colortex2,rasterUV);
    if(colour.a<=0.5||normal.a<=0.5||depth.a<=0.5||depth.x<=0.0)return;
    vec3 ray=positionFromDepth(rasterUV,0.5);
    vec3 view=ray*(depth.x/max(-ray.z,0.00001));
    vec3 worldNormal=lakeNormal(playerFromView(view),normal.xyz,depth.x);
    vec3 n=unitVector(mat3(gbufferModelView)*worldNormal);
    if(dot(n,-view)<0.0)n=-n;
    vec4 traced=sceneryReflection(view+n*0.075,reflect(unitVector(view),n));
    waterReflection=vec4(traced.rgb*traced.a,traced.a);
#endif
}
''')
# Re-route the ordered composites while reusing the half-res buffer.
passes=['water-reflection','lake','atmosphere','atmosphere-resolve','bloom-horizontal','bloom-vertical']
for directory in [root,root/'world-1',root/'world1']:
 dim=0 if directory==root else (-1 if directory.name=='world-1' else 1)
 vertex=(directory/'composite.vsh').read_text()
 for i,lib in enumerate(passes):
  name='composite'+(str(i) if i else '')
  (directory/f'{name}.vsh').write_text(vertex)
  (directory/f'{name}.fsh').write_text(f'#version 330 compatibility\n#define DIMENSION_TYPE {dim}\n#include "/core/{lib}.frag.glsl"\n')
p=root/'shaders.properties';s=p.read_text().replace('blend.composite4=off','blend.composite4=off\nblend.composite5=off');p.write_text(s)
p=root/'core/ceiling.glsl';s=p.read_text()
a=s.index('        float alpha=1.0-exp(-density.x*CLOUD_THICKNESS');b=s.index('\n    }\n    return sky;',a)
s=s[:a]+'''        // Prefilter the broad cloud contribution: sharp density patches do not
        // survive a rough, rippling water reflection.
        float coverage=smoothstep(0.0,0.040,density.x);
        vec3 colour=atmosphericColour()*mix(0.90,1.13,coverage);
        sky=mix(sky,colour,CLOUD_AMOUNT*0.72);'''+s[b:];p.write_text(s)
print('Half-resolution reflection pass, shared water normals and smooth sky fallback')
