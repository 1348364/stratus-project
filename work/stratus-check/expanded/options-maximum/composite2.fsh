#version 330 core
#define DIMENSION_TYPE 0

// BEGIN INCLUDE /core/water-resolve.frag.glsl

// BEGIN INCLUDE /core/options.glsl
#ifndef STRATUS_OPTIONS_INCLUDED
#define STRATUS_OPTIONS_INCLUDED
// Balanced defaults retain physical water optics; High restores the finest sampling.
#define SKY_AMBIENT 4.00 //  [0.20 0.40 0.60 0.80 1.00 1.20 1.40 1.60 1.80 2.00 2.50 3.00 4.00]
#define EXPOSURE 3.00 //  [-3.00 -2.00 -1.50 -1.00 -0.50 0.00 0.20 0.50 0.75 1.00 1.50 2.00 3.00]
const float ambientOcclusionLevel = 1.00; // [0.00 0.15 0.30 0.45 0.60 0.80 1.00]
#define WHITE_BALANCE 0.24 //  [-0.24 -0.16 -0.08 -0.04 0.00 0.04 0.08 0.16 0.24]
#define SURFACE_SATURATION 2.00 //  [0.00 0.25 0.50 0.75 0.85 0.93 1.00 1.07 1.15 1.30 1.50 1.75 2.00]
#define SURFACE_DAMPNESS 3.00 //  [0.00 0.15 0.35 0.65 1.00 1.35 1.70 2.00 2.50 3.00]
#define CLOUD_AMOUNT 1.00 //  [0.00 0.35 0.60 0.68 0.75 0.90 1.00]
#define CLOUD_ALTITUDE 768.0 //  [64.0 96.0 128.0 160.0 192.0 224.0 256.0 320.0 384.0 512.0 640.0 768.0]
#define CLOUD_THICKNESS 200.0 //  [4.0 12.0 20.0 32.0 40.0 56.0 72.0 96.0 128.0 160.0 200.0]
#define SKY_LEAK 2.00 //  [0.00 0.10 0.15 0.25 0.35 0.50 0.70 1.00 1.40 2.00]
#define CLOUD_SPAN 1800.0 //  [64.0 96.0 160.0 240.0 360.0 540.0 700.0 900.0 1200.0 1800.0]
#define CLOUD_DISTORTION 2.00 //  [0.00 0.25 0.45 0.65 0.85 1.00 1.25 1.50 2.00]
#define CLOUD_RELIEF 1.50 //  [0.00 0.25 0.40 0.55 0.75 1.00 1.25 1.50]
#define CLOUD_DRIFT 3.00 //  [0.00 0.10 0.25 0.45 0.70 1.00 1.50 2.00 3.00]
#define CLOUD_LAYERS 3 //  [1 2 3]
#define MIST_AMOUNT 3.00 //  [0.00 0.15 0.30 0.40 0.60 0.75 0.85 1.00 1.25 1.50 2.00 3.00]
#define MIST_Y 320.0 //  [-32.0 0.0 32.0 48.0 64.0 70.0 88.0 112.0 144.0 192.0 256.0 320.0]
#define MIST_THICKNESS 64.0 //  [4.0 7.0 9.0 12.0 18.0 24.0 32.0 48.0 64.0]
#define MIST_CLEAR 144.0 //  [0.0 4.0 8.0 16.0 24.0 32.0 48.0 64.0 80.0 112.0 144.0]
#define MIST_DETAIL 3 //  [1 2 3]
#define REFLECT_LEVEL 1.00 //  [0.00 0.40 0.60 0.85 1.00]
#define REFLECTION_MODE 2 //  [0 1 2]
#define REFLECT_RANGE 320.0 //  [24.0 48.0 64.0 88.0 120.0 160.0 224.0 320.0]
#define WATER_VISIBILITY 16.00 //  [0.05 0.10 0.20 0.35 0.50 0.70 0.90 1.10 1.30 1.70 2.20 3.00 4.00 6.00 8.00 12.00 16.00]
#define WATER_EXTINCTION 3.00 //  [0.10 0.20 0.45 0.65 0.90 1.15 1.40 2.00 3.00]
#define RIPPLE_HEIGHT 3.00 //  [0.00 0.15 0.30 0.55 0.80 1.00 1.30 1.70 2.20 3.00]
#define RIPPLE_SIZE 4.00 //  [0.25 0.40 0.65 0.80 1.00 1.25 1.50 2.00 3.00 4.00]
#define RIPPLE_RATE 3.00 //  [0.00 0.10 0.20 0.45 0.70 1.00 1.50 2.00 3.00]
#define FACE_SHADING 2.00 //  [0.00 0.15 0.25 0.35 0.50 0.70 0.85 1.00 1.25 1.50 2.00]
#define WET_DARKENING 2.50 //  [0.00 0.25 0.50 0.75 1.00 1.30 1.70 2.00 2.50]
#define WET_SHEEN 2.00 //  [0.00 0.15 0.35 0.65 0.85 1.00 1.35 1.70 2.00]
#define BLOOM_STRENGTH 1.00 //  [0.00 0.03 0.06 0.12 0.18 0.25 0.35 0.50 0.75 1.00]
#define BLOOM_RADIUS 12.00 //  [0.25 0.50 1.00 1.50 2.00 3.00 4.00 6.00 8.00 12.00]
#define SUN_VISIBILITY 3.00 //  [0.00 0.25 0.45 0.65 0.85 1.00 1.50 2.00 3.00]
#define LAMP_LEVEL 3.00 //  [0.20 0.40 0.70 0.85 1.00 1.15 1.30 1.60 2.00 3.00]
#define LAMP_HEAT 1.50 //  [0.00 0.15 0.25 0.40 0.60 0.80 1.00 1.50]
// Independent component multipliers. Both 1 reproduce the legacy 65/35 mix.
#define VANILLA_FACE_CONTRAST 3.00 //  [0.00 0.15 0.25 0.35 0.50 0.65 0.85 1.00 1.25 1.50 2.00 3.00]
#define REALISTIC_FACE_CONTRAST 3.00 //  [0.00 0.15 0.25 0.35 0.50 0.65 0.85 1.00 1.25 1.50 2.00 3.00]
#define REALISTIC_LIGHTING 1 //  [0 1]
#define WET_WEATHER_MODE 1 //  [0 1]
#define SUN_CORE_BRIGHTNESS 8.00 //  [0.50 1.00 1.50 2.00 2.80 3.50 4.50 6.00 8.00]
#define SUN_HALO_STRENGTH 3.00 //  [0.00 0.15 0.35 0.65 0.85 1.00 1.20 1.50 2.00 3.00]
#define SUN_HALO_RADIUS 3.00 //  [0.35 0.50 0.75 1.00 1.25 1.50 2.00 3.00]
#define CIRRUS_DENSITY 3.00 //  [0.00 0.25 0.50 0.75 1.00 1.25 1.50 2.00 3.00]
#define FACE_BLEND 1.00 //  [0.00 0.25 0.50 0.75 1.00]
#define GROUND_WARMTH 2.00 //  [0.00 0.20 0.45 0.65 0.85 1.00 1.35 1.70 2.00]
#define WATER_DISTORTION 2.00 //  [0.00 0.20 0.35 0.55 0.75 1.00 1.20 1.35 1.60 2.00]
#define CIRRUS_AMOUNT 1.00 //  [0.00 0.35 0.65 0.85 1.00]
#define CIRRUS_ALTITUDE 1200.0 //  [200.0 240.0 280.0 320.0 360.0 400.0 460.0 560.0 700.0 900.0 1200.0]
#define CLOUD_STYLE 2 //  [0 1 2]
#define SUN_STYLE 1 //  [0 1]
#define WATER_TURBIDITY 6.00 //  [0.00 0.25 0.50 1.00 1.50 2.00 3.00 4.00 6.00]
#define BIOME_WATER 1 //  [0 1]
#define REFRACTION_QUALITY 2 //  [0 1 2]
#define ATMOSPHERE_QUALITY 2 //  [0 1 2]
#define WATER_RENDER_QUALITY 2 //  [0 1 2]
#define CLOUD_DENSITY 3.00 //  [0.15 0.30 0.50 0.75 1.00 1.30 1.70 2.20 3.00]
#define CLOUD_DETAIL 2.00 //  [0.00 0.25 0.50 0.75 1.00 1.30 1.70 2.00]
#define MIST_SCALE 480.0 //  [24.0 40.0 64.0 96.0 144.0 224.0 320.0 480.0]
#define MIST_BREAKUP 2.00 //  [0.00 0.25 0.50 0.85 1.00 1.30 1.70 2.00]
#define MIST_LIGHT 2.00 //  [0.00 0.20 0.40 0.65 0.85 1.00 1.50 2.00]
// Reuse the active animated water atlas pattern without changing opacity.
#define WATER_TEXTURE 1.00 //  [0.00 0.05 0.10 0.15 0.25 0.35 0.50 0.75 1.00]
#endif

