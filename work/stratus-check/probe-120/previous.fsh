#version 330 core
#define DIMENSION_TYPE 0
#ifndef STRATUS_OPTIONS_INCLUDED
#define STRATUS_OPTIONS_INCLUDED
// Reference defaults; quality profiles only change sampling counts.
#define SKY_AMBIENT 1.40 // [0.80 1.00 1.20 1.40 1.60 1.80 2.00]
const float ambientOcclusionLevel = 1.00; // [0.00 0.15 0.30 0.45 0.60 0.80 1.00]
#define WHITE_BALANCE 0.00 // [-0.08 -0.04 0.00 0.04 0.08]
#define SURFACE_SATURATION 1.00 // [0.85 0.93 1.00 1.07 1.15]
#define SURFACE_DAMPNESS 1.00 // [0.00 0.35 0.65 1.00 1.35 1.70 2.00]
#define CLOUD_AMOUNT 1.00 // [0.00 0.35 0.60 0.75 0.90 1.00]
#define CLOUD_ALTITUDE 192.0 // [128.0 160.0 192.0 224.0 256.0 320.0]
#define CLOUD_THICKNESS 56.0 // [20.0 32.0 40.0 56.0 72.0]
#define SKY_LEAK 0.35 // [0.00 0.15 0.25 0.35 0.50 0.70]
#define CLOUD_SPAN 240.0 // [160.0 240.0 360.0 540.0 700.0 900.0]
#define CLOUD_DISTORTION 0.65 // [0.25 0.45 0.65 0.85 1.00]
#define CLOUD_RELIEF 0.55 // [0.25 0.40 0.55 0.70]
#define CLOUD_DRIFT 0.25 // [0.00 0.10 0.25 0.45 0.70]
#define CLOUD_LAYERS 2 // [1 2 3]
#define MIST_AMOUNT 0.75 // [0.00 0.40 0.60 0.75 1.00 1.25]
#define MIST_Y 70.0 // [48.0 64.0 70.0 88.0 112.0 144.0]
#define MIST_THICKNESS 12.0 // [7.0 9.0 12.0 16.0 22.0]
#define MIST_CLEAR 80.0 // [16.0 32.0 48.0 64.0 80.0 112.0 144.0]
#define MIST_DETAIL 2 // [1 2 3]
#define REFLECT_LEVEL 0.85 // [0.40 0.60 0.85 1.00]
#define REFLECTION_MODE 1 // [0 1 2]
#define REFLECT_RANGE 88.0 // [48.0 64.0 88.0 120.0]
#define WATER_VISIBILITY 4.00 //  [0.50 0.70 0.90 1.10 1.30 1.70 2.20 3.00 4.00]
#define WATER_EXTINCTION 0.90 // [0.45 0.65 0.90 1.15 1.40]
#define RIPPLE_HEIGHT 0.55 // [0.00 0.30 0.55 0.80 1.00]
#define RIPPLE_SIZE 1.00 // [0.65 0.80 1.00 1.25 1.50]
#define RIPPLE_RATE 0.45 // [0.00 0.20 0.45 0.70 1.00]
#define FACE_SHADING 0.00 //  [0.00 0.15 0.25 0.35 0.50 0.70 0.85 1.00]
#define WET_SHEEN 0.00 //  [0.00 0.35 0.65 0.85 1.00]
#define BLOOM_STRENGTH 0.06 // [0.00 0.03 0.06 0.09 0.12 0.18]
#define BLOOM_RADIUS 1.50 // [0.50 1.00 1.50 2.00 3.00]
#define SUN_VISIBILITY 0.00 //  [0.00 0.25 0.45 0.65 0.85 1.00]
#define LAMP_LEVEL 1.00 // [0.70 0.85 1.00 1.15 1.30]
#define LAMP_HEAT 0.25 // [0.00 0.15 0.25 0.40 0.60]
#endif

