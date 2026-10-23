#ifndef STRATUS_ENVIRONMENT_INCLUDED
#define STRATUS_ENVIRONMENT_INCLUDED
uniform sampler2D colortex9;
vec3 reflectedEnvironment(vec3 ray){
    ray=unitVector(ray);
    vec2 uv=vec2(atan(ray.z,ray.x)/6.283185307+0.5,ray.y*0.5+0.5);
    vec2 margin=0.5/vec2(textureSize(colortex9,0));
    vec3 reflection=texture(colortex9,clamp(uv,margin,1.0-margin)).rgb;
    // Longitude is undefined at the vertical poles. The environment cache's
    // last row otherwise gives a different colour to each azimuth, which
    // projects as bright wedges when looking straight down at flat water.
    float poleBlend=smoothstep(0.985,0.999,abs(ray.y));
    if(poleBlend>0.0){
        float poleV=ray.y>0.0?1.0-margin.y:margin.y;
        vec3 pole=vec3(0.0);
        for(int i=0;i<4;i++)
            pole+=texture(colortex9,vec2((float(i)+0.5)*0.25,poleV)).rgb;
        reflection=mix(reflection,pole*0.25,poleBlend);
    }
    return reflection;
}
#endif
