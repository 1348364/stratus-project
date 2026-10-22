#ifndef STRATUS_DIFFUSE_INCLUDED
#define STRATUS_DIFFUSE_INCLUDED
#include "/core/field.glsl"
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
