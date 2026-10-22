#version 330 core
#define DIMENSION_TYPE 0
#ifndef STRATUS_OPTIONS_INCLUDED
#define STRATUS_OPTIONS_INCLUDED
// Reference defaults; quality profiles only change sampling counts.
#define SKY_AMBIENT 1.40 // [0.80 1.00 1.20 1.40 1.60 1.80 2.00]
const float ambientOcclusionLevel = 1.00; // [0.00 0.15 0.30 0.45 0.60 0.80 1.00]
#define WHITE_BALANCE 0.00 // [-0.08 -0.04 0.00 0.04 0.08]
#define SURFACE_SATURATION 1.00 // [0.85 0.93 1.00 1.07 1.15]
#define SURFACE_DAMPNESS 1.00 // [0.00 0.35 0.65 1.00 1.35 1.70 2.00]
#define CLOUD_AMOUNT 1.00 // [0.00 0.35 0.60 0.75 0.90 1.00]
#define CLOUD_ALTITUDE 192.0 // [128.0 160.0 192.0 224.0 256.0 320.0]
#define CLOUD_THICKNESS 40.0 // [20.0 32.0 40.0 56.0 72.0]
#define SKY_LEAK 0.00 //  [0.00 0.15 0.25 0.35 0.50 0.70]
#define CLOUD_SPAN 240.0 // [160.0 240.0 360.0 540.0 700.0 900.0]
#define CLOUD_DISTORTION 0.65 // [0.25 0.45 0.65 0.85 1.00]
#define CLOUD_RELIEF 0.55 // [0.25 0.40 0.55 0.70]
#define CLOUD_DRIFT 0.25 // [0.00 0.10 0.25 0.45 0.70]
#define CLOUD_LAYERS 2 // [1 2 3]
#define MIST_AMOUNT 0.75 // [0.00 0.40 0.60 0.75 1.00 1.25]
#define MIST_Y 70.0 // [48.0 64.0 70.0 88.0 112.0 144.0]
#define MIST_THICKNESS 12.0 // [7.0 9.0 12.0 16.0 22.0]
#define MIST_CLEAR 80.0 // [16.0 32.0 48.0 64.0 80.0 112.0 144.0]
#define MIST_DETAIL 2 // [1 2 3]
#define REFLECT_LEVEL 0.85 // [0.40 0.60 0.85 1.00]
#define REFLECTION_MODE 1 // [0 1 2]
#define REFLECT_RANGE 88.0 // [48.0 64.0 88.0 120.0]
#define WATER_VISIBILITY 0.90 // [0.50 0.70 0.90 1.10 1.30]
#define WATER_EXTINCTION 0.90 // [0.45 0.65 0.90 1.15 1.40]
#define RIPPLE_HEIGHT 0.55 // [0.00 0.30 0.55 0.80 1.00]
#define RIPPLE_SIZE 1.00 // [0.65 0.80 1.00 1.25 1.50]
#define RIPPLE_RATE 0.45 // [0.00 0.20 0.45 0.70 1.00]
#define FACE_SHADING 0.00 //  [0.00 0.15 0.25 0.35 0.50 0.70]
#define BLOOM_STRENGTH 0.06 // [0.00 0.03 0.06 0.09 0.12 0.18]
#define LAMP_LEVEL 1.00 // [0.70 0.85 1.00 1.15 1.30]
#define LAMP_HEAT 0.25 // [0.00 0.15 0.25 0.40 0.60]
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
#endif

// END INCLUDE /core/field.glsl

