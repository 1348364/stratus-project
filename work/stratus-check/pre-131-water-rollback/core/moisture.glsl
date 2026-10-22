#ifndef STRATUS_MOISTURE_INCLUDED
#define STRATUS_MOISTURE_INCLUDED
// Material absorption and broad exposed-face films are independent of corners,
// depth-neighbour shapes, view direction and random noise.
vec3 materialMoisture(vec3 dry,vec3 viewPoint,vec2 uv){
#if DIMENSION_TYPE == 0
    if(SURFACE_DAMPNESS<=0.0)return dry;
    vec4 surface=texture(colortex1,uv);
    if(surface.a<0.5)return dry; // Entities, held items, plants and emitters stay dry.
    vec3 n=unitVector(surface.xyz),p=playerFromView(viewPoint);
    vec2 material=texture(colortex2,uv).xy;
    float sky=texture(colortex0,uv).r;
    return wetSurfaceResponse(dry,n,p,sky,material);
#else
    return dry;
#endif
}
#endif
