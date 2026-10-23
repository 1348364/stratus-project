#version 330 core
layout(location = 0) out vec4 shim_FragData[8];
#define DIMENSION_TYPE 0
#define PASS_KIND 3
#define LATE_SURFACE 0

// BEGIN INCLUDE /core/options.glsl
#ifndef STRATUS_OPTIONS_INCLUDED
#define STRATUS_OPTIONS_INCLUDED
// Reference defaults use the explicitly approved latest Main tuning.
// All quality choices remain available; higher presets retain detailed optics.
#define SKY_AMBIENT 1.00 // [0.20 0.40 0.60 0.80 1.00 1.20 1.40 1.60 1.80 2.00 2.50 3.00 4.00]
#define EXPOSURE 0.20 // [-3.00 -2.00 -1.50 -1.00 -0.50 0.00 0.20 0.50 0.75 1.00 1.50 2.00 3.00]
const float ambientOcclusionLevel = 1.00; // [0.00 0.15 0.30 0.45 0.60 0.80 1.00]
#define WHITE_BALANCE 0.00 // [-0.24 -0.16 -0.08 -0.04 0.00 0.04 0.08 0.16 0.24]
#define SURFACE_SATURATION 1.00 // [0.00 0.25 0.50 0.75 0.85 0.93 1.00 1.07 1.15 1.30 1.50 1.75 2.00]
#define SURFACE_DAMPNESS 0.65 // [0.00 0.15 0.35 0.65 1.00 1.35 1.70 2.00 2.50 3.00]
#define CLOUD_AMOUNT 0.68 // [0.00 0.35 0.60 0.68 0.75 0.90 1.00]
#define CLOUD_ALTITUDE 256.0 // [64.0 96.0 128.0 160.0 192.0 224.0 256.0 320.0 384.0 512.0 640.0 768.0]
#define CLOUD_THICKNESS 12.0 // [4.0 12.0 20.0 32.0 40.0 56.0 72.0 96.0 128.0 160.0 200.0]
#define SKY_LEAK 0.35 // [0.00 0.10 0.15 0.25 0.35 0.50 0.70 1.00 1.40 2.00]
#define CLOUD_SPAN 240.0 // [64.0 96.0 160.0 240.0 360.0 540.0 700.0 900.0 1200.0 1800.0]
#define CLOUD_DISTORTION 0.85 // [0.00 0.25 0.45 0.65 0.85 1.00 1.25 1.50 2.00]
#define CLOUD_RELIEF 0.75 // [0.00 0.25 0.40 0.55 0.75 1.00 1.25 1.50]
#define CLOUD_DRIFT 0.25 // [0.00 0.10 0.25 0.45 0.70 1.00 1.50 2.00 3.00]
#define CLOUD_LAYERS 2 // [1 2 3]
#define MIST_AMOUNT 0.85 // [0.00 0.15 0.30 0.40 0.60 0.75 0.85 1.00 1.25 1.50 2.00 3.00]
#define MIST_Y 70.0 // [-32.0 0.0 32.0 48.0 64.0 70.0 88.0 112.0 144.0 192.0 256.0 320.0]
#define MIST_THICKNESS 18.0 // [4.0 7.0 9.0 12.0 18.0 24.0 32.0 48.0 64.0]
#define MIST_CLEAR 24.0 // [0.0 4.0 8.0 16.0 24.0 32.0 48.0 64.0 80.0 112.0 144.0]
#define MIST_DETAIL 3 // [1 2 3]
#define REFLECT_LEVEL 1.00 // [0.00 0.40 0.60 0.85 1.00]
#define REFLECTION_MODE 0 // [0 1 2]
#define REFLECT_RANGE 120.0 // [24.0 48.0 64.0 88.0 120.0 160.0 224.0 320.0]
#define WATER_VISIBILITY 2.20 // [0.05 0.10 0.20 0.35 0.50 0.70 0.90 1.10 1.30 1.70 2.20 3.00 4.00 6.00 8.00 12.00 16.00]
#define WATER_EXTINCTION 0.90 // [0.10 0.20 0.45 0.65 0.90 1.15 1.40 2.00 3.00]
#define RIPPLE_HEIGHT 0.55 // [0.00 0.15 0.30 0.55 0.80 1.00 1.30 1.70 2.20 3.00]
#define RIPPLE_SIZE 0.40 // [0.25 0.40 0.65 0.80 1.00 1.25 1.50 2.00 3.00 4.00]
#define RIPPLE_RATE 1.00 // [0.00 0.10 0.20 0.45 0.70 1.00 1.50 2.00 3.00]
#define FACE_SHADING 1.00 // [0.00 0.15 0.25 0.35 0.50 0.70 0.85 1.00 1.25 1.50 2.00]
#define WET_DARKENING 1.00 // [0.00 0.25 0.50 0.75 1.00 1.30 1.70 2.00 2.50]
#define WET_SHEEN 0.85 // [0.00 0.15 0.35 0.65 0.85 1.00 1.35 1.70 2.00]
#define BLOOM_STRENGTH 0.18 // [0.00 0.03 0.06 0.12 0.18 0.25 0.35 0.50 0.75 1.00]
#define BLOOM_RADIUS 3.00 // [0.25 0.50 1.00 1.50 2.00 3.00 4.00 6.00 8.00 12.00]
#define SUN_VISIBILITY 0.85 // [0.00 0.25 0.45 0.65 0.85 1.00 1.50 2.00 3.00]
#define LAMP_LEVEL 1.00 // [0.20 0.40 0.70 0.85 1.00 1.15 1.30 1.60 2.00 3.00]
#define LAMP_HEAT 0.25 // [0.00 0.15 0.25 0.40 0.60 0.80 1.00 1.50]
// Independent component multipliers. Both 1 reproduce the legacy 65/35 mix.
#define VANILLA_FACE_CONTRAST 1.00 // [0.00 0.15 0.25 0.35 0.50 0.65 0.85 1.00 1.25 1.50 2.00 3.00]
#define REALISTIC_FACE_CONTRAST 1.00 // [0.00 0.15 0.25 0.35 0.50 0.65 0.85 1.00 1.25 1.50 2.00 3.00]
#define REALISTIC_LIGHTING 0 // [0 1]
#define WET_WEATHER_MODE 0 // [0 1]
#define SUN_CORE_BRIGHTNESS 4.50 // [0.50 1.00 1.50 2.00 2.80 3.50 4.50 6.00 8.00]
#define SUN_HALO_STRENGTH 2.00 // [0.00 0.15 0.35 0.65 0.85 1.00 1.20 1.50 2.00 3.00]
#define SUN_HALO_RADIUS 1.50 // [0.35 0.50 0.75 1.00 1.25 1.50 2.00 3.00]
#define CIRRUS_DENSITY 1.00 // [0.00 0.25 0.50 0.75 1.00 1.25 1.50 2.00 3.00]
#define FACE_BLEND 1.00 // [0.00 0.25 0.50 0.75 1.00]
#define GROUND_WARMTH 0.00 // [0.00 0.20 0.45 0.65 0.85 1.00 1.35 1.70 2.00]
#define WATER_DISTORTION 1.00 // [0.00 0.20 0.35 0.55 0.75 1.00 1.20 1.35 1.60 2.00]
#define CIRRUS_AMOUNT 0.65 // [0.00 0.35 0.65 0.85 1.00]
#define CIRRUS_ALTITUDE 360.0 // [200.0 240.0 280.0 320.0 360.0 400.0 460.0 560.0 700.0 900.0 1200.0]
#define CLOUD_STYLE 0 // [0 1 2]
#define SUN_STYLE 0 // [0 1]
#define WATER_TURBIDITY 3.00 // [0.00 0.25 0.50 1.00 1.50 2.00 3.00 4.00 6.00]
#define BIOME_WATER 1 // [0 1]
#define REFRACTION_QUALITY 1 // [0 1 2]
#define ATMOSPHERE_QUALITY 1 // [0 1 2]
#define WATER_RENDER_QUALITY 1 // [0 1 2]
#define CLOUD_DENSITY 1.00 // [0.15 0.30 0.50 0.75 1.00 1.30 1.70 2.20 3.00]
#define CLOUD_DETAIL 1.00 // [0.00 0.25 0.50 0.75 1.00 1.30 1.70 2.00]
#define MIST_SCALE 96.0 // [24.0 40.0 64.0 96.0 144.0 224.0 320.0 480.0]
#define MIST_BREAKUP 0.85 // [0.00 0.25 0.50 0.85 1.00 1.30 1.70 2.00]
#define MIST_LIGHT 0.65 // [0.00 0.20 0.40 0.65 0.85 1.00 1.50 2.00]
// Active native layer strength; retained patterned tint in Stratus mode.
#define WATER_TEXTURE 1.00 // [0.00 0.05 0.10 0.15 0.25 0.35 0.50 0.75 1.00]

