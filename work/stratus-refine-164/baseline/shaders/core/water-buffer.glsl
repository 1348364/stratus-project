#ifndef STRATUS_WATER_BUFFER_INCLUDED
#define STRATUS_WATER_BUFFER_INCLUDED
// Shared reconstruction for above-water and submerged interface reflections.
vec4 readWaterReflection(vec2 screen,vec3 faceNormal,float surfaceDepth){
    vec4 result=vec4(0.0);
#if REFLECTION_MODE != 0
#if REFLECTION_MODE == 2 && WATER_RENDER_QUALITY == 2
    result=texelFetch(colortex7,ivec2(gl_FragCoord.xy),0);
#else
    ivec2 size=textureSize(colortex7,0);
    vec2 grid=screen*vec2(size)-0.5;ivec2 cell=ivec2(floor(grid));vec2 fraction=fract(grid);
    float total=0.0;
    for(int y=0;y<2;y++)for(int x=0;x<2;x++){
        ivec2 c=clamp(cell+ivec2(x,y),ivec2(0),size-ivec2(1));
        vec2 uv=(vec2(c)+0.5)/vec2(size);
        vec4 depth=texture(colortex2,uv),normal=texture(colortex1,uv);
        float weight=(x==0?1.0-fraction.x:fraction.x)*(y==0?1.0-fraction.y:fraction.y);
        weight*=step(0.5,depth.a)*step(0.8,dot(normal.xyz,faceNormal));
        weight*=exp(-abs(depth.x-surfaceDepth)/max(0.25,surfaceDepth*0.02));
        result+=texelFetch(colortex7,c,0)*weight;total+=weight;
    }
    if(total>0.0001)result/=total;
#endif
    result.rgb/=max(result.a,0.0001);
#endif
    return result;
}
#endif
