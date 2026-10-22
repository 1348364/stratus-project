#version 330 core
#define DIMENSION_TYPE 0
#ifndef STRATUS_OPTIONS_INCLUDED
#define STRATUS_OPTIONS_INCLUDED
// Reference-quality water/cloud defaults. Lower-cost sampling profiles remain available.
#define SKY_AMBIENT 1.40 // [0.20 0.40 0.60 0.80 1.00 1.20 1.40 1.60 1.80 2.00 2.50 3.00 4.00]
const float ambientOcclusionLevel = 1.00; // [0.00 0.15 0.30 0.45 0.60 0.80 1.00]
#define WHITE_BALANCE 0.00 // [-0.24 -0.16 -0.08 -0.04 0.00 0.04 0.08 0.16 0.24]
#define SURFACE_SATURATION 1.00 // [0.00 0.25 0.50 0.75 0.85 0.93 1.00 1.07 1.15 1.30 1.50 1.75 2.00]
#define SURFACE_DAMPNESS 1.00 // [0.00 0.15 0.35 0.65 1.00 1.35 1.70 2.00 2.50 3.00]
#define CLOUD_AMOUNT 0.90 // [0.00 0.35 0.60 0.75 0.90 1.00]
#define CLOUD_ALTITUDE 256.0 // [64.0 96.0 128.0 160.0 192.0 224.0 256.0 320.0 384.0 512.0 640.0 768.0]
#define CLOUD_THICKNESS 96.0 // [12.0 20.0 32.0 40.0 56.0 72.0 96.0 128.0 160.0 200.0]
#define SKY_LEAK 0.35 // [0.00 0.10 0.15 0.25 0.35 0.50 0.70 1.00 1.40 2.00]
#define CLOUD_SPAN 240.0 // [64.0 96.0 160.0 240.0 360.0 540.0 700.0 900.0 1200.0 1800.0]
#define CLOUD_DISTORTION 0.85 // [0.00 0.25 0.45 0.65 0.85 1.00 1.25 1.50 2.00]
#define CLOUD_RELIEF 0.75 // [0.00 0.25 0.40 0.55 0.75 1.00 1.25 1.50]
#define CLOUD_DRIFT 0.25 // [0.00 0.10 0.25 0.45 0.70 1.00 1.50 2.00 3.00]
#define CLOUD_LAYERS 3 // [1 2 3]
#define MIST_AMOUNT 0.85 // [0.00 0.15 0.30 0.40 0.60 0.75 0.85 1.00 1.25 1.50 2.00 3.00]
#define MIST_Y 70.0 // [-32.0 0.0 32.0 48.0 64.0 70.0 88.0 112.0 144.0 192.0 256.0 320.0]
#define MIST_THICKNESS 18.0 // [4.0 7.0 9.0 12.0 18.0 24.0 32.0 48.0 64.0]
#define MIST_CLEAR 24.0 // [0.0 4.0 8.0 16.0 24.0 32.0 48.0 64.0 80.0 112.0 144.0]
#define MIST_DETAIL 3 // [1 2 3]
#define REFLECT_LEVEL 1.00 // [0.00 0.40 0.60 0.85 1.00]
#define REFLECTION_MODE 2 // [0 1 2]
#define REFLECT_RANGE 120.0 // [24.0 48.0 64.0 88.0 120.0 160.0 224.0 320.0]
#define WATER_VISIBILITY 1.70 // [0.05 0.10 0.20 0.35 0.50 0.70 0.90 1.10 1.30 1.70 2.20 3.00 4.00 6.00 8.00 12.00 16.00]
#define WATER_EXTINCTION 0.90 // [0.10 0.20 0.45 0.65 0.90 1.15 1.40 2.00 3.00]
#define RIPPLE_HEIGHT 0.80 // [0.00 0.15 0.30 0.55 0.80 1.00 1.30 1.70 2.20 3.00]
#define RIPPLE_SIZE 1.00 // [0.25 0.40 0.65 0.80 1.00 1.25 1.50 2.00 3.00 4.00]
#define RIPPLE_RATE 0.45 // [0.00 0.10 0.20 0.45 0.70 1.00 1.50 2.00 3.00]
#define FACE_SHADING 1.00 // [0.00 0.15 0.25 0.35 0.50 0.70 0.85 1.00 1.25 1.50 2.00]
#define WET_DARKENING 1.00 // [0.00 0.25 0.50 0.75 1.00 1.30 1.70 2.00 2.50]
#define WET_SHEEN 0.85 // [0.00 0.15 0.35 0.65 0.85 1.00 1.35 1.70 2.00]
#define BLOOM_STRENGTH 0.18 // [0.00 0.03 0.06 0.12 0.18 0.25 0.35 0.50 0.75 1.00]
#define BLOOM_RADIUS 3.00 // [0.25 0.50 1.00 1.50 2.00 3.00 4.00 6.00 8.00 12.00]
#define SUN_VISIBILITY 0.85 // [0.00 0.25 0.45 0.65 0.85 1.00 1.50 2.00 3.00]
#define LAMP_LEVEL 1.00 // [0.20 0.40 0.70 0.85 1.00 1.15 1.30 1.60 2.00 3.00]
#define LAMP_HEAT 0.25 // [0.00 0.15 0.25 0.40 0.60 0.80 1.00 1.50]
#define FACE_BLEND 1.00 // [0.00 0.25 0.50 0.75 1.00]
#define GROUND_WARMTH 0.45 // [0.00 0.20 0.45 0.65 0.85 1.00 1.35 1.70 2.00]
#define WATER_DISTORTION 1.00 // [0.00 0.20 0.35 0.55 0.75 1.00 1.20 1.35 1.60 2.00]
#define CIRRUS_AMOUNT 0.65 // [0.00 0.35 0.65 0.85 1.00]
#define CIRRUS_ALTITUDE 360.0 // [200.0 240.0 280.0 320.0 360.0 400.0 460.0 560.0 700.0 900.0 1200.0]
#define CLOUD_STYLE 0 // [0 1 2]
#define SUN_STYLE 0 // [0 1]
#define WATER_TURBIDITY 1.00 // [0.00 0.25 0.50 1.00 1.50 2.00 3.00 4.00 6.00]
#define BIOME_WATER 1 // [0 1]
#define REFRACTION_QUALITY 2 // [0 1 2]
#define CLOUD_DENSITY 1.00 // [0.15 0.30 0.50 0.75 1.00 1.30 1.70 2.20 3.00]
#define CLOUD_DETAIL 1.00 // [0.00 0.25 0.50 0.75 1.00 1.30 1.70 2.00]
#define MIST_SCALE 96.0 // [24.0 40.0 64.0 96.0 144.0 224.0 320.0 480.0]
#define MIST_BREAKUP 0.85 // [0.00 0.25 0.50 0.85 1.00 1.30 1.70 2.00]
#define MIST_LIGHT 0.65 // [0.00 0.20 0.40 0.65 0.85 1.00 1.50 2.00]
#endif

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
    float core=exp(-separation/0.00032)*3.4;
