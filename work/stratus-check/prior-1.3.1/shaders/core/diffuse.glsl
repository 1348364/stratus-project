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
    // Continuous diffuse lighting is blended with vanilla's axis face weights.
    float upperHemisphere = 0.5 + 0.5 * normal.y;
    vec3 sky = mix(vec3(0.31, 0.295, 0.275), vec3(1.025, 1.0, 0.95), upperHemisphere);
    vec3 skyKey=unitVector(broadLightDirection()+vec3(-0.20,0.0,0.13));
    float directional = max(dot(normal, skyKey), 0.0);
    sky += sunlightColour() * 0.23 * directional * daytimeWeight() * (1.0 - 0.65 * rainStrength);
    sky /= 1.12;
    // The lightmap has no point-light positions: retain broad indoor fill.
    float indoor = 0.72 + 0.20 * max(normal.y, 0.0) - 0.12 * max(-normal.y, 0.0);
    vec3 irradiance = mix(vec3(indoor), sky, smoothstep(0.04, 0.85, skyExposure));
    float vertical=normal.y>=0.0?1.0:0.5;
    float vanilla=dot(normal*normal,vec3(0.6,vertical,0.8));
    irradiance*=mix(1.0,vanilla,FACE_BLEND);
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
#if DIMENSION_TYPE == 0
    if(kind>1.05&&kind<2.5){
        float warmth=GROUND_WARMTH*skyExposure*daytimeWeight()*mix(0.60,1.0,max(normal.y,0.0));
        reflected*=mix(vec3(1.0),vec3(1.17,1.035,0.82),warmth);
    }
#endif
    if (moisture > 0.001 && WET_SHEEN > 0.0) {
        vec3 view = unitVector(-playerPoint);
        float nv = max(dot(normal, view), 0.0);
        float roughness = mix(properties.y, max(0.28, properties.y * 0.48), moisture);
        // Vertical faces shed the film but retain damp absorption and sheening.
        float film = moisture * mix(0.32, 1.0, max(normal.y, 0.0)) * WET_SHEEN;
        vec3 ray = reflect(-view, normal);
        vec3 environment = softSkyReflection(ray);
        float exposure = skyExposure * mix(0.12, 1.0, smoothstep(-0.10, 0.45, ray.y));
        float fresnel = waterFresnel(nv) * (1.0 - 0.42 * roughness);
        float coat = clamp(film * fresnel, 0.0, 0.85);
        // Redirect diffuse energy into a sky film, rather than adding a flat glow.
        reflected = mix(reflected, environment * SKY_AMBIENT * exposure, coat);
        float specular = wetSunSpecular(normal, view, broadLightDirection(), roughness);
        float sun = daytimeWeight() * skyExposure * (1.0 - 0.75 * rainStrength);
        reflected += sunlightColour() * 0.72 * specular * sun * film;
    }
    if (kind > 1.5 && kind < 2.5) {
        float interior = smoothstep(0.48, 0.94, max(colour.r, max(colour.g, colour.b)));
        reflected = max(reflected, decodeDisplay(colour) * interior * LAMP_LEVEL * 2.1);
    }
    return reflected;
}
#endif
