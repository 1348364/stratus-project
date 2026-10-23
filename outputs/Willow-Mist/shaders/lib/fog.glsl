#ifndef WM_FOG
#define WM_FOG
float wmEnvironmentFog(vec3 p) {
    if (fogMode == 0) return 0.0;
    float d = fogShape == 1 ? max(length(p.xz), abs(p.y)) : length(p);
    if (fogMode == 2048) return clamp(1.0 - exp(-d * max(fogDensity, 0.0)), 0.0, 1.0);
    if (fogMode == 2049) {
        float x = d * max(fogDensity, 0.0);
        return clamp(1.0 - exp(-x * x), 0.0, 1.0);
    }
    return fogEnd > fogStart ? smoothstep(fogStart, fogEnd, d) : step(fogEnd, d);
}
float wmMistDensity(vec3 world) {
    float h = world.y - FOG_HEIGHT;
    float low = exp(-max(h, 0.0) / FOG_FALLOFF);
    float layerA = exp(-pow((h - 7.0) / 9.0, 2.0));
    float layerB = exp(-pow((h - 34.0) / 15.0, 2.0));
    float variation = mix(0.65, 1.30, wmNoise(world.xz * 0.006));
    return (0.0012 + 0.0034 * low + 0.0055 * layerA + 0.0030 * layerB) * variation;
}
float wmOutdoorFog(vec3 p, float skylight) {
#ifndef WM_OVERWORLD
    return 0.0;
#else
    if (isEyeInWater != 0) return 0.0;
    float d = length(p);
    // Per-surface skylight prevents the valley mist from whitening cave walls.
    float exposure = smoothstep(0.04, 0.55, skylight);
    float density = wmMistDensity(cameraPosition + p * 0.5);
#if FOG_QUALITY >= 2
    density = (wmMistDensity(cameraPosition + p * 0.22) + density
             + wmMistDensity(cameraPosition + p * 0.78)) / 3.0;
#endif
#if FOG_QUALITY >= 3
    density = (density * 3.0 + wmMistDensity(cameraPosition + p * 0.10)
             + wmMistDensity(cameraPosition + p * 0.90)) / 5.0;
#endif
    float mist = (1.0 - exp(-d * density * FOG_DENSITY))
               * smoothstep(FOG_START, FOG_START + 56.0, d) * exposure;
    // Render-distance fade is distinct from 1.21.11's environmental fog range.
    float edge = far > 1.0 ? smoothstep(far * 0.84, far, max(length(p.xz), abs(p.y))) : 0.0;
    return max(mist, edge * exposure);
#endif
}
vec3 wmApplyFog(vec3 color, vec3 p, float skylight) {
    float outdoors = wmOutdoorFog(p, skylight);
    vec3 result = mix(color, wmHorizon(), outdoors);
    float environment = wmEnvironmentFog(p);
    vec3 environmentColor = wmLinear(fogColor);
    if (isEyeInWater == 1) {
        // Submerged air mist is disabled; retain vanilla fluid/status fog.
        float waterFog = 1.0 - exp(-length(p) * 0.045 * WATER_ABSORPTION);
        result = mix(result, wmLinear(vec3(0.13, 0.29, 0.36)), waterFog);
    }
    result = mix(result, environmentColor, environment);
    // Preserve status visibility limits even though the sky is custom drawn.
    float status = clamp(max(blindness, darknessFactor), 0.0, 1.0);
    return result * (1.0 - status * smoothstep(1.5, 14.0, length(p)));
}
#endif
