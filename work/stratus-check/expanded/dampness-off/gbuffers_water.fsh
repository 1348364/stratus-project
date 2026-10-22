#version 330 core
layout(location = 0) out vec4 shim_FragData[8];
#define DIMENSION_TYPE 0
#define PASS_KIND 6
#define LATE_SURFACE 1

// BEGIN INCLUDE /core/raster.frag.glsl

// BEGIN INCLUDE /core/options.glsl
#ifndef STRATUS_OPTIONS_INCLUDED
#define STRATUS_OPTIONS_INCLUDED
// Reference defaults; quality profiles only change sampling counts.
#define SKY_AMBIENT 1.40 // [0.80 1.00 1.20 1.40 1.60 1.80 2.00]
const float ambientOcclusionLevel = 0.30; // [0.00 0.15 0.30 0.45 0.60]
#define WHITE_BALANCE 0.00 // [-0.08 -0.04 0.00 0.04 0.08]
#define SURFACE_SATURATION 1.00 // [0.85 0.93 1.00 1.07 1.15]
#define SURFACE_DAMPNESS 0.00 //  [0.00 0.35 0.65 1.00 1.35 1.70 2.00]
#define CLOUD_AMOUNT 1.00 // [0.75 0.90 1.00]
#define CLOUD_SPAN 540.0 // [360.0 440.0 540.0 700.0 900.0]
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
#define LAMP_LEVEL 1.00 // [0.70 0.85 1.00 1.15 1.30]
#define LAMP_HEAT 0.25 // [0.00 0.15 0.25 0.40 0.60]
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
#endif

// END INCLUDE /core/field.glsl

