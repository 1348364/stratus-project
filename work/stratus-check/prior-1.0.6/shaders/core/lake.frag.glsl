#include "/core/options.glsl"
#include "/core/frame.glsl"
#include "/core/ceiling.glsl"
#include "/core/air.glsl"
#include "/core/trace.glsl"
uniform sampler2D colortex0;
uniform sampler2D colortex1;
uniform sampler2D colortex2;
uniform sampler2D colortex3;
uniform sampler2D depthtex0;
in vec2 rasterUV;
/* RENDERTARGETS: 3 */
layout(location = 0) out vec4 completedScene;

vec3 lakeNormal(vec3 relativePoint, vec2 baseSlope, float viewDistance) {
    vec2 worldPlane = (relativePoint.xz + cameraPosition.xz) / RIPPLE_SIZE;
    vec2 gradient = vec2(0.0);
    float pixelFootprint = viewDistance / max(viewHeight * gbufferProjection[1][1], 1.0);
    for (int component = 0; component < 4; component++) {
        float index = float(component);
        float angle = 1.13 + index * 2.118;
        vec2 propagation = vec2(cos(angle), sin(angle));
        float frequency = 0.57 * pow(1.57, index);
        float amplitude = 0.018 * pow(0.52, index);
        float phase = dot(worldPlane, propagation) * frequency + index * 1.71
                    - frameTimeCounter * RIPPLE_RATE * sqrt(frequency) * 0.93;
        float filterWeight = inversesqrt(1.0 + frequency * frequency * pixelFootprint * pixelFootprint * 8.0);
        gradient += propagation * (cos(phase) * frequency * amplitude * filterWeight);
    }
    float up = sqrt(max(0.0, 1.0 - dot(baseSlope, baseSlope)));
    return unitVector(vec3(baseSlope.x - gradient.x * RIPPLE_HEIGHT, up,
                           baseSlope.y - gradient.y * RIPPLE_HEIGHT));
}
void main() {
    vec3 image = texture(colortex3, rasterUV).rgb;
    vec4 markedColour = texture(colortex0, rasterUV);
    vec4 markedGeometry = texture(colortex1, rasterUV);
    if (markedColour.a > 0.5 && markedGeometry.a > 0.5 && isEyeInWater == 0) {
        vec3 viewRay = positionFromDepth(rasterUV, 0.5);
        vec3 waterView = viewRay * (markedGeometry.z / max(-viewRay.z, 0.00001));
        float frontDepth = texture(depthtex0, rasterUV).r;
        float nearestDistance = -positionFromDepth(rasterUV, frontDepth).z;
        // Conservatively retain ordinary translucency when glass is in front.
        bool waterIsFrontmost = abs(nearestDistance - markedGeometry.z) < 0.16 + markedGeometry.z * 0.001;
        if (waterIsFrontmost && markedGeometry.z > 0.0) {
            vec3 playerPoint = playerFromView(waterView);
            vec3 nWorld = lakeNormal(playerPoint, markedGeometry.xy, markedGeometry.z);
            vec3 nView = unitVector(mat3(gbufferModelView) * nWorld);
            vec3 reflectedRay = reflect(unitVector(waterView), nView);
            vec3 reflectedWorld = mat3(gbufferModelViewInverse) * reflectedRay;
            float opaqueDepth = texture(depthtex1, rasterUV).r;
            float sky = texture(colortex2, rasterUV).a;
            if (opaqueDepth >= 0.999999) sky = 1.0;
            float waterLighting = clamp(max(markedColour.r, max(markedColour.g, markedColour.b)) / 0.16, 0.015, 1.0);
            vec3 fallback = overcastCeiling(vec3(reflectedWorld.x, abs(reflectedWorld.y) + 0.015, reflectedWorld.z));
            fallback *= mix(0.03, 1.0, smoothstep(0.04, 0.8, sky));
            vec4 traced = sceneryReflection(waterView + nView * 0.075, reflectedRay);
            traced.a *= smoothstep(-0.015, 0.06, reflectedWorld.y);
            vec3 reflected = mix(fallback, traced.rgb, traced.a);
            float waterColumn = 36.0;
            if (opaqueDepth < 0.999999)
                waterColumn = clamp(length(positionFromDepth(rasterUV, opaqueDepth) - waterView), 0.0, 36.0);
            vec3 extinction = vec3(0.165, 0.061, 0.024) * WATER_EXTINCTION / WATER_VISIBILITY;
            vec3 transmittance = exp(-waterColumn * extinction);
            vec3 deepColour = mix(vec3(0.022, 0.095, 0.185), markedColour.rgb, 0.22) * waterLighting;
            vec3 submerged = texture(colortex4, rasterUV).rgb;
            // Retain additive differences from later rain and particle layers.
            vec3 overlayDifference = image - mix(submerged, markedColour.rgb, 0.40);
            vec3 transmitted = submerged * transmittance + deepColour * (1.0 - transmittance);
            float grazing = 1.0 - clamp(dot(nView, unitVector(-waterView)), 0.0, 1.0);
            float fresnel = 0.025 + 0.975 * pow(grazing, 5.0);
            float reflectionWeight = REFLECT_LEVEL * (0.18 + 0.82 * fresnel);
            image = mix(transmitted, reflected, reflectionWeight);
            image = throughAir(image, playerPoint, sky) + overlayDifference;
        }
    }
    completedScene = vec4(max(image, vec3(0.0)), 1.0);
}
