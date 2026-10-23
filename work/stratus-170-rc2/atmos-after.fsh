#version 330 core
#define DIMENSION_TYPE 0

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
#define TRANSPARENT_REFLECTIONS 0.00 //  [0.00 0.25 0.50 0.75 1.00 1.50 2.00]
#define TRANSPARENT_REFRACTION 0.00 //  [0.00 0.25 0.50 0.75 1.00 1.50 2.00]

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


// BEGIN INCLUDE /core/scene-depth.glsl
#ifndef STRATUS_SCENE_DEPTH_INCLUDED
#define STRATUS_SCENE_DEPTH_INCLUDED
uniform sampler2D depthtex0;
uniform sampler2D depthtex1;
uniform sampler2D colortex2;
float sceneDistance(vec2 uv){
    float z=texture(depthtex0,uv).r;
    float result=z<0.999999?length(positionFromDepth(uv,z)):7000.0;
    vec4 water=texture(colortex2,uv);
    if(water.w>0.5&&water.x>0.0){
        vec3 ray=positionFromDepth(uv,0.5);
        result=min(result,length(ray*(water.x/max(-ray.z,0.0001))));
    }
    return result;
}
float sceneSkyExposure(vec2 uv){
    vec4 data=texture(colortex2,uv);
    if(data.w>0.5)return clamp(data.y,0.0,1.0);
    return texture(depthtex1,uv).r>=0.999999?1.0:clamp(data.y,0.0,1.0);
}
#endif

// END INCLUDE /core/scene-depth.glsl


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


