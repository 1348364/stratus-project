#ifndef STRATUS_ENVIRONMENT_INCLUDED
#define STRATUS_ENVIRONMENT_INCLUDED
uniform sampler2D colortex9;
vec3 reflectedEnvironment(vec3 ray){
    ray=unitVector(ray);
    vec2 uv=vec2(atan(ray.z,ray.x)/6.283185307+0.5,ray.y*0.5+0.5);
    return texture(colortex9,clamp(uv,vec2(0.0027,0.0053),vec2(0.9973,0.9947))).rgb;
}
#endif