// Native appearance with Stratus optics, or the retained physical water model.
#define WATER_STYLE 1 // [0 1]
#define TRANSPARENT_REFLECTIONS 0.75 // [0.00 0.25 0.50 0.75 1.00 1.50 2.00]
#define TRANSPARENT_REFRACTION 0.50 // [0.00 0.25 0.50 0.75 1.00 1.50 2.00]

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


// BEGIN INCLUDE /core/ceiling.glsl
#ifndef STRATUS_CEILING_INCLUDED
#define STRATUS_CEILING_INCLUDED

// BEGIN INCLUDE /core/field.glsl
#ifndef STRATUS_FIELD_INCLUDED
#define STRATUS_FIELD_INCLUDED
float latticeValue(ivec2 cell) {
    uint seed = uint(cell.x) * 1664525u + uint(cell.y) * 1013904223u;
    seed = (seed ^ (seed >> 16u)) * 2246822519u;
    seed ^= seed >> 13u;
    return float(seed & 0x00ffffffu) / 16777215.0;
}
float smoothField(vec2 location) {
    ivec2 cell = ivec2(floor(location));
    vec2 f = fract(location);
    // Quintic interpolation gives continuous first and second derivatives.
    vec2 t = f * f * f * (f * (f * 6.0 - 15.0) + 10.0);
    vec2 row = vec2(mix(latticeValue(cell), latticeValue(cell + ivec2(1, 0)), t.x),
                    mix(latticeValue(cell + ivec2(0, 1)), latticeValue(cell + ivec2(1, 1)), t.x));
    return mix(row.x, row.y, t.y);
}
float volumeLattice(ivec3 cell) {
    uint seed = uint(cell.x) * 1664525u + uint(cell.y) * 1013904223u + uint(cell.z) * 747796405u;
    seed = (seed ^ (seed >> 16u)) * 2246822519u;
    seed ^= seed >> 13u;
    return float(seed & 0x00ffffffu) / 16777215.0;
}
float smoothVolume(vec3 location) {
    ivec3 cell = ivec3(floor(location));
    vec3 f = fract(location);
    vec3 t = f * f * f * (f * (f * 6.0 - 15.0) + 10.0);
    vec4 row = vec4(mix(volumeLattice(cell), volumeLattice(cell + ivec3(1,0,0)), t.x),
                    mix(volumeLattice(cell + ivec3(0,1,0)), volumeLattice(cell + ivec3(1,1,0)), t.x),
                    mix(volumeLattice(cell + ivec3(0,0,1)), volumeLattice(cell + ivec3(1,0,1)), t.x),
                    mix(volumeLattice(cell + ivec3(0,1,1)), volumeLattice(cell + ivec3(1,1,1)), t.x));
    return mix(mix(row.x, row.y, t.y), mix(row.z, row.w, t.y), t.z);
}
// Tetrahedral gradient noise removes the visible axis-aligned value-noise cells.
vec3 simplexGradient(ivec3 cell) {
    uint h = uint(cell.x) * 1664525u + uint(cell.y) * 1013904223u + uint(cell.z) * 747796405u;
    h = (h ^ (h >> 16u)) * 2246822519u; h ^= h >> 13u;
    const vec3 gradients[12] = vec3[12](vec3(1,1,0),vec3(-1,1,0),vec3(1,-1,0),vec3(-1,-1,0),
        vec3(1,0,1),vec3(-1,0,1),vec3(1,0,-1),vec3(-1,0,-1),
        vec3(0,1,1),vec3(0,-1,1),vec3(0,1,-1),vec3(0,-1,-1));
    return gradients[int(h % 12u)];
}
float simplexCorner(ivec3 cell, vec3 offset) {
    float weight = max(0.6 - dot(offset, offset), 0.0);
    weight *= weight;
    return weight * weight * dot(simplexGradient(cell), offset);
}
float simplexVolume(vec3 point) {
    ivec3 cell = ivec3(floor(point + dot(point, vec3(1.0/3.0))));
    vec3 a = point - vec3(cell) + float(cell.x + cell.y + cell.z) / 6.0;
    vec3 rank = step(a.yzx, a.xyz);
    ivec3 first = ivec3(min(rank, 1.0 - rank.zxy));
    ivec3 second = ivec3(max(rank, 1.0 - rank.zxy));
    float value = simplexCorner(cell, a)
                + simplexCorner(cell + first, a - vec3(first) + 1.0/6.0)
                + simplexCorner(cell + second, a - vec3(second) + 1.0/3.0)
                + simplexCorner(cell + ivec3(1), a - 0.5);
    return clamp(0.5 + 16.0 * value, 0.0, 1.0);
}
#endif

// END INCLUDE /core/field.glsl


// BEGIN INCLUDE /core/weather-volume.glsl
#ifndef STRATUS_WEATHER_VOLUME_INCLUDED
#define STRATUS_WEATHER_VOLUME_INCLUDED
// Original periodic3D data, rebuilt by generate_volume.py. Trilinear hardware
// sampling preserves rounded, continuous structure without cubic noise cells.
uniform sampler3D weatherNoise;
vec4 weatherVolume(vec3 p){return texture(weatherNoise,p);}
#endif

// END INCLUDE /core/weather-volume.glsl

