#include "/core/options.glsl"
#include "/core/frame.glsl"
#include "/core/ceiling.glsl"
#include "/core/volume.glsl"
#include "/core/scene-depth.glsl"
in vec2 rasterUV;
/* RENDERTARGETS: 11 */
layout(location=0)out vec4 integratedAtmosphere;
void main(){
    if(isEyeInWater!=0){integratedAtmosphere=vec4(0.0);return;}
    float limit=sceneDistance(rasterUV),sky=sceneSkyExposure(rasterUV);
    vec3 ray=unitVector(mat3(gbufferModelViewInverse)*positionFromDepth(rasterUV,0.5));
    vec4 volume=completeAtmosphereSegment(cameraPosition,ray,limit,sky,true);
    integratedAtmosphere=vec4(volume.rgb*volume.a,volume.a);
}