#ifndef STRATUS_FRAME_INCLUDED
#define STRATUS_FRAME_INCLUDED
uniform mat4 gbufferProjectionInverse;
uniform mat4 gbufferProjection;
uniform mat4 gbufferModelViewInverse;
uniform mat4 gbufferModelView;
uniform vec3 cameraPosition;
uniform vec3 sunPosition;
uniform float frameTimeCounter;
uniform int worldTime;
uniform float rainStrength;
uniform float viewWidth;
uniform float viewHeight;
uniform float far;
uniform vec3 fogColor;
uniform float fogStart;
uniform float fogEnd;
uniform float fogDensity;
uniform int fogMode;
uniform int fogShape;
uniform int isEyeInWater;
uniform float blindness;
uniform float darknessFactor;

vec3 unitVector(vec3 inputVector) {
    return inputVector * inversesqrt(max(dot(inputVector, inputVector), 1e-12));
}
vec3 decodeDisplay(vec3 displayValue) {
    vec3 lo = displayValue / 12.92;
    vec3 hi = pow(max((displayValue + 0.055) / 1.055, vec3(0.0)), vec3(2.4));
    return mix(hi, lo, lessThanEqual(displayValue, vec3(0.04045)));
}
vec3 encodeDisplay(vec3 linearValue) {
    linearValue = max(linearValue, vec3(0.0));
    vec3 lo = linearValue * 12.92;
    vec3 hi = 1.055 * pow(linearValue, vec3(1.0 / 2.4)) - 0.055;
    return mix(hi, lo, lessThanEqual(linearValue, vec3(0.0031308)));
}
float daytimeWeight() {
    float hour = mod(float(worldTime) + 24000.0, 24000.0);
    float dawn = smoothstep(22500.0, 23999.0, hour) + 1.0 - smoothstep(12000.0, 13700.0, hour);
    return clamp(dawn, 0.0, 1.0);
}
vec3 positionFromDepth(vec2 screen, float deviceDepth) {
    vec4 unprojected = gbufferProjectionInverse * vec4(screen * 2.0 - 1.0, deviceDepth * 2.0 - 1.0, 1.0);
    return unprojected.xyz / max(unprojected.w, 1e-7);
}
vec3 playerFromView(vec3 viewPoint) {
    return (gbufferModelViewInverse * vec4(viewPoint, 1.0)).xyz;
}
vec3 broadLightDirection() {
    vec3 direction = mat3(gbufferModelViewInverse) * sunPosition;
    if (dot(direction, direction) < 0.001) direction = vec3(-0.35, 0.85, 0.40);
    return unitVector(direction);
}
vec2 viewportSize() { return max(vec2(viewWidth, viewHeight), vec2(1.0)); }
#endif

#ifndef STRATUS_CEILING_INCLUDED
#define STRATUS_CEILING_INCLUDED

// BEGIN INCLUDE /core/field.glsl
#ifndef STRATUS_FIELD_INCLUDED
#define STRATUS_FIELD_INCLUDED
float latticeValue(ivec2 cell) {
    uint seed = uint(cell.x) * 1664525u + uint(cell.y) * 1013904223u;
    seed = (seed ^ (seed >> 16u)) * 2246822519u;
    seed ^= seed >> 13u;
    return float(seed & 0x00ffffffu) / 16777215.0;
}
float smoothField(vec2 location) {
    ivec2 cell = ivec2(floor(location));
    vec2 f = fract(location);
    // Quintic interpolation gives continuous first and second derivatives.
    vec2 t = f * f * f * (f * (f * 6.0 - 15.0) + 10.0);
    vec2 row = vec2(mix(latticeValue(cell), latticeValue(cell + ivec2(1, 0)), t.x),
                    mix(latticeValue(cell + ivec2(0, 1)), latticeValue(cell + ivec2(1, 1)), t.x));
    return mix(row.x, row.y, t.y);
}
float volumeLattice(ivec3 cell) {
    uint seed = uint(cell.x) * 1664525u + uint(cell.y) * 1013904223u + uint(cell.z) * 747796405u;
    seed = (seed ^ (seed >> 16u)) * 2246822519u;
    seed ^= seed >> 13u;
    return float(seed & 0x00ffffffu) / 16777215.0;
}
float smoothVolume(vec3 location) {
    ivec3 cell = ivec3(floor(location));
    vec3 f = fract(location);
    vec3 t = f * f * f * (f * (f * 6.0 - 15.0) + 10.0);
    vec4 row = vec4(mix(volumeLattice(cell), volumeLattice(cell + ivec3(1,0,0)), t.x),
                    mix(volumeLattice(cell + ivec3(0,1,0)), volumeLattice(cell + ivec3(1,1,0)), t.x),
                    mix(volumeLattice(cell + ivec3(0,0,1)), volumeLattice(cell + ivec3(1,0,1)), t.x),
                    mix(volumeLattice(cell + ivec3(0,1,1)), volumeLattice(cell + ivec3(1,1,1)), t.x));
    return mix(mix(row.x, row.y, t.y), mix(row.z, row.w, t.y), t.z);
}
#endif