#if SUN_STYLE == 1
    core=0.0;
#endif
    float aureole=exp(-separation/0.008)*0.70;
#if SUN_STYLE == 1
    aureole=0.0;
#endif
    sky+=sunlightColour()*solarDaylight()*(glow+(core+aureole)*SUN_VISIBILITY*(1.0-0.65*rainStrength));
    return sky;
#endif
}
vec2 layeredCloudSample(vec3 worldPoint,bool detailed,bool upper){
    float altitude=upper?CIRRUS_ALTITUDE:CLOUD_ALTITUDE;
    float thickness=upper?32.0:CLOUD_THICKNESS;
    float amount=upper?CIRRUS_AMOUNT:CLOUD_AMOUNT;
    if(amount<=0.0)return vec2(0.0);
    vec2 wind=frameTimeCounter*CLOUD_DRIFT*vec2(0.31,-0.14)*(upper?1.55:1.0);
    vec2 weatherPoint=(worldPoint.xz+wind)/max(CLOUD_SPAN,16.0);
    float weather=weatherVolume(vec3(weatherPoint.x*0.073,0.37,weatherPoint.y*0.073)).a;
    float centre=altitude+(weather-0.5)*thickness*CLOUD_DISTORTION*1.35;
    float height=(worldPoint.y-centre)/max(thickness,1.0)+0.5;
    float envelope=smoothstep(-0.08,0.24,height)*(1.0-smoothstep(0.62,1.12,height));
    if(envelope<=0.0)return vec2(0.0);
    vec3 p=vec3(weatherPoint.x*0.65,(worldPoint.y-altitude)/max(thickness,1.0)*0.55,weatherPoint.y*0.65);
    p.xz=mat2(0.8,-0.6,0.6,0.8)*p.xz;
    p.x+=(weather-0.5)*CLOUD_DISTORTION*0.12;
    if(upper){p.x*=0.24;p.z*=1.65;p.x+=sin(p.z*14.0+weather*3.0)*0.035;}
    vec4 volume=weatherVolume(p);
    float body=upper?volume.b:mix(volume.r,volume.g,0.65);
    float threshold=mix(0.78,upper?0.25:0.23,clamp(amount,0.0,1.0));
    float profile=pow(abs(height-0.5)*1.60,2.0)*0.80;
    float potential=body+(weather-0.5)*0.18-profile;
    float bulk=smoothstep(threshold-0.05,threshold+0.12,potential);
    if(detailed){
        float fine=weatherVolume(p*2.17+vec3(0.29,0.63,0.12)).b;
        float erosion=(1.0-fine)*CLOUD_DETAIL*0.20*(1.0-bulk*0.75);
#if CLOUD_LAYERS > 2
        erosion+=weatherVolume(p*4.13-vec3(0.17,0.42,0.28)).g*CLOUD_DETAIL*0.045*(1.0-bulk*0.8);
#endif
        bulk=clamp((bulk-erosion)/max(1.0-erosion,0.1),0.0,1.0);
    }
    // No minimum-density floor: filled overcast comes from overlapping rounded
    // volumes, not a flat compulsory sheet. Fine detail erodes their edges.
    return vec2(envelope*bulk*amount*CLOUD_DENSITY*(upper?0.024:0.050),height);
}
vec2 cloudVolumeSample(vec3 p,bool detailed){return layeredCloudSample(p,detailed,false);}
vec2 cloudSample(vec3 p){return layeredCloudSample(p,true,false);}
float cloudSunTransmission(vec3 point){
    vec3 l=broadLightDirection();float tau=0.0;
    const int samples=2+CLOUD_LAYERS;
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
    float thickness=upper?32.0:CLOUD_THICKNESS;
    float bottom=altitude-thickness*1.55,top=altitude+thickness*1.55;
    vec3 ray=unitVector(worldRay);float begin=0.0,finish=min(distanceLimit,7000.0);
    if(abs(ray.y)<0.0001){if(origin.y<bottom||origin.y>top)return vec4(0.0);}
    else{float a=(bottom-origin.y)/ray.y,b=(top-origin.y)/ray.y;begin=max(min(a,b),0.0);finish=min(finish,max(a,b));}
    if(finish<=begin)return vec4(0.0);
    // One continuous horizon limit avoids a horizontal seam while flying inside.
    finish=min(finish,begin+2400.0);
    float closeSampling=1.0-smoothstep(0.0,thickness,begin);
    float transmission=1.0;vec3 scattered=vec3(0.0);
    float separation=max(1.0-dot(ray,broadLightDirection()),0.0);
    float phase=cloudPhase(dot(ray,broadLightDirection()));
    float solarPatch=exp(-separation/0.0014)*SUN_VISIBILITY;
    for(int i=0;i<steps;i++){
        float u0=float(i)/float(steps),u1=float(i+1)/float(steps);
        u0=mix(u0,u0*u0,closeSampling);u1=mix(u1,u1*u1,closeSampling);
        float stride=(finish-begin)*(u1-u0);
        vec3 point=origin+ray*(begin+(u0+u1)*0.5*(finish-begin));
        vec2 sampleData=layeredCloudSample(point,shadows||upper,upper);if(sampleData.x<=0.00001)continue;
        float opacity=1.0-exp(-sampleData.x*stride);
        float h=clamp(sampleData.y,0.0,1.0);
        float sunlight=shadows&&!upper?cloudSunTransmission(point):mix(0.35,1.0,h);
        float ambientSky=exp(-layeredCloudSample(point+vec3(0.0,CLOUD_THICKNESS*0.28,0.0),false,upper).x*CLOUD_THICKNESS*0.9);
        float ambient=mix(0.42,1.0,h)*mix(0.60,1.25,ambientSky);
        float powder=1.0-exp(-sampleData.x*35.0);
        vec3 daylight=vec3(0.35,0.39,0.46)*ambient;
        daylight+=sunlightColour()*sunlight*(0.27+phase*0.065*SUN_VISIBILITY);
        daylight+=vec3(0.13,0.145,0.165)*powder*(0.4+0.6*h);
        daylight*=mix(1.0,0.70+0.30*sunlight,CLOUD_RELIEF);
        // Forward scattering exposes a soft warm solar location from below too.
        daylight+=sunlightColour()*(phase*SKY_LEAK*0.08*sunlight+solarPatch*(0.45+1.25*sunlight));
        vec3 colour=mix(vec3(0.006,0.010,0.019)*ambient,daylight,daytimeWeight());
        colour*=1.0-0.17*rainStrength;
        scattered+=transmission*opacity*colour;transmission*=1.0-opacity;
        if(transmission<0.015)break;
    }
    vec3 colour=scattered/max(1.0-transmission,0.0001);
    colour=mix(colour,atmosphericColour(),1.0-exp(-max(begin-150.0,0.0)*0.00025));
    return vec4(colour,1.0-transmission);
#endif
}
vec4 marchCloudLayer(vec3 origin,vec3 ray,float limit,int steps,bool shadows){
    vec4 low=marchSingleCloud(origin,ray,limit,steps,shadows,false);
    vec4 high=marchSingleCloud(origin,ray,limit,max(4,steps/2),false,true);
    return ray.y<0.0?overLayers(high,low):overLayers(low,high);
}
vec4 physicalCloudLayer(vec3 origin,vec3 ray,float limit){return marchCloudLayer(origin,ray,limit,20+CLOUD_LAYERS*16,true);}
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
    for(int i=0;i<steps;i++){
        float a=float(i)/float(steps),b=float(i+1)/float(steps);
        a=a*a;b=b*b;
        float stride=(finish-begin)*(b-a);
        vec3 point=origin+ray*(begin+(a+b)*0.5*(finish-begin));
        float clearWeight=smoothstep(MIST_CLEAR,MIST_CLEAR+22.0,length(point-cameraPosition));
        float density=mistDensityWorld(point)*clearWeight*outdoor;
        if(density<0.000001)continue;
        float opacity=1.0-exp(-density*stride);
        vec3 lightDirection=broadLightDirection();
        float lightDepth=mistDensityWorld(point+lightDirection*12.0)*18.0;
        lightDepth+=mistDensityWorld(point+lightDirection*36.0)*24.0;
        float sunTransmission=exp(-lightDepth);
        vec3 colour=atmosphericColour()*0.91;
        colour+=sunlightColour()*solarDaylight()*sunTransmission*phase*MIST_LIGHT*0.085;
        scattering+=transmission*opacity*colour;transmission*=1.0-opacity;
        if(transmission<0.008)break;
    }
    return vec4(scattering/max(1.0-transmission,0.00001),1.0-transmission);
