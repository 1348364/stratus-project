#version 330 core
#define DIMENSION_TYPE 0
#ifndef STRATUS_OPTIONS_INCLUDED
#define STRATUS_OPTIONS_INCLUDED
// Balanced defaults; quality profiles only change sampling counts.
#define SKY_AMBIENT 1.40 // [0.80 1.00 1.20 1.40 1.60 1.80 2.00]
const float ambientOcclusionLevel = 1.00; // [0.00 0.15 0.30 0.45 0.60 0.80 1.00]
#define WHITE_BALANCE 0.00 // [-0.08 -0.04 0.00 0.04 0.08]
#define SURFACE_SATURATION 1.00 // [0.85 0.93 1.00 1.07 1.15]
#define SURFACE_DAMPNESS 1.00 // [0.00 0.35 0.65 1.00 1.35 1.70 2.00]
#define CLOUD_AMOUNT 1.00 // [0.00 0.35 0.60 0.75 0.90 1.00]
#define CLOUD_ALTITUDE 192.0 // [128.0 160.0 192.0 224.0 256.0 320.0]
#define CLOUD_THICKNESS 72.0 // [20.0 32.0 40.0 56.0 72.0]
#define SKY_LEAK 0.35 // [0.00 0.15 0.25 0.35 0.50 0.70]
#define CLOUD_SPAN 240.0 // [160.0 240.0 360.0 540.0 700.0 900.0]
#define CLOUD_DISTORTION 0.65 // [0.25 0.45 0.65 0.85 1.00]
#define CLOUD_RELIEF 0.55 // [0.25 0.40 0.55 0.70]
#define CLOUD_DRIFT 0.25 // [0.00 0.10 0.25 0.45 0.70]
#define CLOUD_LAYERS 1 // [1 2 3]
#define MIST_AMOUNT 0.75 // [0.00 0.40 0.60 0.75 1.00 1.25]
#define MIST_Y 70.0 // [48.0 64.0 70.0 88.0 112.0 144.0]
#define MIST_THICKNESS 12.0 // [7.0 9.0 12.0 16.0 22.0]
#define MIST_CLEAR 80.0 // [16.0 32.0 48.0 64.0 80.0 112.0 144.0]
#define MIST_DETAIL 2 // [1 2 3]
#define REFLECT_LEVEL 0.85 // [0.40 0.60 0.85 1.00]
#define REFLECTION_MODE 1 // [0 1 2]
#define REFLECT_RANGE 88.0 // [48.0 64.0 88.0 120.0]
#define WATER_VISIBILITY 4.00 //  [0.20 0.35 0.50 0.70 0.90 1.10 1.30 1.70 2.20 3.00 4.00]
#define WATER_EXTINCTION 0.90 // [0.45 0.65 0.90 1.15 1.40]
#define RIPPLE_HEIGHT 0.80 // [0.00 0.30 0.55 0.80 1.00]
#define RIPPLE_SIZE 1.00 // [0.65 0.80 1.00 1.25 1.50]
#define RIPPLE_RATE 0.45 // [0.00 0.20 0.45 0.70 1.00]
#define FACE_SHADING 1.00 // [0.00 0.15 0.25 0.35 0.50 0.70 0.85 1.00]
#define WET_SHEEN 0.65 // [0.00 0.35 0.65 0.85 1.00]
#define BLOOM_STRENGTH 0.18 // [0.00 0.06 0.12 0.18 0.25 0.35]
#define BLOOM_RADIUS 3.00 // [0.50 1.00 1.50 2.00 3.00 4.00]
#define SUN_VISIBILITY 0.00 //  [0.00 0.25 0.45 0.65 0.85 1.00]
#define LAMP_LEVEL 1.00 // [0.70 0.85 1.00 1.15 1.30]
#define LAMP_HEAT 0.25 // [0.00 0.15 0.25 0.40 0.60]
#define FACE_BLEND 0.00 //  [0.00 0.25 0.50 0.75 1.00]
#define GROUND_WARMTH 0.00 //  [0.00 0.20 0.45 0.65 0.85]
#define WATER_DISTORTION 0.75 // [0.00 0.35 0.55 0.75 1.00 1.35]
#define CIRRUS_AMOUNT 0.65 // [0.00 0.35 0.65 0.85 1.00]
#define CIRRUS_ALTITUDE 360.0 // [280.0 320.0 360.0 400.0 460.0]
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
    float aureole=exp(-separation/0.008)*0.70;
    sky+=sunlightColour()*solarDaylight()*(glow+(core+aureole)*SUN_VISIBILITY*(1.0-0.65*rainStrength));
    return sky;
