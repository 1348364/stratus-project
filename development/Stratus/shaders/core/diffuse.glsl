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
    if (material == 4114 || (material>=4120&&material<=4123)) return vec2(0.00, 0.38);
    if (material == 4115) return vec2(0.80, 0.98);
    if (material == 4116) return vec2(0.16, 0.48);
    if (material == 4117) return vec2(0.72, 0.91);
    return vec2(0.45, 0.86);
}
vec3 formIrradiance(vec3 normal, float skyExposure) {
    float vertical=normal.y>=0.0?1.0:0.5;
    float vanilla=dot(normal*normal,vec3(0.6,vertical,0.8));
    float vanillaWeight=1.0,physicalWeight=0.0;
    float physical=1.0;
#if DIMENSION_TYPE == 0
    vec3 sun=broadLightDirection();
    float direct=daytimeWeight()*smoothstep(-0.04,0.16,sun.y)*(1.0-0.85*rainStrength);
    float facing=max(dot(normal,sun),0.0);
    float hemisphere=mix(0.38,0.78,normal.y*0.5+0.5);
    physical=hemisphere*(1.0-0.20*direct)+0.44*direct*facing;
    float exposure=smoothstep(0.08,0.85,skyExposure);
    vanillaWeight=1.0-0.35*exposure;physicalWeight=0.35*exposure;
#endif
    // Separate linear components preserve the exact old mixture at 1/1.
    // Each zero removes only that component; both zero produce unshaded faces.
    float contrast=(vanilla-1.0)*vanillaWeight*VANILLA_FACE_CONTRAST
                  +(physical-1.0)*physicalWeight*REALISTIC_FACE_CONTRAST;
    float irradiance=1.0+contrast;
    float strength=FACE_BLEND*FACE_SHADING;
    // Linear contrast keeps saved 2.0 settings readable instead of squaring
    // already-dark surfaces. Zero for either control is an exact bypass.
    return vec3(clamp(1.0+(irradiance-1.0)*strength,0.18,1.18));
}
// A surface film adds reflected highlights without changing the diffuse albedo.
// Absorption darkening/retained dampness was deliberately retired in 1.6.9.
// Material.x remains in the buffer for saved-layout compatibility, not gating.
vec3 wetSurfaceResponse(vec3 dry,vec3 n,vec3 playerPoint,float sky,vec2 material){
#if DIMENSION_TYPE == 0
    float filmSource=WET_WEATHER_MODE==0?1.0:rainStrength;
    float film=filmSource*SURFACE_DAMPNESS*smoothstep(0.18,0.85,sky)
        *mix(0.78,1.0,clamp(n.y*0.5+0.5,0.0,1.0));
    if(WET_SHEEN>0.0&&film>0.0001){
        vec3 view=unitVector(-playerPoint);
        float nv=max(dot(n,view),0.0);
        if(nv>0.001){
            float fresnel=0.08+0.92*pow(1.0-nv,5.0);
            float coat=clamp(film*WET_SHEEN*fresnel*0.25,0.0,0.22);
            vec3 environment=softSkyReflection(reflect(-view,n));
            // Reflection can be lighter or darker than a white block. This is
            // angle-dependent film, never absorption or diffuse recolouring.
            dry=mix(dry,environment,coat);
            vec3 light=broadLightDirection(),halfway=unitVector(view+light);
            float exponent=mix(80.0,16.0,clamp(material.y,0.0,1.0));
            float lobe=pow(max(dot(n,halfway),0.0),exponent)*(exponent+2.0)/6.283185307;
            dry+=sunlightColour()*solarDaylight()*max(dot(n,light),0.0)
                *lobe*film*WET_SHEEN*0.008*(1.0-0.65*rainStrength);
        }
    }
#endif
    // Keep the retired option discoverable by Iris; every allowed value is a no-op.
    return dry+vec3(0.0)*WET_DARKENING;
}
vec3 diffuseRadiance(vec3 colour, vec3 mappedLight, float skyExposure, vec3 worldNormal,
                     float kind, vec3 playerPoint, int material) {
    if (kind < 0.5) return decodeDisplay(colour);
#if REALISTIC_LIGHTING == 0
    // oldLighting=true supplies Minecraft's original vertex face shading/AO.
    // Vanilla multiplies texture/vertex colour by the game's lightmap in display
    // space. Decode their product once, then bypass artistic grading at output.
    return decodeDisplay(colour*mappedLight);
#else
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
#endif
}
#endif
