#ifndef WM_REFLECTION
#define WM_REFLECTION
uniform sampler2D colortex3;
uniform sampler2D colortex1;
uniform sampler2D depthtex1;

vec2 wmProject(vec3 p) {
    vec4 clip = gbufferProjection * vec4(p, 1.0);
    return clip.xy / max(clip.w, 0.00001) * 0.5 + 0.5;
}
vec4 wmTraceReflection(vec3 origin, vec3 direction) {
#if REFLECTION_QUALITY == 0
    return vec4(0.0);
#else
#if REFLECTION_QUALITY == 2
    const int steps = 48;
    const int refine = 6;
#else
    const int steps = 24;
    const int refine = 4;
#endif
    float maximum = min(REFLECTION_DISTANCE, max(far, 16.0));
    float previousT = 0.08, previousDelta = -1.0;
    for (int i = 1; i <= steps; ++i) {
        float fraction = float(i) / float(steps);
        float t = 0.08 + pow(fraction, 1.65) * maximum;
        vec3 ray = origin + direction * t;
        if (ray.z > -0.10) break;
        vec2 uv = wmProject(ray);
        if (any(lessThanEqual(uv, vec2(0.002))) || any(greaterThanEqual(uv, vec2(0.998)))) break;
        float z = texture(depthtex1, uv).r;
        if (z >= 0.999999) { previousT = t; previousDelta = -1.0; continue; }
        vec3 scene = wmViewPosition(uv, z);
        float delta = scene.z - ray.z;
        if (delta >= 0.0 && previousDelta < 0.0) {
            float lo = previousT, hi = t;
            for (int j = 0; j < refine; ++j) {
                float mid = (lo + hi) * 0.5;
                vec3 candidate = origin + direction * mid;
                vec2 candidateUV = wmProject(candidate);
                float depth = texture(depthtex1, candidateUV).r;
                vec3 actual = wmViewPosition(candidateUV, depth);
                if (depth < 0.999999 && actual.z - candidate.z > 0.0) hi = mid;
                else lo = mid;
            }
            vec3 hit = origin + direction * hi;
            vec2 hitUV = wmProject(hit);
            float hitDepth = texture(depthtex1, hitUV).r;
            vec3 actual = wmViewPosition(hitUV, hitDepth);
            float thickness = 0.18 + abs(actual.z) * 0.018;
            float error = abs(actual.z - hit.z);
            float confidence = (1.0 - smoothstep(thickness * 0.45, thickness, error));
            confidence *= smoothstep(0.5, 1.5, -actual.z);
            vec2 edge = min(hitUV, vec2(1.0) - hitUV);
            confidence *= smoothstep(0.0, 0.09, min(edge.x, edge.y));
            confidence *= 1.0 - smoothstep(maximum * 0.72, maximum, hi);
            confidence *= step(hitDepth, 0.999998);
            // Emissive lanterns and the held item intentionally do not reflect.
            confidence *= texture(colortex1, hitUV).r;
            return vec4(texture(colortex3, hitUV).rgb, clamp(confidence, 0.0, 1.0));
        }
        previousT = t;
        previousDelta = delta;
    }
    return vec4(0.0);
#endif
}
#endif
