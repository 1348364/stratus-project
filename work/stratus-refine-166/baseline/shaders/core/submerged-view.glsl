#ifndef STRATUS_SUBMERGED_VIEW_INCLUDED
#define STRATUS_SUBMERGED_VIEW_INCLUDED
// Underwater transmission stays on the rasterized camera ray: no Snell
// direction, environment dome, or screen-space refraction lookup. Reflection
// remains a separate Fresnel-weighted path.
vec3 submergedView(vec2 screen,vec3 scene,vec4 mark,vec4 normal,vec4 depth){
    float sky=clamp(float(eyeBrightnessSmooth.y)/240.0,0.0,1.0);
    bool interfaceVisible=mark.a>0.5&&normal.a>0.5&&depth.a>0.5&&depth.x>0.0;
    // Direct submerged terrain is transported in the full-resolution resolve;
    // a reduced optics buffer must not filter opaque block or particle edges.
    if(!interfaceVisible)return scene;
    vec3 ray=positionFromDepth(screen,0.5);
    vec3 surface=ray*(depth.x/max(-ray.z,0.00001));sky=depth.y;
    vec4 tint=texture(colortex8,screen);
    if(dot(tint.rgb,tint.rgb)<0.001)tint.rgb=biomeWaterTint;
    vec3 face=unitVector(mat3(gbufferModelView)*normal.xyz);
    if(dot(face,-surface)<0.0)face=-face;
    vec3 worldNormal=lakeNormal(playerFromView(surface),normal.xyz,depth.x,sky);
    vec3 wave=unitVector(mat3(gbufferModelView)*worldNormal);
    if(dot(wave,face)<0.0)wave=-wave;
    WaterBoundary boundary=waterBoundary(surface,wave,true);
    vec4 hit=readWaterReflection(screen,normal.xyz,depth.x);
    vec3 reflected=mix(waterBodyColour(tint.rgb,sky,tint.a),hit.rgb,hit.a);
    vec3 transmitted=scene;
    vec3 interfaceRadiance=mix(transmitted,reflected,waterReflectionWeight(boundary));
    return travelThroughWater(interfaceRadiance,length(surface),tint.rgb,sky,tint.a);
}
#endif
