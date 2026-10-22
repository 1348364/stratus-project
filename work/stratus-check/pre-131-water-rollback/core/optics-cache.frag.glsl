#include "/core/options.glsl"
#include "/core/frame.glsl"
#include "/core/ceiling.glsl"
#include "/core/diffuse.glsl"
uniform sampler2D gtexture;
uniform sampler2D lightmap;
uniform int entityId;
uniform int renderStage;
in vec4 cacheTint;
in vec2 cacheUV;
in vec2 cacheLight;
in vec3 cachePoint;
in vec3 cacheNormal;
flat in int cacheMaterial;
flat in int cacheFace;
#include "/core/optics-cube.glsl"
#if OPTICS_CACHE_QUALITY == 2
const int shadowMapResolution=4096;
#elif OPTICS_CACHE_QUALITY == 1
const int shadowMapResolution=2048;
#else
const int shadowMapResolution=1024;
#endif
#if OPTICS_CACHE_DISTANCE == 16
const float shadowDistance=16.0;
#elif OPTICS_CACHE_DISTANCE == 24
const float shadowDistance=24.0;
#elif OPTICS_CACHE_DISTANCE == 32
const float shadowDistance=32.0;
#elif OPTICS_CACHE_DISTANCE == 48
const float shadowDistance=48.0;
#elif OPTICS_CACHE_DISTANCE == 64
const float shadowDistance=64.0;
#elif OPTICS_CACHE_DISTANCE == 96
const float shadowDistance=96.0;
#elif OPTICS_CACHE_DISTANCE == 128
const float shadowDistance=128.0;
#else
const float shadowDistance=160.0;
#endif
const float shadowDistanceRenderMul=1.0;
const float shadowIntervalSize=0.0;
const int RGBA16F=34842;
const int shadowcolor0Format=RGBA16F;
const int RGBA32F=34836;
const int shadowcolor1Format=RGBA32F;
const vec4 shadowcolor0ClearColor=vec4(0.0,0.0,0.0,0.0);
const vec4 shadowcolor1ClearColor=vec4(0.0,0.0,0.0,0.0);
/* DRAWBUFFERS:01 */
void main(){
    vec2 tilePixel=gl_FragCoord.xy/float(shadowMapResolution)*vec2(4,2)-cubeTile(cacheFace);
    if(min(tilePixel.x,tilePixel.y)<0.0||max(tilePixel.x,tilePixel.y)>=1.0)discard;
    if(entityId==4200||entityId==4201)discard;
#ifdef MC_RENDER_STAGE_ENTITIES
    // Iris 1.21.11 batches entity geometry; prevent the local first-person body
    // from enclosing the eye in every cube face. Keep other entity reflections.
    if(renderStage==MC_RENDER_STAGE_ENTITIES&&max(abs(cachePoint.x),abs(cachePoint.z))<0.9&&cachePoint.y>-2.0&&cachePoint.y<0.65)discard;
#endif
    if(cacheMaterial==4100||cacheMaterial==4103)discard;
    vec4 albedo=texture(gtexture,cacheUV)*cacheTint;
    if(albedo.a<0.1)discard;
    vec3 n=unitVector(cacheNormal);
    float sky=clamp((cacheLight.y*32.0-1.0)/30.0,0.0,1.0);
    vec3 light=texture(lightmap,cacheLight).rgb;
    vec3 colour=diffuseRadiance(albedo.rgb,light,sky,n,1.3,cachePoint,cacheMaterial);
    colour=wetSurfaceResponse(colour,n,cachePoint,sky,wetMaterialProperties(cacheMaterial));
    gl_FragData[0]=vec4(colour,1.0);
    gl_FragData[1]=vec4(n,length(cachePoint-cubeOrigin(cacheFace)));
}
