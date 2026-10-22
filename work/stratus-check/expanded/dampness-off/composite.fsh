#version 330 core
#define DIMENSION_TYPE 0

// BEGIN INCLUDE /core/lake.frag.glsl

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


// BEGIN INCLUDE /core/trace.glsl
#ifndef STRATUS_TRACE_INCLUDED
#define STRATUS_TRACE_INCLUDED
uniform sampler2D depthtex1;
uniform sampler2D colortex4;

float screenDepthError(vec3 rayPoint, vec2 coordinate) {
    float sampledDepth = texture(depthtex1, coordinate).r;
    if (sampledDepth >= 0.999999) return -100000.0;
    return positionFromDepth(coordinate, sampledDepth).z - rayPoint.z;
}
vec4 sceneryReflection(vec3 viewOrigin, vec3 viewDirection) {
#if REFLECTION_MODE == 0
    return vec4(0.0);
#else
    float distanceLimit = min(REFLECT_RANGE, max(16.0, far));
    if (viewDirection.z > 0.00001)
        distanceLimit = min(distanceLimit, max(0.0, (-0.15 - viewOrigin.z) / viewDirection.z));
    if (distanceLimit < 0.1) return vec4(0.0);
    vec3 rayEnd = viewOrigin + viewDirection * distanceLimit;
    vec4 clipBegin = gbufferProjection * vec4(viewOrigin, 1.0);
    vec4 clipEnd = gbufferProjection * vec4(rayEnd, 1.0);
    float reciprocalBegin = 1.0 / max(clipBegin.w, 0.00001);
    float reciprocalEnd = 1.0 / max(clipEnd.w, 0.00001);
    vec2 screenBegin = clipBegin.xy * reciprocalBegin * 0.5 + 0.5;
    vec2 screenEnd = clipEnd.xy * reciprocalEnd * 0.5 + 0.5;
    vec3 projectiveBegin = viewOrigin * reciprocalBegin;
    vec3 projectiveEnd = rayEnd * reciprocalEnd;
#if REFLECTION_MODE == 2
    const int count = 46;
    const int bisections = 6;
#else
    const int count = 22;
    const int bisections = 5;
#endif
    float previousFraction = 0.0;
    float previousError = -1.0;
    for (int sampleIndex = 1; sampleIndex <= count; sampleIndex++) {
        float fraction = float(sampleIndex) / float(count);
        vec2 screen = mix(screenBegin, screenEnd, fraction);
        if (min(screen.x, screen.y) < 0.001 || max(screen.x, screen.y) > 0.999) break;
        float reciprocal = mix(reciprocalBegin, reciprocalEnd, fraction);
        vec3 rayPoint = mix(projectiveBegin, projectiveEnd, fraction) / reciprocal;
        float error = screenDepthError(rayPoint, screen);
        if (error >= 0.0 && previousError < 0.0) {
            float left = previousFraction, right = fraction;
            for (int refinement = 0; refinement < bisections; refinement++) {
                float middle = (left + right) * 0.5;
                vec2 middleScreen = mix(screenBegin, screenEnd, middle);
                vec3 middlePoint = mix(projectiveBegin, projectiveEnd, middle)
                                 / mix(reciprocalBegin, reciprocalEnd, middle);
                if (screenDepthError(middlePoint, middleScreen) >= 0.0) right = middle;
                else left = middle;
            }
            vec2 hitScreen = mix(screenBegin, screenEnd, right);
            vec3 hitPoint = mix(projectiveBegin, projectiveEnd, right)
                          / mix(reciprocalBegin, reciprocalEnd, right);
            float missDistance = abs(screenDepthError(hitPoint, hitScreen));
            float tolerance = 0.22 + abs(hitPoint.z) * 0.009;
            vec2 border = min(hitScreen, 1.0 - hitScreen);
            float confidence = 1.0 - smoothstep(tolerance * 0.35, tolerance, missDistance);
            confidence *= smoothstep(0.0, 0.075, min(border.x, border.y));
            confidence *= smoothstep(0.35, 1.4, -hitPoint.z);
            confidence *= 1.0 - smoothstep(distanceLimit * 0.67, distanceLimit, length(hitPoint - viewOrigin));
            vec4 centre = texture(colortex4, hitScreen);
            confidence *= centre.a;
            vec2 texel = vec2(0.85, 0.45) / viewportSize();
            vec3 softened = centre.rgb * 0.60
                          + texture(colortex4, hitScreen + texel).rgb * 0.20
                          + texture(colortex4, hitScreen - texel).rgb * 0.20;
            return vec4(softened, clamp(confidence, 0.0, 1.0));
        }
        previousFraction = fraction;
        previousError = error;
    }
    return vec4(0.0);
#endif
}
#endif

// END INCLUDE /core/trace.glsl

uniform sampler2D colortex0;
uniform sampler2D colortex1;
uniform sampler2D colortex2;
uniform sampler2D colortex3;
uniform sampler2D depthtex0;
in vec2 rasterUV;
/* RENDERTARGETS: 3 */
layout(location = 0) out vec4 completedScene;