// END INCLUDE /core/options.glsl


// BEGIN INCLUDE /core/frame.glsl
#ifndef STRATUS_FRAME_INCLUDED
#define STRATUS_FRAME_INCLUDED
uniform mat4 gbufferProjectionInverse;
uniform mat4 gbufferProjection;
uniform mat4 gbufferModelViewInverse;
uniform mat4 gbufferModelView;
uniform vec3 cameraPosition;
uniform vec3 sunPosition;
uniform float frameTimeCounter;
uniform int worldTime;
uniform vec3 biomeWaterTint;
uniform float biomeSilt;
uniform float biomeHumidity;
uniform float biomeWarmth;
uniform ivec2 eyeBrightnessSmooth;
uniform float rainStrength;
uniform float viewWidth;
uniform float viewHeight;
uniform float far;
uniform vec3 fogColor;
uniform float fogStart;
uniform float fogEnd;
uniform float fogDensity;
uniform int fogMode;
uniform int fogShape;
uniform int isEyeInWater;
uniform float blindness;
uniform float darknessFactor;

vec3 unitVector(vec3 inputVector) {
    return inputVector * inversesqrt(max(dot(inputVector, inputVector), 1e-12));
}
vec3 decodeDisplay(vec3 displayValue) {
    vec3 lo = displayValue / 12.92;
    vec3 hi = pow(max((displayValue + 0.055) / 1.055, vec3(0.0)), vec3(2.4));
    return mix(hi, lo, lessThanEqual(displayValue, vec3(0.04045)));
}
vec3 encodeDisplay(vec3 linearValue) {
    linearValue = max(linearValue, vec3(0.0));
    vec3 lo = linearValue * 12.92;
    vec3 hi = 1.055 * pow(linearValue, vec3(1.0 / 2.4)) - 0.055;
    return mix(hi, lo, lessThanEqual(linearValue, vec3(0.0031308)));
}
float daytimeWeight() {
    float hour = mod(float(worldTime) + 24000.0, 24000.0);
    float dawn = smoothstep(22500.0, 23999.0, hour) + 1.0 - smoothstep(12000.0, 13700.0, hour);
    return clamp(dawn, 0.0, 1.0);
}
vec3 positionFromDepth(vec2 screen, float deviceDepth) {
    vec4 unprojected = gbufferProjectionInverse * vec4(screen * 2.0 - 1.0, deviceDepth * 2.0 - 1.0, 1.0);
    return unprojected.xyz / max(unprojected.w, 1e-7);
}
vec3 playerFromView(vec3 viewPoint) {
    return (gbufferModelViewInverse * vec4(viewPoint, 1.0)).xyz;
}
vec3 broadLightDirection() {
    vec3 direction = mat3(gbufferModelViewInverse) * sunPosition;
    if (dot(direction, direction) < 0.001) direction = vec3(-0.35, 0.85, 0.40);
    return unitVector(direction);
}
vec3 sunlightColour() {
    float height = max(broadLightDirection().y, 0.0);
    return mix(vec3(1.0, 0.53, 0.25), vec3(1.0, 0.84, 0.61), smoothstep(0.02, 0.65, height));
}
vec2 viewportSize() { return max(vec2(viewWidth, viewHeight), vec2(1.0)); }
#endif