vec3 atmosphericColour() {
#if DIMENSION_TYPE == 0
    return decodeDisplay(mix(vec3(0.10, 0.135, 0.185), vec3(0.715, 0.763, 0.813), daytimeWeight()) * (1.0 - 0.08 * rainStrength));
#else
    return decodeDisplay(fogColor);
#endif
}
vec3 skyBackdrop(vec3 worldRay) {
#if DIMENSION_TYPE != 0
    return decodeDisplay(fogColor);
#else
    vec3 ray = unitVector(worldRay);
    float horizon = exp(-abs(ray.y) * 5.0);
    vec3 zenith = decodeDisplay(mix(vec3(0.045, 0.072, 0.12), vec3(0.51, 0.63, 0.77), daytimeWeight()));
    vec3 sky = mix(zenith, atmosphericColour(), horizon);
    // Retain the reference sky's distant overcast bands above the finite layer.
    // This high ceiling supplies detail even through thin nearby cloud regions.
    vec2 sheet = (ray.xz / max(ray.y + 0.16, 0.20) * 450.0 + cameraPosition.xz) / (CLOUD_SPAN * 1.8);
    sheet += frameTimeCounter * CLOUD_DRIFT * vec2(0.0013, -0.0006);
    float bend = smoothField(sheet * 0.37 + vec2(8.1, -19.4));
    float phase = sheet.y * 5.4 + CLOUD_DISTORTION * ((bend - 0.5) * 5.0 + sin(sheet.x * 1.1) * 0.9);
    float shape = mix(0.5 + 0.5 * sin(phase), smoothField(sheet * vec2(0.62, 2.75) + vec2(-4.3, 7.2)), 0.52);
    float relief = (shape - 0.5) * CLOUD_RELIEF;
    vec3 upper = vec3(0.61, 0.66, 0.73) + relief * vec3(0.38, 0.36, 0.33);
    upper = mix(vec3(0.068, 0.095, 0.145), upper, daytimeWeight());
    upper *= 1.0 - 0.14 * rainStrength;
    float highCloud = CLOUD_AMOUNT * smoothstep(-0.02, 0.20, ray.y);
    sky = mix(sky, decodeDisplay(upper), highCloud * (1.0 - exp(-max(ray.y, 0.0) * 8.5)));
    float alignment = pow(max(dot(ray, broadLightDirection()), 0.0), 7.0);
    // Broad warm light through thinner cloud bands, with no hard sun disc.
    sky += vec3(0.24, 0.19, 0.12) * alignment * SKY_LEAK * daytimeWeight() * (0.45 + 0.55 * (1.0 - shape));
    return sky;
#endif
}
vec2 cloudSample(vec3 worldPoint) {
    vec2 sheet = worldPoint.xz / CLOUD_SPAN;
    sheet += frameTimeCounter * CLOUD_DRIFT * vec2(0.0013, -0.0006);
    float bend = smoothField(sheet * 0.47 + vec2(8.1, -19.4));
    float phase = sheet.y * 5.4 + CLOUD_DISTORTION * ((bend - 0.5) * 4.0 + sin(sheet.x * 1.1) * 0.8);
    float shape = mix(0.5 + 0.5 * sin(phase), smoothField(sheet * vec2(0.85, 2.75)), 0.55);
#if CLOUD_LAYERS > 1
    shape = mix(shape, smoothField(sheet * vec2(1.4, 4.15) + vec2(16.4, 12.9)), 0.16);
#endif
#if CLOUD_LAYERS > 2
    shape = mix(shape, smoothField(sheet * vec2(2.1, 6.3) - vec2(25.2, 1.7)), 0.07);
#endif
    float centre = CLOUD_ALTITUDE + (shape - 0.5) * CLOUD_THICKNESS * 0.35;
    float height = (worldPoint.y - centre) / CLOUD_THICKNESS + 0.5;
    float edge = smoothstep(0.0, 0.23, height) * (1.0 - smoothstep(0.68, 1.0, height));
    float coverage = CLOUD_AMOUNT * (0.25 + 0.75 * smoothstep(0.10, 0.72, shape));
    return vec2(edge * coverage * (0.020 + shape * 0.045), shape);
}
vec4 physicalCloudLayer(vec3 origin, vec3 worldRay, float maximumDistance) {
#if DIMENSION_TYPE != 0
    return vec4(0.0);
#else
    if (CLOUD_AMOUNT <= 0.0) return vec4(0.0);
    vec3 ray = unitVector(worldRay);
    float bottom = CLOUD_ALTITUDE - CLOUD_THICKNESS * 0.70;
    float top = CLOUD_ALTITUDE + CLOUD_THICKNESS * 0.70;
    float start = 0.0;
    float finish = min(maximumDistance, 7000.0);
    if (abs(ray.y) < 0.0001) {
        if (origin.y < bottom || origin.y > top) return vec4(0.0);
        finish = min(finish, 1200.0);
    } else {
        float a = (bottom - origin.y) / ray.y;
        float b = (top - origin.y) / ray.y;
        start = max(min(a,b), 0.0);
        finish = min(finish, max(a,b));
    }
    if (finish <= start) return vec4(0.0);
    const int steps = 6 + CLOUD_LAYERS * 4;
    float stride = (finish - start) / float(steps);
    float transmission = 1.0;
    vec3 scattered = vec3(0.0);
    float opening = pow(max(dot(ray, broadLightDirection()), 0.0), 6.0);
    for (int sampleIndex = 0; sampleIndex < steps; sampleIndex++) {
        vec3 point = origin + ray * (start + (float(sampleIndex) + 0.5) * stride);
        vec2 sampleData = cloudSample(point);
        float density = sampleData.x;
        float opacity = 1.0 - exp(-density * stride);
        float height = clamp((point.y - CLOUD_ALTITUDE) / CLOUD_THICKNESS + 0.5, 0.0, 1.0);
        float relief = mix(0.78, 1.13, height) * (0.98 - CLOUD_RELIEF * sampleData.y * 0.65);
        vec3 daylight = decodeDisplay(vec3(0.79, 0.81, 0.85)) * relief;
        daylight += vec3(0.22, 0.17, 0.10) * opening * SKY_LEAK * (1.0 - clamp(density * 10.0, 0.0, 0.8));
        vec3 colour = mix(vec3(0.006, 0.010, 0.019), daylight, daytimeWeight());
        colour *= 1.0 - 0.15 * rainStrength;
        scattered += transmission * opacity * colour;
        transmission *= 1.0 - opacity;
        if (transmission < 0.015) break;
    }
    float horizonFade = origin.y < bottom || origin.y > top ? smoothstep(0.0, 0.045, abs(ray.y)) : 1.0;
    return vec4(scattered / max(1.0 - transmission, 0.0001), (1.0 - transmission) * horizonFade);
#endif
}
vec3 overcastCeiling(vec3 worldRay) {
    vec3 sky = skyBackdrop(worldRay);
    vec4 cloud = physicalCloudLayer(cameraPosition, worldRay, 7000.0);
    return mix(sky, cloud.rgb, cloud.a);
}
#endif

