#include "/core/options.glsl"
#include "/core/frame.glsl"
#include "/core/lake-normal.glsl"
#include "/core/trace.glsl"
uniform sampler2D colortex0;
uniform sampler2D colortex1;
uniform sampler2D colortex2;
in vec2 rasterUV;
/* RENDERTARGETS: 7 */
layout(location=0)out vec4 waterReflection;
void main(){
    waterReflection=vec4(0.0);
#if REFLECTION_MODE != 0
    vec4 colour=texture(colortex0,rasterUV),normal=texture(colortex1,rasterUV),depth=texture(colortex2,rasterUV);
    if(colour.a<=0.5||normal.a<=0.5||depth.a<=0.5||depth.x<=0.0)return;
    vec3 ray=positionFromDepth(rasterUV,0.5);
    vec3 view=ray*(depth.x/max(-ray.z,0.00001));
    vec3 worldNormal=lakeNormal(playerFromView(view),normal.xyz,depth.x);
    vec3 n=unitVector(mat3(gbufferModelView)*worldNormal);
    if(dot(n,-view)<0.0)n=-n;
    vec4 traced=sceneryReflection(view+n*0.075,reflect(unitVector(view),n));
    waterReflection=vec4(traced.rgb*traced.a,traced.a);
#endif
}
