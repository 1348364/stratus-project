#ifndef STRATUS_VOLUME_INCLUDED
#define STRATUS_VOLUME_INCLUDED
float mistDensityWorld(vec3 point){
    vec3 drift=vec3(frameTimeCounter*0.045,0.0,-frameTimeCounter*0.025);
    float field=simplexVolume((point+drift)*vec3(0.009,0.022,0.009));
    float centre=MIST_Y+(field-0.5)*MIST_THICKNESS*1.4;
    float h=(point.y-centre)/max(MIST_THICKNESS*1.7,1.0);
    float lower=exp(-h*h*0.5);
    float upper=exp(-pow((point.y-MIST_Y-MIST_THICKNESS*2.1)/max(MIST_THICKNESS*0.65,1.0),2.0)*0.5);
    return (0.0065*lower+0.0020*upper)*mix(0.22,1.60,smoothstep(0.18,0.80,field))*MIST_AMOUNT;
}
vec4 volumetricMist(vec3 origin,vec3 worldRay,float distanceLimit,float skyExposure,int steps){
#if DIMENSION_TYPE != 0
    return vec4(0.0);
#else
    if(MIST_AMOUNT<=0.0||skyExposure<0.03)return vec4(0.0);
    vec3 ray=unitVector(worldRay);
    float begin=max(MIST_CLEAR-length(origin-cameraPosition),0.0),finish=min(distanceLimit,900.0);
    float bottom=MIST_Y-MIST_THICKNESS*6.0,top=MIST_Y+MIST_THICKNESS*4.0;
    if(abs(ray.y)<0.0001){if(origin.y<bottom||origin.y>top)return vec4(0.0);}
    else{float a=(bottom-origin.y)/ray.y,b=(top-origin.y)/ray.y;begin=max(begin,min(a,b));finish=min(finish,max(a,b));}
    begin=max(begin,0.0);if(finish<=begin)return vec4(0.0);
    float stride=(finish-begin)/float(steps),opticalDepth=0.0;
    for(int i=0;i<steps;i++){
        vec3 point=origin+ray*(begin+(float(i)+0.5)*stride);
        float clearWeight=smoothstep(MIST_CLEAR,MIST_CLEAR+45.0,length(point-cameraPosition));
        opticalDepth+=mistDensityWorld(point)*stride*clearWeight;
    }
    float opacity=(1.0-exp(-opticalDepth))*smoothstep(0.03,0.70,skyExposure);
    float sun=pow(max(dot(ray,broadLightDirection()),0.0),5.0)*solarDaylight();
    return vec4(atmosphericColour()+sunlightColour()*sun*0.055,opacity);
#endif
}
vec4 atmosphereSegment(vec3 origin,vec3 ray,float distanceLimit,float skyExposure,bool detailed){
    int cloudSteps=detailed?6+CLOUD_LAYERS*4:6;
    vec4 clouds=marchCloudLayer(origin,ray,distanceLimit,cloudSteps,detailed);
    vec4 mist=volumetricMist(origin,ray,distanceLimit,skyExposure,detailed?2+MIST_DETAIL*2:3);
    return ray.y<0.0?overLayers(clouds,mist):overLayers(mist,clouds);
}
#endif
