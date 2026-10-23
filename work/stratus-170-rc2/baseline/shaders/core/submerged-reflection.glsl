#ifndef STRATUS_SUBMERGED_REFLECTION_INCLUDED
#define STRATUS_SUBMERGED_REFLECTION_INCLUDED
// Radiance arriving at the underside of the interface. Camera-to-interface
// water is deliberately absent here; submergedView transports it exactly once.
vec4 submergedReflection(vec3 surface,vec3 geometricNormal,WaterBoundary boundary,vec4 tint,float sky){
#if REFLECTION_MODE == 0
    return vec4(0.0);
#else
    float distance;
    vec4 hit=traceOpticalScene(surface+geometricNormal*0.015,boundary.reflected,
        geometricNormal,1,REFLECTION_MODE,min(REFLECT_RANGE,max(16.0,far)),false,distance);
    if(hit.a<=0.0)return vec4(0.0);
    vec3 colour=travelThroughWater(hit.rgb,distance,tint.rgb,sky,tint.a);
    return vec4(colour*hit.a,hit.a);
#endif
}
#endif
