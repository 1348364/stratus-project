#include "/core/options.glsl"
#include "/core/frame.glsl"
#include "/core/scene-depth.glsl"
#include "/core/ceiling.glsl"
#include "/core/volume.glsl"
uniform sampler2D colortex3;
uniform sampler2D colortex11;
#include "/core/transparent-optics.glsl"
in vec2 rasterUV;
/* RENDERTARGETS: 3 */
layout(location=0)out vec4 completedScene;
void main(){
    vec3 scene=transparentSolidOptics(texture(colortex3,rasterUV).rgb,rasterUV);
    // The atmosphere producer writes exact zero in water/lava/snow. Avoid
    // depth reconstruction and four bilateral taps that cannot contribute.
    if(isEyeInWater!=0){completedScene=vec4(max(scene,vec3(0.0)),1.0);return;}
    float distanceToScene=sceneDistance(rasterUV);
    ivec2 size=textureSize(colortex11,0);
    vec2 p=rasterUV*vec2(size)-0.5;
    ivec2 cell=ivec2(floor(p));vec2 f=fract(p);
    vec4 volume=vec4(0.0);float sum=0.0;
    for(int y=0;y<2;y++)for(int x=0;x<2;x++){
        ivec2 sampleCell=clamp(cell+ivec2(x,y),ivec2(0),size-ivec2(1));
        vec2 uv=(vec2(sampleCell)+0.5)/vec2(size);
        // Radial opaque/water depth is cached in the unused metadata channel.
        // The centre still uses exact depth, retaining near translucent edges.
        float depth=texture(colortex2,uv).z;
        float depthWeight=exp(-abs(depth-distanceToScene)/max(1.0,distanceToScene*0.025));
        float weight=(x==0?1.0-f.x:f.x)*(y==0?1.0-f.y:f.y)*depthWeight;
        volume+=texelFetch(colortex11,sampleCell,0)*weight;sum+=weight;
    }
    volume/=max(sum,0.000001);
    if(isEyeInWater==0&&sum<0.12){
        // A subpixel leaf can be absent from every reduced-resolution depth
        // sample. Returning zero here punched an unfogged dark dot in the haze.
        // Integrate only these rejected pixels at their exact full-res depth.
        // Smooth confidence blending prevents a binary fallback threshold.
        vec3 ray=unitVector(mat3(gbufferModelViewInverse)*positionFromDepth(rasterUV,0.5));
        vec4 exact=completeAtmosphereSegment(cameraPosition,ray,distanceToScene,sceneSkyExposure(rasterUV),true);
        exact=vec4(exact.rgb*exact.a,exact.a);
        volume=mix(exact,volume,smoothstep(0.02,0.12,sum));
    }
    completedScene=vec4(max(scene*(1.0-volume.a)+volume.rgb,vec3(0.0)),1.0);
}
