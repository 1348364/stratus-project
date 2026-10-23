#ifndef STRATUS_TRANSPARENT_OPTICS_INCLUDED
#define STRATUS_TRANSPARENT_OPTICS_INCLUDED
uniform sampler2D colortex15;
#include "/core/environment.glsl"
#include "/core/medium.glsl"
uniform sampler2D colortex4;
#include "/core/scene-trace.glsl"
// One nearest visible thin-solid interface. No volume traversal or water waves.
vec3 transparentSolidOptics(vec3 scene,vec2 uv){
    if(TRANSPARENT_REFLECTIONS<=0.0&&TRANSPARENT_REFRACTION<=0.0)return scene;
    vec4 data=texture(colortex15,uv);
    if(data.a<0.5||data.z<=0.0)return scene;
    vec3 ray=positionFromDepth(uv,0.5),point=ray*(data.z/max(-ray.z,0.00001));
    float front=texture(depthtex0,uv).r;
    if(front<0.999999&&-positionFromDepth(uv,front).z<data.z-max(0.04,data.z*0.002))return scene;
    vec3 n=vec3(data.xy,1.0-abs(data.x)-abs(data.y));
    if(n.z<0.0)n.xy=(1.0-abs(n.yx))*mix(vec2(-1),vec2(1),greaterThanEqual(n.xy,vec2(0)));
    n=unitVector(n);vec3 incident=unitVector(point);if(dot(n,-incident)<0.0)n=-n;
    if(TRANSPARENT_REFRACTION>0.0){
        // Fixed thin-slab offset: opposite parallel faces cancel angular bending.
        // Cap displacement, reject foreground and cross-interface samples.
        vec3 through=refract(incident,n,1.0/1.5);
        vec2 shift=(through.xy/max(abs(through.z),0.2)-incident.xy/max(abs(incident.z),0.2))*0.006*TRANSPARENT_REFRACTION/max(data.z*0.04,1.0);
        shift=clamp(shift,vec2(-0.015),vec2(0.015));vec2 refracted=uv+shift;
        if(min(refracted.x,refracted.y)>0.005&&max(refracted.x,refracted.y)<0.995){
            vec4 other=texture(colortex15,refracted);float back=texture(depthtex1,refracted).r;
            bool same=other.a>0.5&&abs(other.z-data.z)<max(0.08,data.z*0.015);
            bool behind=back>=0.999999||-positionFromDepth(refracted,back).z>data.z+0.02;
            if(same&&behind)scene=texture(colortex3,refracted).rgb;
        }
    }
    if(TRANSPARENT_REFLECTIONS>0.0){
        vec3 direction=reflect(incident,n),world=mat3(gbufferModelViewInverse)*direction;
        vec4 hit=vec4(0.0);
#if REFLECTION_MODE != 0
        float path;hit=traceOpticalScene(point+n*0.015,direction,n,1,REFLECTION_MODE,min(REFLECT_RANGE,max(16.0,far)),false,path);
#endif
        float sky=clamp(float(eyeBrightnessSmooth.y)/240.0,0.0,1.0);
        vec3 fallback=reflectedEnvironment(world)*mix(0.03,1.0,smoothstep(0.04,0.8,sky));
        vec3 reflected=mix(fallback,hit.rgb,hit.a);
        float f=dielectricWaterFresnel(clamp(dot(n,-incident),0.0,1.0),1.0,1.5);
        scene=mix(scene,reflected,clamp(f*TRANSPARENT_REFLECTIONS,0.0,0.85));
    }
    return scene;
}
#endif
