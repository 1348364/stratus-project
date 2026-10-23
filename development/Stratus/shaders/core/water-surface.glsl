#ifndef STRATUS_WATER_SURFACE_INCLUDED
#define STRATUS_WATER_SURFACE_INCLUDED
// Native animated still/flow luminance is already sampled with atlas derivatives
// in the water geometry pass. Apply a bounded, multiplicative surface tint to
// the completed optics: no extra sampling, blur, opacity or added radiance.
vec3 vanillaWaterSurface(vec3 radiance,float nativePattern,vec3 biomeTint){
    float pattern=mix(0.65,1.0,clamp(nativePattern,0.0,1.0));
    vec3 tint=mix(vec3(1.0),activeWaterTint(biomeTint),0.40);
    return radiance*mix(vec3(1.0),pattern*tint,WATER_TEXTURE);
}
// Native alpha blend in display space, matching the game's texture/light path.
vec3 nativeWaterSurface(vec3 behind,vec4 nativeLayer){
    float coverage=clamp(nativeLayer.a*WATER_TEXTURE,0.0,1.0);
    return decodeDisplay(mix(encodeDisplay(behind),encodeDisplay(nativeLayer.rgb),coverage));
}
#endif
