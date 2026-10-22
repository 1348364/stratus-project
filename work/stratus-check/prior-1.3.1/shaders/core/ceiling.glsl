#ifndef STRATUS_CEILING_INCLUDED
#define STRATUS_CEILING_INCLUDED
#include "/core/field.glsl"
vec3 atmosphericColour() {
#if DIMENSION_TYPE == 0
    vec3 day=decodeDisplay(vec3(0.69,0.72,0.76));
    return mix(decodeDisplay(vec3(0.06,0.085,0.14)),day,daytimeWeight())*(1.0-0.12*rainStrength);
#else
    return decodeDisplay(fogColor);
#endif
}
float solarDaylight(){return daytimeWeight()*smoothstep(-0.06,0.10,broadLightDirection().y);}
vec3 softSkyReflection(vec3 worldRay){
    vec3 ray=unitVector(worldRay);
    vec3 sky=atmosphericColour()*mix(0.65,1.05,smoothstep(-0.1,0.8,ray.y));
    float glow=exp(-max(1.0-dot(ray,broadLightDirection()),0.0)/0.08);
    return sky+sunlightColour()*glow*0.16*solarDaylight()*SKY_LEAK;
}
vec3 skyBackdrop(vec3 worldRay){
#if DIMENSION_TYPE != 0
    return decodeDisplay(fogColor);
#else
    vec3 ray=unitVector(worldRay);
    float horizon=exp(-max(ray.y,0.0)*5.0);
    vec3 zenith=decodeDisplay(mix(vec3(0.045,0.072,0.12),vec3(0.56,0.65,0.76),daytimeWeight()));
    vec3 sky=mix(zenith,atmosphericColour(),horizon);
    sky=mix(sky,atmosphericColour(),CLOUD_AMOUNT*0.20);
    float separation=max(1.0-dot(ray,broadLightDirection()),0.0);
    float glow=exp(-separation/0.08)*SKY_LEAK*0.22;
    float core=exp(-separation/0.00032)*3.4;
    float aureole=exp(-separation/0.008)*0.70;
    sky+=sunlightColour()*solarDaylight()*(glow+(core+aureole)*SUN_VISIBILITY*(1.0-0.65*rainStrength));
    return sky;
#endif
}
vec2 layeredCloudSample(vec3 worldPoint,bool detailed,bool upper){
    float altitude=upper?CIRRUS_ALTITUDE:CLOUD_ALTITUDE;
    float thickness=upper?32.0:CLOUD_THICKNESS;
    float amount=upper?CIRRUS_AMOUNT:CLOUD_AMOUNT;
    vec2 wind=frameTimeCounter*CLOUD_DRIFT*vec2(0.31,-0.14)*(upper?1.55:1.0);
    vec2 weatherPoint=(worldPoint.xz+wind)/CLOUD_SPAN;
    float weather=smoothField(weatherPoint*vec2(0.72,1.40)+vec2(8.1,-19.4));
    float centre=altitude+(weather-0.5)*thickness*CLOUD_DISTORTION*0.65;
    float height=(worldPoint.y-centre)/thickness+0.5;
    float envelope=smoothstep(0.0,0.24,height)*(1.0-smoothstep(0.66,1.0,height));
    if(envelope<=0.0||amount<=0.0)return vec2(0.0);
    float scale=max(CLOUD_SPAN*(upper?0.23:0.28),24.0);
    vec3 p=vec3((worldPoint.x+wind.x)/scale,(worldPoint.y-altitude)/max(thickness*0.9,1.0),(worldPoint.z+wind.y)/scale);
    p.xz=mat2(0.8,-0.6,0.6,0.8)*p.xz;
    if(upper){p.x*=0.34;p.z*=1.8;p.x+=sin(p.z*0.8+weather*3.0)*0.35;}
    p.x+=(weather-0.5)*CLOUD_DISTORTION;
    float body=simplexVolume(p);
    if(detailed){
        vec3 detail=vec3(p.z+p.y*.4,p.x-p.z*.3,p.y+p.x*.3)*2.07+vec3(7.2,2.3,-8.1);
        body=mix(body,simplexVolume(detail),0.25);
#if CLOUD_LAYERS > 2
        body-=0.065*(1.0-simplexVolume(p*4.13-vec3(4.7,8.2,2.1)));
#endif
    }
    float threshold=mix(0.70,upper?0.46:0.43,amount);
    float bulk=smoothstep(threshold-0.15,threshold+0.17,body+(weather-0.5)*0.25);
    float density=envelope*bulk*amount*(upper?0.026:0.055);
    return vec2(density,height);
}
vec2 cloudVolumeSample(vec3 p,bool detailed){return layeredCloudSample(p,detailed,false);}
vec2 cloudSample(vec3 p){return layeredCloudSample(p,true,false);}
float cloudSunTransmission(vec3 point){
    vec3 l=broadLightDirection();float span=CLOUD_THICKNESS;
    float tau=layeredCloudSample(point+l*span*0.32,false,false).x*span*0.60;
#if CLOUD_LAYERS > 2
    tau+=layeredCloudSample(point+l*span*0.75,false,false).x*span*0.45;
#endif
    return exp(-tau);
}
vec4 overLayers(vec4 front,vec4 back){
    float alpha=front.a+(1.0-front.a)*back.a;
    return vec4((front.rgb*front.a+back.rgb*back.a*(1.0-front.a))/max(alpha,0.00001),alpha);
}
vec4 marchSingleCloud(vec3 origin,vec3 worldRay,float distanceLimit,int steps,bool shadows,bool upper){
#if DIMENSION_TYPE != 0
    return vec4(0.0);
#else
    float amount=upper?CIRRUS_AMOUNT:CLOUD_AMOUNT;if(amount<=0.0)return vec4(0.0);
    float altitude=upper?CIRRUS_ALTITUDE:CLOUD_ALTITUDE;
    float thickness=upper?32.0:CLOUD_THICKNESS;
    float bottom=altitude-thickness*0.90,top=altitude+thickness*0.90;
    vec3 ray=unitVector(worldRay);float begin=0.0,finish=min(distanceLimit,7000.0);
    if(abs(ray.y)<0.0001){if(origin.y<bottom||origin.y>top)return vec4(0.0);finish=min(finish,450.0);}
    else{float a=(bottom-origin.y)/ray.y,b=(top-origin.y)/ray.y;begin=max(min(a,b),0.0);finish=min(finish,max(a,b));}
    if(finish<=begin)return vec4(0.0);
    float stride=min((finish-begin)/float(steps),thickness*0.70);
    float transmission=1.0;vec3 scattered=vec3(0.0);
    float separation=max(1.0-dot(ray,broadLightDirection()),0.0);
    float phase=0.75/pow(max(0.25+separation,0.05),1.5);
    float solarPatch=exp(-separation/0.0014)*SUN_VISIBILITY;
    for(int i=0;i<steps;i++){
        vec3 point=origin+ray*(begin+(float(i)+0.5)*stride);
        vec2 sampleData=layeredCloudSample(point,shadows||upper,upper);if(sampleData.x<=0.00001)continue;
        float opacity=1.0-exp(-sampleData.x*stride);
        float h=clamp(sampleData.y,0.0,1.0);
        float sunlight=shadows&&!upper?cloudSunTransmission(point):mix(0.35,1.0,h);
        float ambient=mix(0.48,1.0,h);
        vec3 daylight=vec3(0.35,0.39,0.46)*ambient;
        daylight+=sunlightColour()*sunlight*(0.31+phase*0.055*SUN_VISIBILITY);
        daylight*=mix(1.0,0.70+0.30*sunlight,CLOUD_RELIEF);
        // Forward scattering exposes a soft warm solar location from below too.
        daylight+=sunlightColour()*(phase*SKY_LEAK*0.08*sunlight+solarPatch*(0.45+1.25*sunlight));
        vec3 colour=mix(vec3(0.006,0.010,0.019)*ambient,daylight,daytimeWeight());
        colour*=1.0-0.17*rainStrength;
        scattered+=transmission*opacity*colour;transmission*=1.0-opacity;
        if(transmission<0.015)break;
    }
    vec3 colour=scattered/max(1.0-transmission,0.0001);
    colour=mix(colour,atmosphericColour(),1.0-exp(-max(begin-150.0,0.0)*0.00025));
    return vec4(colour,1.0-transmission);
#endif
}
vec4 marchCloudLayer(vec3 origin,vec3 ray,float limit,int steps,bool shadows){
    vec4 low=marchSingleCloud(origin,ray,limit,steps,shadows,false);
    vec4 high=marchSingleCloud(origin,ray,limit,max(4,steps/2),false,true);
    return ray.y<0.0?overLayers(high,low):overLayers(low,high);
}
vec4 physicalCloudLayer(vec3 origin,vec3 ray,float limit){return marchCloudLayer(origin,ray,limit,6+CLOUD_LAYERS*4,true);}
vec3 overcastCeiling(vec3 worldRay){
    // A prefiltered reflection approximation avoids a cloud ray march per water pixel.
    vec3 ray=unitVector(worldRay);vec3 sky=skyBackdrop(ray);
    if(abs(ray.y)<0.01)return mix(sky,atmosphericColour(),0.75);
    float distanceToLayer=(CLOUD_ALTITUDE-cameraPosition.y)/ray.y;
    if(distanceToLayer>0.0){
        vec3 point=cameraPosition+ray*distanceToLayer;
        vec2 density=layeredCloudSample(point,false,false);
        // Prefilter the broad cloud contribution: sharp density patches do not
        // survive a rough, rippling water reflection.
        float coverage=smoothstep(0.0,0.040,density.x);
        vec3 colour=atmosphericColour()*mix(0.90,1.13,coverage);
        sky=mix(sky,colour,CLOUD_AMOUNT*0.72);
    }
    return sky;
}
#endif