#endif
}
vec4 atmosphereSegment(vec3 origin,vec3 ray,float distanceLimit,float skyExposure,bool detailed){
    int cloudSteps=detailed?20+CLOUD_LAYERS*16:12;
    vec4 clouds=marchCloudLayer(origin,ray,distanceLimit,cloudSteps,detailed);
    vec4 mist=volumetricMist(origin,ray,distanceLimit,skyExposure,detailed?12+MIST_DETAIL*16:8);
    return ray.y<0.0?overLayers(clouds,mist):overLayers(mist,clouds);
}
#endif

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
    if (material == 4114) return vec2(0.00, 0.38);
    if (material == 4115) return vec2(0.80, 0.98);
    if (material == 4116) return vec2(0.16, 0.48);
    if (material == 4117) return vec2(0.72, 0.91);
    return vec2(0.45, 0.86);
}
float exposedWetFilm(float sky){
#if DIMENSION_TYPE == 0
    float outdoors=smoothstep(0.12,0.83,sky);
    float humidity=clamp(biomeHumidity,0.0,1.0);
    return clamp(SURFACE_DAMPNESS*outdoors*(0.40+0.30*humidity+0.25*rainStrength),0.0,1.0);
#else
    return 0.0;
#endif
}
float materialWetDarkening(float sky,float absorption){
    float saturation=exposedWetFilm(sky)*(0.45+0.55*clamp(biomeHumidity,0.0,1.0));
    return 1.0/(1.0+1.40*WET_DARKENING*saturation*clamp(absorption,0.0,1.0));
}
vec3 formIrradiance(vec3 normal, float skyExposure) {
    // Broad sky/ground hemispheres plus a cosine-weighted soft sun contribution.
    // Continuous diffuse lighting is blended with vanilla's axis face weights.
    float upperHemisphere = 0.5 + 0.5 * normal.y;
    vec3 sky = mix(vec3(0.31, 0.295, 0.275), vec3(1.025, 1.0, 0.95), upperHemisphere);
    vec3 skyKey=unitVector(broadLightDirection()+vec3(-0.20,0.0,0.13));
    float directional = max(dot(normal, skyKey), 0.0);
    sky += sunlightColour() * 0.23 * directional * daytimeWeight() * (1.0 - 0.65 * rainStrength);
    sky /= 1.12;
    // The lightmap has no point-light positions: retain broad indoor fill.
    float indoor = 0.72 + 0.20 * max(normal.y, 0.0) - 0.12 * max(-normal.y, 0.0);
    vec3 irradiance = mix(vec3(indoor), sky, smoothstep(0.04, 0.85, skyExposure));
    float vertical=normal.y>=0.0?1.0:0.5;
    float vanilla=dot(normal*normal,vec3(0.6,vertical,0.8));
    irradiance*=mix(1.0,vanilla,FACE_BLEND);
    return pow(max(irradiance,vec3(0.02)),vec3(FACE_SHADING));
}
float waterFresnel(float cosine) {
    return 0.0204 + 0.9796 * pow(1.0 - clamp(cosine, 0.0, 1.0), 5.0);
}
float wetSunSpecular(vec3 n, vec3 v, vec3 l, float roughness) {
    float nv = max(dot(n, v), 0.001), nl = max(dot(n, l), 0.0);
    if (nl <= 0.0) return 0.0;
    vec3 h = unitVector(v + l);
    float nh = max(dot(n, h), 0.0), vh = max(dot(v, h), 0.0);
    float alpha = max(roughness * roughness, 0.08), a2 = alpha * alpha;
    float denominator = nh * nh * (a2 - 1.0) + 1.0;
    float distribution = a2 / max(3.14159265 * denominator * denominator, 0.00001);
    float visibility = 0.5 / max(nl * sqrt(nv * nv * (1.0 - a2) + a2)
                        + nv * sqrt(nl * nl * (1.0 - a2) + a2), 0.0001);
    return distribution * visibility * waterFresnel(vh) * nl;
}
vec3 wetSurfaceResponse(vec3 dry,vec3 n,vec3 playerPoint,float sky,vec2 material){
    // Absorbed water darkens porous substrates. A separate surface film covers
    // exposed faces of every material, including nonabsorbing metal/ceramic.
    float film=exposedWetFilm(sky);
    vec3 wet=dry*materialWetDarkening(sky,material.x);
    vec3 v=unitVector(-playerPoint);
    float roughness=mix(material.y,max(0.13,material.y*0.38),film);
    float sheen=film*WET_SHEEN;
    float coat=clamp(sheen*waterFresnel(max(dot(n,v),0.0))*(1.0-roughness*0.35),0.0,0.65);
    wet=mix(wet,softSkyReflection(reflect(-v,n))*sky*SKY_AMBIENT,coat);
    wet+=sunlightColour()*wetSunSpecular(n,v,broadLightDirection(),roughness)*sheen*sky*daytimeWeight()*0.65;
    return wet;
}
vec3 diffuseRadiance(vec3 colour, vec3 mappedLight, float skyExposure, vec3 worldNormal,
                     float kind, vec3 playerPoint, int material) {
    if (kind < 0.5) return decodeDisplay(colour);
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
#if DIMENSION_TYPE == 0
    if(kind>1.05&&kind<2.5){
        float warmth=GROUND_WARMTH*skyExposure*daytimeWeight()*mix(0.60,1.0,max(normal.y,0.0));
        reflected*=mix(vec3(1.0),vec3(1.17,1.035,0.82),warmth);
    }
#endif
    if (kind > 1.5 && kind < 2.5) {
        float interior = smoothstep(0.48, 0.94, max(colour.r, max(colour.g, colour.b)));
        reflected = max(reflected, decodeDisplay(colour) * interior * LAMP_LEVEL * 2.1);
    }
    return reflected;
}
#endif

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

