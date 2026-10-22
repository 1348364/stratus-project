#version 330 core
#define RGBA16F 34842
#define RGBA8 32856
layout(location = 0) out vec4 shim_FragData[8];

#define WM_OVERWORLD
#define WM_HIDE_SKY

// BEGIN INCLUDE /lib/geometry.fsh

// BEGIN INCLUDE /lib/settings.glsl
#ifndef WM_SETTINGS
#define WM_SETTINGS
// Shared artistic defaults. Presets change only sampling budgets.
#define AMBIENT_BRIGHTNESS 1.05 // [0.85 0.95 1.05 1.15 1.25]
const float ambientOcclusionLevel = 0.35; // [0.00 0.20 0.35 0.50 0.70]
#define COLOUR_TEMPERATURE 0.00 // [-0.10 -0.05 0.00 0.05 0.10]
#define SATURATION 0.98 // [0.85 0.92 0.98 1.05 1.12]
#define CLOUD_COVERAGE 1.00 // [0.70 0.85 1.00]
#define CLOUD_SCALE 600.0 // [350.0 450.0 600.0 800.0 1000.0]
#define CLOUD_IRREGULARITY 0.75 // [0.25 0.50 0.75 1.00]
#define CLOUD_SHADING 0.55 // [0.25 0.40 0.55 0.70]
#define CLOUD_SPEED 0.35 // [0.00 0.15 0.35 0.60 1.00]
#define CLOUD_QUALITY 3 //  [1 2 3]
#define FOG_DENSITY 0.85 // [0.00 0.45 0.65 0.85 1.10 1.35]
#define FOG_HEIGHT 72.0 // [48.0 64.0 72.0 88.0 104.0 128.0 160.0]
#define FOG_FALLOFF 28.0 // [16.0 22.0 28.0 40.0 56.0]
#define FOG_START 28.0 // [12.0 20.0 28.0 40.0 56.0]
#define FOG_QUALITY 3 //  [1 2 3]
#define WATER_REFLECTION 0.80 // [0.40 0.60 0.80 1.00]
#define REFLECTION_QUALITY 2 //  [0 1 2]
#define REFLECTION_DISTANCE 96.0 // [48.0 72.0 96.0 128.0]
#define WATER_TRANSPARENCY 0.90 // [0.60 0.75 0.90 1.00]
#define WATER_ABSORPTION 0.80 // [0.40 0.60 0.80 1.00 1.25]
#define RIPPLE_STRENGTH 0.55 // [0.00 0.30 0.55 0.80 1.00]
#define RIPPLE_SCALE 1.00 // [0.60 0.80 1.00 1.30 1.60]
#define RIPPLE_SPEED 0.50 // [0.00 0.25 0.50 0.75 1.00]
#define BLOCKLIGHT_BRIGHTNESS 1.00 // [0.70 0.85 1.00 1.15 1.30]
#define BLOCKLIGHT_WARMTH 0.35 // [0.00 0.20 0.35 0.50 0.70]
#endif

// END INCLUDE /lib/settings.glsl


// BEGIN INCLUDE /lib/uniforms.glsl
#ifndef WM_UNIFORMS
#define WM_UNIFORMS
uniform mat4 gbufferModelView;
uniform mat4 gbufferModelViewInverse;
uniform mat4 gbufferProjection;
uniform mat4 gbufferProjectionInverse;
uniform vec3 cameraPosition;
uniform vec3 fogColor;
uniform float fogStart;
uniform float fogEnd;
uniform float fogDensity;
uniform int fogMode;
uniform int fogShape;
uniform int isEyeInWater;
uniform int worldTime;
uniform float frameTimeCounter;
uniform float rainStrength;
uniform float blindness;
uniform float darknessFactor;
uniform float far;
uniform float viewWidth;
uniform float viewHeight;
#endif

// END INCLUDE /lib/uniforms.glsl


// BEGIN INCLUDE /lib/math.glsl
#ifndef WM_MATH
#define WM_MATH

