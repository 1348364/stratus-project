#ifndef WM_MATH
#define WM_MATH
#include "/lib/uniforms.glsl"
const float WM_PI = 3.14159265359;
vec3 wmLinear(vec3 c) { return pow(max(c, vec3(0.0)), vec3(2.2)); }
vec3 wmDisplay(vec3 c) { return pow(max(c, vec3(0.0)), vec3(1.0 / 2.2)); }
float wmLuma(vec3 c) { return dot(c, vec3(0.2126, 0.7152, 0.0722)); }
vec3 wmSafeNormal(vec3 v) { return v / max(length(v), 0.00001); }
float wmHash(vec2 p) {
    // Polynomial hash avoids large-angle sine precision errors on mobile GPUs.
    vec3 q = fract(vec3(p.xyx) * vec3(0.1031, 0.1030, 0.0973));
    q += dot(q, q.yzx + 33.33);
    return fract((q.x + q.y) * q.z);
}
float wmNoise(vec2 p) {
    vec2 cell = floor(p), f = fract(p);
    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(mix(wmHash(cell), wmHash(cell + vec2(1.0, 0.0)), u.x),
        mix(wmHash(cell + vec2(0.0, 1.0)), wmHash(cell + vec2(1.0)), u.x), u.y);
}
float wmDaylight() {
    float elevation = cos((float(worldTime) - 6000.0) * (2.0 * WM_PI / 24000.0));
    return smoothstep(-0.16, 0.24, elevation);
}
vec3 wmViewPosition(vec2 uv, float depth) {
    vec4 p = gbufferProjectionInverse * vec4(uv * 2.0 - 1.0, depth * 2.0 - 1.0, 1.0);
    return p.xyz / max(p.w, 0.000001);
}
vec3 wmWorldDirection(vec3 viewDirection) {
    return wmSafeNormal(mat3(gbufferModelViewInverse) * viewDirection);
}
#endif