uniform sampler2D depthtex1;uniform sampler2D colortex4;
#ifndef STRATUS_REFRACTION_INCLUDED
#define STRATUS_REFRACTION_INCLUDED
// Perspective-correct screen-space tracing against actual receiver normals.
// Geometry is sampled along Snell's ray, never warped from the starting pixel's
// tangent plane or squeezed into an arbitrary UV-displacement budget.
uniform sampler2D colortex10;
bool refractionProjection(vec3 point,out vec2 uv){
    vec4 clip=gbufferProjection*vec4(point,1.0);
    uv=clip.xy/max(clip.w,0.00001)*0.5+0.5;
    return clip.w>0.0&&min(uv.x,uv.y)>0.001&&max(uv.x,uv.y)<0.999;
}
float refractionDepthError(vec3 point,vec2 uv){
    float d=texture(depthtex1,uv).r;
    return d>=0.999999?-100000.0:positionFromDepth(uv,d).z-point.z;
}
vec4 traceWaterTransmission(vec3 origin,vec3 direction,vec3 interfaceNormal,out float opticalPath){
    opticalPath=0.0;
    float maximum=min(160.0,max(far,24.0));
    if(direction.z>0.00001)maximum=min(maximum,max(0.0,(-0.12-origin.z)/direction.z));
    if(maximum<0.03)return vec4(0.0);
    vec3 beginPoint=origin+direction*0.025,endPoint=origin+direction*maximum;
    vec4 a=gbufferProjection*vec4(beginPoint,1.0),b=gbufferProjection*vec4(endPoint,1.0);
    float ka=1.0/max(a.w,0.00001),kb=1.0/max(b.w,0.00001);
    vec2 pa=a.xy*ka*0.5+0.5,pb=b.xy*kb*0.5+0.5;
    vec3 qa=beginPoint*ka,qb=endPoint*kb;
    vec2 delta=pb-pa;
    float visible=1.0;
    for(int axis=0;axis<2;axis++){
        if(delta[axis]>0.00001)visible=min(visible,(0.998-pa[axis])/delta[axis]);
        else if(delta[axis]<-0.00001)visible=min(visible,(0.002-pa[axis])/delta[axis]);
    }
    visible=clamp(visible,0.0,1.0);pb=mix(pa,pb,visible);qb=mix(qa,qb,visible);kb=mix(ka,kb,visible);
#if REFRACTION_QUALITY == 2
    const int maximumSamples=256;
    const float pixelStride=2.0;
#elif REFRACTION_QUALITY == 1
    const int maximumSamples=96;
    const float pixelStride=4.0;
#else
    const int maximumSamples=32;
    const float pixelStride=8.0;
#endif
    int samples=int(clamp(ceil(length((pb-pa)*viewportSize())/pixelStride),8.0,float(maximumSamples)));
    float previous=0.0,previousError=-1.0;
    for(int i=1;i<=maximumSamples;i++){
        if(i>samples)break;
        float f=float(i)/float(samples);
        vec2 uv=mix(pa,pb,f);
        if(min(uv.x,uv.y)<0.001||max(uv.x,uv.y)>0.999)break;
        vec3 point=mix(qa,qb,f)/mix(ka,kb,f);
        float error=refractionDepthError(point,uv);
        if(error>=0.0&&previousError<0.0){
            float left=previous,right=f;
            for(int refine=0;refine<8;refine++){
                float middle=(left+right)*0.5;
                vec2 testUV=mix(pa,pb,middle);
                vec3 testPoint=mix(qa,qb,middle)/mix(ka,kb,middle);
                if(refractionDepthError(testPoint,testUV)>=0.0)right=middle;else left=middle;
            }
            vec2 hitUV=mix(pa,pb,right);
            float hitDepth=texture(depthtex1,hitUV).r;
            vec3 receiver=positionFromDepth(hitUV,hitDepth);
            ivec2 receiverCell=clamp(ivec2(hitUV*vec2(textureSize(colortex10,0))),ivec2(0),textureSize(colortex10,0)-ivec2(1));
            vec4 receiverData=texelFetch(colortex10,receiverCell,0);
            vec3 n=unitVector(mat3(gbufferModelView)*receiverData.xyz);
            float denominator=dot(direction,n);
            float distance=abs(denominator)>0.00001?dot(receiver-origin,n)/denominator:-1.0;
            vec3 candidate=origin+direction*max(distance,0.0);
            vec2 candidateUV;
            bool projected=refractionProjection(candidate,candidateUV);
            if(projected&&distance>0.02&&distance<maximum&&receiverData.a>0.5){
                float candidateDepth=texture(depthtex1,candidateUV).r;
                vec3 actual=positionFromDepth(candidateUV,candidateDepth);
                float residual=length(actual-candidate);
                float tolerance=0.045+0.0015*length(candidate);
                // The endpoint must lie on the transmitted side of the water;
                // foreground banks must never smear across a water silhouette.
                bool transmittedSide=dot(actual-origin,interfaceNormal)<0.02;
                if(candidateDepth<0.999999&&residual<tolerance&&transmittedSide){
                    vec2 border=min(candidateUV,1.0-candidateUV);
                    float confidence=1.0-smoothstep(tolerance*0.35,tolerance,residual);
                    confidence*=smoothstep(0.002,0.018,min(border.x,border.y));
                    opticalPath=distance;
                    return vec4(texture(colortex4,candidateUV).rgb,confidence);
                }
            }
        }
        previous=f;previousError=error;
    }
    return vec4(0.0);
}
#endif

