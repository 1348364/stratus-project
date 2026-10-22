#ifndef STRATUS_REFRACTION_INCLUDED
#define STRATUS_REFRACTION_INCLUDED
// Restored from Stratus v1.3.1: inexpensive normal-offset transmission.
// This is a screen-space approximation, not a Snell geometry ray tracer.
vec2 legacyWaterRefractionUV(vec2 uv,vec3 nView,vec3 faceView,float thickness,float surfaceDepth){
    vec2 distortion=(nView.xy-faceView.xy)*WATER_DISTORTION*0.15*clamp(thickness*0.3,0.25,1.0);
    vec2 shifted=clamp(uv+distortion,vec2(0.001),vec2(0.999));
    float shiftedDepth=texture(depthtex1,shifted).r;
    if(shiftedDepth<0.999999&&-positionFromDepth(shifted,shiftedDepth).z<surfaceDepth+0.03)return uv;
#if REFRACTION_QUALITY > 0
    // Optional extra edge protection; mode zero is the original v1.3.1 guard.
    int checks=REFRACTION_QUALITY==2?4:2;
    for(int i=1;i<=checks;i++){
        vec2 edge=mix(uv,shifted,float(i)/float(checks));float d=texture(depthtex1,edge).r;
        if(d<0.999999&&-positionFromDepth(edge,d).z<surfaceDepth+0.03)return uv;
    }
#endif
    return shifted;
}
#endif
