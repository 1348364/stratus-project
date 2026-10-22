#ifndef STRATUS_ENVIRONMENT_INCLUDED
#define STRATUS_ENVIRONMENT_INCLUDED
uniform sampler2D colortex9;
vec3 reflectedEnvironment(vec3 ray){
    ray=unitVector(ray);
    vec2 uv=vec2(atan(ray.z,ray.x)/6.283185307+0.5,ray.y*0.5+0.5);
    vec2 margin=0.5/vec2(textureSize(colortex9,0));
    return texture(colortex9,clamp(uv,margin,1.0-margin)).rgb;
}
#endif