// END INCLUDE /core/field.glsl

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

#ifndef STRATUS_DIFFUSE_INCLUDED
#define STRATUS_DIFFUSE_INCLUDED
// Approximate properties for ordinary textures without PBR maps.
// x: porosity, y: perceptual roughness. Stone and embedded ores share a class.
vec2 wetMaterialProperties(int material) {
    if (material == 4110) return vec2(0.90, 0.96);
    if (material == 4111) return vec2(0.64, 0.80);
    if (material == 4113) return vec2(0.18, 0.68);
    if (material == 4114) return vec2(0.04, 0.38);
    if (material == 4115) return vec2(0.80, 0.98);
    return vec2(0.58, 0.86);
}
float outdoorMoisture(float skyExposure, float kind) {
#if DIMENSION_TYPE == 0
    if (kind > 1.05 && kind < 2.5) {
        float outdoors = smoothstep(0.18, 0.88, skyExposure);
        return outdoors * (1.0 - exp(-1.75 * SURFACE_DAMPNESS)) * (1.0 + 0.08 * rainStrength);
    }
#endif
    return 0.0;
}
vec3 absorbedWetAlbedo(vec3 dryAlbedo, float moisture, float porosity) {
    // Pore filling changes the RGB absorption curve, preserving texture detail.
    // Brighter channels lose less light, giving a restrained saturation change.
    vec3 saturated = dryAlbedo / (vec3(1.0) + 1.55 * porosity * (vec3(1.0) - dryAlbedo));
    return mix(dryAlbedo, saturated, clamp(moisture, 0.0, 1.0));
}
vec3 formIrradiance(vec3 normal, float skyExposure) {
    // Broad sky/ground hemispheres plus a cosine-weighted soft sun contribution.
    // The result follows the normal continuously, without compass-side colours.
    float upperHemisphere = 0.5 + 0.5 * normal.y;
    vec3 sky = mix(vec3(0.31, 0.295, 0.275), vec3(0.98, 1.0, 1.025), upperHemisphere);
    float directional = max(dot(normal, broadLightDirection()), 0.0);
    sky += vec3(0.19, 0.176, 0.151) * directional * daytimeWeight() * (1.0 - 0.65 * rainStrength);
    sky /= 1.12;
    // The lightmap has no point-light positions: retain broad indoor fill.
    float indoor = 0.72 + 0.20 * max(normal.y, 0.0) - 0.12 * max(-normal.y, 0.0);
    vec3 irradiance = mix(vec3(indoor), sky, smoothstep(0.04, 0.85, skyExposure));
    return mix(vec3(1.0), irradiance, FACE_SHADING);
}
float waterFresnel(float cosine) {
    return 0.0204 + 0.9796 * pow(1.0 - clamp(cosine, 0.0, 1.0), 5.0);
}
float wetSunSpecular(vec3 n, vec3 v, vec3 l, float roughness) {
    float nv = max(dot(n, v), 0.001), nl = max(dot(n, l), 0.0);
    if (nl <= 0.0) return 0.0;
    vec3 h = unitVector(v + l);
    float nh = max(dot(n, h), 0.0), vh = max(dot(v, h), 0.0);
    float alpha = max(roughness * roughness, 0.08), a2 = alpha * alpha;
    float denominator = nh * nh * (a2 - 1.0) + 1.0;
    float distribution = a2 / max(3.14159265 * denominator * denominator, 0.00001);
    float visibility = 0.5 / max(nl * sqrt(nv * nv * (1.0 - a2) + a2)
                        + nv * sqrt(nl * nl * (1.0 - a2) + a2), 0.0001);
    return distribution * visibility * waterFresnel(vh) * nl;
}
vec3 diffuseRadiance(vec3 colour, vec3 mappedLight, float skyExposure, vec3 worldNormal,
                     float kind, vec3 playerPoint, int material) {
    if (kind < 0.5) return decodeDisplay(colour);
    vec3 normal = unitVector(worldNormal);
    if (dot(normal, normal) < 0.1) normal = vec3(0.0, 1.0, 0.0);
    float lampShare = 1.0 - smoothstep(0.08, 0.85, skyExposure) * daytimeWeight();
    vec3 light = decodeDisplay(mappedLight) * mix(LAMP_LEVEL, SKY_AMBIENT, skyExposure);
    light *= mix(vec3(1.0), vec3(1.015, 0.985, 0.87), LAMP_HEAT * lampShare);
    // Entities, held items and blocks get form lighting; billboard quads do not.
    vec3 form = kind > 0.95 ? formIrradiance(normal, skyExposure) : vec3(1.0);
    vec2 properties = wetMaterialProperties(material);
    float moisture = clamp(outdoorMoisture(skyExposure, kind), 0.0, 1.0);
    vec3 albedo = absorbedWetAlbedo(decodeDisplay(colour), moisture, properties.x);
    vec3 reflected = albedo * light * form;
    if (moisture > 0.001 && WET_SHEEN > 0.0) {
        vec3 view = unitVector(-playerPoint);
        float nv = max(dot(normal, view), 0.0);
        float roughness = mix(properties.y, max(0.28, properties.y * 0.48), moisture);
        // Vertical faces shed the film but retain damp absorption and sheening.
        float film = moisture * mix(0.32, 1.0, max(normal.y, 0.0)) * WET_SHEEN;
        vec3 ray = reflect(-view, normal);
        vec3 environment = mix(atmosphericColour(), skyBackdrop(ray), 0.35 * (1.0 - roughness));
        float exposure = skyExposure * mix(0.12, 1.0, smoothstep(-0.10, 0.45, ray.y));
        float fresnel = waterFresnel(nv) * (1.0 - 0.42 * roughness);
        float coat = clamp(film * fresnel, 0.0, 0.85);
        // Redirect diffuse energy into a sky film, rather than adding a flat glow.
        reflected = mix(reflected, environment * SKY_AMBIENT * exposure, coat);
        float specular = wetSunSpecular(normal, view, broadLightDirection(), roughness);
        float sun = daytimeWeight() * skyExposure * (1.0 - 0.75 * rainStrength);
        reflected += vec3(0.72, 0.64, 0.52) * specular * sun * film;
    }
    if (kind > 1.5 && kind < 2.5) {
        float interior = smoothstep(0.48, 0.94, max(colour.r, max(colour.g, colour.b)));
        reflected = max(reflected, decodeDisplay(colour) * interior * LAMP_LEVEL);
    }
    return reflected;
}
#endif

