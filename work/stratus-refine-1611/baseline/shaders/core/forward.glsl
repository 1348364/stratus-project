#ifndef STRATUS_FORWARD_INCLUDED
#define STRATUS_FORWARD_INCLUDED
// A dedicated single-channel target stores background transmittance left by
// ordinary forward alpha blends. RGB remains the composited forward scene.
// Recover premultiplied foreground radiance without subtracting an entire
// opaque background from partially transparent pixels.
vec3 forwardRadiance(vec3 scene,vec3 background,float transmission){
    return max(scene-background*clamp(transmission,0.0,1.0),vec3(0.0));
}
vec3 compositeForward(vec3 replacementBackground,vec3 foreground,float transmission){
    return replacementBackground*clamp(transmission,0.0,1.0)+foreground;
}
#endif
