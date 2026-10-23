#ifndef STRATUS_SUBMERGED_COMPOSE_INCLUDED
#define STRATUS_SUBMERGED_COMPOSE_INCLUDED
// A clear interface still needs an invisible depth boundary: only the
// camera-to-exit segment contains water, never the air beyond the surface.
float submergedWaterDistance(vec2 screen,float deviceDepth,vec4 exitData){
    bool receiver=deviceDepth<0.999999;
    float distance=receiver?length(positionFromDepth(screen,deviceDepth)):0.0;
    if(exitData.a>0.5&&exitData.x>0.0){
        vec3 ray=positionFromDepth(screen,0.5);
        float exitDistance=length(ray)*(exitData.x/max(-ray.z,0.00001));
        return receiver?min(distance,exitDistance):exitDistance;
    }
    // Preserve the open-sky view when no exit geometry was rasterized.
    return distance;
}
vec3 submergedDirectView(vec3 scene,vec3 opaque,float transmission,vec2 screen,
    float frontDepth,float opaqueDepth,vec4 exitData){
    float sky=clamp(float(eyeBrightnessSmooth.y)/240.0,0.0,1.0);
    float lamp=clamp(float(eyeBrightnessSmooth.x)/240.0,0.0,1.0);
    float backgroundPath=submergedWaterDistance(screen,opaqueDepth,exitData);
    float foregroundPath=submergedWaterDistance(screen,frontDepth,exitData);
#if WATER_STYLE == 1
    // Minecraft applies its linear fog to native display-space radiance.
    vec3 nativeOpaque=encodeDisplay(opaque),nativeScene=encodeDisplay(scene);
    vec3 bg=mix(nativeOpaque,fogColor,nativeWaterOpacity(backgroundPath));
    float t=1.0-nativeWaterOpacity(foregroundPath);
    if(transmission>=0.999)return decodeDisplay(bg+(nativeScene-nativeOpaque)*t);
    vec3 fg=forwardRadiance(nativeScene,nativeOpaque,transmission)*t;
    fg+=fogColor*(1.0-transmission)*(1.0-t);
    return decodeDisplay(compositeForward(bg,fg,transmission));
#else
    vec3 background=travelThroughWater(opaque,backgroundPath,biomeWaterTint,sky,lamp);
    vec3 attenuation=waterTransmission(foregroundPath,biomeWaterTint,sky);
    // Keep signed additive/crack corrections, while alpha-covered glass and
    // particles use their own foreground path and preserve background tint.
    if(transmission>=0.999)return background+(scene-opaque)*attenuation;
    vec3 foreground=forwardRadiance(scene,opaque,transmission)*attenuation;
    foreground+=waterBodyColour(biomeWaterTint,sky,lamp)*(1.0-transmission)*(1.0-attenuation);
    return compositeForward(background,foreground,transmission);
#endif
}
#endif