// END INCLUDE /core/frame.glsl


// BEGIN INCLUDE /core/medium.glsl
#ifndef STRATUS_MEDIUM_INCLUDED
#define STRATUS_MEDIUM_INCLUDED
// Snell and unpolarised dielectric Fresnel, air/water n=1.000/1.333.
// PBRT4, Reflection Models, Specular Reflection and Transmission.
float dielectricWaterFresnel(float cosine,float etaI,float etaT){
    float ci=clamp(cosine,0.0,1.0);
    float st2=(etaI*etaI)/(etaT*etaT)*(1.0-ci*ci);
    if(st2>=1.0)return 1.0;
    float ct=sqrt(max(1.0-st2,0.0));
    float rs=(etaI*ci-etaT*ct)/max(etaI*ci+etaT*ct,0.00001);
    float rp=(etaT*ci-etaI*ct)/max(etaT*ci+etaI*ct,0.00001);
    return clamp(0.5*(rs*rs+rp*rp),0.0,1.0);
}
vec3 activeWaterTint(vec3 tint){
#if BIOME_WATER == 1
    return clamp(tint,vec3(0.02),vec3(1.0));
#else
    return vec3(0.247,0.463,0.894);
#endif
}
float suspendedSediment(vec3 tint,float skyExposure){
#if BIOME_WATER == 1
    // Green/brown biome water carries organics. Rain runoff requires an open sky.
    float organic=smoothstep(0.05,0.38,tint.g-tint.b);
    float runoff=rainStrength*skyExposure*(0.16+0.28*biomeHumidity);
    float shelter=1.0-smoothstep(0.05,0.60,skyExposure);
    return WATER_TURBIDITY*(0.035+0.56*max(biomeSilt,organic)+runoff)*(1.0-0.65*shelter);
#else
    return WATER_TURBIDITY*0.06;
#endif
}
vec3 waterExtinction(vec3 tint,float skyExposure){
    tint=activeWaterTint(tint);
    float sediment=suspendedSediment(tint,skyExposure);
    // Beer-Lambert RGB absorption plus approximately achromatic particle scattering.
    vec3 absorption=vec3(0.205,0.067,0.026);
    absorption+=max(vec3(0.0),vec3(0.247,0.463,0.894)-tint)*vec3(0.08,0.18,0.18);
    return (absorption+vec3(sediment*0.42))*WATER_EXTINCTION/max(WATER_VISIBILITY,0.05);
}
vec3 waterBodyColour(vec3 tint,float skyExposure,float blockLight){
    tint=activeWaterTint(tint);
    float sediment=suspendedSediment(tint,skyExposure);
    vec3 regional=clamp(tint/vec3(0.247,0.463,0.894),vec3(0.15),vec3(2.0));
    vec3 blueGreen=vec3(0.035,0.125,0.180)*mix(vec3(1.0),regional,0.70);
    vec3 body=mix(blueGreen,vec3(0.16,0.13,0.065),clamp(sediment*0.8,0.0,0.65));
    float lighting=0.025+skyExposure*daytimeWeight()*0.9+blockLight*0.45;
    return body*lighting;
}
vec3 travelThroughWater(vec3 radiance,float distanceInWater,vec3 tint,float skyExposure,float blockLight){
    vec3 transmission=exp(-waterExtinction(tint,skyExposure)*max(distanceInWater,0.0));
    return radiance*transmission+waterBodyColour(tint,skyExposure,blockLight)*(1.0-transmission);
}
// Shared defaults also cover underwater pixels with no visible interface.
vec3 waterExtinction(){return waterExtinction(biomeWaterTint,1.0);}
vec3 waterBodyColour(float sky){return waterBodyColour(biomeWaterTint,sky,0.0);}
vec3 travelThroughWater(vec3 c,float d,float sky){return travelThroughWater(c,d,biomeWaterTint,sky,0.0);}
#endif

