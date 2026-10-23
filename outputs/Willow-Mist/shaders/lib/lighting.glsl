#ifndef WM_LIGHTING
#define WM_LIGHTING
uniform sampler2D lightmap;
vec2 wmLightLevels(vec2 uv) { return clamp((uv - vec2(0.03125)) / 0.9375, 0.0, 1.0); }
vec3 wmLight(vec2 uv, vec3 normal) {
    vec2 levels = wmLightLevels(uv);
    vec3 light = wmLinear(texture(lightmap, uv).rgb);
    float block = smoothstep(0.15, 1.0, levels.x) * (1.0 - levels.y * wmDaylight() * 0.70);
    // Vanilla light levels (including darkness/night vision) remain authoritative.
    light *= mix(1.0, AMBIENT_BRIGHTNESS, levels.y);
    light *= mix(1.0, BLOCKLIGHT_BRIGHTNESS, block);
    light *= mix(vec3(1.0), vec3(1.04, 0.96, 0.82), block * BLOCKLIGHT_WARMTH);
    // Gentle vanilla-style face orientation shading. No shadow map or sun ray.
    vec3 n = wmSafeNormal(normal);
    float face = 0.88 + 0.12 * max(n.y, 0.0) - 0.14 * max(-n.y, 0.0);
    face -= 0.035 * abs(n.x);
    return light * face;
}
#endif
