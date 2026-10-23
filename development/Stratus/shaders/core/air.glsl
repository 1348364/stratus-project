#ifndef STRATUS_AIR_INCLUDED
#define STRATUS_AIR_INCLUDED
#include "/core/field.glsl"
// Closed-form integrals for a vertical mist profile. No volumetric ray march.
float approximateErf(float inputValue) {
    float x = abs(inputValue);
    float t = 1.0 / (1.0 + 0.3275911 * x);
    float polynomial = (((((1.061405429 * t - 1.453152027) * t)
                       + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t;
    return sign(inputValue) * (1.0 - polynomial * exp(-x * x));
}
float averageGaussian(float lowY, float highY, float centre, float sigma) {
    float a = (lowY - centre) / (1.41421356237 * sigma);
    float b = (highY - centre) / (1.41421356237 * sigma);
    if (abs(highY - lowY) < 0.02) return exp(-a * a);
    return max(0.0, sigma * 1.2533141373 * (approximateErf(b) - approximateErf(a)) / (highY - lowY));
}
float averageExponential(float lowY, float highY) {
    float a = clamp(lowY - MIST_Y, -60.0, 500.0);
    float b = clamp(highY - MIST_Y, -60.0, 500.0);
    float scale = MIST_THICKNESS * 2.7;
    if (abs(b - a) < 0.02) return exp(-a / scale);
    return max(0.0, (exp(-a / scale) - exp(-b / scale)) * scale / (b - a));
}
float backgroundMistWeight(float distanceAlongRay) {
    // A clear foreground and a gradual transition prevent a nearby grey veil.
    float blendDistance = max(32.0, MIST_CLEAR * 0.80);
    return smoothstep(MIST_CLEAR, MIST_CLEAR + blendDistance, distanceAlongRay);
}
float valleyOpacity(vec3 relativePoint, float skyExposure) {
#if DIMENSION_TYPE != 0
    return 0.0;
#else
    if (isEyeInWater != 0) return 0.0;
    float distanceAlongRay = length(relativePoint);
    float coveredLength = max(distanceAlongRay - MIST_CLEAR, 0.0);
    vec3 startWorld = cameraPosition + relativePoint * min(MIST_CLEAR / max(distanceAlongRay, 0.001), 1.0);
    vec3 finishWorld = cameraPosition + relativePoint;
    float density = 0.0011 * averageExponential(startWorld.y, finishWorld.y);
    density += 0.0068 * averageGaussian(startWorld.y, finishWorld.y, MIST_Y, MIST_THICKNESS);
    density += 0.0038 * averageGaussian(startWorld.y, finishWorld.y, MIST_Y + MIST_THICKNESS * 2.45, MIST_THICKNESS * 0.80);
    vec2 midpoint = (startWorld.xz + finishWorld.xz) * 0.0018;
    float patch = smoothField(midpoint);
#if MIST_DETAIL > 1
    patch = mix(patch, smoothField(midpoint * 1.71 + vec2(17.2, -9.8)), 0.25);
#endif
#if MIST_DETAIL > 2
    patch = mix(patch, smoothField(midpoint * 2.43 - vec2(11.3, 28.6)), 0.09);
#endif
    float opticalDepth = coveredLength * density * MIST_AMOUNT * mix(0.72, 1.24, patch)
                       * backgroundMistWeight(distanceAlongRay);
    float localMist = 1.0 - exp(-min(opticalDepth, 25.0));
    float edge = smoothstep(max(far * 0.86, 1.0), max(far, 2.0), max(length(relativePoint.xz), abs(relativePoint.y)));
    return (1.0 - (1.0 - localMist) * (1.0 - edge)) * smoothstep(0.06, 0.58, skyExposure);
#endif
}
float engineOpacity(vec3 relativePoint) {
    if (fogMode == 0) return 0.0;
    float distanceMetric = length(relativePoint);
    if (fogShape == 1) distanceMetric = max(length(relativePoint.xz), abs(relativePoint.y));
    if (fogMode == 2048) return 1.0 - exp(-distanceMetric * max(fogDensity, 0.0));
    if (fogMode == 2049) return 1.0 - exp(-pow(distanceMetric * max(fogDensity, 0.0), 2.0));
    if (fogEnd <= fogStart) return float(distanceMetric >= fogEnd);
    return smoothstep(fogStart, fogEnd, distanceMetric);
}
vec3 throughAir(vec3 radiance, vec3 relativePoint, float skyExposure) {
#if DIMENSION_TYPE == 0
    // Outdoor atmospheric transport is integrated once after water, at half res.
    if(isEyeInWater==0 && max(blindness,darknessFactor)<0.001)return radiance;
#endif
    float mist = 0.0;
    vec3 airResult = radiance * (1.0 - mist) + atmosphericColour() * mist;
    // Water attenuation is applied once in composite, to the actual camera-to-
    // interface distance. This keeps top, side and underwater paths consistent.
    if (isEyeInWater == 1) {
#if WATER_STYLE == 1
        // Native environmental fog already includes game status effects.
        return airResult;
#endif
        float waterStatus = clamp(max(blindness, darknessFactor), 0.0, 1.0);
        return airResult * (1.0 - waterStatus * smoothstep(2.0, 13.0, length(relativePoint)));
    }
    float engineFog = clamp(engineOpacity(relativePoint), 0.0, 1.0);
#if DIMENSION_TYPE == 0
    if (isEyeInWater == 0 && max(blindness, darknessFactor) < 0.001) {
        // Ordinary outdoor engine fog fills only opacity missing from our mist,
        // rather than applying a second full haze layer over the scene.
        engineFog *= backgroundMistWeight(length(relativePoint));
        engineFog = max(engineFog - mist, 0.0) / max(1.0 - mist, 0.0001);
    }
#endif
    airResult = mix(airResult, decodeDisplay(fogColor), engineFog);
    float status = clamp(max(blindness, darknessFactor), 0.0, 1.0);
    return airResult * (1.0 - status * smoothstep(2.0, 13.0, length(relativePoint)));
}
#endif