#endif
}
vec2 layeredCloudSample(vec3 worldPoint,bool detailed,bool upper){
    float altitude=upper?CIRRUS_ALTITUDE:CLOUD_ALTITUDE;
    float thickness=upper?32.0:CLOUD_THICKNESS;
    float amount=upper?CIRRUS_AMOUNT:CLOUD_AMOUNT;
    vec2 wind=frameTimeCounter*CLOUD_DRIFT*vec2(0.31,-0.14)*(upper?1.55:1.0);
    vec2 weatherPoint=(worldPoint.xz+wind)/CLOUD_SPAN;
    float weather=smoothField(weatherPoint*vec2(0.72,1.40)+vec2(8.1,-19.4));
    float centre=altitude+(weather-0.5)*thickness*CLOUD_DISTORTION*0.65;
    float height=(worldPoint.y-centre)/thickness+0.5;
    float envelope=smoothstep(0.0,0.24,height)*(1.0-smoothstep(0.66,1.0,height));
    if(envelope<=0.0||amount<=0.0)return vec2(0.0);
    float scale=max(CLOUD_SPAN*(upper?0.23:0.28),24.0);
    vec3 p=vec3((worldPoint.x+wind.x)/scale,(worldPoint.y-altitude)/max(thickness*0.9,1.0),(worldPoint.z+wind.y)/scale);
    p.xz=mat2(0.8,-0.6,0.6,0.8)*p.xz;
    if(upper){p.x*=0.34;p.z*=1.8;p.x+=sin(p.z*0.8+weather*3.0)*0.35;}
    p.x+=(weather-0.5)*CLOUD_DISTORTION;
    float body=simplexVolume(p);
    if(detailed){
        vec3 detail=vec3(p.z+p.y*.4,p.x-p.z*.3,p.y+p.x*.3)*2.07+vec3(7.2,2.3,-8.1);
        body=mix(body,simplexVolume(detail),0.25);
#if CLOUD_LAYERS > 2
        body-=0.065*(1.0-simplexVolume(p*4.13-vec3(4.7,8.2,2.1)));
#endif
    }
    float threshold=mix(0.70,upper?0.46:0.43,amount);
    float bulk=smoothstep(threshold-0.15,threshold+0.17,body+(weather-0.5)*0.25);
    float density=envelope*bulk*amount*(upper?0.026:0.055);
    return vec2(density,height);
}
vec2 cloudVolumeSample(vec3 p,bool detailed){return layeredCloudSample(p,detailed,false);}
vec2 cloudSample(vec3 p){return layeredCloudSample(p,true,false);}
float cloudSunTransmission(vec3 point){
    vec3 l=broadLightDirection();float span=CLOUD_THICKNESS;
    float tau=layeredCloudSample(point+l*span*0.32,false,false).x*span*0.60;
#if CLOUD_LAYERS > 2
    tau+=layeredCloudSample(point+l*span*0.75,false,false).x*span*0.45;
#endif
    return exp(-tau);
}
vec4 overLayers(vec4 front,vec4 back){
    float alpha=front.a+(1.0-front.a)*back.a;
    return vec4((front.rgb*front.a+back.rgb*back.a*(1.0-front.a))/max(alpha,0.00001),alpha);
}
vec4 marchSingleCloud(vec3 origin,vec3 worldRay,float distanceLimit,int steps,bool shadows,bool upper){
#if DIMENSION_TYPE != 0
    return vec4(0.0);
#else
    float amount=upper?CIRRUS_AMOUNT:CLOUD_AMOUNT;if(amount<=0.0)return vec4(0.0);
    float altitude=upper?CIRRUS_ALTITUDE:CLOUD_ALTITUDE;
    float thickness=upper?32.0:CLOUD_THICKNESS;
    float bottom=altitude-thickness*0.90,top=altitude+thickness*0.90;
    vec3 ray=unitVector(worldRay);float begin=0.0,finish=min(distanceLimit,7000.0);
    if(abs(ray.y)<0.0001){if(origin.y<bottom||origin.y>top)return vec4(0.0);finish=min(finish,450.0);}
    else{float a=(bottom-origin.y)/ray.y,b=(top-origin.y)/ray.y;begin=max(min(a,b),0.0);finish=min(finish,max(a,b));}
    if(finish<=begin)return vec4(0.0);
    float stride=min((finish-begin)/float(steps),thickness*0.70);
    float transmission=1.0;vec3 scattered=vec3(0.0);
    float separation=max(1.0-dot(ray,broadLightDirection()),0.0);
    float phase=0.75/pow(max(0.25+separation,0.05),1.5);
    float solarPatch=exp(-separation/0.0014)*SUN_VISIBILITY;
    for(int i=0;i<steps;i++){
        vec3 point=origin+ray*(begin+(float(i)+0.5)*stride);
        vec2 sampleData=layeredCloudSample(point,shadows||upper,upper);if(sampleData.x<=0.00001)continue;
        float opacity=1.0-exp(-sampleData.x*stride);
        float h=clamp(sampleData.y,0.0,1.0);
        float sunlight=shadows&&!upper?cloudSunTransmission(point):mix(0.35,1.0,h);
        float ambient=mix(0.48,1.0,h);
        vec3 daylight=vec3(0.35,0.39,0.46)*ambient;
        daylight+=sunlightColour()*sunlight*(0.31+phase*0.055*SUN_VISIBILITY);
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
vec4 physicalCloudLayer(vec3 origin,vec3 ray,float limit){return marchCloudLayer(origin,ray,limit,6+CLOUD_LAYERS*4,true);}
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
    vec3 drift=vec3(frameTimeCounter*0.045,0.0,-frameTimeCounter*0.025);
    float field=simplexVolume((point+drift)*vec3(0.009,0.022,0.009));
    float centre=MIST_Y+(field-0.5)*MIST_THICKNESS*1.4;
    float h=(point.y-centre)/max(MIST_THICKNESS*1.7,1.0);
    float lower=exp(-h*h*0.5);
    float upper=exp(-pow((point.y-MIST_Y-MIST_THICKNESS*2.1)/max(MIST_THICKNESS*0.65,1.0),2.0)*0.5);
    return (0.0065*lower+0.0020*upper)*mix(0.22,1.60,smoothstep(0.18,0.80,field))*MIST_AMOUNT;
}
vec4 volumetricMist(vec3 origin,vec3 worldRay,float distanceLimit,float skyExposure,int steps){
#if DIMENSION_TYPE != 0
    return vec4(0.0);
#else
    if(MIST_AMOUNT<=0.0||skyExposure<0.03)return vec4(0.0);
    vec3 ray=unitVector(worldRay);
    float begin=max(MIST_CLEAR-length(origin-cameraPosition),0.0),finish=min(distanceLimit,900.0);
    float bottom=MIST_Y-MIST_THICKNESS*6.0,top=MIST_Y+MIST_THICKNESS*4.0;
    if(abs(ray.y)<0.0001){if(origin.y<bottom||origin.y>top)return vec4(0.0);}
    else{float a=(bottom-origin.y)/ray.y,b=(top-origin.y)/ray.y;begin=max(begin,min(a,b));finish=min(finish,max(a,b));}
    begin=max(begin,0.0);if(finish<=begin)return vec4(0.0);
    float stride=(finish-begin)/float(steps),opticalDepth=0.0;
    for(int i=0;i<steps;i++){
        vec3 point=origin+ray*(begin+(float(i)+0.5)*stride);
        float clearWeight=smoothstep(MIST_CLEAR,MIST_CLEAR+45.0,length(point-cameraPosition));
        opticalDepth+=mistDensityWorld(point)*stride*clearWeight;
    }
    float opacity=(1.0-exp(-opticalDepth))*smoothstep(0.03,0.70,skyExposure);
    float sun=pow(max(dot(ray,broadLightDirection()),0.0),5.0)*solarDaylight();
    return vec4(atmosphericColour()+sunlightColour()*sun*0.055,opacity);
#endif
}
vec4 atmosphereSegment(vec3 origin,vec3 ray,float distanceLimit,float skyExposure,bool detailed){
    int cloudSteps=detailed?6+CLOUD_LAYERS*4:6;
    vec4 clouds=marchCloudLayer(origin,ray,distanceLimit,cloudSteps,detailed);
    vec4 mist=volumetricMist(origin,ray,distanceLimit,skyExposure,detailed?2+MIST_DETAIL*2:3);
    return ray.y<0.0?overLayers(clouds,mist):overLayers(mist,clouds);
}
#endif

#ifndef STRATUS_DIFFUSE_INCLUDED
#define STRATUS_DIFFUSE_INCLUDED
// Approximate properties for ordinary textures without PBR maps.
// x: porosity, y: perceptual roughness. Stone and embedded ores share a class.
vec2 wetMaterialProperties(int material) {
    if (material == 4110) return vec2(0.90, 0.96);
    if (material == 4111) return vec2(0.64, 0.80);
    if (material == 4113) return vec2(0.18, 0.68);
    if (material == 4114) return vec2(0.04, 0.38);
    if (material == 4115) return vec2(0.80, 0.98);
    return vec2(0.58, 0.86);
}
float outdoorMoisture(float skyExposure, float kind) {
#if DIMENSION_TYPE == 0
    if (kind > 1.05 && kind < 2.5) {
        float outdoors = smoothstep(0.18, 0.88, skyExposure);
        return outdoors * (1.0 - exp(-1.75 * SURFACE_DAMPNESS)) * (1.0 + 0.08 * rainStrength);
    }
#endif
    return 0.0;
}
vec3 absorbedWetAlbedo(vec3 dryAlbedo, float moisture, float porosity) {
    // Pore filling changes the RGB absorption curve, preserving texture detail.
    // Brighter channels lose less light, giving a restrained saturation change.
    vec3 saturated = dryAlbedo / (vec3(1.0) + 1.55 * porosity * (vec3(1.0) - dryAlbedo));
    return mix(dryAlbedo, saturated, clamp(moisture, 0.0, 1.0));
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
    return mix(vec3(1.0), irradiance, FACE_SHADING);
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
    vec2 properties = wetMaterialProperties(material);
    float moisture = clamp(outdoorMoisture(skyExposure, kind), 0.0, 1.0);
    vec3 albedo = absorbedWetAlbedo(decodeDisplay(colour), moisture, properties.x);
    vec3 reflected = albedo * light * form;
#if DIMENSION_TYPE == 0
    if(kind>1.05&&kind<2.5){
        float warmth=GROUND_WARMTH*skyExposure*daytimeWeight()*mix(0.60,1.0,max(normal.y,0.0));
        reflected*=mix(vec3(1.0),vec3(1.17,1.035,0.82),warmth);
    }
#endif
    if (moisture > 0.001 && WET_SHEEN > 0.0) {
        vec3 view = unitVector(-playerPoint);
        float nv = max(dot(normal, view), 0.0);
        float roughness = mix(properties.y, max(0.28, properties.y * 0.48), moisture);
        // Vertical faces shed the film but retain damp absorption and sheening.
        float film = moisture * mix(0.32, 1.0, max(normal.y, 0.0)) * WET_SHEEN;
        vec3 ray = reflect(-view, normal);
        vec3 environment = softSkyReflection(ray);
        float exposure = skyExposure * mix(0.12, 1.0, smoothstep(-0.10, 0.45, ray.y));
        float fresnel = waterFresnel(nv) * (1.0 - 0.42 * roughness);
        float coat = clamp(film * fresnel, 0.0, 0.85);
        // Redirect diffuse energy into a sky film, rather than adding a flat glow.
        reflected = mix(reflected, environment * SKY_AMBIENT * exposure, coat);
        float specular = wetSunSpecular(normal, view, broadLightDirection(), roughness);
        float sun = daytimeWeight() * skyExposure * (1.0 - 0.75 * rainStrength);
        reflected += sunlightColour() * 0.72 * specular * sun * film;
    }
    if (kind > 1.5 && kind < 2.5) {
        float interior = smoothstep(0.48, 0.94, max(colour.r, max(colour.g, colour.b)));
        reflected = max(reflected, decodeDisplay(colour) * interior * LAMP_LEVEL * 2.1);
    }
    return reflected;
}
#endif

#ifndef STRATUS_MEDIUM_INCLUDED
#define STRATUS_MEDIUM_INCLUDED
vec3 waterExtinction() {
    return vec3(0.205, 0.081, 0.035) * WATER_EXTINCTION / max(WATER_VISIBILITY, 0.05);
}
vec3 waterBodyColour(float skyExposure) {
    float illumination = mix(0.06, 1.0, skyExposure * daytimeWeight());
    return vec3(0.035, 0.125, 0.180) * illumination;
}
vec3 travelThroughWater(vec3 radiance, float distanceInWater, float skyExposure) {
    vec3 transmission = exp(-waterExtinction() * max(distanceInWater, 0.0));
    return radiance * transmission + waterBodyColour(skyExposure) * (1.0 - transmission);
}
#endif


uniform float probeDistance;
layout(location=0) out vec4 result;
void main(){
int c=int(probeDistance+0.5);
if(c==0)result=vec4(vec3(outdoorMoisture(0.0,1.3)),1.0);
if(c==1)result=vec4(vec3(outdoorMoisture(1.0,1.0)),1.0);
if(c==2)result=vec4(absorbedWetAlbedo(vec3(.08,.25,.60),outdoorMoisture(1.0,1.3),.58),1.0);
if(c==3)result=vec4(diffuseRadiance(vec3(.1),vec3(.8),1.0,vec3(0,1,0),1.3,vec3(0,-.15,-10),4112),1.0);
if(c==4)result=vec4(diffuseRadiance(vec3(.65),vec3(.8),1.0,vec3(0,1,0),1.0,vec3(0,0,-10),4112),1.0);
if(c==5)result=vec4(diffuseRadiance(vec3(.65),vec3(.8),1.0,vec3(1,0,0),1.0,vec3(0,0,-10),4112),1.0);
if(c==6)result=vec4(diffuseRadiance(vec3(.65),vec3(.8),1.0,vec3(0,-1,0),1.0,vec3(0,0,-10),4112),1.0);
if(c==7)result=vec4(diffuseRadiance(vec3(.85),vec3(0),0.0,vec3(0,1,0),1.0,vec3(0,0,-10),4112),1.0);
if(c==8)result=vec4(diffuseRadiance(vec3(.95),vec3(0),0.0,vec3(0,1,0),2.0,vec3(0,0,-10),4101),1.0);
if(c==9)result=vec4(abs(diffuseRadiance(vec3(.5),vec3(.8),1.0,vec3(0,1,0),.8,vec3(0,0,-10),4112)-diffuseRadiance(vec3(.5),vec3(.8),1.0,vec3(1,0,0),.8,vec3(0,0,-10),4112)),1.0);
if(c==10)result=vec4(abs(travelThroughWater(travelThroughWater(vec3(.5),2,1),3,1)-travelThroughWater(vec3(.5),5,1)),1.0);
if(c==11)result=vec4(travelThroughWater(vec3(.5),2,1),1.0);
if(c==12)result=vec4(travelThroughWater(vec3(.5),8,1),1.0);
if(c==13)result=vec4(travelThroughWater(vec3(.5),20,1),1.0);
if(c==14)result=vec4(formIrradiance(vec3(0,1,0),1.0),1.0);
if(c==15)result=vec4(formIrradiance(vec3(1,0,0),1.0),1.0);
if(c==16)result=vec4(formIrradiance(vec3(-1,0,0),1.0),1.0);
if(c==17)result=vec4(formIrradiance(vec3(0,0,1),1.0),1.0);
if(c==18)result=vec4(formIrradiance(vec3(0,0,-1),1.0),1.0);
if(c==19)result=vec4(formIrradiance(vec3(0,-1,0),1.0),1.0);
if(c==20)result=vec4(diffuseRadiance(vec3(.5),vec3(.8),1.0,vec3(0,1,0),1.3,vec3(0,0,-10),4112),1.0);
if(c==21)result=vec4(diffuseRadiance(vec3(.5),vec3(.8),1.0,vec3(0,1,0),1.3,vec3(0,0,-10),4112),1.0);
if(c==22)result=vec4(vec3(simplexVolume(vec3(1.2,.3,4.5)),simplexVolume(vec3(1.2,.9,4.5)),simplexVolume(vec3(1.2,1.6,4.5))),1.0);
if(c==23)result=vec4(vec3(physicalCloudLayer(vec3(200,100,200),normalize(vec3(.2,1,.1)),7000).a,physicalCloudLayer(vec3(200,192,200),vec3(1,0,0),7000).a,physicalCloudLayer(vec3(200,285,200),normalize(vec3(.2,-1,.1)),7000).a),1.0);
if(c==24)result=vec4(vec3(physicalCloudLayer(vec3(200,100,200),vec3(0,-1,0),7000).a,physicalCloudLayer(vec3(200,100,200),vec3(1,0,0),7000).a,physicalCloudLayer(vec3(200,100,200),vec3(0,1,0),10).a),1.0);
if(c==25)result=vec4(vec3(marchSingleCloud(vec3(200,290,200),vec3(0,1,0),7000,8,false,true).a),1.0);
if(c==26)result=vec4(vec3(mistDensityWorld(vec3(0,70,0)),mistDensityWorld(vec3(100,70,100)),mistDensityWorld(vec3(0,120,0))),1.0);
if(c==27)result=vec4(vec3(volumetricMist(cameraPosition,vec3(1,0,0),60,1,8).a),1.0);
if(c==28)result=vec4(vec3(volumetricMist(cameraPosition,vec3(1,0,0),300,0,8).a),1.0);
if(c==29)result=vec4(vec3(volumetricMist(cameraPosition,vec3(1,0,0),300,1,8).a),1.0);
if(c==30)result=vec4(sunlightColour(),1.0);
if(c==31)result=vec4(skyBackdrop(broadLightDirection()),1.0);
if(c==32)result=vec4(skyBackdrop(broadLightDirection()),1.0);
if(c==33)result=vec4(skyBackdrop(-broadLightDirection()),1.0);
}
