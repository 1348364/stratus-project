#ifndef WM_WATER_LIBRARY
#define WM_WATER_LIBRARY
#include "/lib/reflection.glsl"
vec3 wmWaterNormal(vec3 p, vec3 normal) {
    vec2 xz = (p.xz + cameraPosition.xz) * RIPPLE_SCALE;
    float t = frameTimeCounter * RIPPLE_SPEED;
    float a = dot(xz, vec2(0.81, 0.47)) + t * 1.25;
    float b = dot(xz, vec2(-0.63, 1.07)) - t * 0.91;
    float c = dot(xz, vec2(1.41, -0.79)) + t * 0.63;
    vec2 slopes = cos(a) * vec2(0.81, 0.47)
                + cos(b) * vec2(-0.63, 1.07) * 0.47
                + cos(c) * vec2(1.41, -0.79) * 0.21;
    // Only normals move. Shared block edges and the atlas remain unchanged.
    vec2 footprint = fwidth(xz);
    float attenuation = inversesqrt(1.0 + dot(footprint, footprint) * 0.8);
    return wmSafeNormal(normal + vec3(-slopes.x, 0.0, -slopes.y) * RIPPLE_STRENGTH * 0.045 * attenuation);
}
vec3 wmWater(vec3 albedo, vec3 player, vec3 baseNormal, float skyLight, vec2 uv) {
    vec3 viewPosition = (gbufferModelView * vec4(player, 1.0)).xyz;
    vec3 n = wmWaterNormal(player, wmSafeNormal(baseNormal));
    vec3 nView = wmSafeNormal(mat3(gbufferModelView) * n);
    vec3 reflectedView = wmSafeNormal(reflect(wmSafeNormal(viewPosition), nView));
    vec3 reflectedWorld = wmWorldDirection(reflectedView);
    // A sky fallback always exists, including when terrain exits the viewport.
    vec3 sky = wmSky(vec3(reflectedWorld.x, max(reflectedWorld.y, 0.025), reflectedWorld.z));
    sky *= mix(0.08, 1.0, smoothstep(0.05, 0.85, skyLight));
    vec4 terrain = wmTraceReflection(viewPosition + nView * 0.06, reflectedView);
    terrain.a *= smoothstep(-0.02, 0.08, reflectedWorld.y);
    vec3 reflection = mix(sky, terrain.rgb, terrain.a);

    float depth = texture(depthtex1, uv).r;
    vec3 behindView = wmViewPosition(uv, min(depth, 0.999998));
    float thickness = depth >= 0.999999 ? 32.0 : clamp(length(behindView - viewPosition), 0.0, 32.0);
    vec3 transmission = exp(-vec3(0.18, 0.065, 0.028) * thickness * WATER_ABSORPTION);
    transmission *= mix(0.40, 1.0, WATER_TRANSPARENCY);
    vec3 waterTint = mix(wmLinear(vec3(0.16, 0.34, 0.49)), albedo, 0.18);
    waterTint *= mix(0.08, 0.90, wmDaylight()) * mix(0.15, 1.0, skyLight);
    waterTint = wmApplyFog(waterTint, player, skyLight);
    vec3 behind = texture(colortex3, uv).rgb;
    vec3 through = behind * transmission + waterTint * (vec3(1.0) - transmission);
    float cosine = max(dot(n, wmSafeNormal(-player)), 0.0);
    float fresnel = 0.035 + 0.965 * pow(1.0 - cosine, 5.0);
    // The cloud ceiling produces a broad sheen, without sunlight sparkles.
    float reflectivity = WATER_REFLECTION * (0.20 + 0.80 * fresnel);
    reflection = wmApplyFog(reflection, player, skyLight);
    return mix(through, reflection, reflectivity);
}
#endif
