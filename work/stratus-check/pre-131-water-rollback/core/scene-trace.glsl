#ifndef STRATUS_SCENE_TRACE_INCLUDED
#define STRATUS_SCENE_TRACE_INCLUDED
// Original surface reconstruction: contiguous projected pixels, actual receiver
// planes, and explicit water/air half-space checks shared by both optical rays.
#include "/core/optics-cube.glsl"
uniform sampler2D colortex10;
int opticsFace=0;
uniform sampler2D shadowcolor0;
uniform sampler2D shadowcolor1;
ivec2 opticsSize(bool cache){return cache?textureSize(shadowcolor1,0)/ivec2(4,2):textureSize(depthtex1,0);}
vec3 opticsRadiance(ivec2 cell,bool cache){return cache?texelFetch(shadowcolor0,cell+ivec2(cubeTile(opticsFace))*opticsSize(true),0).rgb:texelFetch(colortex4,cell,0).rgb;}

bool opticsProjection(vec3 p,out vec2 uv,bool cache){
    if(cache){
        vec3 pWorld=mat3(gbufferModelViewInverse)*p;
        vec3 q=cubeCoordinates(pWorld-cubeOrigin(opticsFace),opticsFace);
        uv=q.xy/(max(q.z,0.00001)*cubeExtent(opticsFace))*0.5+0.5;
        return q.z>0.0&&min(uv.x,uv.y)>0.00001&&max(uv.x,uv.y)<0.99999;
    }
    vec4 q=gbufferProjection*vec4(p,1.0);uv=q.xy/max(q.w,0.00001)*0.5+0.5;
    return q.w>0.0&&min(uv.x,uv.y)>0.001&&max(uv.x,uv.y)<0.999;
}
vec3 opticsReceiver(ivec2 cell,out vec4 normal,bool cache){
    ivec2 size=opticsSize(cache);cell=clamp(cell,ivec2(0),size-ivec2(1));
    vec2 uv=(vec2(cell)+0.5)/vec2(size);
    normal=cache?texelFetch(shadowcolor1,cell+ivec2(cubeTile(opticsFace))*size,0):texelFetch(colortex10,cell,0);
    if(cache){
        float radius=normal.a;normal.a=radius>0.0001?1.0:0.0;
        return mat3(gbufferModelView)*(normalize(cubeRay(uv,opticsFace))*radius+cubeOrigin(opticsFace));
    }
    float d=texelFetch(depthtex1,cell,0).r;
    if(d>=0.999999)normal.a=0.0;
    return positionFromDepth(uv,d);
}
vec3 opticsColour(vec2 uv,vec3 planePoint,vec3 planeNormal,bool cache){
    ivec2 size=opticsSize(cache);
    vec2 grid=uv*vec2(size)-0.5;ivec2 cell=ivec2(floor(grid));vec2 f=fract(grid);
    vec3 sum=vec3(0.0);float total=0.0;
    for(int y=0;y<2;y++)for(int x=0;x<2;x++){
        ivec2 c=clamp(cell+ivec2(x,y),ivec2(0),size-ivec2(1));
        vec4 data;vec3 receiver=opticsReceiver(c,data,cache);
        vec3 n=unitVector(mat3(gbufferModelView)*data.xyz);
        float weight=(x==0?1.0-f.x:f.x)*(y==0?1.0-f.y:f.y);
        if(data.a<0.5||dot(n,planeNormal)<0.95||abs(dot(receiver-planePoint,planeNormal))>0.02+length(receiver)*0.0004)continue;
        sum+=opticsRadiance(c,cache)*weight;total+=weight;
    }
    ivec2 centre=clamp(ivec2(uv*vec2(size)),ivec2(0),size-ivec2(1));
    return total>0.001?sum/total:opticsRadiance(centre,cache);
}
// Bound expensive pixel traversal by a receiver plane that has already been
// validated at the projected intersection. This preserves the depth search in
// front of it, but avoids marching empty space all the way to the far plane.
float opticsPlaneBound(vec3 origin,vec3 direction,vec3 interfaceNormal,int side,bool cache,float minimum,float maximum,out vec2 boundUV,out vec3 boundPoint,out vec3 boundNormal){
    float sampleT=minimum+0.025;boundUV=vec2(0);boundPoint=vec3(0);boundNormal=vec3(0);
    for(int iteration=0;iteration<4;iteration++){
        vec2 uv;if(!opticsProjection(origin+direction*sampleT,uv,cache))break;
        ivec2 size=opticsSize(cache),cell=clamp(ivec2(uv*vec2(size)),ivec2(0),size-ivec2(1));
        vec4 data;vec3 receiver=opticsReceiver(cell,data,cache);if(data.a<0.5)break;
        vec3 n=unitVector(mat3(gbufferModelView)*data.xyz);float denominator=dot(direction,n);
        if(abs(denominator)<0.00001)break;
        float distance=dot(receiver-origin,n)/denominator;
        if(distance<=minimum||distance>maximum)break;
        vec3 candidate=origin+direction*distance;vec2 hitUV;if(!opticsProjection(candidate,hitUV,cache))break;
        vec4 hitData;vec3 actual=opticsReceiver(clamp(ivec2(hitUV*vec2(size)),ivec2(0),size-ivec2(1)),hitData,cache);
        vec3 hitNormal=unitVector(mat3(gbufferModelView)*hitData.xyz);
        bool samePlane=hitData.a>0.5&&dot(hitNormal,n)>0.95&&abs(dot(actual-candidate,n))<0.018+length(actual)*0.0004;
        if(samePlane&&float(side)*dot(actual-origin,interfaceNormal)>0.005){boundUV=hitUV;boundPoint=candidate;boundNormal=n;return distance;}
        sampleT=distance;
    }
    return maximum;
}
vec4 traceOpticalSegment(vec3 origin,vec3 direction,vec3 interfaceNormal,int side,int quality,float maximum,bool cache,float minimum,out float path){
    path=0.0;
    if(!cache&&direction.z>0.00001)maximum=min(maximum,max(0.0,(-0.10-origin.z)/direction.z));
    if(maximum<0.03)return vec4(0.0);
    vec2 boundUV;vec3 boundPoint,boundNormal;
    float previousMaximum=maximum;
    maximum=opticsPlaneBound(origin,direction,interfaceNormal,side,cache,max(minimum,0.025),maximum,boundUV,boundPoint,boundNormal);
    bool bounded=maximum<previousMaximum;
    vec3 start=origin+direction*max(minimum,0.025),end=origin+direction*maximum;
    vec4 a=gbufferProjection*vec4(start,1.0),b=gbufferProjection*vec4(end,1.0);
    if(cache){
        vec3 p=cubeCoordinates(mat3(gbufferModelViewInverse)*start-cubeOrigin(opticsFace),opticsFace);
        vec3 q=cubeCoordinates(mat3(gbufferModelViewInverse)*end-cubeOrigin(opticsFace),opticsFace);
        a=vec4(p.xy/cubeExtent(opticsFace),0.0,p.z);b=vec4(q.xy/cubeExtent(opticsFace),0.0,q.z);
    }
    float ka=1.0/max(a.w,0.00001),kb=1.0/max(b.w,0.00001);
    float projectionScale=1.0;
    vec2 pa=a.xy*ka/projectionScale*0.5+0.5,pb=b.xy*kb/projectionScale*0.5+0.5;
    vec3 qa=start*ka,qb=end*kb;vec2 delta=pb-pa;
    float visible=1.0;
    for(int axis=0;axis<2;axis++){
        if(delta[axis]>0.00001)visible=min(visible,(0.999-pa[axis])/delta[axis]);
        else if(delta[axis]<-0.00001)visible=min(visible,(0.001-pa[axis])/delta[axis]);
    }
    visible=clamp(visible,0.0,1.0);pb=mix(pa,pb,visible);qb=mix(qa,qb,visible);kb=mix(ka,kb,visible);
    ivec2 size=opticsSize(cache);vec2 pixels=abs((pb-pa)*vec2(size));
    float stride=quality==2?1.0:(quality==1?2.0:4.0);
    // High retains contiguous pixel traversal; lower profiles bound long rays.
    float budget=quality==2?2048.0:(quality==1?128.0:64.0);
    int count=int(clamp(ceil(max(pixels.x,pixels.y)/stride),1.0,budget));
    for(int i=0;i<2048;i++){
        if(i>=count)break;
        float f0=float(i)/float(count),f1=float(i+1)/float(count),f=(f0+f1)*0.5;
        vec2 uv=mix(pa,pb,f);
        if(min(uv.x,uv.y)<0.001||max(uv.x,uv.y)>0.999)break;
        vec3 p0=mix(qa,qb,f0)/mix(ka,kb,f0),p1=mix(qa,qb,f1)/mix(ka,kb,f1);
        vec3 point=mix(qa,qb,f)/mix(ka,kb,f);
        ivec2 cell=clamp(ivec2(uv*vec2(size)),ivec2(0),size-ivec2(1));
        vec4 data;vec3 receiver=opticsReceiver(cell,data,cache);
        if(data.a<0.5)continue;
        vec3 n=unitVector(mat3(gbufferModelView)*data.xyz);
        float denominator=dot(direction,n);
        float distance=abs(denominator)>0.00001?dot(receiver-origin,n)/denominator:-1.0;
        float t0=dot(p0-origin,direction),t1=dot(p1-origin,direction);
        float footprint=max(0.012,length(receiver)/(float(size.y)*max(gbufferProjection[1][1],0.1)));
        if(distance>=max(0.025,t0-footprint)&&distance<=min(maximum,t1+footprint)){
            vec3 candidate=origin+direction*distance;vec2 hitUV;
            if(opticsProjection(candidate,hitUV,cache)){
                ivec2 hitCell=clamp(ivec2(hitUV*vec2(size)),ivec2(0),size-ivec2(1));
                vec4 hitData;vec3 actual=opticsReceiver(hitCell,hitData,cache);
                vec3 hitNormal=unitVector(mat3(gbufferModelView)*hitData.xyz);
                bool samePlane=hitData.a>0.5&&dot(hitNormal,n)>0.95&&abs(dot(actual-candidate,n))<0.018+length(actual)*0.0004;
                bool correctMedium=float(side)*dot(actual-origin,interfaceNormal)>0.005;
                if(samePlane&&correctMedium&&max(abs(hitUV.x-uv.x)*float(size.x),abs(hitUV.y-uv.y)*float(size.y))<stride+1.0){
                    vec2 border=min(hitUV,1.0-hitUV)*vec2(size);
                    float coverage=smoothstep(1.0,8.0,min(border.x,border.y));
                    // A cube face border is a seam, not missing scene coverage.
                    if(cache)coverage=1.0;
                    path=distance;
                    return vec4(opticsColour(hitUV,candidate,n,cache),coverage);
                }
            }
        }
        // A foreground occluder ends the search. Never continue through a
        // rejected shore edge and steal a farther river-floor pixel.
        float occlusion=cache?dot(mat3(gbufferModelViewInverse)*(point-receiver),cubeForward(opticsFace)):receiver.z-point.z;
        if(!cache&&occlusion>max(0.08,footprint*3.0))return vec4(0.0);
    }
    if(bounded){path=maximum;return vec4(opticsColour(boundUV,boundPoint,boundNormal,cache),1.0);}
    return vec4(0.0);
}
// Continuous local environment when a reflected receiver is hidden from every
// depth view. It avoids flat blue holes during underwater total reflection;
// parallax of this last-resort lookup is approximate, unlike validated ray hits.
vec4 cachedOpticalEnvironment(vec3 origin,vec3 direction,out float distance){
    vec3 worldDirection=mat3(gbufferModelViewInverse)*direction;
    int face=0;float alignment=-1.0;
    for(int i=0;i<6;i++){float a=dot(worldDirection,cubeForward(i));if(a>alignment){alignment=a;face=i;}}
    opticsFace=face;vec3 q=cubeCoordinates(worldDirection,face);
    vec2 uv=q.xy/(max(q.z,0.00001)*cubeExtent(face))*0.5+0.5;
    ivec2 size=opticsSize(true),cell=clamp(ivec2(uv*vec2(size)),ivec2(0),size-ivec2(1));
    vec4 data;vec3 receiver=opticsReceiver(cell,data,true);
    distance=length(receiver-origin);
    return vec4(opticsColour(uv,receiver,unitVector(mat3(gbufferModelView)*data.xyz),true),data.a);
}
// Clip the ray to each cube pyramid, then perform perspective-correct DDA
// within it. This includes terrain behind the eye and below the waterline.
bool opticsClip(float a,float b,inout float lo,inout float hi){
 if(abs(b)<0.0000001)return a>=0.0;
 float t=-a/b;if(b>0.0)lo=max(lo,t);else hi=min(hi,t);return hi>lo;
}
vec4 traceOpticalScene(vec3 origin,vec3 direction,vec3 interfaceNormal,int side,int quality,float maximum,bool cache,out float path){
 if(!cache)return traceOpticalSegment(origin,direction,interfaceNormal,side,quality,maximum,false,0.025,path);
 vec3 worldOrigin=mat3(gbufferModelViewInverse)*origin,worldDirection=mat3(gbufferModelViewInverse)*direction;
 // The shadow cache covers nearby chunks; do not scan empty far-away views.
 float cacheLo=0.025,cacheHi=maximum;float reach=float(OPTICS_CACHE_DISTANCE)+16.0;
 bool covered=opticsClip(reach-worldOrigin.x,-worldDirection.x,cacheLo,cacheHi)&&opticsClip(reach+worldOrigin.x,worldDirection.x,cacheLo,cacheHi);
 covered=covered&&opticsClip(reach-worldOrigin.z,-worldDirection.z,cacheLo,cacheHi)&&opticsClip(reach+worldOrigin.z,worldDirection.z,cacheLo,cacheHi);
 path=0.0;if(!covered)return vec4(0.0);maximum=min(maximum,cacheHi);
 vec4 best=vec4(0.0);float nearest=maximum+1.0;
 for(int face=0;face<8;face++){
  vec3 o=cubeCoordinates(worldOrigin-cubeOrigin(face),face),d=cubeCoordinates(worldDirection,face);
  float lo=max(0.025,cacheLo),hi=maximum;
  bool inside=opticsClip(o.z-0.05,d.z,lo,hi);
  inside=inside&&opticsClip(o.z*cubeExtent(face)-o.x,d.z*cubeExtent(face)-d.x,lo,hi)&&opticsClip(o.z*cubeExtent(face)+o.x,d.z*cubeExtent(face)+d.x,lo,hi);
  inside=inside&&opticsClip(o.z*cubeExtent(face)-o.y,d.z*cubeExtent(face)-d.y,lo,hi)&&opticsClip(o.z*cubeExtent(face)+o.y,d.z*cubeExtent(face)+d.y,lo,hi);
  if(!inside||hi<=lo||lo>=nearest)continue;
  opticsFace=face;float distance;
  vec4 hit=traceOpticalSegment(origin,direction,interfaceNormal,side,quality,hi,true,lo+0.0001,distance);
  if(hit.a>0.0&&distance<nearest){best=hit;nearest=distance;path=distance;}
 }
 return best;
}
#endif
