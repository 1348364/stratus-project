#ifndef WM_SKY
#define WM_SKY
// All returned colours are linear. The same sky function shades water misses.
vec3 wmHorizon() {
#ifdef WM_OVERWORLD
    vec3 day = wmLinear(vec3(0.70, 0.75, 0.81));
    vec3 night = wmLinear(vec3(0.115, 0.145, 0.20));
    return mix(night, day, wmDaylight()) * (1.0 - rainStrength * 0.10);
#else
    return wmLinear(fogColor);
#endif
}
vec3 wmSky(vec3 direction) {
#ifndef WM_OVERWORLD
    return wmLinear(fogColor);
#else
    vec3 ray = wmSafeNormal(direction);
    float day = wmDaylight();
    float horizon = 1.0 - smoothstep(0.015, 0.32, max(ray.y, 0.0));
    // A distant cloud sheet, anchored in world coordinates, with a soft horizon.
    float planeDistance = clamp((360.0 - cameraPosition.y) / max(ray.y, 0.12), 30.0, 2400.0);
    vec2 p = (cameraPosition.xz + ray.xz * planeDistance) / CLOUD_SCALE;
    p += vec2(frameTimeCounter * CLOUD_SPEED * 0.0009, frameTimeCounter * CLOUD_SPEED * 0.0003);
    vec2 warp = vec2(wmNoise(p * 0.43 + vec2(13.2, 4.7)),
                     wmNoise(p * 0.37 + vec2(-7.8, 22.0))) - 0.5;
    vec2 q = p + warp * CLOUD_IRREGULARITY * 1.65;
    float band = wmNoise(q * vec2(0.48, 2.65));
#if CLOUD_QUALITY >= 2
    band = band * 0.78 + wmNoise(q * vec2(0.83, 4.60) + vec2(21.7, 4.3)) * 0.22;
#endif
#if CLOUD_QUALITY >= 3
    band = band * 0.93 + wmNoise(q * vec2(1.2, 7.1) + vec2(9.8, -18.0)) * 0.07;
#endif
    // An unbroken, broad grey ceiling at default coverage; no small cumulus.
    float shade = (band - 0.5) * CLOUD_SHADING * 0.55;
    vec3 ceiling = vec3(0.565, 0.605, 0.675) + shade;
    vec3 clearSky = vec3(0.47, 0.59, 0.72);
    vec3 cloud = mix(clearSky, ceiling, CLOUD_COVERAGE);
    cloud = mix(vec3(0.075, 0.10, 0.15), cloud, day);
    cloud *= 1.0 - rainStrength * 0.13;
    return mix(wmLinear(cloud), wmHorizon(), horizon);
#endif
}
#endif
