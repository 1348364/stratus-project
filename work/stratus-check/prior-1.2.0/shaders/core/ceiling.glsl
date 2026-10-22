#ifndef STRATUS_CEILING_INCLUDED
#define STRATUS_CEILING_INCLUDED
#include "/core/field.glsl"
vec3 atmosphericColour() {
#if DIMENSION_TYPE == 0
    vec3 day = decodeDisplay(vec3(0.66, 0.71, 0.78));
    vec3 night = decodeDisplay(vec3(0.06, 0.085, 0.14));
    return mix(night, day, daytimeWeight()) * (1.0 - 0.12 * rainStrength);
#else
    return decodeDisplay(fogColor);
#endif
}
float solarDaylight() {
    return daytimeWeight() * smoothstep(-0.06, 0.10, broadLightDirection().y);
}
vec3 skyBackdrop(vec3 worldRay) {
#if DIMENSION_TYPE != 0
    return decodeDisplay(fogColor);
#else
    vec3 ray = unitVector(worldRay);
    // Below the horizon, match distant terrain fog instead of showing blue zenith.
    float horizon = exp(-max(ray.y, 0.0) * 5.0);
    vec3 zenith = decodeDisplay(mix(vec3(0.045,0.072,0.12), vec3(0.51,0.63,0.77), daytimeWeight()));
    vec3 sky = mix(zenith, atmosphericColour(), horizon);
    // A distant soft stratus sheet retains overcast coverage between 3D forms.
    vec2 sheet = (ray.xz / max(ray.y + 0.16, 0.20) * 450.0 + cameraPosition.xz) / (CLOUD_SPAN * 1.8);
    sheet += frameTimeCounter * CLOUD_DRIFT * vec2(0.0013, -0.0006);
    float bend = smoothField(sheet * 0.37 + vec2(8.1,-19.4));
    float shape = mix(smoothField(sheet * vec2(0.8,2.4)), smoothField(sheet * 1.7 + bend * CLOUD_DISTORTION), 0.3);
    vec3 upper = vec3(0.62,0.67,0.74) + (shape - 0.5) * CLOUD_RELIEF * vec3(0.24,0.22,0.20);
    upper = mix(vec3(0.068,0.095,0.145), upper, daytimeWeight()) * (1.0 - 0.14 * rainStrength);
    float sheetOpacity = CLOUD_AMOUNT * 0.70 * smoothstep(-0.02,0.22,ray.y);
    sky = mix(sky, decodeDisplay(upper), sheetOpacity);
    float mu = clamp(dot(ray, broadLightDirection()), -1.0, 1.0);
    float separation = max(1.0 - mu, 0.0);
    float broadGlow = exp(-separation / 0.075) * SKY_LEAK;
    // Haze-softened solar core and aureole; still occluded by the cloud volume.
    float core = exp(-separation / 0.00022) * 2.6;
    float aureole = exp(-separation / 0.006) * 0.55;
    float visibility = SUN_VISIBILITY * (1.0 - 0.65 * rainStrength);
    sky += vec3(1.0,0.86,0.64) * solarDaylight()
         * (broadGlow * 0.25 + (core + aureole) * visibility);
    return sky;
#endif
}
vec2 cloudVolumeSample(vec3 worldPoint, bool detailed) {
    vec2 wind = frameTimeCounter * CLOUD_DRIFT * vec2(0.31,-0.14);
    vec2 weatherPoint = (worldPoint.xz + wind) / CLOUD_SPAN;
    float weather = smoothField(weatherPoint * vec2(0.72,1.40) + vec2(8.1,-19.4));
    float centre = CLOUD_ALTITUDE + (weather - 0.5) * CLOUD_THICKNESS * CLOUD_DISTORTION * 0.45;
    float height = (worldPoint.y - centre) / CLOUD_THICKNESS + 0.5;
    float profile = smoothstep(0.0,0.22,height) * (1.0 - smoothstep(0.65,1.0,height));
    if (profile <= 0.0 || CLOUD_AMOUNT <= 0.0) return vec2(0.0);
    float scale = max(CLOUD_SPAN * 0.30, 24.0);
    vec3 p = vec3((worldPoint.x + wind.x) / scale,
                  (worldPoint.y - CLOUD_ALTITUDE) / max(CLOUD_THICKNESS * 0.65, 1.0),
                  (worldPoint.z + wind.y) / scale);
    p.x += (weather - 0.5) * CLOUD_DISTORTION;
    float body = smoothVolume(p);
#if CLOUD_LAYERS > 1
    if (detailed) body = mix(body, smoothVolume(p * 2.07 + vec3(7.2,2.3,-8.1)), 0.24);
#endif
#if CLOUD_LAYERS > 2
    if (detailed) body -= (1.0 - smoothVolume(p * 4.13 - vec3(4.7,8.2,2.1))) * 0.065;
#endif
    float threshold = mix(0.72, 0.46, CLOUD_AMOUNT);
    float bulk = smoothstep(threshold - 0.16, threshold + 0.20, body + (weather - 0.5) * 0.22);
    float density = profile * bulk * (0.035 + 0.036 * weather) * CLOUD_AMOUNT;
    return vec2(density, height);
}
vec2 cloudSample(vec3 worldPoint) { return cloudVolumeSample(worldPoint, true); }
float cloudSunTransmission(vec3 point) {
    vec3 light = broadLightDirection();
    float span = CLOUD_THICKNESS;
    float opticalDepth = cloudVolumeSample(point + light * span * 0.22, false).x * span * 0.35;
#if CLOUD_LAYERS > 1
    opticalDepth += cloudVolumeSample(point + light * span * 0.65, false).x * span * 0.65;
#endif
    return exp(-opticalDepth);
}
vec4 marchCloudLayer(vec3 origin, vec3 worldRay, float maximumDistance, int steps, bool lightMarch) {
#if DIMENSION_TYPE != 0
    return vec4(0.0);
#else
    if (CLOUD_AMOUNT <= 0.0) return vec4(0.0);
    vec3 ray = unitVector(worldRay);
    float bottom = CLOUD_ALTITUDE - CLOUD_THICKNESS * 0.75;
    float top = CLOUD_ALTITUDE + CLOUD_THICKNESS * 0.75;
    float start = 0.0, finish = min(maximumDistance, 7000.0);
    if (abs(ray.y) < 0.0001) {
        if (origin.y < bottom || origin.y > top) return vec4(0.0);
        finish = min(finish, 450.0);
    } else {
        float a = (bottom - origin.y) / ray.y, b = (top - origin.y) / ray.y;
        start = max(min(a,b), 0.0); finish = min(finish, max(a,b));
    }
    if (finish <= start) return vec4(0.0);
    float stride = min((finish - start) / float(steps), CLOUD_THICKNESS * 0.70);
    float transmission = 1.0;
    vec3 scattered = vec3(0.0);
    float mu = dot(ray, broadLightDirection());
    // Forward-biased single scattering plus an ambient multiple-scattering floor.
    float phase = 0.75 / pow(max(1.25 - mu, 0.05), 1.5);
    for (int i = 0; i < steps; i++) {
        vec3 point = origin + ray * (start + (float(i) + 0.5) * stride);
        vec2 sampleData = cloudVolumeSample(point, lightMarch);
        if (sampleData.x <= 0.00001) continue;
        float opacity = 1.0 - exp(-sampleData.x * stride);
        float sunlight = lightMarch ? cloudSunTransmission(point) : mix(0.30,1.0,clamp(sampleData.y,0.0,1.0));
        float height = clamp(sampleData.y, 0.0, 1.0);
        float ambient = mix(0.50,1.0,height);
        vec3 daylight = vec3(0.38,0.42,0.49) * ambient;
        daylight += vec3(0.56,0.51,0.43) * sunlight * (0.58 + phase * 0.10 * SUN_VISIBILITY);
        daylight *= mix(1.0, 0.72 + 0.28 * sunlight, CLOUD_RELIEF);
        daylight += vec3(0.10,0.083,0.058) * phase * SKY_LEAK * sunlight;
        vec3 colour = mix(vec3(0.006,0.010,0.019) * ambient, daylight, daytimeWeight());
        colour *= 1.0 - 0.17 * rainStrength;
        scattered += transmission * opacity * colour;
        transmission *= 1.0 - opacity;
        if (transmission < 0.015) break;
    }
    float fade = origin.y < bottom || origin.y > top ? smoothstep(0.0,0.035,abs(ray.y)) : 1.0;
    vec3 cloudColour = scattered / max(1.0 - transmission,0.0001);
    float distantHaze = 1.0 - exp(-max(start - 80.0, 0.0) * 0.0004);
    cloudColour = mix(cloudColour, atmosphericColour(), distantHaze);
    return vec4(cloudColour, (1.0 - transmission) * fade);
#endif
}
vec4 physicalCloudLayer(vec3 origin, vec3 worldRay, float maximumDistance) {
    return marchCloudLayer(origin, worldRay, maximumDistance, 8 + CLOUD_LAYERS * 4, true);
}
vec3 overcastCeiling(vec3 worldRay) {
    vec3 sky = skyBackdrop(worldRay);
    // Lower-frequency integration is sufficient for rippled water reflections.
    vec4 cloud = marchCloudLayer(cameraPosition, worldRay, 7000.0, 6, false);
    return mix(sky, cloud.rgb, cloud.a);
}
#endif
