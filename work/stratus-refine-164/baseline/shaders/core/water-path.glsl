#ifndef STRATUS_WATER_PATH_INCLUDED
#define STRATUS_WATER_PATH_INCLUDED
// A falling sheet does not fill the entire gap to the opaque terrain. Its
// foreground water segment and the air behind it must be transported separately.
float fallingWaterThickness(vec3 worldPoint,vec3 faceNormal,vec3 viewRay,float receiverDistance){
    float vertical=abs(faceNormal.y);
    float height=clamp(fract(worldPoint.y+0.02),0.08,0.90);
    float slab=mix(0.95,height,vertical);
    return min(receiverDistance,slab/max(abs(dot(viewRay,faceNormal)),0.15));
}
bool hasBackgroundWater(vec4 background,float frontDepth,float receiverDepth){
    float separation=max(0.12,frontDepth*0.002);
    return background.a>0.5&&background.x>frontDepth+separation&&background.x<receiverDepth;
}
// At a waterfall/ocean junction Minecraft omits the internal horizontal face.
// Confirm the surrounding water level on both sides of the pixel instead of
// treating that missing internal face as an air gap. This is a local screen-space
// fallback; it does not invent an ocean level from world height or biome alone.
bool joinsSurroundingWater(sampler2D horizontalWater,vec2 uv,vec3 frontWorld,vec3 ray,float receiverDistance){
    if(ray.y>=-0.01)return false;
    vec2 pixel=1.0/vec2(textureSize(horizontalWater,0));
    for(int i=0;i<4;i++){
        float radius=i==0?8.0:(i==1?24.0:(i==2?64.0:128.0));
        vec2 a=uv-vec2(pixel.x*radius,0.0),b=uv+vec2(pixel.x*radius,0.0);
        if(a.x<=0.001||b.x>=0.999)continue;
        vec4 da=texture(horizontalWater,a),db=texture(horizontalWater,b);
        if(da.a<0.5||db.a<0.5)continue;
        vec3 ra=positionFromDepth(a,0.5),rb=positionFromDepth(b,0.5);
        float ya=(playerFromView(ra*(da.x/max(-ra.z,0.00001)))+cameraPosition).y;
        float yb=(playerFromView(rb*(db.x/max(-rb.z,0.00001)))+cameraPosition).y;
        if(abs(ya-yb)>0.20)continue;
        float crossing=((ya+yb)*0.5-frontWorld.y)/ray.y;
        if(crossing>0.0&&crossing<receiverDistance)return true;
    }
    return false;
}
// Transport only the air *after* a finite water sheet or an underwater exit.
// The final atmosphere pass already handles camera-to-front-water transport.
vec3 airBehindWater(vec3 colour,vec3 origin,vec3 direction,float distanceLimit,float skyExposure,bool geometry){
#if DIMENSION_TYPE == 0
    if(distanceLimit<=0.001)return colour;
    int steps=ATMOSPHERE_QUALITY==2?12+MIST_DETAIL*16:12+MIST_DETAIL*8;
    vec4 mist=volumetricMist(origin,direction,distanceLimit,skyExposure,steps);
    // Opaque receivers need the cloud segment as well. Sky samples already
    // contain clouds from the environment cache, so do not apply them twice.
    if(geometry){
        vec4 cloud=marchCloudLayer(origin,direction,distanceLimit,12,false);
        mist=direction.y<0.0?overLayers(cloud,mist):overLayers(mist,cloud);
    }
    colour=mix(colour,mist.rgb,mist.a);
    if(geometry){
        float horizontal=length((origin-cameraPosition+direction*distanceLimit).xz);
        float border=smoothstep(max(far*0.84,1.0),max(far,2.0),horizontal)*smoothstep(0.0,1.0,skyExposure);
        colour=mix(colour,atmosphericColour(),border);
    }
#endif
    return colour;
}
#endif