// END INCLUDE /core/medium.glsl


// BEGIN INCLUDE /core/forward.glsl
#ifndef STRATUS_FORWARD_INCLUDED
#define STRATUS_FORWARD_INCLUDED
// A dedicated single-channel target stores background transmittance left by
// ordinary forward alpha blends. RGB remains the composited forward scene.
// Recover premultiplied foreground radiance without subtracting an entire
// opaque background from partially transparent pixels.
vec3 forwardRadiance(vec3 scene,vec3 background,float transmission){
    return max(scene-background*clamp(transmission,0.0,1.0),vec3(0.0));
}
vec3 compositeForward(vec3 replacementBackground,vec3 foreground,float transmission){
    return replacementBackground*clamp(transmission,0.0,1.0)+foreground;
}
#endif

// END INCLUDE /core/forward.glsl


// BEGIN INCLUDE /core/submerged-compose.glsl
#ifndef STRATUS_SUBMERGED_COMPOSE_INCLUDED
#define STRATUS_SUBMERGED_COMPOSE_INCLUDED
// A clear interface still needs an invisible depth boundary: only the
// camera-to-exit segment contains water, never the air beyond the surface.
float submergedWaterDistance(vec2 screen,float deviceDepth,vec4 exitData){
    bool receiver=deviceDepth<0.999999;
    float distance=receiver?length(positionFromDepth(screen,deviceDepth)):0.0;
    if(exitData.a>0.5&&exitData.x>0.0){
        vec3 ray=positionFromDepth(screen,0.5);
        float exitDistance=length(ray)*(exitData.x/max(-ray.z,0.00001));
        return receiver?min(distance,exitDistance):exitDistance;
    }
    // Preserve the open-sky view when no exit geometry was rasterized.
    return distance;
}
vec3 submergedDirectView(vec3 scene,vec3 opaque,float transmission,vec2 screen,
    float frontDepth,float opaqueDepth,vec4 exitData){
    float sky=clamp(float(eyeBrightnessSmooth.y)/240.0,0.0,1.0);
    float lamp=clamp(float(eyeBrightnessSmooth.x)/240.0,0.0,1.0);
    float backgroundPath=submergedWaterDistance(screen,opaqueDepth,exitData);
    float foregroundPath=submergedWaterDistance(screen,frontDepth,exitData);
    vec3 background=travelThroughWater(opaque,backgroundPath,biomeWaterTint,sky,lamp);
    vec3 attenuation=exp(-waterExtinction(biomeWaterTint,sky)*foregroundPath);
    // Keep signed additive/crack corrections, while alpha-covered glass and
    // particles use their own foreground path and preserve background tint.
    if(transmission>=0.999)return background+(scene-opaque)*attenuation;
    vec3 foreground=forwardRadiance(scene,opaque,transmission)*attenuation;
    foreground+=waterBodyColour(biomeWaterTint,sky,lamp)*(1.0-transmission)*(1.0-attenuation);
    return compositeForward(background,foreground,transmission);
}
#endif