// BEGIN INCLUDE /core/volume.glsl
#ifndef STRATUS_VOLUME_INCLUDED
#define STRATUS_VOLUME_INCLUDED
float mistDensityWorld(vec3 point){
    vec3 drift=frameTimeCounter*vec3(0.055,0.0,-0.035);
    vec3 p=(point+drift)/max(MIST_SCALE,8.0);
    float broad=weatherVolume(p*vec3(0.16,0.12,0.16)).a;
    float centre=MIST_Y+(broad-0.5)*MIST_THICKNESS*2.4;
    float h=(point.y-centre)/max(MIST_THICKNESS*1.35,1.0);
    float valley=exp(-0.5*h*h);
    float shelf=exp(-0.5*pow((point.y-MIST_Y-MIST_THICKNESS*2.25)/max(MIST_THICKNESS*0.70,1.0),2.0));
    vec4 volume=weatherVolume(p*vec3(0.24,0.37,0.24));
    float billow=smoothstep(0.35,0.75,mix(volume.r,volume.g,0.75));
    float fine=weatherVolume(p*0.77+vec3(0.23,0.61,0.17)).b;
    float variation=clamp(billow+(fine-0.5)*0.25,0.0,1.0);
    float pocket=mix(0.85,mix(0.025,2.25,variation),clamp(MIST_BREAKUP,0.0,1.0));
    pocket=pow(max(pocket,0.005),max(MIST_BREAKUP,1.0));
    return (0.0045*valley+0.0009*shelf)*pocket*MIST_AMOUNT;
}
vec4 volumetricMist(vec3 origin,vec3 worldRay,float distanceLimit,float skyExposure,int steps){
#if DIMENSION_TYPE != 0
    return vec4(0.0);
#else
    float cameraSky=clamp(float(eyeBrightnessSmooth.y)/240.0,0.0,1.0);
    float exposure=mix(cameraSky,skyExposure,0.45);
    if(MIST_AMOUNT<=0.0||exposure<0.03)return vec4(0.0);
    vec3 ray=unitVector(worldRay);
    float begin=max(MIST_CLEAR-length(origin-cameraPosition),0.0),finish=min(distanceLimit,1100.0);
    float bottom=MIST_Y-MIST_THICKNESS*6.0,top=MIST_Y+MIST_THICKNESS*5.0;
    if(abs(ray.y)<0.0001){if(origin.y<bottom||origin.y>top)return vec4(0.0);}
    else{float a=(bottom-origin.y)/ray.y,b=(top-origin.y)/ray.y;begin=max(begin,min(a,b));finish=min(finish,max(a,b));}
    begin=max(begin,0.0);if(finish<=begin)return vec4(0.0);
    float transmission=1.0;vec3 scattering=vec3(0.0);
    float cosine=dot(ray,broadLightDirection());
    float g=0.45;
    float phase=(1.0-g*g)/pow(max(1.0+g*g-2.0*g*cosine,0.05),1.5);
    float outdoor=smoothstep(0.03,0.60,exposure);
    // These values depend only on the ray/uniforms, never the integration step.
    vec3 lightDirection=broadLightDirection();
    vec3 ambientColour=atmosphericColour()*0.91;
    vec3 sunRadiance=sunlightColour()*solarDaylight();
    for(int i=0;i<steps;i++){
        float a=float(i)/float(steps),b=float(i+1)/float(steps);
        a=a*a;b=b*b;
        float stride=(finish-begin)*(b-a);
        vec3 point=origin+ray*(begin+(a+b)*0.5*(finish-begin));
        float clearWeight=smoothstep(MIST_CLEAR,MIST_CLEAR+22.0,length(point-cameraPosition));
        // The clear foreground contributes exactly zero; avoid field reads
        // there, including reflected paths that first turn toward the camera.
        if(clearWeight<=0.0)continue;
        float density=mistDensityWorld(point)*clearWeight*outdoor;
        if(density<0.000001)continue;
        float opacity=1.0-exp(-density*stride);
        float sunTransmission=1.0;
        // At night or with scattering disabled, this entire contribution is
        // exactly zero. Retain every illumination sample whenever it is visible.
        if(any(greaterThan(sunRadiance,vec3(0.0)))&&MIST_LIGHT>0.0){
            float lightDepth=mistDensityWorld(point+lightDirection*12.0)*18.0;
            lightDepth+=mistDensityWorld(point+lightDirection*36.0)*24.0;
            sunTransmission=exp(-lightDepth);
        }
        vec3 colour=ambientColour;
        colour+=sunRadiance*sunTransmission*phase*MIST_LIGHT*0.085;
        scattering+=transmission*opacity*colour;transmission*=1.0-opacity;
        if(transmission<0.008)break;
    }
    return vec4(scattering/max(1.0-transmission,0.00001),1.0-transmission);
#endif
}
vec4 atmosphereSegment(vec3 origin,vec3 ray,float distanceLimit,float skyExposure,bool detailed){
    int cloudSteps=detailed?(ATMOSPHERE_QUALITY==2?32+CLOUD_LAYERS*40:16+CLOUD_LAYERS*16):20;
    vec4 clouds=marchCloudLayer(origin,ray,distanceLimit,cloudSteps,detailed);
    vec4 mist=volumetricMist(origin,ray,distanceLimit,skyExposure,detailed?(ATMOSPHERE_QUALITY==2?12+MIST_DETAIL*16:12+MIST_DETAIL*8):8);
    return ray.y<0.0?overLayers(clouds,mist):overLayers(mist,clouds);
}
// Shared by the reduced-resolution pass and its confidence fallback. Avoids
// inconsistent border fog/blindness between tiny cutouts and larger surfaces.
vec4 completeAtmosphereSegment(vec3 origin,vec3 ray,float limit,float sky,bool detailed){
    vec4 volume=atmosphereSegment(origin,ray,limit,sky,detailed);
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
    return volume;
}
#endif

// END INCLUDE /core/volume.glsl

uniform sampler2D colortex3;
uniform sampler2D colortex11;

// BEGIN INCLUDE /core/transparent-optics.glsl
#ifndef STRATUS_TRANSPARENT_OPTICS_INCLUDED
#define STRATUS_TRANSPARENT_OPTICS_INCLUDED
uniform sampler2D colortex15;

// BEGIN INCLUDE /core/environment.glsl
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

// END INCLUDE /core/environment.glsl


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

uniform sampler2D colortex4;

// BEGIN INCLUDE /core/scene-trace.glsl
#ifndef STRATUS_SCENE_TRACE_INCLUDED
#define STRATUS_SCENE_TRACE_INCLUDED
// Original surface reconstruction: contiguous projected pixels, actual receiver
// planes, and explicit water/air half-space checks shared by both optical rays.
uniform sampler2D colortex10;
ivec2 opticsSize(bool unused){return textureSize(depthtex1,0);}
vec3 opticsRadiance(ivec2 cell,bool unused){return texelFetch(colortex4,cell,0).rgb;}

