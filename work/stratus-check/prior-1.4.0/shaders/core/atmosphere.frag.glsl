#include "/core/options.glsl"
#include "/core/frame.glsl"
#include "/core/ceiling.glsl"
#include "/core/volume.glsl"
#include "/core/scene-depth.glsl"
in vec2 rasterUV;
/* RENDERTARGETS: 7 */
layout(location=0)out vec4 integratedAtmosphere;
void main(){
    if(isEyeInWater!=0){integratedAtmosphere=vec4(0.0);return;}
    float limit=sceneDistance(rasterUV),sky=sceneSkyExposure(rasterUV);
    vec3 ray=unitVector(mat3(gbufferModelViewInverse)*positionFromDepth(rasterUV,0.5));
    vec4 volume=atmosphereSegment(cameraPosition,ray,limit,sky,true);
#if DIMENSION_TYPE == 0
    if(limit<6999.0&&sky>0.05){
        vec3 point=ray*limit;
        // Minecraft loads complete vertical columns: only horizontal distance
        // approaches the chunk boundary, including when looking down from clouds.
        float metric=length(point.xz);
        float border=smoothstep(max(far*0.84,1.0),max(far,2.0),metric)*smoothstep(0.0,1.0,sky);
        volume=overLayers(volume,vec4(atmosphericColour(),border));
    }
#endif
    volume.rgb*=1.0-clamp(max(blindness,darknessFactor),0.0,1.0);
    integratedAtmosphere=vec4(volume.rgb*volume.a,volume.a);
}