#ifndef STRATUS_DIFFUSE_INCLUDED
#define STRATUS_DIFFUSE_INCLUDED
vec3 dampDiffuseColour(vec3 albedo, float skyExposure, vec3 normal, float kind, vec3 playerPoint) {
#if DIMENSION_TYPE == 0
    // All terrain/block entities, with no procedural dampness pattern.
    if (kind > 1.05 && kind < 2.5 && SURFACE_DAMPNESS > 0.0) {
        float outdoors = smoothstep(0.18, 0.88, skyExposure);
        float moisture = SURFACE_DAMPNESS * (1.0 + 0.15 * rainStrength);
        albedo *= exp(-0.90 * moisture * outdoors);
    }
#endif
    return albedo;
}
vec3 diffuseRadiance(vec3 colour, vec3 mappedLight, float skyExposure, vec3 worldNormal, float kind, vec3 playerPoint) {
    if (kind < 0.5) return decodeDisplay(colour);
    vec3 normal = unitVector(worldNormal);
    float faceVisibility = 1.0;
    vec3 hemisphereTint = vec3(1.0);
    if (kind > 1.05 && kind < 2.5) {
        float facing = max(dot(normal, broadLightDirection()), 0.0);
        float shape = 0.87 + 0.13 * max(normal.y, 0.0)
                    - 0.16 * max(-normal.y, 0.0) + 0.08 * (facing - 0.4);
        faceVisibility = mix(1.0, shape, FACE_SHADING);
        // Broad cool sky illumination and a restrained warm ground bounce.
        vec3 tint = mix(vec3(1.035, 1.005, 0.955), vec3(0.975, 1.0, 1.025), normal.y * 0.5 + 0.5);
        hemisphereTint = mix(vec3(1.0), tint, FACE_SHADING * skyExposure);
    }
    float lampShare = 1.0 - smoothstep(0.08, 0.85, skyExposure) * daytimeWeight();
    vec3 light = decodeDisplay(mappedLight) * mix(LAMP_LEVEL, SKY_AMBIENT, skyExposure);
    light *= mix(vec3(1.0), vec3(1.015, 0.985, 0.87), LAMP_HEAT * lampShare);
    vec3 albedo = dampDiffuseColour(decodeDisplay(colour), skyExposure, normal, kind, playerPoint);
    vec3 reflected = albedo * light * faceVisibility * hemisphereTint;
    if (kind > 1.5 && kind < 2.5) {
        float interior = smoothstep(0.48, 0.94, max(colour.r, max(colour.g, colour.b)));
        reflected = max(reflected, decodeDisplay(colour) * interior * LAMP_LEVEL);
    }
    return reflected;
}
#endif

