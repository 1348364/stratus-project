#ifndef STRATUS_DIFFUSE_INCLUDED
#define STRATUS_DIFFUSE_INCLUDED
// Approximate properties for ordinary textures without PBR maps.
// x: water-absorption response, y: perceptual roughness. These are independent:
// rough metal/glazed ceramic still has zero pore absorption. Heuristic classes,
// not measured porosity. Stone and embedded ores share a class.
vec2 wetMaterialProperties(int material) {
    if (material == 4110) return vec2(0.90, 0.96);
    if (material == 4111) return vec2(0.64, 0.80);
    if (material == 4113) return vec2(0.02, 0.68);
    if (material == 4114) return vec2(0.00, 0.38);
    if (material == 4115) return vec2(0.80, 0.98);
    if (material == 4116) return vec2(0.16, 0.48);
    if (material == 4117) return vec2(0.72, 0.91);
    return vec2(0.45, 0.86);
}
float exposedWetFilm(float sky){
#if DIMENSION_TYPE == 0
    float outdoors=smoothstep(0.12,0.83,sky);
    float humidity=clamp(biomeHumidity,0.0,1.0);
    return clamp(SURFACE_DAMPNESS*outdoors*(0.40+0.30*humidity+0.25*rainStrength),0.0,1.0);
#else
    return 0.0;
#endif
}
float materialWetDarkening(float sky,float absorption){
    float saturation=exposedWetFilm(sky)*(0.45+0.55*clamp(biomeHumidity,0.0,1.0));
    return 1.0/(1.0+1.40*WET_DARKENING*saturation*clamp(absorption,0.0,1.0));
}
vec3 formIrradiance(vec3 normal, float skyExposure) {
    // Vanilla axis weights only. No second sky hemisphere or directional
    // diffuse term is stacked on top of the familiar block-face contrast.
    float vertical=normal.y>=0.0?1.0:0.5;
    float vanilla=dot(normal*normal,vec3(0.6,vertical,0.8));
    return vec3(pow(max(mix(1.0,vanilla,FACE_BLEND),0.02),FACE_SHADING));
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
vec3 wetSurfaceResponse(vec3 dry,vec3 n,vec3 playerPoint,float sky,vec2 material){
    // Absorbed water darkens porous substrates. A separate surface film covers
    // exposed faces of every material, including nonabsorbing metal/ceramic.
    float film=exposedWetFilm(sky);
    vec3 wet=dry*materialWetDarkening(sky,material.x);
    vec3 v=unitVector(-playerPoint);
    float roughness=mix(material.y,max(0.13,material.y*0.38),film);
    float sheen=film*WET_SHEEN;
    float coat=clamp(sheen*waterFresnel(max(dot(n,v),0.0))*(1.0-roughness*0.35),0.0,0.65);
    wet=mix(wet,softSkyReflection(reflect(-v,n))*sky*SKY_AMBIENT,coat);
    wet+=sunlightColour()*wetSunSpecular(n,v,broadLightDirection(),roughness)*sheen*sky*daytimeWeight()*0.65;
    return wet;
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
    // Material wetness is applied once by the opaque resolve (or late block pass).
    vec3 albedo = decodeDisplay(colour);
    vec3 reflected = albedo * light * form;
    if (kind > 1.5 && kind < 2.5) {
        float interior = smoothstep(0.48, 0.94, max(colour.r, max(colour.g, colour.b)));
        reflected = max(reflected, decodeDisplay(colour) * interior * LAMP_LEVEL * 2.1);
    }
    return reflected;
}
#endif
