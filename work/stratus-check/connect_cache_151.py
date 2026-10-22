from pathlib import Path
p=Path('outputs/Stratus/shaders/core/scene-trace.glsl');s=p.read_text()
s=s.replace('uniform sampler2D colortex10;','''uniform sampler2D colortex10;
uniform sampler2D shadowtex1;
uniform sampler2D shadowcolor0;
uniform sampler2D shadowcolor1;
ivec2 opticsSize(bool cache){return cache?textureSize(shadowtex1,0):textureSize(depthtex1,0);}
vec3 opticsRadiance(ivec2 cell,bool cache){return cache?texelFetch(shadowcolor0,cell,0).rgb:texelFetch(colortex4,cell,0).rgb;}
''')
s=s.replace('bool opticsProjection(vec3 p,out vec2 uv){','bool opticsProjection(vec3 p,out vec2 uv,bool cache){').replace('uv=q.xy/max(q.w,0.00001)*0.5+0.5;','uv=q.xy/(max(q.w,0.00001)*(cache?3.0:1.0))*0.5+0.5;')
s=s.replace('vec3 opticsReceiver(ivec2 cell,out vec4 normal){','vec3 opticsReceiver(ivec2 cell,out vec4 normal,bool cache){').replace('ivec2 size=textureSize(depthtex1,0);','ivec2 size=opticsSize(cache);')
s=s.replace('normal=texelFetch(colortex10,cell,0);\n    return positionFromDepth(uv,texelFetch(depthtex1,cell,0).r);','''normal=cache?texelFetch(shadowcolor1,cell,0):texelFetch(colortex10,cell,0);
    float d=cache?texelFetch(shadowtex1,cell,0).r:texelFetch(depthtex1,cell,0).r;
    if(d>=0.999999)normal.a=0.0;
    return positionFromDepth((uv-0.5)*(cache?3.0:1.0)+0.5,d);''')
s=s.replace('vec3 opticsColour(vec2 uv,vec3 planePoint,vec3 planeNormal){','vec3 opticsColour(vec2 uv,vec3 planePoint,vec3 planeNormal,bool cache){').replace('ivec2 size=textureSize(colortex4,0);','ivec2 size=opticsSize(cache);')
s=s.replace('opticsReceiver(c,data)','opticsReceiver(c,data,cache)').replace('texelFetch(colortex4,c,0).rgb','opticsRadiance(c,cache)').replace('texelFetch(colortex4,centre,0).rgb','opticsRadiance(centre,cache)')
s=s.replace('float maximum,out float path){','float maximum,bool cache,out float path){')
s=s.replace('vec2 pa=a.xy*ka*0.5+0.5,pb=b.xy*kb*0.5+0.5;','float projectionScale=cache?3.0:1.0;\n    vec2 pa=a.xy*ka/projectionScale*0.5+0.5,pb=b.xy*kb/projectionScale*0.5+0.5;')
s=s.replace('opticsReceiver(cell,data)','opticsReceiver(cell,data,cache)').replace('opticsReceiver(hitCell,hitData)','opticsReceiver(hitCell,hitData,cache)').replace('opticsProjection(candidate,hitUV)','opticsProjection(candidate,hitUV,cache)').replace('opticsColour(hitUV,candidate,n)','opticsColour(hitUV,candidate,n,cache)')
p.write_text(s)
p=Path('outputs/Stratus/shaders/core/refraction.glsl');p.write_text('''#ifndef STRATUS_REFRACTION_INCLUDED
#define STRATUS_REFRACTION_INCLUDED
#include "/core/scene-trace.glsl"
vec4 traceWaterTransmission(vec3 origin,vec3 direction,vec3 interfaceNormal,out float path){
    float maximum=min(160.0,max(far,24.0));
#if DIMENSION_TYPE == 0
    vec4 cached=traceOpticalScene(origin,direction,interfaceNormal,-1,REFRACTION_QUALITY,maximum,true,path);
    if(cached.a>0.99)return cached;
#endif
    return traceOpticalScene(origin,direction,interfaceNormal,-1,REFRACTION_QUALITY,maximum,false,path);
}
#endif
''')
p=Path('outputs/Stratus/shaders/core/trace.glsl');s=p.read_text();s=s.replace('return traceOpticalScene(origin,direction,interfaceNormal,1,REFLECTION_MODE,min(REFLECT_RANGE,max(16.0,far)),distance);','''float maximum=min(REFLECT_RANGE,max(16.0,far));
#if DIMENSION_TYPE == 0
    vec4 cached=traceOpticalScene(origin,direction,interfaceNormal,1,REFLECTION_MODE,maximum,true,distance);
    if(cached.a>0.99)return cached;
#endif
    return traceOpticalScene(origin,direction,interfaceNormal,1,REFLECTION_MODE,maximum,false,distance);''');p.write_text(s)
p=Path('outputs/Stratus/shaders/core/optics-cache.frag.glsl');s=p.read_text().replace('const int shadowMapResolution=2048;','const int shadowMapResolution=4096;');s=s.replace('const int shadowcolor1Format=RGBA16F;','const int shadowcolor1Format=RGBA16F;\nconst vec4 shadowcolor0ClearColor=vec4(0.0);\nconst vec4 shadowcolor1ClearColor=vec4(0.0);');p.write_text(s)
print('Connected wide-view geometry to both ray types; native view remains unchanged.')
