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
    if (kind > 1.05 && kind < 2.5) {
        // Vanilla-style orientation weights, fixed in world space.
        // Squared components blend smoothly across non-axis-aligned models.
        float verticalShade = normal.y >= 0.0 ? 1.0 : 0.5;
        float shape = dot(normal * normal, vec3(0.6, verticalShade, 0.8));
        faceVisibility = mix(1.0, shape, FACE_SHADING);
    }
    float lampShare = 1.0 - smoothstep(0.08, 0.85, skyExposure) * daytimeWeight();
    vec3 light = decodeDisplay(mappedLight) * mix(LAMP_LEVEL, SKY_AMBIENT, skyExposure);
    light *= mix(vec3(1.0), vec3(1.015, 0.985, 0.87), LAMP_HEAT * lampShare);
    // Apply before display-to-linear conversion, as vanilla vertex shading does.
    // oldLighting stays disabled so the game does not apply this a second time.
    vec3 albedo = dampDiffuseColour(decodeDisplay(colour * faceVisibility), skyExposure, normal, kind, playerPoint);
    vec3 reflected = albedo * light;
    if (kind > 1.5 && kind < 2.5) {
        float interior = smoothstep(0.48, 0.94, max(colour.r, max(colour.g, colour.b)));
        reflected = max(reflected, decodeDisplay(colour) * interior * LAMP_LEVEL);
    }
    return reflected;
}
#endif
