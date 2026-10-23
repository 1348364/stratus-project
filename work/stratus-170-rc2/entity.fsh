#version 330 core
#ifndef STRATUS_ENTITY_LIGHTING_INCLUDED
#define STRATUS_ENTITY_LIGHTING_INCLUDED
// Vanilla's two fixed diffuse lights, 0.6 direct + 0.4 ambient, clamp at one.
// World/player normal retains model orientation without rotating with camera.
// The lightmap remains independent; emissive/spidereyes passes bypass this.
float nativeEntityLighting(vec3 normal){
    vec3 a=normalize(vec3(0.2,1.0,-0.7));
    vec3 b=normalize(vec3(-0.2,1.0,0.7));
    return min(1.0,0.4+0.6*(max(dot(a,normal),0.0)+max(dot(b,normal),0.0)));
}
#endif

uniform vec3 probeNormal;layout(location=0)out vec4 result;void main(){result=vec4(vec3(nativeEntityLighting(probeNormal)),1);}
