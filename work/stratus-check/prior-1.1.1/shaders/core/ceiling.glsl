#ifndef STRATUS_CEILING_INCLUDED
#define STRATUS_CEILING_INCLUDED
#include "/core/field.glsl"
vec3 atmosphericColour() {
#if DIMENSION_TYPE == 0
    return decodeDisplay(mix(vec3(0.10, 0.135, 0.185), vec3(0.715, 0.763, 0.813), daytimeWeight()) * (1.0 - 0.08 * rainStrength));
#else
    return decodeDisplay(fogColor);
#endif
}
vec3 skyBackdrop(vec3 worldRay) {
#if DIMENSION_TYPE != 0
    return decodeDisplay(fogColor);
#else
    vec3 ray = unitVector(worldRay);
    float horizon = exp(-abs(ray.y) * 5.0);
    vec3 zenith = decodeDisplay(mix(vec3(0.045, 0.072, 0.12), vec3(0.51, 0.63, 0.77), daytimeWeight()));
    vec3 sky = mix(zenith, atmosphericColour(), horizon);
    // Retain the reference sky's distant overcast bands above the finite layer.
    // This high ceiling supplies detail even through thin nearby cloud regions.
    vec2 sheet = (ray.xz / max(ray.y + 0.16, 0.20) * 450.0 + cameraPosition.xz) / (CLOUD_SPAN * 1.8);
    sheet += frameTimeCounter * CLOUD_DRIFT * vec2(0.0013, -0.0006);
    float bend = smoothField(sheet * 0.37 + vec2(8.1, -19.4));
    float phase = sheet.y * 5.4 + CLOUD_DISTORTION * ((bend - 0.5) * 5.0 + sin(sheet.x * 1.1) * 0.9);
    float shape = mix(0.5 + 0.5 * sin(phase), smoothField(sheet * vec2(0.62, 2.75) + vec2(-4.3, 7.2)), 0.52);
    float relief = (shape - 0.5) * CLOUD_RELIEF;
    vec3 upper = vec3(0.61, 0.66, 0.73) + relief * vec3(0.38, 0.36, 0.33);
    upper = mix(vec3(0.068, 0.095, 0.145), upper, daytimeWeight());
    upper *= 1.0 - 0.14 * rainStrength;
    float highCloud = CLOUD_AMOUNT * smoothstep(-0.02, 0.20, ray.y);
    sky = mix(sky, decodeDisplay(upper), highCloud * (1.0 - exp(-max(ray.y, 0.0) * 8.5)));
    float alignment = pow(max(dot(ray, broadLightDirection()), 0.0), 7.0);
    // Broad warm light through thinner cloud bands, with no hard sun disc.
    sky += vec3(0.24, 0.19, 0.12) * alignment * SKY_LEAK * daytimeWeight() * (0.45 + 0.55 * (1.0 - shape));
    return sky;
#endif
}
vec2 cloudSample(vec3 worldPoint) {
    vec2 sheet = worldPoint.xz / CLOUD_SPAN;
    sheet += frameTimeCounter * CLOUD_DRIFT * vec2(0.0013, -0.0006);
    float bend = smoothField(sheet * 0.47 + vec2(8.1, -19.4));
    float phase = sheet.y * 5.4 + CLOUD_DISTORTION * ((bend - 0.5) * 4.0 + sin(sheet.x * 1.1) * 0.8);
    float shape = mix(0.5 + 0.5 * sin(phase), smoothField(sheet * vec2(0.85, 2.75)), 0.55);
#if CLOUD_LAYERS > 1
    shape = mix(shape, smoothField(sheet * vec2(1.4, 4.15) + vec2(16.4, 12.9)), 0.16);
#endif
#if CLOUD_LAYERS > 2
    shape = mix(shape, smoothField(sheet * vec2(2.1, 6.3) - vec2(25.2, 1.7)), 0.07);
#endif
    float centre = CLOUD_ALTITUDE + (shape - 0.5) * CLOUD_THICKNESS * 0.35;
    float height = (worldPoint.y - centre) / CLOUD_THICKNESS + 0.5;
    float edge = smoothstep(0.0, 0.23, height) * (1.0 - smoothstep(0.68, 1.0, height));
    float coverage = CLOUD_AMOUNT * (0.25 + 0.75 * smoothstep(0.10, 0.72, shape));
    return vec2(edge * coverage * (0.020 + shape * 0.045), shape);
}
vec4 physicalCloudLayer(vec3 origin, vec3 worldRay, float maximumDistance) {
#if DIMENSION_TYPE != 0
    return vec4(0.0);
#else
    if (CLOUD_AMOUNT <= 0.0) return vec4(0.0);
    vec3 ray = unitVector(worldRay);
    float bottom = CLOUD_ALTITUDE - CLOUD_THICKNESS * 0.70;
    float top = CLOUD_ALTITUDE + CLOUD_THICKNESS * 0.70;
    float start = 0.0;
    float finish = min(maximumDistance, 7000.0);
    if (abs(ray.y) < 0.0001) {
        if (origin.y < bottom || origin.y > top) return vec4(0.0);
        finish = min(finish, 1200.0);
    } else {
        float a = (bottom - origin.y) / ray.y;
        float b = (top - origin.y) / ray.y;
        start = max(min(a,b), 0.0);
        finish = min(finish, max(a,b));
    }
    if (finish <= start) return vec4(0.0);
    const int steps = 6 + CLOUD_LAYERS * 4;
    float stride = (finish - start) / float(steps);
    float transmission = 1.0;
    vec3 scattered = vec3(0.0);
    float opening = pow(max(dot(ray, broadLightDirection()), 0.0), 6.0);
    for (int sampleIndex = 0; sampleIndex < steps; sampleIndex++) {
        vec3 point = origin + ray * (start + (float(sampleIndex) + 0.5) * stride);
        vec2 sampleData = cloudSample(point);
        float density = sampleData.x;
        float opacity = 1.0 - exp(-density * stride);
        float height = clamp((point.y - CLOUD_ALTITUDE) / CLOUD_THICKNESS + 0.5, 0.0, 1.0);
        float relief = mix(0.78, 1.13, height) * (0.98 - CLOUD_RELIEF * sampleData.y * 0.65);
        vec3 daylight = decodeDisplay(vec3(0.79, 0.81, 0.85)) * relief;
        daylight += vec3(0.22, 0.17, 0.10) * opening * SKY_LEAK * (1.0 - clamp(density * 10.0, 0.0, 0.8));
        vec3 colour = mix(vec3(0.006, 0.010, 0.019), daylight, daytimeWeight());
        colour *= 1.0 - 0.15 * rainStrength;
        scattered += transmission * opacity * colour;
        transmission *= 1.0 - opacity;
        if (transmission < 0.015) break;
    }
    float horizonFade = origin.y < bottom || origin.y > top ? smoothstep(0.0, 0.045, abs(ray.y)) : 1.0;
    return vec4(scattered / max(1.0 - transmission, 0.0001), (1.0 - transmission) * horizonFade);
#endif
}
vec3 overcastCeiling(vec3 worldRay) {
    vec3 sky = skyBackdrop(worldRay);
    vec4 cloud = physicalCloudLayer(cameraPosition, worldRay, 7000.0);
    return mix(sky, cloud.rgb, cloud.a);
}
#endif
