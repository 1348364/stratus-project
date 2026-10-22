#ifndef STRATUS_REFRACTION_INCLUDED
#define STRATUS_REFRACTION_INCLUDED
// Perspective-correct screen-space tracing against actual receiver normals.
// Geometry is sampled along Snell's ray, never warped from the starting pixel's
// tangent plane or squeezed into an arbitrary UV-displacement budget.
uniform sampler2D colortex10;
bool refractionProjection(vec3 point,out vec2 uv){
    vec4 clip=gbufferProjection*vec4(point,1.0);
    uv=clip.xy/max(clip.w,0.00001)*0.5+0.5;
    return clip.w>0.0&&min(uv.x,uv.y)>0.001&&max(uv.x,uv.y)<0.999;
}
float refractionDepthError(vec3 point,vec2 uv){
    float d=texture(depthtex1,uv).r;
    return d>=0.999999?-100000.0:positionFromDepth(uv,d).z-point.z;
}
vec4 traceWaterTransmission(vec3 origin,vec3 direction,vec3 interfaceNormal,out float opticalPath){
    opticalPath=0.0;
    float maximum=min(160.0,max(far,24.0));
    if(direction.z>0.00001)maximum=min(maximum,max(0.0,(-0.12-origin.z)/direction.z));
    if(maximum<0.03)return vec4(0.0);
    vec3 beginPoint=origin+direction*0.025,endPoint=origin+direction*maximum;
    vec4 a=gbufferProjection*vec4(beginPoint,1.0),b=gbufferProjection*vec4(endPoint,1.0);
    float ka=1.0/max(a.w,0.00001),kb=1.0/max(b.w,0.00001);
    vec2 pa=a.xy*ka*0.5+0.5,pb=b.xy*kb*0.5+0.5;
    vec3 qa=beginPoint*ka,qb=endPoint*kb;
    vec2 delta=pb-pa;
    float visible=1.0;
    for(int axis=0;axis<2;axis++){
        if(delta[axis]>0.00001)visible=min(visible,(0.998-pa[axis])/delta[axis]);
        else if(delta[axis]<-0.00001)visible=min(visible,(0.002-pa[axis])/delta[axis]);
    }
    visible=clamp(visible,0.0,1.0);pb=mix(pa,pb,visible);qb=mix(qa,qb,visible);kb=mix(ka,kb,visible);
#if REFRACTION_QUALITY == 2
    const int maximumSamples=256;
    const float pixelStride=2.0;
#elif REFRACTION_QUALITY == 1
    const int maximumSamples=96;
    const float pixelStride=4.0;
#else
    const int maximumSamples=32;
    const float pixelStride=8.0;
#endif
    int samples=int(clamp(ceil(length((pb-pa)*viewportSize())/pixelStride),8.0,float(maximumSamples)));
    float previous=0.0,previousError=-1.0;
    for(int i=1;i<=maximumSamples;i++){
        if(i>samples)break;
        float f=float(i)/float(samples);
        vec2 uv=mix(pa,pb,f);
        if(min(uv.x,uv.y)<0.001||max(uv.x,uv.y)>0.999)break;
        vec3 point=mix(qa,qb,f)/mix(ka,kb,f);
        float error=refractionDepthError(point,uv);
        if(error>=0.0&&previousError<0.0){
            float left=previous,right=f;
            for(int refine=0;refine<8;refine++){
                float middle=(left+right)*0.5;
                vec2 testUV=mix(pa,pb,middle);
                vec3 testPoint=mix(qa,qb,middle)/mix(ka,kb,middle);
                if(refractionDepthError(testPoint,testUV)>=0.0)right=middle;else left=middle;
            }
            vec2 hitUV=mix(pa,pb,right);
            float hitDepth=texture(depthtex1,hitUV).r;
            vec3 receiver=positionFromDepth(hitUV,hitDepth);
            ivec2 receiverCell=clamp(ivec2(hitUV*vec2(textureSize(colortex10,0))),ivec2(0),textureSize(colortex10,0)-ivec2(1));
            vec4 receiverData=texelFetch(colortex10,receiverCell,0);
            vec3 n=unitVector(mat3(gbufferModelView)*receiverData.xyz);
            float denominator=dot(direction,n);
            float distance=abs(denominator)>0.00001?dot(receiver-origin,n)/denominator:-1.0;
            vec3 candidate=origin+direction*max(distance,0.0);
            vec2 candidateUV;
            bool projected=refractionProjection(candidate,candidateUV);
            if(projected&&distance>0.02&&distance<maximum&&receiverData.a>0.5){
                float candidateDepth=texture(depthtex1,candidateUV).r;
                vec3 actual=positionFromDepth(candidateUV,candidateDepth);
                float residual=length(actual-candidate);
                float tolerance=0.045+0.0015*length(candidate);
                // The endpoint must lie on the transmitted side of the water;
                // foreground banks must never smear across a water silhouette.
                bool transmittedSide=dot(actual-origin,interfaceNormal)<0.02;
                if(candidateDepth<0.999999&&residual<tolerance&&transmittedSide){
                    vec2 border=min(candidateUV,1.0-candidateUV);
                    float confidence=1.0-smoothstep(tolerance*0.35,tolerance,residual);
                    confidence*=smoothstep(0.002,0.018,min(border.x,border.y));
                    opticalPath=distance;
                    return vec4(texture(colortex4,candidateUV).rgb,confidence);
                }
            }
        }
        previous=f;previousError=error;
    }
    return vec4(0.0);
}
#endif