vec3 lakeNormal(vec3 relativePoint, vec2 baseSlope, float viewDistance) {
    vec2 worldPlane = (relativePoint.xz + cameraPosition.xz) / RIPPLE_SIZE;
    vec2 gradient = vec2(0.0);
    float pixelFootprint = viewDistance / max(viewHeight * gbufferProjection[1][1], 1.0);
    for (int component = 0; component < 4; component++) {
        float index = float(component);
        float angle = 1.13 + index * 2.118;
        vec2 propagation = vec2(cos(angle), sin(angle));
        float frequency = 0.57 * pow(1.57, index);
        float amplitude = 0.018 * pow(0.52, index);
        float phase = dot(worldPlane, propagation) * frequency + index * 1.71
                    - frameTimeCounter * RIPPLE_RATE * sqrt(frequency) * 0.93;
        float filterWeight = inversesqrt(1.0 + frequency * frequency * pixelFootprint * pixelFootprint * 8.0);
        gradient += propagation * (cos(phase) * frequency * amplitude * filterWeight);
    }
    float up = sqrt(max(0.0, 1.0 - dot(baseSlope, baseSlope)));
    return unitVector(vec3(baseSlope.x - gradient.x * RIPPLE_HEIGHT, up,
                           baseSlope.y - gradient.y * RIPPLE_HEIGHT));
}
void main() {
    vec3 image = texture(colortex3, rasterUV).rgb;
    vec4 markedColour = texture(colortex0, rasterUV);
    vec4 markedGeometry = texture(colortex1, rasterUV);
    if (markedColour.a > 0.5 && markedGeometry.a > 0.5 && isEyeInWater == 0) {
        vec3 viewRay = positionFromDepth(rasterUV, 0.5);
        vec3 waterView = viewRay * (markedGeometry.z / max(-viewRay.z, 0.00001));
        float frontDepth = texture(depthtex0, rasterUV).r;
        float nearestDistance = -positionFromDepth(rasterUV, frontDepth).z;
        // Conservatively retain ordinary translucency when glass is in front.
        bool waterIsFrontmost = abs(nearestDistance - markedGeometry.z) < 0.16 + markedGeometry.z * 0.001;
        if (waterIsFrontmost && markedGeometry.z > 0.0) {
            vec3 playerPoint = playerFromView(waterView);
            vec3 nWorld = lakeNormal(playerPoint, markedGeometry.xy, markedGeometry.z);
            vec3 nView = unitVector(mat3(gbufferModelView) * nWorld);
            vec3 reflectedRay = reflect(unitVector(waterView), nView);
            vec3 reflectedWorld = mat3(gbufferModelViewInverse) * reflectedRay;
            float opaqueDepth = texture(depthtex1, rasterUV).r;
            float sky = texture(colortex2, rasterUV).a;
            if (opaqueDepth >= 0.999999) sky = 1.0;
            float waterLighting = clamp(max(markedColour.r, max(markedColour.g, markedColour.b)) / 0.16, 0.015, 1.0);
            vec3 fallback = overcastCeiling(vec3(reflectedWorld.x, abs(reflectedWorld.y) + 0.015, reflectedWorld.z));
            fallback *= mix(0.03, 1.0, smoothstep(0.04, 0.8, sky));
            vec4 traced = sceneryReflection(waterView + nView * 0.075, reflectedRay);
            traced.a *= smoothstep(-0.015, 0.06, reflectedWorld.y);
            vec3 reflected = mix(fallback, traced.rgb, traced.a);
            float waterColumn = 36.0;
            if (opaqueDepth < 0.999999)
                waterColumn = clamp(length(positionFromDepth(rasterUV, opaqueDepth) - waterView), 0.0, 36.0);
            vec3 extinction = vec3(0.165, 0.061, 0.024) * WATER_EXTINCTION / WATER_VISIBILITY;
            vec3 transmittance = exp(-waterColumn * extinction);
            vec3 deepColour = mix(vec3(0.022, 0.095, 0.185), markedColour.rgb, 0.22) * waterLighting;
            vec3 submerged = texture(colortex4, rasterUV).rgb;
            // Retain additive differences from later rain and particle layers.
            vec3 overlayDifference = image - mix(submerged, markedColour.rgb, 0.40);
            vec3 transmitted = submerged * transmittance + deepColour * (1.0 - transmittance);
            float grazing = 1.0 - clamp(dot(nView, unitVector(-waterView)), 0.0, 1.0);
            float fresnel = 0.025 + 0.975 * pow(grazing, 5.0);
            float reflectionWeight = REFLECT_LEVEL * (0.18 + 0.82 * fresnel);
            image = mix(transmitted, reflected, reflectionWeight);
            image = throughAir(image, playerPoint, sky) + overlayDifference;
        }
    }
    completedScene = vec4(max(image, vec3(0.0)), 1.0);
}

// END INCLUDE /core/lake.frag.glsl
