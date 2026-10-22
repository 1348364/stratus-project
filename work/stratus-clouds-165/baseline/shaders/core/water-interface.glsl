#ifndef STRATUS_WATER_INTERFACE_INCLUDED
#define STRATUS_WATER_INTERFACE_INCLUDED
// One orientation and dielectric convention for either side of a water face.
// Normal points into the camera's medium; incident points towards the face.
struct WaterBoundary {
    vec3 incident;
    vec3 normal;
    vec3 reflected;
    vec3 transmitted;
    float reflectance;
    bool totalReflection;
};
WaterBoundary waterBoundary(vec3 viewPosition,vec3 viewNormal,bool submerged){
    WaterBoundary b;
    b.incident=unitVector(viewPosition);
    b.normal=dot(viewNormal,-b.incident)>=0.0?viewNormal:-viewNormal;
    float etaI=submerged?1.333:1.0,etaT=submerged?1.0:1.333;
    float cosine=clamp(dot(-b.incident,b.normal),0.0,1.0);
    b.reflected=reflect(b.incident,b.normal);
    b.transmitted=refract(b.incident,b.normal,etaI/etaT);
    b.totalReflection=dot(b.transmitted,b.transmitted)<0.000001;
    b.reflectance=dielectricWaterFresnel(cosine,etaI,etaT);
    return b;
}
float waterReflectionWeight(WaterBoundary b){
    return b.totalReflection?1.0:clamp(REFLECT_LEVEL*b.reflectance,0.0,1.0);
}
#endif
