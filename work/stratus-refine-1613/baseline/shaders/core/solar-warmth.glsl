#ifndef STRATUS_SOLAR_WARMTH_INCLUDED
#define STRATUS_SOLAR_WARMTH_INCLUDED
float localSunVisibility(vec3 viewPoint,vec3 worldNormal){
    vec3 direction=unitVector(mat3(gbufferModelView)*broadLightDirection());
    vec3 origin=viewPoint+mat3(gbufferModelView)*worldNormal*0.045;
    float previous=-1.0;
    for(int i=0;i<16;i++){
        float u=(float(i)+0.5)/16.0;
        vec3 p=origin+direction*(0.12+32.0*u*u);
        vec4 clip=gbufferProjection*vec4(p,1.0);
        if(clip.w<=0.1)break;
        vec2 uv=clip.xy/clip.w*0.5+0.5;
        if(min(uv.x,uv.y)<0.001||max(uv.x,uv.y)>0.999)break;
        float d=texture(depthtex1,uv).r;
        float error=d<0.999999?positionFromDepth(uv,d).z-p.z:-1000.0;
        if(previous<0.0&&error>=0.0&&error<0.12+length(p)*0.004)return 0.0;
        previous=error;
    }
    return 1.0;
}
vec3 goldenSurfaceWarmth(vec3 radiance,vec3 viewPoint,vec3 worldNormal,float sky){
#if DIMENSION_TYPE == 0 && REALISTIC_LIGHTING == 1
    float facing=max(dot(worldNormal,broadLightDirection()),0.0);
    float strength=GROUND_WARMTH*facing*smoothstep(0.15,0.9,sky)*solarDaylight()*(1.0-0.8*rainStrength);
    if(strength>0.001)strength*=localSunVisibility(viewPoint,worldNormal);
    // Add golden illumination without subtracting blue or staining unlit
    // sides brown. Faces directed away from the sun receive exactly zero.
    return radiance*(vec3(1.0)+vec3(0.15,0.105,0.018)*strength);
#else
    return radiance;
#endif
}
#endif
