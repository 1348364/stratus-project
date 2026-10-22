#ifndef STRATUS_REFRACTION_INCLUDED
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