vec3 atmosphericColour() {
#if DIMENSION_TYPE == 0
    vec3 day=decodeDisplay(vec3(0.69,0.72,0.76));
    return mix(decodeDisplay(vec3(0.06,0.085,0.14)),day,daytimeWeight())*(1.0-0.12*rainStrength);
#else
    return decodeDisplay(fogColor);
#endif
}
float solarDaylight(){return daytimeWeight()*smoothstep(-0.06,0.10,broadLightDirection().y);}
vec3 softSkyReflection(vec3 worldRay){
    vec3 ray=unitVector(worldRay);
    vec3 sky=atmosphericColour()*mix(0.65,1.05,smoothstep(-0.1,0.8,ray.y));
    float glow=exp(-max(1.0-dot(ray,broadLightDirection()),0.0)/0.08);
    return sky+sunlightColour()*glow*0.16*solarDaylight()*SKY_LEAK;
}
// Sample the running game's current vanilla square sun (or resource-pack
// replacement). It is shared by the sky and reflection environment cache.
uniform sampler2D vanillaSun;
vec3 polishedVanillaSun(vec3 ray){
    vec3 sun=broadLightDirection();
    float forward=dot(ray,sun);
    if(forward<=0.0)return vec3(0.0);
    vec3 pole=abs(sun.z)<0.99?vec3(0.0,0.0,1.0):vec3(0.0,1.0,0.0);
    vec3 right=unitVector(cross(pole,sun)),up=cross(sun,right);
    // Vanilla's textured sky quad has half extent 30 at distance 100.
    vec2 uv=vec2(dot(ray,right),dot(ray,up))/(forward*0.60)+0.5;
    if(min(uv.x,uv.y)<0.0||max(uv.x,uv.y)>=1.0)return vec3(0.0);
    ivec2 size=textureSize(vanillaSun,0);
    vec4 texel=texelFetch(vanillaSun,ivec2(uv*vec2(size)),0);
    // Keep the pixel silhouette; HDR warmth and the existing broad haze glow
    // provide polish without adding a round solar core over the square.
    return decodeDisplay(texel.rgb)*texel.a*sunlightColour()*SUN_CORE_BRIGHTNESS;
}
vec3 skyBackdrop(vec3 worldRay){
#if DIMENSION_TYPE != 0
    return decodeDisplay(fogColor);
#else
    vec3 ray=unitVector(worldRay);
    float horizon=exp(-max(ray.y,0.0)*5.0);
    vec3 zenith=decodeDisplay(mix(vec3(0.045,0.072,0.12),vec3(0.56,0.65,0.76),daytimeWeight()));
    vec3 sky=mix(zenith,atmosphericColour(),horizon);
    sky=mix(sky,atmosphericColour(),CLOUD_AMOUNT*0.20);
    float separation=max(1.0-dot(ray,broadLightDirection()),0.0);
    float glow=exp(-separation/0.08)*SKY_LEAK*0.22;
    vec3 disc=vec3(0.0);
#if SUN_STYLE == 0
    disc=polishedVanillaSun(ray)*SUN_VISIBILITY;
    // Sun-local scatter with a finite angular reach and smooth inverse-square
    // falloff. It never raises bloom on blocks, entities or the rest of the sky.
    float radius2=SUN_HALO_RADIUS*SUN_HALO_RADIUS;
    float halo=1.0/pow(1.0+separation/max(0.003*radius2,0.000001),2.0);
    halo*=1.0-smoothstep(0.025*radius2,0.060*radius2,separation);
    disc+=sunlightColour()*halo*SUN_HALO_STRENGTH*SUN_VISIBILITY*0.65;
#endif
    sky+=solarDaylight()*(sunlightColour()*glow+disc*(1.0-0.65*rainStrength));
    return sky;
#endif
}
// Read the running game's cloud map: current vanilla (including resource-pack
// replacements), rather than a guessed procedural or bundled historical layout.
// texelFetch and explicit wrapping preserve every connected pixel and hole.
uniform sampler2D vanillaClouds;
vec2 cloudMapPosition(vec2 worldXZ){
    float cellSize=max(CLOUD_SPAN*0.05,1.0); // default 240 -> vanilla 12-block cells
    vec2 wind=vec2(frameTimeCounter*CLOUD_DRIFT*2.4,0.0);
    return (worldXZ+wind)/cellSize+vec2(0.0,0.33);
}
float vanillaCloudCell(vec2 mapPoint){
    ivec2 size=textureSize(vanillaClouds,0);
    ivec2 cell=ivec2(mod(floor(mapPoint),vec2(size)));
    return step(0.1,texelFetch(vanillaClouds,cell,0).a);
}
vec2 layeredCloudSample(vec3 worldPoint,bool detailed,bool upper){
    float altitude=upper?CIRRUS_ALTITUDE:CLOUD_ALTITUDE;
    float thickness=upper?28.0:CLOUD_THICKNESS;
    float amount=upper?CIRRUS_AMOUNT:CLOUD_AMOUNT;
    if(amount<=0.0)return vec2(0.0);
    float h=(worldPoint.y-altitude)/max(thickness,1.0)+0.5;
    if(upper){
        // The envelope is exactly zero outside this slab: skip all field work.
        if(h<=0.0||h>=1.0)return vec2(0.0,h);
        // A continuous thin veil, independent of the lower cloud texture, span,
        // coverage and distortion. Broad stretched fields give gentle wisps
        // across the sky, including the gaps between the physical clouds.
        vec2 p=(worldPoint.xz+frameTimeCounter*CLOUD_DRIFT*vec2(1.2,-0.3))/680.0;
        float broad=smoothField(p*vec2(0.32,1.4)+vec2(37.2,-19.1));
        float strands=smoothField(p*vec2(0.55,4.2)+vec2(broad*0.4,13.5));
        float veil=mix(0.22,0.90,smoothstep(0.15,0.85,mix(broad,strands,0.55)));
        float envelope=smoothstep(0.0,0.3,h)*(1.0-smoothstep(0.65,1.0,h));
        return vec2(veil*envelope*amount*CLOUD_DENSITY*CIRRUS_DENSITY*0.045,h);
    }
    // Relief can shift h by at most this amount. Beyond it the lower envelope
    // is exactly zero, including overburden/sun samples outside the cloud.
    float reliefBound=abs(CLOUD_DISTORTION)*0.04;
    if(h<=-reliefBound||h>=1.0+reliefBound)return vec2(0.0,h);
    vec2 mapPoint=cloudMapPosition(worldPoint.xz);
    float mask=vanillaCloudCell(mapPoint);
    if(mask<0.5)return vec2(0.0);
    // Simple extruded, connected forms. No erosion, pores or 3D billow noise.
    // Gentle vertical relief never moves the vanilla horizontal silhouette.
    float broad=smoothField(mapPoint*0.065+vec2(8.1,3.7));
    h-=(broad-0.5)*CLOUD_DISTORTION*0.08;
    float envelope=smoothstep(0.0,0.08,h)*(1.0-smoothstep(0.88,1.0,h));
    float gradient=mix(0.88,1.05,clamp(h,0.0,1.0));
    // Retain the saved CLOUD_DETAIL control as broad gradient strength. It no
    // longer adds high-frequency geometry; sampling quality cannot alter shape.
    gradient=mix(1.0,gradient,clamp(CLOUD_DETAIL*0.5,0.0,1.0));
    return vec2(mask*envelope*gradient*CLOUD_DENSITY*(amount/0.68)*0.120,h);
}
vec2 cloudVolumeSample(vec3 p,bool detailed){return layeredCloudSample(p,detailed,false);}
vec2 cloudSample(vec3 p){return layeredCloudSample(p,true,false);}
float cloudSunTransmission(vec3 point){
    vec3 l=broadLightDirection();float tau=0.0;
    const int samples=ATMOSPHERE_QUALITY==2?2+CLOUD_LAYERS:3;
    float distance=CLOUD_THICKNESS*1.8;
    for(int i=0;i<samples;i++){
        float t=(float(i)+0.5)/float(samples);
        tau+=layeredCloudSample(point+l*distance*t,false,false).x*distance/float(samples);
    }
    return exp(-tau);
}
float cloudPhase(float cosine){
    float forward=0.64,backward=-0.25;
    float f=(1.0-forward*forward)/pow(max(1.0+forward*forward-2.0*forward*cosine,0.02),1.5);
    float b=(1.0-backward*backward)/pow(max(1.0+backward*backward-2.0*backward*cosine,0.02),1.5);
    return 0.85*f+0.15*b;
}
vec4 overLayers(vec4 front,vec4 back){
    float alpha=front.a+(1.0-front.a)*back.a;
    return vec4((front.rgb*front.a+back.rgb*back.a*(1.0-front.a))/max(alpha,0.00001),alpha);
}
vec4 marchSingleCloud(vec3 origin,vec3 worldRay,float distanceLimit,int steps,bool shadows,bool upper){
#if DIMENSION_TYPE != 0 || CLOUD_STYLE != 0
    return vec4(0.0);
#else
    float amount=upper?CIRRUS_AMOUNT:CLOUD_AMOUNT;if(amount<=0.0)return vec4(0.0);
    float altitude=upper?CIRRUS_ALTITUDE:CLOUD_ALTITUDE;
    float thickness=upper?28.0:CLOUD_THICKNESS;
    float bottom=altitude-thickness*0.72,top=altitude+thickness*0.72;
    vec3 ray=unitVector(worldRay);float begin=0.0,finish=min(distanceLimit,7000.0);
    if(abs(ray.y)<0.0001){if(origin.y<bottom||origin.y>top)return vec4(0.0);}
    else{float a=(bottom-origin.y)/ray.y,b=(top-origin.y)/ray.y;begin=max(min(a,b),0.0);finish=min(finish,max(a,b));}
    // From inside a cloud, kilometre-long grazing rays spent almost the whole
    // budget on distant cells and resolved the nearby volume as thin sheets.
    // Keep four broad formations in range, blending the bound through the slab
    // edges so vertical movement does not switch integration domains abruptly.
    float interior=smoothstep(bottom,bottom+thickness*0.22,origin.y)
        *(1.0-smoothstep(top-thickness*0.22,top,origin.y));
    finish=min(finish,mix(7000.0,max(512.0,CLOUD_SPAN*4.0),interior));
    if(finish<=begin)return vec4(0.0);
    // Continuous midpoint quadrature over the clipped segment. Direction-
    // dependent world-plane sizes changed grid phase across pixels, producing
    // seams and moire inside the layer. The density field remains world-space;
    // no temporal jitter or camera-anchored noise is introduced.
    float advance=(finish-begin)/max(float(steps),1.0),start=begin;
    float transmission=1.0;vec3 scattered=vec3(0.0);
    float phase=cloudPhase(dot(ray,broadLightDirection()));
    for(int i=0;i<1024;i++){
        if((upper&&i>=steps)||start>=finish)break;
        float end=min(start+advance,finish);
        if(!upper){
            // Split quadrature at the exact vanilla cell boundary. Uniform
            // long steps skipped tiny cells and created horizon speckles.
            // Density is simple enough to spend samples on silhouette accuracy.
            float epsilon=0.0005;
            vec2 grid=cloudMapPosition((origin+ray*(start+epsilon)).xz);
            vec2 fraction=fract(grid);
            vec2 edge=mix(fraction,1.0-fraction,greaterThan(ray.xz,vec2(0.0)));
            vec2 crossing=edge*max(CLOUD_SPAN*0.05,1.0)/max(abs(ray.xz),vec2(0.000001));
            end=min(end,start+epsilon+min(crossing.x,crossing.y));
        }
        float stride=max(end-start,0.0);
        vec3 point=origin+ray*(start+end)*0.5;
        vec2 sampleData=layeredCloudSample(point,true,upper);
        if(sampleData.x>0.00001){
            float opacity=1.0-exp(-sampleData.x*stride);
            float h=clamp(sampleData.y,0.0,1.0);
            float sunlight=shadows&&!upper?cloudSunTransmission(point):mix(0.3,1.0,h);
            float overburden=layeredCloudSample(point+vec3(0.0,thickness*0.22,0.0),false,upper).x;
            float ambientSky=exp(-overburden*thickness*0.85);
            float ambient=mix(0.48,1.0,h)*mix(0.62,1.2,ambientSky);
            float powder=1.0-exp(-sampleData.x*35.0);
            vec3 daylight=vec3(0.32,0.37,0.45)*ambient;
            daylight+=sunlightColour()*sunlight*(0.30+phase*0.055*SUN_VISIBILITY);
            daylight+=vec3(0.12,0.135,0.16)*powder*(0.4+0.6*h);
            if(upper)daylight=mix(daylight,vec3(0.80,0.84,0.90)+sunlightColour()*0.10,0.65);
            daylight*=mix(1.0,0.72+0.28*sunlight,CLOUD_RELIEF);
            daylight+=sunlightColour()*phase*SKY_LEAK*0.055*sunlight;
            vec3 colour=mix(vec3(0.006,0.010,0.019)*ambient,daylight,solarDaylight());
            colour*=1.0-0.17*rainStrength;
            scattered+=transmission*opacity*colour;transmission*=1.0-opacity;
            if(transmission<0.012)break;
        }
        start=end;
    }
    vec3 colour=scattered/max(1.0-transmission,0.0001);
    colour=mix(colour,atmosphericColour(),1.0-exp(-max(begin-150.0,0.0)*0.00025));
    return vec4(colour,(1.0-transmission)*(1.0-smoothstep(3500.0,7000.0,begin)));
#endif
}
vec4 marchCloudLayer(vec3 origin,vec3 ray,float limit,int steps,bool shadows){
    vec4 low=marchSingleCloud(origin,ray,limit,steps,shadows,false);
    vec4 high=marchSingleCloud(origin,ray,limit,max(4,steps/2),false,true);
    return ray.y<0.0?overLayers(high,low):overLayers(low,high);
}
vec4 physicalCloudLayer(vec3 origin,vec3 ray,float limit){return marchCloudLayer(origin,ray,limit,32+CLOUD_LAYERS*40,true);}
vec3 overcastCeiling(vec3 worldRay){
    // A prefiltered reflection approximation avoids a cloud ray march per water pixel.
    vec3 ray=unitVector(worldRay);vec3 sky=skyBackdrop(ray);
    if(abs(ray.y)<0.01)return mix(sky,atmosphericColour(),0.75);
    float distanceToLayer=(CLOUD_ALTITUDE-cameraPosition.y)/ray.y;
    if(distanceToLayer>0.0){
        vec3 point=cameraPosition+ray*distanceToLayer;
        vec2 density=layeredCloudSample(point,false,false);
        // Prefilter the broad cloud contribution: sharp density patches do not
        // survive a rough, rippling water reflection.
        float coverage=smoothstep(0.0,0.040,density.x);
        vec3 colour=atmosphericColour()*mix(0.90,1.13,coverage);
        sky=mix(sky,colour,CLOUD_AMOUNT*0.72);
    }
    return sky;
}
#endif