bool opticsProjection(vec3 p,out vec2 uv,bool cache){
    vec4 q=gbufferProjection*vec4(p,1.0);uv=q.xy/max(q.w,0.00001)*0.5+0.5;
    return q.w>0.0&&min(uv.x,uv.y)>0.001&&max(uv.x,uv.y)<0.999;
}
vec3 opticsReceiver(ivec2 cell,out vec4 normal,bool cache){
    ivec2 size=opticsSize(cache);cell=clamp(cell,ivec2(0),size-ivec2(1));
    vec2 uv=(vec2(cell)+0.5)/vec2(size);
    normal=texelFetch(colortex10,cell,0);
    float d=texelFetch(depthtex1,cell,0).r;
    if(d>=0.999999)normal.a=0.0;
    return positionFromDepth(uv,d);
}
vec3 opticsColour(vec2 uv,vec3 planePoint,vec3 planeNormal,bool cache){
    ivec2 size=opticsSize(cache);
    vec2 grid=uv*vec2(size)-0.5;ivec2 cell=ivec2(floor(grid));vec2 f=fract(grid);
    vec3 sum=vec3(0.0);float total=0.0;
    for(int y=0;y<2;y++)for(int x=0;x<2;x++){
        ivec2 c=clamp(cell+ivec2(x,y),ivec2(0),size-ivec2(1));
        vec4 data;vec3 receiver=opticsReceiver(c,data,cache);
        vec3 n=unitVector(mat3(gbufferModelView)*data.xyz);
        float weight=(x==0?1.0-f.x:f.x)*(y==0?1.0-f.y:f.y);
        if(data.a<0.5||dot(n,planeNormal)<0.95||abs(dot(receiver-planePoint,planeNormal))>0.02+length(receiver)*0.0004)continue;
        sum+=opticsRadiance(c,cache)*weight;total+=weight;
    }
    ivec2 centre=clamp(ivec2(uv*vec2(size)),ivec2(0),size-ivec2(1));
    return total>0.001?sum/total:opticsRadiance(centre,cache);
}
float opticsBorderCoverage(vec2 uv,ivec2 size){
    vec2 border=min(uv,1.0-uv)*vec2(size);
    return smoothstep(1.0,8.0,min(border.x,border.y));
}
float opticsHitPixelTolerance(vec2 projectedPixels,int count,float requestedStride){
    // A capped ray spans more than requestedStride pixels per iteration. Its
    // validated plane hit may lie anywhere inside that larger segment.
    return max(requestedStride,max(projectedPixels.x,projectedPixels.y)/float(count))+1.0;
}
// Bound expensive pixel traversal by a receiver plane that has already been
// validated at the projected intersection. This preserves the depth search in
// front of it, but avoids marching empty space all the way to the far plane.
float opticsPlaneBound(vec3 origin,vec3 direction,vec3 interfaceNormal,int side,bool cache,float minimum,float maximum,out vec2 boundUV,out vec3 boundPoint,out vec3 boundNormal){
    float sampleT=minimum+0.025;boundUV=vec2(0);boundPoint=vec3(0);boundNormal=vec3(0);
    for(int iteration=0;iteration<4;iteration++){
        vec2 uv;if(!opticsProjection(origin+direction*sampleT,uv,cache))break;
        ivec2 size=opticsSize(cache),cell=clamp(ivec2(uv*vec2(size)),ivec2(0),size-ivec2(1));
        vec4 data;vec3 receiver=opticsReceiver(cell,data,cache);if(data.a<0.5)break;
        vec3 n=unitVector(mat3(gbufferModelView)*data.xyz);float denominator=dot(direction,n);
        if(abs(denominator)<0.00001)break;
        float distance=dot(receiver-origin,n)/denominator;
        if(distance<=minimum||distance>maximum)break;
        vec3 candidate=origin+direction*distance;vec2 hitUV;if(!opticsProjection(candidate,hitUV,cache))break;
        vec4 hitData;vec3 actual=opticsReceiver(clamp(ivec2(hitUV*vec2(size)),ivec2(0),size-ivec2(1)),hitData,cache);
        vec3 hitNormal=unitVector(mat3(gbufferModelView)*hitData.xyz);
        bool samePlane=hitData.a>0.5&&dot(hitNormal,n)>0.95&&abs(dot(actual-candidate,n))<0.018+length(actual)*0.0004;
        if(samePlane&&float(side)*dot(actual-origin,interfaceNormal)>0.005){boundUV=hitUV;boundPoint=candidate;boundNormal=n;return distance;}
        sampleT=distance;
    }
    return maximum;
}
vec4 traceOpticalSegment(vec3 origin,vec3 direction,vec3 interfaceNormal,int side,int quality,float maximum,bool cache,float minimum,out float path){
    path=0.0;
    if(!cache&&direction.z>0.00001)maximum=min(maximum,max(0.0,(-0.10-origin.z)/direction.z));
    if(maximum<0.03)return vec4(0.0);
    vec2 boundUV;vec3 boundPoint,boundNormal;
    float previousMaximum=maximum;
    maximum=opticsPlaneBound(origin,direction,interfaceNormal,side,cache,max(minimum,0.025),maximum,boundUV,boundPoint,boundNormal);
    bool bounded=maximum<previousMaximum;
    vec3 start=origin+direction*max(minimum,0.025),end=origin+direction*maximum;
    vec4 a=gbufferProjection*vec4(start,1.0),b=gbufferProjection*vec4(end,1.0);
    float ka=1.0/max(a.w,0.00001),kb=1.0/max(b.w,0.00001);
    float projectionScale=1.0;
    vec2 pa=a.xy*ka/projectionScale*0.5+0.5,pb=b.xy*kb/projectionScale*0.5+0.5;
    vec3 qa=start*ka,qb=end*kb;vec2 delta=pb-pa;
    float visible=1.0;
    for(int axis=0;axis<2;axis++){
        if(delta[axis]>0.00001)visible=min(visible,(0.999-pa[axis])/delta[axis]);
        else if(delta[axis]<-0.00001)visible=min(visible,(0.001-pa[axis])/delta[axis]);
    }
    visible=clamp(visible,0.0,1.0);pb=mix(pa,pb,visible);qb=mix(qa,qb,visible);kb=mix(ka,kb,visible);
    ivec2 size=opticsSize(cache);vec2 pixels=abs((pb-pa)*vec2(size));
    float stride=quality==2?1.0:(quality==1?2.0:4.0);
    // Short rays traverse contiguous pixels; all profiles bound long rays.
    float budget=quality==2?192.0:(quality==1?48.0:24.0);
    int count=int(clamp(ceil(max(pixels.x,pixels.y)/stride),1.0,budget));
    float hitPixelTolerance=opticsHitPixelTolerance(pixels,count,stride);
    // Projected points remain on this unit ray. Hoist the invariant dot
    // products and reuse each interval end as the next interval start.
    float qaAlong=dot(qa,direction),qbAlong=dot(qb,direction);
    float originAlong=dot(origin,direction);
    float previousT=qaAlong/ka-originAlong;
    for(int i=0;i<192;i++){
        if(i>=count)break;
        float f0=float(i)/float(count),f1=float(i+1)/float(count),f=(f0+f1)*0.5;
        vec2 uv=mix(pa,pb,f);
        if(min(uv.x,uv.y)<0.001||max(uv.x,uv.y)>0.999)break;
        float t0=previousT;
        float t1=mix(qaAlong,qbAlong,f1)/mix(ka,kb,f1)-originAlong;
        previousT=t1;
        float pointZ=mix(qa.z,qb.z,f)/mix(ka,kb,f);
        ivec2 cell=clamp(ivec2(uv*vec2(size)),ivec2(0),size-ivec2(1));
        vec4 data;vec3 receiver=opticsReceiver(cell,data,cache);
        if(data.a<0.5)continue;
        vec3 n=unitVector(mat3(gbufferModelView)*data.xyz);
        float denominator=dot(direction,n);
        float distance=abs(denominator)>0.00001?dot(receiver-origin,n)/denominator:-1.0;
        float footprint=max(0.012,length(receiver)/(float(size.y)*max(gbufferProjection[1][1],0.1)));
        if(distance>=max(0.025,t0-footprint)&&distance<=min(maximum,t1+footprint)){
            vec3 candidate=origin+direction*distance;vec2 hitUV;
            if(opticsProjection(candidate,hitUV,cache)){
                ivec2 hitCell=clamp(ivec2(hitUV*vec2(size)),ivec2(0),size-ivec2(1));
                vec4 hitData;vec3 actual=opticsReceiver(hitCell,hitData,cache);
                vec3 hitNormal=unitVector(mat3(gbufferModelView)*hitData.xyz);
                bool samePlane=hitData.a>0.5&&dot(hitNormal,n)>0.95&&abs(dot(actual-candidate,n))<0.018+length(actual)*0.0004;
                bool correctMedium=float(side)*dot(actual-origin,interfaceNormal)>0.005;
                if(samePlane&&correctMedium&&max(abs(hitUV.x-uv.x)*float(size.x),abs(hitUV.y-uv.y)*float(size.y))<hitPixelTolerance){
                    float coverage=opticsBorderCoverage(hitUV,size);
                    path=distance;
                    return vec4(opticsColour(hitUV,candidate,n,cache),coverage);
                }
            }
        }
        // A foreground occluder ends the search. Never continue through a
        // rejected shore edge and steal a farther river-floor pixel.
        float occlusion=receiver.z-pointZ;
        if(!cache&&occlusion>max(0.08,footprint*3.0))return vec4(0.0);
    }
    if(bounded){path=maximum;return vec4(opticsColour(boundUV,boundPoint,boundNormal,cache),opticsBorderCoverage(boundUV,size));}
    return vec4(0.0);
}
vec4 traceOpticalScene(vec3 origin,vec3 direction,vec3 interfaceNormal,int side,int quality,float maximum,bool unused,out float path){
    return traceOpticalSegment(origin,direction,interfaceNormal,side,quality,maximum,false,0.025,path);
}
#endif

