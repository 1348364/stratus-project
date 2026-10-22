#include "/core/options.glsl"
#include "/core/frame.glsl"
#include "/core/ceiling.glsl"
#include "/core/air.glsl"
#include "/core/medium.glsl"
#include "/core/trace.glsl"
uniform sampler2D colortex0;
uniform sampler2D colortex1;
uniform sampler2D colortex2;
uniform sampler2D colortex3;
uniform sampler2D depthtex0;
in vec2 rasterUV;
/* RENDERTARGETS: 3 */
layout(location = 0) out vec4 completedScene;
vec3 lakeNormal(vec3 point, vec3 faceNormal, float viewDistance) {
    vec3 n = unitVector(faceNormal);
    vec3 worldPoint = (point + cameraPosition) / RIPPLE_SIZE;
    vec3 gradient = vec3(0.0);
    float footprint = viewDistance / max(viewHeight * gbufferProjection[1][1], 1.0);
    for (int component = 0; component < 4; component++) {
        float index = float(component);
        float angle = 1.13 + index * 2.118;
        vec3 propagation = unitVector(vec3(cos(angle), 0.21 * sin(index + 1.0), sin(angle)));
        float frequency = 0.57 * pow(1.57, index);
        float phase = dot(worldPoint, propagation) * frequency + index * 1.71
                    - frameTimeCounter * RIPPLE_RATE * sqrt(frequency) * 0.93;
        float filterWeight = inversesqrt(1.0 + frequency * frequency * footprint * footprint * 8.0);
        gradient += propagation * (cos(phase) * frequency * 0.018 * pow(0.52, index) * filterWeight);
    }
    // One world-space field projected onto each actual face, including sides.
    gradient -= n * dot(gradient, n);
    return unitVector(n - gradient * RIPPLE_HEIGHT);
}
void main() {
    vec3 image = texture(colortex3, rasterUV).rgb;
    vec4 markedColour = texture(colortex0, rasterUV);
    vec4 markedNormal = texture(colortex1, rasterUV);
    vec4 markedDepth = texture(colortex2, rasterUV);
    float frontDepth = texture(depthtex0, rasterUV).r;
    vec3 nearestView = positionFromDepth(rasterUV, min(frontDepth, 0.999999));
    float cameraWaterPath = frontDepth < 0.999999 ? length(nearestView) : 64.0;
    float waterSky = 1.0;
    if (markedColour.a > 0.5 && markedNormal.a > 0.5 && markedDepth.a > 0.5) {
        vec3 viewRay = positionFromDepth(rasterUV, 0.5);
        vec3 waterView = viewRay * (markedDepth.x / max(-viewRay.z, 0.00001));
        waterSky = markedDepth.y;
        if (markedDepth.x > 0.0) {
            vec3 point = playerFromView(waterView);
            vec3 nWorld = lakeNormal(point, markedNormal.xyz, markedDepth.x);
            vec3 nView = unitVector(mat3(gbufferModelView) * nWorld);
            if (dot(nView, -waterView) < 0.0) { nView = -nView; nWorld = -nWorld; }
            vec3 reflectedRay = reflect(unitVector(waterView), nView);
            vec3 reflectedWorld = mat3(gbufferModelViewInverse) * reflectedRay;
            vec3 fallback = isEyeInWater == 1 ? waterBodyColour(waterSky) : overcastCeiling(reflectedWorld);
            if (isEyeInWater == 0) fallback *= mix(0.03, 1.0, smoothstep(0.04, 0.8, waterSky));
            vec4 traced = sceneryReflection(waterView + nView * 0.075, reflectedRay);
            vec3 reflected = mix(fallback, traced.rgb, traced.a);
            vec3 opaque = texture(colortex4, rasterUV).rgb;
            vec3 overlay = image - opaque;
            vec3 transmitted = opaque;
            if (isEyeInWater == 0) {
                float opaqueDepth = texture(depthtex1, rasterUV).r;
                float thickness = opaqueDepth < 0.999999
                    ? length(positionFromDepth(rasterUV, opaqueDepth) - waterView) : 24.0;
                // No second-interface buffer exists for a free-standing waterfall.
                // A bounded side thickness avoids treating distant air as water.
                float sideWeight = 1.0 - abs(markedNormal.y);
                thickness = mix(clamp(thickness, 0.0, 36.0), min(thickness, 1.8), sideWeight);
                transmitted = travelThroughWater(opaque, thickness, waterSky);
            } else {
                cameraWaterPath = length(waterView);
            }
            float cosine = clamp(dot(nView, unitVector(-waterView)), 0.0, 1.0);
            float fresnel = 0.025 + 0.975 * pow(1.0 - cosine, 5.0);
            if (isEyeInWater == 1) fresnel = max(fresnel, 1.0 - smoothstep(0.63, 0.69, cosine));
            float reflectionWeight = REFLECT_LEVEL * mix(0.08, 1.0, fresnel);
            image = mix(transmitted, reflected, reflectionWeight) + overlay;
        }
    }
    if (isEyeInWater == 1) image = travelThroughWater(image, cameraWaterPath, waterSky);
    completedScene = vec4(max(image, vec3(0.0)), 1.0);
}
