#ifndef STRATUS_MEDIUM_INCLUDED
#define STRATUS_MEDIUM_INCLUDED
vec3 waterExtinction() {
    return vec3(0.205, 0.081, 0.035) * WATER_EXTINCTION / max(WATER_VISIBILITY, 0.05);
}
vec3 waterBodyColour(float skyExposure) {
    float illumination = mix(0.06, 1.0, skyExposure * daytimeWeight());
    return vec3(0.035, 0.125, 0.180) * illumination;
}
vec3 travelThroughWater(vec3 radiance, float distanceInWater, float skyExposure) {
    vec3 transmission = exp(-waterExtinction() * max(distanceInWater, 0.0));
    return radiance * transmission + waterBodyColour(skyExposure) * (1.0 - transmission);
}
#endif
