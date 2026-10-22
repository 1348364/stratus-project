#ifndef STRATUS_LAKE_NORMAL_INCLUDED
#define STRATUS_LAKE_NORMAL_INCLUDED
vec3 lakeNormal(vec3 point,vec3 faceNormal,float viewDistance){
    vec3 n=unitVector(faceNormal),worldPoint=(point+cameraPosition)/RIPPLE_SIZE,gradient=vec3(0.0);
    float footprint=viewDistance/max(viewHeight*gbufferProjection[1][1],1.0);
    for(int component=0;component<4;component++){
        float index=float(component),angle=1.13+index*2.118;
        vec3 direction=unitVector(vec3(cos(angle),0.21*sin(index+1.0),sin(angle)));
        float frequency=0.57*pow(1.57,index);
        float phase=dot(worldPoint,direction)*frequency+index*1.71-frameTimeCounter*RIPPLE_RATE*sqrt(frequency)*0.93;
        float filterWeight=inversesqrt(1.0+frequency*frequency*footprint*footprint*8.0);
        gradient+=direction*(cos(phase)*frequency*0.035*pow(0.52,index)*filterWeight);
    }
    gradient-=n*dot(gradient,n);
    return unitVector(n-gradient*RIPPLE_HEIGHT);
}
#endif
