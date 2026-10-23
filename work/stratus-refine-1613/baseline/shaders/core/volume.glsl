#ifndef STRATUS_VOLUME_INCLUDED
#define STRATUS_VOLUME_INCLUDED
float mistDensityWorld(vec3 point){
    vec3 drift=frameTimeCounter*vec3(0.055,0.0,-0.035);
    vec3 p=(point+drift)/max(MIST_SCALE,8.0);
    float broad=weatherVolume(p*vec3(0.16,0.12,0.16)).a;
    float centre=MIST_Y+(broad-0.5)*MIST_THICKNESS*2.4;
    float h=(point.y-centre)/max(MIST_THICKNESS*1.35,1.0);
    float valley=exp(-0.5*h*h);
    float shelf=exp(-0.5*pow((point.y-MIST_Y-MIST_THICKNESS*2.25)/max(MIST_THICKNESS*0.70,1.0),2.0));
    vec4 volume=weatherVolume(p*vec3(0.24,0.37,0.24));
    float billow=smoothstep(0.35,0.75,mix(volume.r,volume.g,0.75));
    float fine=weatherVolume(p*0.77+vec3(0.23,0.61,0.17)).b;
    float variation=clamp(billow+(fine-0.5)*0.25,0.0,1.0);
    float pocket=mix(0.85,mix(0.025,2.25,variation),clamp(MIST_BREAKUP,0.0,1.0));
    pocket=pow(max(pocket,0.005),max(MIST_BREAKUP,1.0));
    return (0.0045*valley+0.0009*shelf)*pocket*MIST_AMOUNT;
}
vec4 volumetricMist(vec3 origin,vec3 worldRay,float distanceLimit,float skyExposure,int steps){
#if DIMENSION_TYPE != 0
    return vec4(0.0);
#else
    float cameraSky=clamp(float(eyeBrightnessSmooth.y)/240.0,0.0,1.0);
    float exposure=mix(cameraSky,skyExposure,0.45);
    if(MIST_AMOUNT<=0.0||exposure<0.03)return vec4(0.0);
    vec3 ray=unitVector(worldRay);
    float begin=max(MIST_CLEAR-length(origin-cameraPosition),0.0),finish=min(distanceLimit,1100.0);
    float bottom=MIST_Y-MIST_THICKNESS*6.0,top=MIST_Y+MIST_THICKNESS*5.0;
    if(abs(ray.y)<0.0001){if(origin.y<bottom||origin.y>top)return vec4(0.0);}
    else{float a=(bottom-origin.y)/ray.y,b=(top-origin.y)/ray.y;begin=max(begin,min(a,b));finish=min(finish,max(a,b));}
    begin=max(begin,0.0);if(finish<=begin)return vec4(0.0);
    float transmission=1.0;vec3 scattering=vec3(0.0);
    float cosine=dot(ray,broadLightDirection());
    float g=0.45;
    float phase=(1.0-g*g)/pow(max(1.0+g*g-2.0*g*cosine,0.05),1.5);
    float outdoor=smoothstep(0.03,0.60,exposure);
    // These values depend only on the ray/uniforms, never the integration step.
    vec3 lightDirection=broadLightDirection();
    vec3 ambientColour=atmosphericColour()*0.91;
    vec3 sunRadiance=sunlightColour()*solarDaylight();
    for(int i=0;i<steps;i++){
        float a=float(i)/float(steps),b=float(i+1)/float(steps);
        a=a*a;b=b*b;
        float stride=(finish-begin)*(b-a);
        vec3 point=origin+ray*(begin+(a+b)*0.5*(finish-begin));
        float clearWeight=smoothstep(MIST_CLEAR,MIST_CLEAR+22.0,length(point-cameraPosition));
        // The clear foreground contributes exactly zero; avoid field reads
        // there, including reflected paths that first turn toward the camera.
        if(clearWeight<=0.0)continue;
        float density=mistDensityWorld(point)*clearWeight*outdoor;
        if(density<0.000001)continue;
        float opacity=1.0-exp(-density*stride);
        float sunTransmission=1.0;
        // At night or with scattering disabled, this entire contribution is
        // exactly zero. Retain every illumination sample whenever it is visible.
        if(any(greaterThan(sunRadiance,vec3(0.0)))&&MIST_LIGHT>0.0){
            float lightDepth=mistDensityWorld(point+lightDirection*12.0)*18.0;
            lightDepth+=mistDensityWorld(point+lightDirection*36.0)*24.0;
            sunTransmission=exp(-lightDepth);
        }
        vec3 colour=ambientColour;
        colour+=sunRadiance*sunTransmission*phase*MIST_LIGHT*0.085;
        scattering+=transmission*opacity*colour;transmission*=1.0-opacity;
        if(transmission<0.008)break;
    }
    return vec4(scattering/max(1.0-transmission,0.00001),1.0-transmission);
#endif
}
vec4 atmosphereSegment(vec3 origin,vec3 ray,float distanceLimit,float skyExposure,bool detailed){
    int cloudSteps=detailed?(ATMOSPHERE_QUALITY==2?32+CLOUD_LAYERS*40:16+CLOUD_LAYERS*16):20;
    vec4 clouds=marchCloudLayer(origin,ray,distanceLimit,cloudSteps,detailed);
    vec4 mist=volumetricMist(origin,ray,distanceLimit,skyExposure,detailed?(ATMOSPHERE_QUALITY==2?12+MIST_DETAIL*16:12+MIST_DETAIL*8):8);
    return ray.y<0.0?overLayers(clouds,mist):overLayers(mist,clouds);
}
// Shared by the reduced-resolution pass and its confidence fallback. Avoids
// inconsistent border fog/blindness between tiny cutouts and larger surfaces.
vec4 completeAtmosphereSegment(vec3 origin,vec3 ray,float limit,float sky,bool detailed){
    vec4 volume=atmosphereSegment(origin,ray,limit,sky,detailed);
#if DIMENSION_TYPE == 0
    if(limit<6999.0&&sky>0.05){
        vec3 point=ray*limit;
        // Minecraft loads complete vertical columns: only horizontal distance
        // approaches the chunk boundary, including when looking down from clouds.
        float metric=length(point.xz);
        float border=smoothstep(max(far*0.84,1.0),max(far,2.0),metric)*smoothstep(0.0,1.0,sky);
        volume=overLayers(volume,vec4(atmosphericColour(),border));
    }
#endif
    volume.rgb*=1.0-clamp(max(blindness,darknessFactor),0.0,1.0);
    return volume;
}
#endif