// END INCLUDE /core/ceiling.glsl


// BEGIN INCLUDE /core/air.glsl
#ifndef STRATUS_AIR_INCLUDED
#define STRATUS_AIR_INCLUDED

// BEGIN INCLUDE /core/field.glsl
#ifndef STRATUS_FIELD_INCLUDED
#define STRATUS_FIELD_INCLUDED
float latticeValue(ivec2 cell) {
    uint seed = uint(cell.x) * 1664525u + uint(cell.y) * 1013904223u;
    seed = (seed ^ (seed >> 16u)) * 2246822519u;
    seed ^= seed >> 13u;
    return float(seed & 0x00ffffffu) / 16777215.0;
}
float smoothField(vec2 location) {
    ivec2 cell = ivec2(floor(location));
    vec2 f = fract(location);
    // Quintic interpolation gives continuous first and second derivatives.
    vec2 t = f * f * f * (f * (f * 6.0 - 15.0) + 10.0);
    vec2 row = vec2(mix(latticeValue(cell), latticeValue(cell + ivec2(1, 0)), t.x),
                    mix(latticeValue(cell + ivec2(0, 1)), latticeValue(cell + ivec2(1, 1)), t.x));
    return mix(row.x, row.y, t.y);
}
float volumeLattice(ivec3 cell) {
    uint seed = uint(cell.x) * 1664525u + uint(cell.y) * 1013904223u + uint(cell.z) * 747796405u;
    seed = (seed ^ (seed >> 16u)) * 2246822519u;
    seed ^= seed >> 13u;
    return float(seed & 0x00ffffffu) / 16777215.0;
}
float smoothVolume(vec3 location) {
    ivec3 cell = ivec3(floor(location));
    vec3 f = fract(location);
    vec3 t = f * f * f * (f * (f * 6.0 - 15.0) + 10.0);
    vec4 row = vec4(mix(volumeLattice(cell), volumeLattice(cell + ivec3(1,0,0)), t.x),
                    mix(volumeLattice(cell + ivec3(0,1,0)), volumeLattice(cell + ivec3(1,1,0)), t.x),
                    mix(volumeLattice(cell + ivec3(0,0,1)), volumeLattice(cell + ivec3(1,0,1)), t.x),
                    mix(volumeLattice(cell + ivec3(0,1,1)), volumeLattice(cell + ivec3(1,1,1)), t.x));
    return mix(mix(row.x, row.y, t.y), mix(row.z, row.w, t.y), t.z);
}
// Tetrahedral gradient noise removes the visible axis-aligned value-noise cells.
vec3 simplexGradient(ivec3 cell) {
    uint h = uint(cell.x) * 1664525u + uint(cell.y) * 1013904223u + uint(cell.z) * 747796405u;
    h = (h ^ (h >> 16u)) * 2246822519u; h ^= h >> 13u;
    const vec3 gradients[12] = vec3[12](vec3(1,1,0),vec3(-1,1,0),vec3(1,-1,0),vec3(-1,-1,0),
        vec3(1,0,1),vec3(-1,0,1),vec3(1,0,-1),vec3(-1,0,-1),
        vec3(0,1,1),vec3(0,-1,1),vec3(0,1,-1),vec3(0,-1,-1));
    return gradients[int(h % 12u)];
}
float simplexCorner(ivec3 cell, vec3 offset) {
    float weight = max(0.6 - dot(offset, offset), 0.0);
    weight *= weight;
    return weight * weight * dot(simplexGradient(cell), offset);
}
float simplexVolume(vec3 point) {
    ivec3 cell = ivec3(floor(point + dot(point, vec3(1.0/3.0))));
    vec3 a = point - vec3(cell) + float(cell.x + cell.y + cell.z) / 6.0;
    vec3 rank = step(a.yzx, a.xyz);
    ivec3 first = ivec3(min(rank, 1.0 - rank.zxy));
    ivec3 second = ivec3(max(rank, 1.0 - rank.zxy));
    float value = simplexCorner(cell, a)
                + simplexCorner(cell + first, a - vec3(first) + 1.0/6.0)
                + simplexCorner(cell + second, a - vec3(second) + 1.0/3.0)
                + simplexCorner(cell + ivec3(1), a - 0.5);
    return clamp(0.5 + 16.0 * value, 0.0, 1.0);
}
#endif