// END INCLUDE /core/submerged-compose.glsl

uniform sampler2D colortex0;
uniform sampler2D colortex1;
uniform sampler2D colortex2;
uniform sampler2D colortex3;
uniform sampler2D colortex4;
uniform sampler2D colortex8;
uniform sampler2D colortex12;
uniform sampler2D colortex13;
uniform sampler2D colortex14;
uniform sampler2D depthtex0;
uniform sampler2D depthtex1;
in vec2 rasterUV;
/* RENDERTARGETS: 3 */
layout(location=0)out vec4 completedScene;
void main(){
    vec3 scene=texture(colortex3,rasterUV).rgb;
    if(isEyeInWater==1){
        // The interface contributes depth only; all visible radiance remains
        // on the unbent camera ray, with water fog clipped at the exit.
        vec3 result=submergedDirectView(scene,texture(colortex4,rasterUV).rgb,
            clamp(texture(colortex14,rasterUV).r,0.0,1.0),rasterUV,
            texture(depthtex0,rasterUV).r,texture(depthtex1,rasterUV).r,
            texelFetch(colortex13,ivec2(gl_FragCoord.xy),0));
        completedScene=vec4(max(result,vec3(0)),1.0);return;
    }
    vec4 mark=texture(colortex0,rasterUV),depth=texture(colortex2,rasterUV);
    vec3 n=texture(colortex1,rasterUV).xyz;
    float sky=clamp(float(eyeBrightnessSmooth.y)/240.0,0.0,1.0);
    float lamp=clamp(float(eyeBrightnessSmooth.x)/240.0,0.0,1.0);
    if(mark.a<=0.5||depth.a<=0.5){
        completedScene=vec4(max(scene,vec3(0)),1.0);return;
    }
    ivec2 size=textureSize(colortex12,0);vec2 grid=rasterUV*vec2(size)-0.5;
    ivec2 cell=ivec2(floor(grid));vec2 f=fract(grid);vec3 optics=vec3(0);float total=0.0;
    for(int y=0;y<2;y++)for(int x=0;x<2;x++){
        ivec2 c=clamp(cell+ivec2(x,y),ivec2(0),size-ivec2(1));vec2 uv=(vec2(c)+0.5)/vec2(size);
        vec4 d=texture(colortex2,uv);vec3 normal=texture(colortex1,uv).xyz;
        float weight=(x==0?1.0-f.x:f.x)*(y==0?1.0-f.y:f.y);
        weight*=step(0.5,d.a)*step(0.8,dot(n,normal));
        weight*=exp(-abs(depth.x-d.x)/max(0.10,depth.x*0.025));
        optics+=texelFetch(colortex12,c,0).rgb*weight;total+=weight;
    }
    vec4 tint=texture(colortex8,rasterUV);if(dot(tint.rgb,tint.rgb)<0.001)tint.rgb=biomeWaterTint;
    vec3 ray=positionFromDepth(rasterUV,0.5),water=ray*(depth.x/max(-ray.z,0.00001));
    if(total>0.0001)optics/=total;
    else{
        float z=texture(depthtex1,rasterUV).r;
        float path=z<0.999999?length(positionFromDepth(rasterUV,z)-water):24.0;
        optics=travelThroughWater(texture(colortex4,rasterUV).rgb,path,tint.rgb,depth.y,tint.a);
    }
    // Keep glass, particles and other forward surfaces at full resolution.
    // A dark/tinted pane replaces part of the background; it is not a signed
    // colour delta that can be added to a different water background.
    float transmission=clamp(texture(colortex14,rasterUV).r,0.0,1.0);
    if(transmission>=0.999){
        // Preserve the existing full-resolution correction where no ordinary
        // alpha-blended surface replaces the background. Only covered pixels
        // need the new foreground/background transparency composition below.
        vec3 correction=scene-texture(colortex4,rasterUV).rgb;
        completedScene=vec4(max(optics+correction,vec3(0)),1.0);return;
    }
    vec3 foreground=forwardRadiance(scene,texture(colortex4,rasterUV).rgb,transmission);
    completedScene=vec4(max(compositeForward(optics,foreground,transmission),vec3(0)),1.0);
}

// END INCLUDE /core/water-resolve.frag.glsl