// BEGIN INCLUDE /lib/uniforms.glsl
#ifndef WM_UNIFORMS
#define WM_UNIFORMS
uniform mat4 gbufferModelView;
uniform mat4 gbufferModelViewInverse;
uniform mat4 gbufferProjection;
uniform mat4 gbufferProjectionInverse;
uniform vec3 cameraPosition;
uniform vec3 fogColor;
uniform float fogStart;
uniform float fogEnd;
uniform float fogDensity;
uniform int fogMode;
uniform int fogShape;
uniform int isEyeInWater;
uniform int worldTime;
uniform float frameTimeCounter;
uniform float rainStrength;
uniform float blindness;
uniform float darknessFactor;
uniform float far;
uniform float viewWidth;
uniform float viewHeight;
#endif

// END INCLUDE /lib/uniforms.glsl

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

// END INCLUDE /lib/math.glsl


// BEGIN INCLUDE /lib/sky.glsl
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

// END INCLUDE /lib/sky.glsl


// BEGIN INCLUDE /lib/fog.glsl
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

// END INCLUDE /lib/fog.glsl

in vec4 vertexColor;
in vec3 playerPosition;
in vec3 surfaceNormal;
#ifdef WM_TEXTURED
uniform sampler2D gtexture;
in vec2 textureUV;
#endif
#ifdef WM_LIT
in vec2 lightUV;

// BEGIN INCLUDE /lib/lighting.glsl
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

// END INCLUDE /lib/lighting.glsl

#endif
#ifdef WM_ENTITY
uniform vec4 entityColor;
#endif
#ifdef WM_MATERIAL
flat in int materialID;
#endif
#ifdef WM_WATER

// BEGIN INCLUDE /lib/water.glsl
#ifndef WM_WATER_LIBRARY
#define WM_WATER_LIBRARY

// BEGIN INCLUDE /lib/reflection.glsl
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

// END INCLUDE /lib/reflection.glsl

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

// END INCLUDE /lib/water.glsl

#endif

#ifdef WM_MASK
/* RENDERTARGETS: 0,1 */
#else
/* RENDERTARGETS: 0 */
#endif
void main() {
#ifdef WM_HIDE_SKY
    // Sky is generated once in deferred, then reused as the reflection fallback.
    discard;
#else
    vec4 color = vertexColor;
#ifdef WM_TEXTURED
    color *= texture(gtexture, textureUV);
#endif
#ifdef WM_ENTITY
    color.rgb = mix(color.rgb, entityColor.rgb, entityColor.a);
#endif
    vec3 albedo = wmLinear(color.rgb);
    vec3 shaded = albedo;
    float skyLight = 1.0;
    float reflectable = 1.0;
#ifdef WM_LIT
    skyLight = wmLightLevels(lightUV).y;
    shaded *= wmLight(lightUV, surfaceNormal);
#endif
#ifdef WM_MATERIAL
    if (materialID == 1002 || materialID == 1003) {
        float bright = smoothstep(0.30, 0.85, max(color.r, max(color.g, color.b)));
        shaded = max(shaded, albedo * bright * BLOCKLIGHT_BRIGHTNESS);
        reflectable = 0.0;
    }
#endif
#ifdef WM_HAND
    reflectable = 0.0;
#endif
#ifdef WM_EMISSIVE
    reflectable = 0.0;
#endif
    bool waterSurface = false;
#ifdef WM_WATER
    if (materialID == 1001 && wmSafeNormal(surfaceNormal).y > 0.5 && isEyeInWater == 0) {
        vec2 uv = gl_FragCoord.xy / vec2(max(viewWidth, 1.0), max(viewHeight, 1.0));
        shaded = wmWater(albedo, playerPosition, surfaceNormal, skyLight, uv);
        // Depth absorption and opaque-scene transmission are already composed.
        color.a = 1.0;
        waterSurface = true;
    }
#endif
#ifdef WM_FOGGED
    if (!waterSurface) shaded = wmApplyFog(shaded, playerPosition, skyLight);
#endif
    // Legacy output preserves Iris's per-draw alpha tests, including entities.
    shim_FragData[0] = vec4(shaded, color.a);
#ifdef WM_MASK
    shim_FragData[1] = vec4(reflectable, skyLight, 0.0, 1.0);
#endif
#endif
}

// END INCLUDE /lib/geometry.fsh
