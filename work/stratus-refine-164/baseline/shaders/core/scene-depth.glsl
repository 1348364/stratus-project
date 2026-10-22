#ifndef STRATUS_SCENE_DEPTH_INCLUDED
#define STRATUS_SCENE_DEPTH_INCLUDED
uniform sampler2D depthtex0;
uniform sampler2D depthtex1;
uniform sampler2D colortex2;
float sceneDistance(vec2 uv){
    float z=texture(depthtex0,uv).r;
    float result=z<0.999999?length(positionFromDepth(uv,z)):7000.0;
    vec4 water=texture(colortex2,uv);
    if(water.w>0.5&&water.x>0.0){
        vec3 ray=positionFromDepth(uv,0.5);
        result=min(result,length(ray*(water.x/max(-ray.z,0.0001))));
    }
    return result;
}
float sceneSkyExposure(vec2 uv){
    vec4 data=texture(colortex2,uv);
    if(data.w>0.5)return clamp(data.y,0.0,1.0);
    return texture(depthtex1,uv).r>=0.999999?1.0:clamp(data.y,0.0,1.0);
}
#endif
