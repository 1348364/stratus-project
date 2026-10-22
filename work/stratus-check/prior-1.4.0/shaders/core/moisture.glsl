#ifndef STRATUS_MOISTURE_INCLUDED
#define STRATUS_MOISTURE_INCLUDED
// Depth-neighbour contact retention: raised neighbours shelter a surface and
// inhibit drainage. No random dampness pattern or per-block ore discontinuity.
vec3 retainedMoisture(vec3 dry,vec3 viewPoint,vec2 uv){
#if DIMENSION_TYPE == 0
    if(SURFACE_DAMPNESS<=0.0)return dry;
    vec4 surface=texture(colortex1,uv);
    if(surface.a<0.5)return dry; // Entities, held items, plants and emitters stay dry.
    vec3 n=unitVector(surface.xyz),p=playerFromView(viewPoint);
    vec2 material=texture(colortex2,uv).xy;
    float sky=texture(colortex0,uv).r;
    float outdoors=smoothstep(0.12,0.83,sky);
    if(outdoors<0.001)return dry;
    vec2 radius=clamp(vec2(gbufferProjection[0][0],gbufferProjection[1][1])*0.70/max(-viewPoint.z,0.5),2.0/viewportSize(),vec2(0.055));
    float trapped=0.0;
    for(int i=0;i<8;i++){
        float angle=float(i)*0.785398163;
        vec2 sampleUV=clamp(uv+vec2(cos(angle),sin(angle))*radius,vec2(0.001),vec2(0.999));
        float d=texture(depthtex1,sampleUV).r;
        if(d>=0.999999)continue;
        vec3 neighbour=playerFromView(positionFromDepth(sampleUV,d));
        vec3 delta=neighbour-p;
        float distanceToNeighbour=length(delta);
        float rise=dot(delta,n);
        trapped+=smoothstep(0.035,0.38,rise)*(1.0-smoothstep(0.8,2.2,distanceToNeighbour));
    }
    trapped=clamp(trapped*0.35,0.0,1.0);
    float upward=max(n.y,0.0);
    float moisture=retainedMoistureAmount(sky,upward,material.x,trapped);
    float absorption=moisture*material.x;
    vec3 wet=dry/(vec3(1.0)+absorption*vec3(0.80));
    vec3 v=unitVector(-p);
    float roughness=mix(material.y,max(0.17,material.y*0.40),moisture);
    float film=moisture*WET_SHEEN;
    float coat=clamp(film*waterFresnel(max(dot(n,v),0.0))*(1.0-roughness*0.35),0.0,0.65);
    wet=mix(wet,softSkyReflection(reflect(-v,n))*sky*SKY_AMBIENT,coat);
    wet+=sunlightColour()*wetSunSpecular(n,v,broadLightDirection(),roughness)*film*sky*daytimeWeight()*0.65;
    return wet;
#else
    return dry;
#endif
}
#endif