// END INCLUDE /core/scene-trace.glsl

// One nearest visible thin-solid interface. No volume traversal or water waves.
vec3 transparentSolidOptics(vec3 scene,vec2 uv){
    if(TRANSPARENT_REFLECTIONS<=0.0&&TRANSPARENT_REFRACTION<=0.0)return scene;
    vec4 data=texture(colortex15,uv);
    if(data.a<0.5||data.z<=0.0)return scene;
    vec3 ray=positionFromDepth(uv,0.5),point=ray*(data.z/max(-ray.z,0.00001));
    float front=texture(depthtex0,uv).r;
    if(front<0.999999&&-positionFromDepth(uv,front).z<data.z-max(0.04,data.z*0.002))return scene;
    vec3 n=vec3(data.xy,1.0-abs(data.x)-abs(data.y));
    if(n.z<0.0)n.xy=(1.0-abs(n.yx))*mix(vec2(-1),vec2(1),greaterThanEqual(n.xy,vec2(0)));
    n=unitVector(n);vec3 incident=unitVector(point);if(dot(n,-incident)<0.0)n=-n;
    if(TRANSPARENT_REFRACTION>0.0){
        // Fixed thin-slab offset: opposite parallel faces cancel angular bending.
        // Cap displacement, reject foreground and cross-interface samples.
        vec3 through=refract(incident,n,1.0/1.5);
        vec2 shift=(through.xy/max(abs(through.z),0.2)-incident.xy/max(abs(incident.z),0.2))*0.006*TRANSPARENT_REFRACTION/max(data.z*0.04,1.0);
        shift=clamp(shift,vec2(-0.015),vec2(0.015));vec2 refracted=uv+shift;
        if(min(refracted.x,refracted.y)>0.005&&max(refracted.x,refracted.y)<0.995){
            vec4 other=texture(colortex15,refracted);float back=texture(depthtex1,refracted).r;
            bool same=other.a>0.5&&abs(other.z-data.z)<max(0.08,data.z*0.015);
            bool behind=back>=0.999999||-positionFromDepth(refracted,back).z>data.z+0.02;
            if(same&&behind)scene=texture(colortex3,refracted).rgb;
        }
    }
    if(TRANSPARENT_REFLECTIONS>0.0){
        vec3 direction=reflect(incident,n),world=mat3(gbufferModelViewInverse)*direction;
        vec4 hit=vec4(0.0);
#if REFLECTION_MODE != 0
        float path;hit=traceOpticalScene(point+n*0.015,direction,n,1,REFLECTION_MODE,min(REFLECT_RANGE,max(16.0,far)),false,path);
#endif
        float sky=clamp(float(eyeBrightnessSmooth.y)/240.0,0.0,1.0);
        vec3 fallback=reflectedEnvironment(world)*mix(0.03,1.0,smoothstep(0.04,0.8,sky));
        vec3 reflected=mix(fallback,hit.rgb,hit.a);
        float f=dielectricWaterFresnel(clamp(dot(n,-incident),0.0,1.0),1.0,1.5);
        scene=mix(scene,reflected,clamp(f*TRANSPARENT_REFLECTIONS,0.0,0.85));
    }
    return scene;
}
#endif

// END INCLUDE /core/transparent-optics.glsl

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
