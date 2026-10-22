#ifndef STRATUS_CEILING_INCLUDED
#define STRATUS_CEILING_INCLUDED
#include "/core/field.glsl"

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