// END INCLUDE /core/field.glsl

// Closed-form integrals for a vertical mist profile. No volumetric ray march.
float approximateErf(float inputValue) {
    float x = abs(inputValue);
    float t = 1.0 / (1.0 + 0.3275911 * x);
    float polynomial = (((((1.061405429 * t - 1.453152027) * t)
                       + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t;
    return sign(inputValue) * (1.0 - polynomial * exp(-x * x));
}
float averageGaussian(float lowY, float highY, float centre, float sigma) {
    float a = (lowY - centre) / (1.41421356237 * sigma);
    float b = (highY - centre) / (1.41421356237 * sigma);
    if (abs(highY - lowY) < 0.02) return exp(-a * a);
    return max(0.0, sigma * 1.2533141373 * (approximateErf(b) - approximateErf(a)) / (highY - lowY));
}
float averageExponential(float lowY, float highY) {
    float a = clamp(lowY - MIST_Y, -60.0, 500.0);
    float b = clamp(highY - MIST_Y, -60.0, 500.0);
    float scale = MIST_THICKNESS * 2.7;
    if (abs(b - a) < 0.02) return exp(-a / scale);
    return max(0.0, (exp(-a / scale) - exp(-b / scale)) * scale / (b - a));
}
float backgroundMistWeight(float distanceAlongRay) {
    // A clear foreground and a gradual transition prevent a nearby grey veil.
    float blendDistance = max(32.0, MIST_CLEAR * 0.80);
    return smoothstep(MIST_CLEAR, MIST_CLEAR + blendDistance, distanceAlongRay);
}
float valleyOpacity(vec3 relativePoint, float skyExposure) {
#if DIMENSION_TYPE != 0
    return 0.0;
#else
    if (isEyeInWater != 0) return 0.0;
    float distanceAlongRay = length(relativePoint);
    float coveredLength = max(distanceAlongRay - MIST_CLEAR, 0.0);
    vec3 startWorld = cameraPosition + relativePoint * min(MIST_CLEAR / max(distanceAlongRay, 0.001), 1.0);
    vec3 finishWorld = cameraPosition + relativePoint;
    float density = 0.0011 * averageExponential(startWorld.y, finishWorld.y);
    density += 0.0068 * averageGaussian(startWorld.y, finishWorld.y, MIST_Y, MIST_THICKNESS);
    density += 0.0038 * averageGaussian(startWorld.y, finishWorld.y, MIST_Y + MIST_THICKNESS * 2.45, MIST_THICKNESS * 0.80);
    vec2 midpoint = (startWorld.xz + finishWorld.xz) * 0.0018;
    float patch = smoothField(midpoint);
#if MIST_DETAIL > 1
    patch = mix(patch, smoothField(midpoint * 1.71 + vec2(17.2, -9.8)), 0.25);
#endif
#if MIST_DETAIL > 2
    patch = mix(patch, smoothField(midpoint * 2.43 - vec2(11.3, 28.6)), 0.09);
#endif
    float opticalDepth = coveredLength * density * MIST_AMOUNT * mix(0.72, 1.24, patch)
                       * backgroundMistWeight(distanceAlongRay);
    float localMist = 1.0 - exp(-min(opticalDepth, 25.0));
    float edge = smoothstep(max(far * 0.86, 1.0), max(far, 2.0), max(length(relativePoint.xz), abs(relativePoint.y)));
    return (1.0 - (1.0 - localMist) * (1.0 - edge)) * smoothstep(0.06, 0.58, skyExposure);
#endif
}
float engineOpacity(vec3 relativePoint) {
    if (fogMode == 0) return 0.0;
    float distanceMetric = length(relativePoint);
    if (fogShape == 1) distanceMetric = max(length(relativePoint.xz), abs(relativePoint.y));
    if (fogMode == 2048) return 1.0 - exp(-distanceMetric * max(fogDensity, 0.0));
    if (fogMode == 2049) return 1.0 - exp(-pow(distanceMetric * max(fogDensity, 0.0), 2.0));
    if (fogEnd <= fogStart) return float(distanceMetric >= fogEnd);
    return smoothstep(fogStart, fogEnd, distanceMetric);
}
vec3 throughAir(vec3 radiance, vec3 relativePoint, float skyExposure) {
#if DIMENSION_TYPE == 0
    // Outdoor atmospheric transport is integrated once after water, at half res.
    if(isEyeInWater==0 && max(blindness,darknessFactor)<0.001)return radiance;
#endif
    float mist = 0.0;
    vec3 airResult = radiance * (1.0 - mist) + atmosphericColour() * mist;
    // Water attenuation is applied once in composite, to the actual camera-to-
    // interface distance. This keeps top, side and underwater paths consistent.
    if (isEyeInWater == 1) {
#if WATER_STYLE == 1
        // Native environmental fog already includes game status effects.
        return airResult;
#endif
        float waterStatus = clamp(max(blindness, darknessFactor), 0.0, 1.0);
        return airResult * (1.0 - waterStatus * smoothstep(2.0, 13.0, length(relativePoint)));
    }
    float engineFog = clamp(engineOpacity(relativePoint), 0.0, 1.0);
#if DIMENSION_TYPE == 0
    if (isEyeInWater == 0 && max(blindness, darknessFactor) < 0.001) {
        // Ordinary outdoor engine fog fills only opacity missing from our mist,
        // rather than applying a second full haze layer over the scene.
        engineFog *= backgroundMistWeight(length(relativePoint));
        engineFog = max(engineFog - mist, 0.0) / max(1.0 - mist, 0.0001);
    }
#endif
    airResult = mix(airResult, decodeDisplay(fogColor), engineFog);
    float status = clamp(max(blindness, darknessFactor), 0.0, 1.0);
    return airResult * (1.0 - status * smoothstep(2.0, 13.0, length(relativePoint)));
}
#endif

// END INCLUDE /core/air.glsl


// BEGIN INCLUDE /core/diffuse.glsl
#ifndef STRATUS_DIFFUSE_INCLUDED
#define STRATUS_DIFFUSE_INCLUDED
// Approximate properties for ordinary textures without PBR maps.
// x: water-absorption response, y: perceptual roughness. These are independent:
// rough metal/glazed ceramic still has zero pore absorption. Heuristic classes,
// not measured porosity. Stone and embedded ores share a class.
vec2 wetMaterialProperties(int material) {
    if (material == 4110) return vec2(0.90, 0.96);
    if (material == 4111) return vec2(0.64, 0.80);
    if (material == 4113) return vec2(0.02, 0.68);
    if (material == 4114 || (material>=4120&&material<=4123)) return vec2(0.00, 0.38);
    if (material == 4115) return vec2(0.80, 0.98);
    if (material == 4116) return vec2(0.16, 0.48);
    if (material == 4117) return vec2(0.72, 0.91);
    return vec2(0.45, 0.86);
}
vec3 formIrradiance(vec3 normal, float skyExposure) {
    float vertical=normal.y>=0.0?1.0:0.5;
    float vanilla=dot(normal*normal,vec3(0.6,vertical,0.8));
    float vanillaWeight=1.0,physicalWeight=0.0;
    float physical=1.0;
#if DIMENSION_TYPE == 0
    vec3 sun=broadLightDirection();
    float direct=daytimeWeight()*smoothstep(-0.04,0.16,sun.y)*(1.0-0.85*rainStrength);
    float facing=max(dot(normal,sun),0.0);
    float hemisphere=mix(0.38,0.78,normal.y*0.5+0.5);
    physical=hemisphere*(1.0-0.20*direct)+0.44*direct*facing;
    float exposure=smoothstep(0.08,0.85,skyExposure);
    vanillaWeight=1.0-0.35*exposure;physicalWeight=0.35*exposure;
#endif
    // Separate linear components preserve the exact old mixture at 1/1.
    // Each zero removes only that component; both zero produce unshaded faces.
    float contrast=(vanilla-1.0)*vanillaWeight*VANILLA_FACE_CONTRAST
                  +(physical-1.0)*physicalWeight*REALISTIC_FACE_CONTRAST;
    float irradiance=1.0+contrast;
    float strength=FACE_BLEND*FACE_SHADING;
    // Linear contrast keeps saved 2.0 settings readable instead of squaring
    // already-dark surfaces. Zero for either control is an exact bypass.
    return vec3(clamp(1.0+(irradiance-1.0)*strength,0.18,1.18));
}
// A surface film adds reflected highlights without changing the diffuse albedo.
// Absorption darkening/retained dampness was deliberately retired in 1.6.9.
// Material.x remains in the buffer for saved-layout compatibility, not gating.
vec3 wetSurfaceResponse(vec3 dry,vec3 n,vec3 playerPoint,float sky,vec2 material){
#if DIMENSION_TYPE == 0
    float filmSource=WET_WEATHER_MODE==0?1.0:rainStrength;
    float film=filmSource*SURFACE_DAMPNESS*smoothstep(0.18,0.85,sky)
        *mix(0.78,1.0,clamp(n.y*0.5+0.5,0.0,1.0));
    if(WET_SHEEN>0.0&&film>0.0001){
        vec3 view=unitVector(-playerPoint);
        float nv=max(dot(n,view),0.0);
        if(nv>0.001){
            float fresnel=0.08+0.92*pow(1.0-nv,5.0);
            float coat=clamp(film*WET_SHEEN*fresnel*0.25,0.0,0.22);
            vec3 environment=softSkyReflection(reflect(-view,n));
            // Reflection can be lighter or darker than a white block. This is
            // angle-dependent film, never absorption or diffuse recolouring.
            dry=mix(dry,environment,coat);
            vec3 light=broadLightDirection(),halfway=unitVector(view+light);
            float exponent=mix(80.0,16.0,clamp(material.y,0.0,1.0));
            float lobe=pow(max(dot(n,halfway),0.0),exponent)*(exponent+2.0)/6.283185307;
            dry+=sunlightColour()*solarDaylight()*max(dot(n,light),0.0)
                *lobe*film*WET_SHEEN*0.008*(1.0-0.65*rainStrength);
        }
    }
#endif
    // Keep the retired option discoverable by Iris; every allowed value is a no-op.
    return dry+vec3(0.0)*WET_DARKENING;
}
vec3 diffuseRadiance(vec3 colour, vec3 mappedLight, float skyExposure, vec3 worldNormal,
                     float kind, vec3 playerPoint, int material) {
    if (kind < 0.5) return decodeDisplay(colour);
#if REALISTIC_LIGHTING == 0
    // oldLighting=true supplies Minecraft's original vertex face shading/AO.
    // Vanilla multiplies texture/vertex colour by the game's lightmap in display
    // space. Decode their product once, then bypass artistic grading at output.
    return decodeDisplay(colour*mappedLight);
#else
    vec3 normal = unitVector(worldNormal);
    if (dot(normal, normal) < 0.1) normal = vec3(0.0, 1.0, 0.0);
    float lampShare = 1.0 - smoothstep(0.08, 0.85, skyExposure) * daytimeWeight();
    vec3 light = decodeDisplay(mappedLight) * mix(LAMP_LEVEL, SKY_AMBIENT, skyExposure);
    light *= mix(vec3(1.0), vec3(1.015, 0.985, 0.87), LAMP_HEAT * lampShare);
    // Entities, held items and blocks get form lighting; billboard quads do not.
    vec3 form = kind > 0.95 ? formIrradiance(normal, skyExposure) : vec3(1.0);
    // Material wetness is applied once by the opaque resolve (or late block pass).
    vec3 albedo = decodeDisplay(colour);
    vec3 reflected = albedo * light * form;
    if (kind > 1.5 && kind < 2.5) {
        float interior = smoothstep(0.48, 0.94, max(colour.r, max(colour.g, colour.b)));
        reflected = max(reflected, decodeDisplay(colour) * interior * LAMP_LEVEL * 2.1);
    }
    return reflected;
#endif
}
#endif

// END INCLUDE /core/diffuse.glsl


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
// Native underwater fog uses the running game's environmental range/colour.
// Above the interface vanilla has a surface alpha layer, not water-depth fog.
float nativeWaterOpacity(float distanceInWater){
    if(isEyeInWater!=1||distanceInWater<=0.0)return 0.0;
    return clamp((distanceInWater-fogStart)/max(fogEnd-fogStart,0.0001),0.0,1.0);
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
#if WATER_STYLE == 1
    return decodeDisplay(fogColor);
#else
    tint=activeWaterTint(tint);
    float sediment=suspendedSediment(tint,skyExposure);
    vec3 regional=clamp(tint/vec3(0.247,0.463,0.894),vec3(0.15),vec3(2.0));
    vec3 blueGreen=vec3(0.035,0.125,0.180)*mix(vec3(1.0),regional,0.70);
    vec3 body=mix(blueGreen,vec3(0.16,0.13,0.065),clamp(sediment*0.8,0.0,0.65));
    float lighting=0.025+skyExposure*daytimeWeight()*0.9+blockLight*0.45;
    return body*lighting;
#endif
}
vec3 waterTransmission(float distanceInWater,vec3 tint,float skyExposure){
#if WATER_STYLE == 1
    return vec3(1.0-nativeWaterOpacity(distanceInWater));
#else
    return exp(-waterExtinction(tint,skyExposure)*max(distanceInWater,0.0));
#endif
}
vec3 travelThroughWater(vec3 radiance,float distanceInWater,vec3 tint,float skyExposure,float blockLight){
#if WATER_STYLE == 1
    return decodeDisplay(mix(encodeDisplay(radiance),fogColor,nativeWaterOpacity(distanceInWater)));
#else
    vec3 transmission=waterTransmission(distanceInWater,tint,skyExposure);
    return radiance*transmission+waterBodyColour(tint,skyExposure,blockLight)*(1.0-transmission);
#endif
}
// Shared defaults also cover underwater pixels with no visible interface.
vec3 waterExtinction(){return waterExtinction(biomeWaterTint,1.0);}
vec3 waterBodyColour(float sky){return waterBodyColour(biomeWaterTint,sky,0.0);}
vec3 travelThroughWater(vec3 c,float d,float sky){return travelThroughWater(c,d,biomeWaterTint,sky,0.0);}
#endif

// END INCLUDE /core/medium.glsl

#ifndef BLOCK_SURFACE
#define BLOCK_SURFACE 0
#endif
in vec4 tintAndOpacity;
in vec2 atlasCoordinate;
in vec2 illuminationCoordinate;
in vec3 relativeLocation;
in vec3 orientedNormal;
uniform sampler2D gtexture;
uniform sampler2D lightmap;
uniform int entityId;
#if PASS_KIND == 3 || PASS_KIND == 6
flat in int blockCategory;
#endif
#if PASS_KIND == 4 || PASS_KIND == 5
uniform vec4 entityColor;
#endif
#if PASS_KIND == 6
/* RENDERTARGETS: 3,0,1,2,8,13,14,15 */
#elif LATE_SURFACE == 1
/* RENDERTARGETS: 3,0,1,2,8,14 */
#else
/* RENDERTARGETS: 3,0,1,2,8 */
#endif
void main() {
#if PASS_KIND == 8 || (PASS_KIND == 12 && SUN_STYLE == 0) || (PASS_KIND == 13 && CLOUD_STYLE != 1)
    discard;
#else
    if (entityId == 4200) discard;
    vec4 surface = tintAndOpacity;
#if PASS_KIND != 0
    vec4 atlasTexel=texture(gtexture, atlasCoordinate);
    surface *= atlasTexel;
#endif
#if PASS_KIND == 12
    // Vanilla sun/moon textures use black additive backgrounds, not cutout alpha.
    if(max(surface.r,max(surface.g,surface.b))<0.012)discard;
#endif
#if PASS_KIND == 6
    bool opticalSolid=blockCategory>=4120&&blockCategory<=4123;
    // Clear glass interiors still have a reflective interface.
    if(surface.a<=0.001&&!opticalSolid)discard;
#else
    if(surface.a<=0.001)discard;
#endif
#if PASS_KIND == 3
    if (surface.a < 0.10) discard;
#endif
#if PASS_KIND == 4 || PASS_KIND == 5
    surface.rgb = mix(surface.rgb, entityColor.rgb, entityColor.a);
#endif
    vec3 lm = vec3(1.0);
    float sky = 1.0;
    float category = 0.0;
    int material = 4112;
#if (PASS_KIND >= 2 && PASS_KIND <= 7)
    lm = texture(lightmap, illuminationCoordinate).rgb;
    sky = clamp((illuminationCoordinate.t * 32.0 - 1.0) / 30.0, 0.0, 1.0);
    category = 1.0;
#endif
#if PASS_KIND == 3 || PASS_KIND == 6 || BLOCK_SURFACE == 1
    // Includes unlisted, modded and translucent blocks. Water has its own medium.
    category = 1.3;
#endif
#if PASS_KIND == 3 || PASS_KIND == 6
    material = blockCategory;
    if (blockCategory == 4101 || blockCategory == 4102) category = 2.0;
#endif
#if PASS_KIND == 6
    if (isEyeInWater == 1 && (blockCategory == 4100 || blockCategory == 4103)) {
        // Independent exit depth stops fog before air beyond the interface.
        // Stratus mode stays clear; native mode also supplies its atlas layer.
        vec3 exitView = (gbufferModelView * vec4(relativeLocation, 1.0)).xyz;
        // Native mode restores the animated underside at the actual exit.
        // Ordinary alpha blending keeps nearer glass/particles in draw order;
        // the dedicated transmission buffer carries its coverage into fog.
        vec4 underside=vec4(0.0);
#if WATER_STYLE == 1
        vec3 nativeColour=surface.rgb*lm;
#if REALISTIC_LIGHTING != 0
        vec3 fn=unitVector(orientedNormal);
        nativeColour*=dot(fn*fn,vec3(0.6,fn.y>=0.0?1.0:0.5,0.8));
#endif
        underside=vec4(decodeDisplay(nativeColour),clamp(surface.a*WATER_TEXTURE,0.0,1.0));
#endif
        shim_FragData[0] = underside;
        shim_FragData[1] = vec4(0.0);
        shim_FragData[2] = vec4(0.0);
        shim_FragData[3] = vec4(0.0);
        shim_FragData[4] = vec4(0.0);
        shim_FragData[5] = vec4(-exitView.z, sky,
            clamp((illuminationCoordinate.s * 32.0 - 1.0) / 30.0, 0.0, 1.0), 1.0);
        shim_FragData[6] = vec4(0.0,0.0,0.0,underside.a);
        shim_FragData[7] = vec4(0.0);
        return;
    }
#endif
#if PASS_KIND == 2 || PASS_KIND == 7
    // Billboard normals do not describe a solid material surface.
    category = 0.8;
#endif
#if PASS_KIND == 5
    category = 3.0;
#endif
    vec3 colour = diffuseRadiance(surface.rgb, lm, sky, orientedNormal, category, relativeLocation, material);
#if PASS_KIND == 6
    if(blockCategory!=4100&&blockCategory!=4103)
        colour=wetSurfaceResponse(colour,unitVector(orientedNormal),relativeLocation,sky,wetMaterialProperties(material));
#elif BLOCK_SURFACE == 1 && LATE_SURFACE == 1
    // Translucent block entities receive film; ordinary entities stay excluded.
    colour=wetSurfaceResponse(colour,unitVector(orientedNormal),relativeLocation,sky,vec2(0.0,0.40));
#endif
    float emission=category>1.5&&category<2.5?smoothstep(0.48,0.94,max(surface.r,max(surface.g,surface.b))):0.0;
#if PASS_KIND == 10 || PASS_KIND == 12 || PASS_KIND == 1
    emission=1.0;
#endif
    colour = throughAir(colour, relativeLocation, sky);
    vec4 nativeWater=vec4(0.0);
#if PASS_KIND == 6 && WATER_STYLE == 1
    vec3 nativeColour=surface.rgb*lm;
#if REALISTIC_LIGHTING != 0
    vec3 fn=unitVector(orientedNormal);nativeColour*=dot(fn*fn,vec3(0.6,fn.y>=0.0?1.0:0.5,0.8));
#endif
    nativeWater=vec4(decodeDisplay(nativeColour),surface.a);
#endif
    float mark = 0.0;
    float depth = 0.0;
    float radialDepth = 0.0;
    float reflectable = 0.0;
#if PASS_KIND == 3 || PASS_KIND == 4 || PASS_KIND == 10 || BLOCK_SURFACE == 1
    reflectable = 1.0;
#endif
#if PASS_KIND == 6
    if (blockCategory == 4100 || blockCategory == 4103) {
        mark = 1.0;
        vec3 waterView = (gbufferModelView * vec4(relativeLocation, 1.0)).xyz;
        depth = -waterView.z;
        radialDepth = length(waterView);
        // Identical baseline on top, side and underside; no texture seam.
        colour = waterBodyColour(sky);
        // Water itself is composed once, after all water faces are captured.
        // Zero colour alpha avoids accumulating overlapping blue baselines.
        surface.a = 0.0;
    }
#endif
#if PASS_KIND == 9
    // Breaking cracks multiply the already-lit HDR scene.
    colour = surface.rgb;
#elif PASS_KIND == 12
    colour = decodeDisplay(surface.rgb);
#endif
    shim_FragData[0] = vec4(colour, surface.a);
    shim_FragData[4] = vec4(0.0);
#if PASS_KIND == 6
    if(mark>0.5){
#if WATER_STYLE == 1
        shim_FragData[4]=vec4(nativeWater.rgb,1.0);
#else
        shim_FragData[4]=vec4(tintAndOpacity.rgb,clamp((illuminationCoordinate.s*32.0-1.0)/30.0,0.0,1.0));
#endif
    }
    vec3 opticalNormal=unitVector(mat3(gbufferModelView)*orientedNormal);
    opticalNormal/=max(abs(opticalNormal.x)+abs(opticalNormal.y)+abs(opticalNormal.z),0.00001);
    vec2 encoded=opticalNormal.xy;
    if(opticalNormal.z<0.0)encoded=(1.0-abs(encoded.yx))*mix(vec2(-1),vec2(1),greaterThanEqual(encoded,vec2(0)));
    vec3 opticalView=(gbufferModelView*vec4(relativeLocation,1.0)).xyz;
    shim_FragData[7]=opticalSolid?vec4(encoded,-opticalView.z,1.0):vec4(0.0);
    // Preserve a horizontal water entry behind a falling curtain. Vertical
    // fragments have zero coverage in this attachment and cannot erase it.
    float horizontalEntry=mark*float(orientedNormal.y>0.5&&isEyeInWater==0);
    shim_FragData[5]=vec4(depth,sky,clamp((illuminationCoordinate.s*32.0-1.0)/30.0,0.0,1.0),horizontalEntry);
    shim_FragData[6]=vec4(0.0,0.0,0.0,surface.a);
#elif LATE_SURFACE == 1
    shim_FragData[5]=vec4(0.0,0.0,0.0,surface.a);
#endif
#if LATE_SURFACE == 1
    #if PASS_KIND == 6
    #if WATER_STYLE == 1
    shim_FragData[1] = vec4(dot(atlasTexel.rgb,vec3(0.2126,0.7152,0.0722)), mark>0.5?nativeWater.a:emission, float(blockCategory==4103), mark);
#else
    shim_FragData[1] = vec4(dot(atlasTexel.rgb,vec3(0.2126,0.7152,0.0722)), emission, float(blockCategory==4103), mark);
#endif
#else
    shim_FragData[1] = vec4(0.0, emission, 0.0, surface.a);
#endif
    shim_FragData[2] = vec4(unitVector(orientedNormal), mark);
    shim_FragData[3] = vec4(depth, sky, radialDepth, mark);
#else
    shim_FragData[1] = vec4(sky, emission, 0.0, reflectable);
    shim_FragData[2] = vec4(unitVector(orientedNormal),float(category>1.05&&category<1.5&&material!=4113));
    shim_FragData[3] = vec4(wetMaterialProperties(material),0.0,0.0);
#endif
#endif
}