vec3 transmissionProbe(vec2 uv,bool bent){
 vec3 incident=normalize(vec3(uv*2.-1.,-1.));
 vec3 origin=incident/(-incident.y);
 vec3 direction=bent?refract(incident,vec3(0,1,0),1./1.333):incident;
 float path;vec4 hit=traceWaterTransmission(origin,direction,vec3(0,1,0),path);
 return vec3(hit.a,path,hit.r);
}
uniform float probeDistance;layout(location=0)out vec4 result;void main(){int c=int(probeDistance+.5);
if(c==0)result=vec4(vec3(dielectricWaterFresnel(1.,1.,1.333)),1.);
if(c==1)result=vec4(vec3(dielectricWaterFresnel(.02,1.,1.333)),1.);
if(c==2)result=vec4(vec3(dielectricWaterFresnel(.5,1.333,1.)),1.);
if(c==3)result=vec4(vec3(dielectricWaterFresnel(.9,1.333,1.)),1.);
if(c==4)result=vec4(refract(normalize(vec3(.70710678,-.70710678,0)),vec3(0,1,0),1./1.333),1.);
if(c==5)result=vec4(refract(normalize(vec3(.5,.8660254,0)),vec3(0,-1,0),1.333),1.);
if(c==6)result=vec4(refract(normalize(vec3(.8660254,.5,0)),vec3(0,-1,0),1.333),1.);
if(c==7)result=vec4(vec3(materialWetDarkening(1.,wetMaterialProperties(4110).x)),1.);
if(c==8)result=vec4(vec3(materialWetDarkening(1.,wetMaterialProperties(4111).x)),1.);
if(c==9)result=vec4(vec3(materialWetDarkening(1.,wetMaterialProperties(4112).x)),1.);
if(c==10)result=vec4(vec3(materialWetDarkening(1.,wetMaterialProperties(4116).x)),1.);
if(c==11)result=vec4(vec3(materialWetDarkening(1.,wetMaterialProperties(4117).x)),1.);
if(c==12)result=vec4(vec3(materialWetDarkening(1.,wetMaterialProperties(4115).x)),1.);
if(c==13)result=vec4(vec3(materialWetDarkening(1.,wetMaterialProperties(4114).x)),1.);
if(c==14)result=vec4(vec3(materialWetDarkening(0.,.9)),1.);
if(c==15)result=vec4(vec3(exposedWetFilm(1.)),1.);
if(c==16)result=vec4(vec3(exposedWetFilm(0.)),1.);
if(c==17)result=vec4(travelThroughWater(vec3(.5),2.,vec3(.247,.463,.894),1.,0.),1.);
if(c==18)result=vec4(travelThroughWater(vec3(.5),8.,vec3(.247,.463,.894),1.,0.),1.);
if(c==19)result=vec4(travelThroughWater(vec3(.5),24.,vec3(.247,.463,.894),1.,0.),1.);
if(c==20)result=vec4(abs(travelThroughWater(travelThroughWater(vec3(.5),2.,1.),3.,1.)-travelThroughWater(vec3(.5),5.,1.)),1.);
if(c==21)result=vec4(waterBodyColour(vec3(.247,.463,.894),0.,0.),1.);
if(c==22)result=vec4(waterBodyColour(vec3(.247,.463,.894),1.,0.),1.);
if(c==23)result=vec4(waterBodyColour(vec3(.247,.463,.894),0.,1.),1.);
if(c==24)result=vec4(vec3(physicalCloudLayer(vec3(200,100,200),vec3(0,1,0),7000.).a),1.);
if(c==25)result=vec4(vec3(physicalCloudLayer(vec3(200,256,200),vec3(1,0,0),7000.).a),1.);
if(c==26)result=vec4(vec3(physicalCloudLayer(vec3(200,420,200),vec3(0,-1,0),7000.).a),1.);
if(c==27)result=vec4(vec3(physicalCloudLayer(vec3(200,100,200),vec3(0,-1,0),7000.).a),1.);
if(c==28)result=vec4(vec3(physicalCloudLayer(vec3(200,100,200),vec3(0,1,0),10.).a),1.);
if(c==29)result=vec4(vec3(mistDensityWorld(vec3(0,70,0))),1.);
if(c==30)result=vec4(vec3(mistDensityWorld(vec3(40,70,30))),1.);
if(c==31)result=vec4(vec3(mistDensityWorld(vec3(0,600,0))),1.);
if(c==32)result=vec4(vec3(volumetricMist(vec3(0,70,0),vec3(1,0,0),20.,1.,60).a),1.);
if(c==33)result=vec4(vec3(volumetricMist(vec3(0,70,0),vec3(1,0,0),120.,1.,60).a),1.);
if(c==34)result=vec4(vec3(volumetricMist(vec3(0,70,0),vec3(1,0,0),120.,0.,60).a),1.);
if(c==35)result=vec4(formIrradiance(vec3(0,1,0),1.),1.);
if(c==36)result=vec4(formIrradiance(vec3(1,0,0),1.),1.);
if(c==37)result=vec4(diffuseRadiance(vec3(.8),vec3(0),0.,vec3(0,1,0),1.,vec3(0,0,-10),4112),1.);
if(c==38)result=vec4(transmissionProbe(vec2(.5,.35),true),1.);
if(c==39)result=vec4(transmissionProbe(vec2(.5,.35),false),1.);
if(c==40)result=vec4(transmissionProbe(vec2(.20,.35),true),1.);
}