#ifndef STRATUS_MEDIUM_INCLUDED
#define STRATUS_MEDIUM_INCLUDED
vec3 waterExtinction() {
    return vec3(0.165, 0.061, 0.024) * WATER_EXTINCTION / max(WATER_VISIBILITY, 0.05);
}
vec3 waterBodyColour(float skyExposure) {
    float illumination = mix(0.06, 1.0, skyExposure * daytimeWeight());
    return vec3(0.022, 0.095, 0.185) * illumination;
}
vec3 travelThroughWater(vec3 radiance, float distanceInWater, float skyExposure) {
    vec3 transmission = exp(-waterExtinction() * max(distanceInWater, 0.0));
    return radiance * transmission + waterBodyColour(skyExposure) * (1.0 - transmission);
}
#endif


uniform float probeDistance;
layout(location=0) out vec4 result;
void main(){
int c=int(probeDistance+0.5);
if(c==0) result=vec4(absorbedWetAlbedo(vec3(0.08,0.25,0.60),outdoorMoisture(1.0,1.3),0.58),1.0);
if(c==1) result=vec4(vec3(outdoorMoisture(0.0,1.3)),1.0);
if(c==2) result=vec4(vec3(outdoorMoisture(1.0,1.0)),1.0);
if(c==3) result=vec4(absorbedWetAlbedo(vec3(0.08,0.25,0.60),outdoorMoisture(1.0,1.3),0.04),1.0);
if(c==4) result=vec4(diffuseRadiance(vec3(0.1),vec3(0.8),1.0,vec3(0,1,0),1.3,vec3(0,-0.15,-10),4112),1.0);
if(c==5) result=vec4(diffuseRadiance(vec3(0.1),vec3(0.8),1.0,vec3(0,1,0),1.3,vec3(0,-10,0),4112),1.0);
if(c==6) result=vec4(diffuseRadiance(vec3(0.65),vec3(0.8),1.0,vec3(0,1,0),1.0,vec3(0,0,-10),4112),1.0);
if(c==7) result=vec4(diffuseRadiance(vec3(0.65),vec3(0.8),1.0,vec3(1,0,0),1.0,vec3(0,0,-10),4112),1.0);
if(c==8) result=vec4(diffuseRadiance(vec3(0.65),vec3(0.8),1.0,vec3(0,-1,0),1.0,vec3(0,0,-10),4112),1.0);
if(c==9) result=vec4(diffuseRadiance(vec3(0.85),vec3(0),0.0,vec3(0,1,0),1.0,vec3(0,0,-10),4112),1.0);
if(c==10) result=vec4(diffuseRadiance(vec3(0.95),vec3(0),0.0,vec3(0,1,0),2.0,vec3(0,0,-10),4101),1.0);
if(c==11) result=vec4(abs(diffuseRadiance(vec3(0.5),vec3(0.8),1.0,vec3(0,1,0),0.8,vec3(0,0,-10),4112)-diffuseRadiance(vec3(0.5),vec3(0.8),1.0,vec3(1,0,0),0.8,vec3(0,0,-10),4112)),1.0);
if(c==12) result=vec4(abs(travelThroughWater(travelThroughWater(vec3(0.5),2,1),3,1)-travelThroughWater(vec3(0.5),5,1)),1.0);
if(c==13) result=vec4(travelThroughWater(vec3(0.5),20,1),1.0);
if(c==14) result=vec4(vec3(smoothVolume(vec3(1.2,0.3,4.5)),smoothVolume(vec3(1.2,0.9,4.5)),smoothVolume(vec3(1.2,1.6,4.5))),1.0);
if(c==15) result=vec4(vec3(physicalCloudLayer(vec3(200,140,200),normalize(vec3(0.2,1,0.1)),7000).a,physicalCloudLayer(vec3(200,192,200),vec3(1,0,0),7000).a,physicalCloudLayer(vec3(200,245,200),normalize(vec3(0.2,-1,0.1)),7000).a),1.0);
if(c==16) result=vec4(vec3(physicalCloudLayer(vec3(200,140,200),vec3(0,-1,0),7000).a,physicalCloudLayer(vec3(200,140,200),vec3(1,0,0),7000).a,physicalCloudLayer(vec3(200,140,200),vec3(0,1,0),10).a),1.0);
if(c==17) result=vec4(vec3(cloudSunTransmission(vec3(200,180,200)),cloudSunTransmission(vec3(200,205,200)),cloudSunTransmission(vec3(200,240,200))),1.0);
if(c==18) result=vec4(skyBackdrop(broadLightDirection()),1.0);
if(c==19) result=vec4(skyBackdrop(broadLightDirection()),1.0);
if(c==20) result=vec4(skyBackdrop(-broadLightDirection()),1.0);
}
