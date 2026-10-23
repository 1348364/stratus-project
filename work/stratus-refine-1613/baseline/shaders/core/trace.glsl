#ifndef STRATUS_TRACE_INCLUDED
#define STRATUS_TRACE_INCLUDED
uniform sampler2D depthtex1;
uniform sampler2D colortex4;
#include "/core/scene-trace.glsl"
vec4 sceneryReflection(vec3 origin,vec3 direction,vec3 interfaceNormal,out float distance){
#if REFLECTION_MODE == 0
    distance=0.0;return vec4(0.0);
#else
    float maximum=min(REFLECT_RANGE,max(16.0,far));
    return traceOpticalScene(origin,direction,interfaceNormal,1,REFLECTION_MODE,maximum,false,distance);
#endif
}
#endif