#ifndef STRATUS_MEDIUM_INCLUDED
#define STRATUS_MEDIUM_INCLUDED
vec3 waterExtinction() {
    return vec3(0.165, 0.061, 0.024) * WATER_EXTINCTION / max(WATER_VISIBILITY, 0.05);
}
vec3 waterBodyColour(float skyExposure) {
    float illumination = mix(0.06, 1.0, skyExposure * daytimeWeight());
    return vec3(0.022, 0.095, 0.185) * illumination;
}
vec3 travelThroughWater(vec3 radiance, float distanceInWater, float skyExposure) {
    vec3 transmission = exp(-waterExtinction() * max(distanceInWater, 0.0));
    return radiance * transmission + waterBodyColour(skyExposure) * (1.0 - transmission);
}
#endif


uniform float probeDistance;
layout(location=0) out vec4 result;
void main(){
 int c=int(probeDistance+0.5);vec3 base=vec3(0.5);vec3 n=vec3(0,1,0);vec3 p=vec3(0);
 if(c==0)result=vec4(dampDiffuseColour(base,1,n,1.3,p),1);
 if(c==1)result=vec4(dampDiffuseColour(base,1,n,1.3,vec3(100000,87,-524)),1);
 if(c==2)result=vec4(dampDiffuseColour(base,0,n,1.3,p),1);
 if(c==3)result=vec4(dampDiffuseColour(base,1,n,1.0,p),1);
 if(c==4)result=vec4(abs(dampDiffuseColour(base,1,n,1.1,p)-dampDiffuseColour(base,1,n,1.3,p)),1);
 if(c==5)result=vec4(abs(dampDiffuseColour(base,1,n,1.3,p)-dampDiffuseColour(base,1,vec3(1,0,0),1.3,p)),1);
 if(c==6)result=vec4(abs(travelThroughWater(travelThroughWater(base,2,1),3,1)-travelThroughWater(base,5,1)),1);
 if(c==7)result=vec4(travelThroughWater(base,2,1),1);
 if(c==8)result=vec4(travelThroughWater(base,8,1),1);
 if(c==9)result=vec4(physicalCloudLayer(vec3(200,140,200),normalize(vec3(0.2,1,0.1)),7000).a,physicalCloudLayer(vec3(200,192,200),vec3(1,0,0),7000).a,physicalCloudLayer(vec3(200,245,200),normalize(vec3(0.2,-1,0.1)),7000).a,1);
 if(c==10)result=vec4(physicalCloudLayer(vec3(200,140,200),vec3(0,-1,0),7000).a,physicalCloudLayer(vec3(200,140,200),vec3(1,0,0),7000).a,physicalCloudLayer(vec3(200,140,200),vec3(0,1,0),10).a,1);
 if(c==11)result=vec4(skyBackdrop(broadLightDirection()),1);
 if(c==12)result=vec4(diffuseRadiance(base,vec3(0.8),0,n,1.3,p),1);
}