vec3 atmosphericColour() {
#if DIMENSION_TYPE == 0
    vec3 coolDay = vec3(0.715, 0.763, 0.813);
    vec3 quietNight = vec3(0.10, 0.135, 0.185);
    return decodeDisplay(mix(quietNight, coolDay, daytimeWeight()) * (1.0 - 0.08 * rainStrength));
#else
    return decodeDisplay(fogColor);
#endif
}
vec3 overcastCeiling(vec3 worldRay) {
#if DIMENSION_TYPE != 0
    return decodeDisplay(fogColor);
#else
    vec3 r = unitVector(worldRay);
    float denominator = max(r.y + 0.16, 0.20);
    vec2 sheet = (r.xz / denominator * 450.0 + cameraPosition.xz) / CLOUD_SPAN;
    sheet += frameTimeCounter * CLOUD_DRIFT * vec2(0.0013, -0.0006);
    float bend = smoothField(sheet * 0.37 + vec2(8.1, -19.4));
    float spacing = 0.85 + smoothField(sheet * 0.23 - vec2(31.0, 8.0)) * 0.35;
    float phase = sheet.y * 5.4 * spacing + CLOUD_DISTORTION *
        ((bend - 0.5) * 5.0 + sin(sheet.x * 1.1 + bend * 2.8) * 0.9);
    float ribbons = 0.5 + sin(phase) * 0.5;
    float breakup = smoothField(sheet * vec2(0.62, 2.75) + vec2(-4.3, 7.2));
    float shape = mix(ribbons, breakup, 0.52);
#if CLOUD_LAYERS > 1
    shape = mix(shape, smoothField(sheet * vec2(1.10, 4.15) + vec2(16.4, 12.9)), 0.16);
#endif
#if CLOUD_LAYERS > 2
    shape = mix(shape, smoothField(sheet * vec2(1.45, 6.30) - vec2(25.2, 1.7)), 0.055);
#endif
    float relief = (shape - 0.5) * CLOUD_RELIEF;
    vec3 ceiling = vec3(0.565, 0.610, 0.681) + relief * vec3(0.22, 0.21, 0.19);
    ceiling = mix(vec3(0.53, 0.62, 0.73), ceiling, CLOUD_AMOUNT);
    ceiling = mix(vec3(0.068, 0.095, 0.145), ceiling, daytimeWeight());
    ceiling *= 1.0 - 0.14 * rainStrength;
    float horizonBlend = exp(-max(r.y, 0.0) * 8.5);
    return mix(decodeDisplay(ceiling), atmosphericColour(), horizonBlend);
#endif
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
    float mist = valleyOpacity(relativePoint, skyExposure);
    vec3 airResult = radiance * (1.0 - mist) + atmosphericColour() * mist;
    if (isEyeInWater == 1) {
        vec3 loss = exp(-vec3(0.12, 0.055, 0.035) * length(relativePoint) * WATER_EXTINCTION);
        airResult = airResult * loss + decodeDisplay(vec3(0.13, 0.28, 0.36)) * (vec3(1.0) - loss);
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

vec3 dampDiffuseColour(vec3 albedo, float skyExposure, vec3 normal, float kind, vec3 playerPoint) {
#if DIMENSION_TYPE == 0
    // Fractional solid classes retain the existing <1.5 reflection eligibility.
    // Unclassified blocks, entities, emitters and held items have no damp mask.
    if (kind > 1.05 && kind < 1.45 && SURFACE_DAMPNESS > 0.0) {
        int material = int(floor((kind - 1.0) * 10.0 + 0.5));
        float absorbency = material == 1 ? 1.12 : material == 2 ? 0.90
                         : material == 3 ? 0.98 : 0.25;
        float outdoors = smoothstep(0.18, 0.88, skyExposure);
        float facing = mix(0.80, 1.0, max(normal.y, 0.0));
        facing *= 1.0 - 0.85 * max(-normal.y, 0.0);
        // Static broad variation stays anchored to the world during movement.
        vec3 worldPoint = cameraPosition + playerPoint;
        float field = smoothField(worldPoint.xz * 0.13);
        float patch = mix(0.60, 1.15, smoothstep(0.20, 0.80, field));
        float moisture = SURFACE_DAMPNESS * (1.0 + 0.15 * rainStrength);
        // Exponential absorption gives a useful extended range without clipping
        // dark texture pixels. Side faces retain enough coverage to read damp.
        albedo *= exp(-absorbency * moisture * outdoors * facing * patch);
    }
#endif
    return albedo;
}
vec3 diffuseRadiance(vec3 colour, vec3 mappedLight, float skyExposure, vec3 worldNormal, float kind, vec3 playerPoint) {
    if (kind < 0.5) return decodeDisplay(colour);
    vec3 normal = unitVector(worldNormal);
    float faceVisibility = 0.90 + 0.10 * max(normal.y, 0.0) - 0.13 * max(-normal.y, 0.0)
                         - 0.045 * normal.x * normal.x;
    float lampShare = (1.0 - smoothstep(0.08, 0.85, skyExposure) * daytimeWeight());
    vec3 light = decodeDisplay(mappedLight) * mix(LAMP_LEVEL, SKY_AMBIENT, skyExposure);
    light *= mix(vec3(1.0), vec3(1.015, 0.985, 0.87), LAMP_HEAT * lampShare);
    vec3 albedo = dampDiffuseColour(decodeDisplay(colour), skyExposure, normal, kind, playerPoint);
    vec3 reflected = albedo * light * faceVisibility;
    if (kind > 1.5 && kind < 2.5) {
        float interior = smoothstep(0.48, 0.94, max(colour.r, max(colour.g, colour.b)));
        reflected = max(reflected, decodeDisplay(colour) * interior * LAMP_LEVEL);
    }
    return reflected;
}
#endif

// END INCLUDE /core/diffuse.glsl

in vec4 tintAndOpacity;
in vec2 atlasCoordinate;
in vec2 illuminationCoordinate;
in vec3 relativeLocation;
in vec3 orientedNormal;
uniform sampler2D gtexture;
uniform sampler2D lightmap;
#if PASS_KIND == 3 || PASS_KIND == 6
flat in int blockCategory;
#endif
#if PASS_KIND == 4 || PASS_KIND == 5
uniform vec4 entityColor;
#endif

#if LATE_SURFACE == 1
/* RENDERTARGETS: 3,0,1 */
#elif PASS_KIND == 9
/* RENDERTARGETS: 0 */
#else
/* RENDERTARGETS: 0,1,2 */
#endif
void main() {
#if PASS_KIND == 8
    discard;
#else
    vec4 surface = tintAndOpacity;
#if PASS_KIND != 0
    surface *= texture(gtexture, atlasCoordinate);
#endif
#if PASS_KIND == 4 || PASS_KIND == 5
    surface.rgb = mix(surface.rgb, entityColor.rgb, entityColor.a);
#endif
    vec3 lm = vec3(1.0);
    float sky = 1.0;
    float category = 0.0;
#if PASS_KIND >= 2 && PASS_KIND <= 7
    lm = texture(lightmap, illuminationCoordinate).rgb;
    sky = clamp((illuminationCoordinate.t * 32.0 - 1.0) / 30.0, 0.0, 1.0);
    category = 1.0;
#endif
#if PASS_KIND == 3 || PASS_KIND == 6
    if (blockCategory == 4101 || blockCategory == 4102) category = 2.0;
#if PASS_KIND == 3
    // Soil, wood, mineral and foliage absorbency; no new render attachment.
    if (blockCategory >= 4110 && blockCategory <= 4113)
        category = 1.0 + float(blockCategory - 4109) * 0.1;
#endif
#endif
#if PASS_KIND == 5
    category = 3.0;
#endif
#if LATE_SURFACE == 1
    vec3 lateColour = diffuseRadiance(surface.rgb, lm, sky, orientedNormal, category, relativeLocation);
    lateColour = throughAir(lateColour, relativeLocation, sky);
    float mark = 0.0;
#if PASS_KIND == 6
    if (blockCategory == 4100 && orientedNormal.y > 0.5 && isEyeInWater == 0) {
        mark = 1.0;
        // Composite will replace this baseline when water is frontmost.
        surface.a = 0.40;
    }
#endif
    shim_FragData[0] = vec4(lateColour, surface.a);
    // With alpha zero for glass, these data targets preserve earlier water.
    shim_FragData[1] = vec4(lateColour, mark);
    vec3 n = unitVector(orientedNormal);
    float waterViewDepth = -(gbufferModelView * vec4(relativeLocation, 1.0)).z;
    shim_FragData[2] = vec4(n.x, n.z, waterViewDepth, mark);
#elif PASS_KIND == 9
    shim_FragData[0] = surface;
#else
    shim_FragData[0] = surface;
    shim_FragData[1] = vec4(unitVector(orientedNormal), category);
    shim_FragData[2] = vec4(lm, sky);
#endif
    // shim_FragData deliberately delegates per-draw alpha tests to Iris.
#endif
}

// END INCLUDE /core/raster.frag.glsl
