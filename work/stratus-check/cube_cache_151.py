from pathlib import Path
r=Path('outputs/Stratus/shaders');c=r/'core'
(c/'optics-cube.glsl').write_text('''#ifndef STRATUS_OPTICS_CUBE
#define STRATUS_OPTICS_CUBE
// Six camera-centred 90 degree views share one 3 by 2 atlas.
vec3 cubeForward(int face){
 if(face==0)return vec3(1,0,0);if(face==1)return vec3(-1,0,0);
 if(face==2)return vec3(0,1,0);if(face==3)return vec3(0,-1,0);
 return face==4?vec3(0,0,1):vec3(0,0,-1);
}
vec3 cubeRight(int face){return face<2?vec3(0,0,1):vec3(1,0,0);}
vec3 cubeUp(int face){return cross(cubeForward(face),cubeRight(face));}
vec3 cubeCoordinates(vec3 p,int face){return vec3(dot(p,cubeRight(face)),dot(p,cubeUp(face)),dot(p,cubeForward(face)));}
vec2 cubeTile(int face){return vec2(face%3,face/3);}
vec2 cubeAtlas(vec2 uv,int face){return (cubeTile(face)+uv)/vec2(3,2);}
vec3 cubeRay(vec2 uv,int face){return cubeForward(face)+cubeRight(face)*(uv.x*2.-1.)+cubeUp(face)*(uv.y*2.-1.);}
#endif
''')
p=c/'optics-cache.vert.glsl';s=p.read_text();s=s.replace('out vec','out vec').replace('cacheTint','vertexTint').replace('cacheUV','vertexUV').replace('cacheLight','vertexLight').replace('cachePoint','vertexPoint').replace('cacheNormal','vertexNormal').replace('cacheMaterial','vertexMaterial');s=s[:s.index('    // Independent wide')]+'''    gl_Position=p;
}
''';p.write_text(s)
(c/'optics-cache.geom.glsl').write_text('''#include "/core/optics-cube.glsl"
layout(triangles)in;
layout(triangle_strip,max_vertices=18)out;
in vec4 vertexTint[];in vec2 vertexUV[];in vec2 vertexLight[];
in vec3 vertexPoint[];in vec3 vertexNormal[];flat in int vertexMaterial[];
out vec4 cacheTint;out vec2 cacheUV;out vec2 cacheLight;
out vec3 cachePoint;out vec3 cacheNormal;flat out int cacheMaterial;flat out int cacheFace;
void main(){
 for(int face=0;face<6;face++){
  bool visible=false;
  for(int i=0;i<3;i++)if(cubeCoordinates(vertexPoint[i],face).z>0.025)visible=true;
  if(!visible)continue;
  for(int i=0;i<3;i++){
   vec3 p=cubeCoordinates(vertexPoint[i],face);float w=p.z;
   vec2 tile=cubeTile(face);
   vec2 atlasClip=vec2((p.x+(tile.x*2.+1.)*w)/3.-w,(p.y+(tile.y*2.+1.)*w)/2.-w);
   gl_Position=vec4(atlasClip,1.000500125*w-0.100025006,w);
   cacheTint=vertexTint[i];cacheUV=vertexUV[i];cacheLight=vertexLight[i];
   cachePoint=vertexPoint[i];cacheNormal=vertexNormal[i];cacheMaterial=vertexMaterial[i];cacheFace=face;
   EmitVertex();
  }
  EndPrimitive();
 }
}
''')
for d in ('','world-1','world1'):
 (r/d/'shadow.gsh').write_text('#version 330 compatibility\n#include "/core/optics-cache.geom.glsl"\n')
p=c/'optics-cache.frag.glsl';s=p.read_text().replace('flat in int cacheMaterial;','flat in int cacheMaterial;\nflat in int cacheFace;\n#include "/core/optics-cube.glsl"');s=s.replace('void main(){','''void main(){
    vec2 tilePixel=gl_FragCoord.xy/float(shadowMapResolution)*vec2(3,2)-cubeTile(cacheFace);
    if(min(tilePixel.x,tilePixel.y)<0.0||max(tilePixel.x,tilePixel.y)>=1.0)discard;''');s=s.replace('-(gbufferModelView*vec4(cachePoint,1.0)).z','length(cachePoint)');p.write_text(s)
p=c/'scene-trace.glsl';s=p.read_text().replace('uniform sampler2D colortex10;','#include "/core/optics-cube.glsl"\nuniform sampler2D colortex10;\nint opticsFace=0;')
s=s.replace('return cache?textureSize(shadowcolor1,0):textureSize(depthtex1,0);','return cache?textureSize(shadowcolor1,0)/ivec2(3,2):textureSize(depthtex1,0);')
s=s.replace('texelFetch(shadowcolor0,cell,0).rgb','texelFetch(shadowcolor0,cell+ivec2(cubeTile(opticsFace))*opticsSize(true),0).rgb')
a=s.index('    vec4 q=gbufferProjection');b=s.index('\n    float d=texelFetch',a)
s=s[:a]+'''    if(cache){
        vec3 pWorld=mat3(gbufferModelViewInverse)*p;
        vec3 q=cubeCoordinates(pWorld,opticsFace);
        uv=q.xy/max(q.z,0.00001)*0.5+0.5;
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
        return mat3(gbufferModelView)*normalize(cubeRay(uv,opticsFace))*radius;
    }'''+s[b:]
s=s.replace('vec4 traceOpticalScene(', 'vec4 traceOpticalSegment(')
s=s.replace('bool cache,out float path){\n    path=0.0;','bool cache,float minimum,out float path){\n    path=0.0;')
s=s.replace('if(direction.z>0.00001)', 'if(!cache&&direction.z>0.00001)')
s=s.replace('vec3 start=origin+direction*0.025','vec3 start=origin+direction*max(minimum,0.025)')
s=s.replace('float ka=1.0/max(a.w,0.00001)', '''if(cache){
        vec3 p=cubeCoordinates(mat3(gbufferModelViewInverse)*start,opticsFace);
        vec3 q=cubeCoordinates(mat3(gbufferModelViewInverse)*end,opticsFace);
        a=vec4(p.xy,0.0,p.z);b=vec4(q.xy,0.0,q.z);
    }
    float ka=1.0/max(a.w,0.00001)''')
s=s.replace('float projectionScale=cache?3.0:1.0;', 'float projectionScale=1.0;')
s=s.replace('if(side>0)coverage*=1.0-smoothstep(maximum*0.8,maximum,distance);','// A cube face border is a seam, not missing scene coverage.\n                    if(cache)coverage=1.0;')
s=s.replace('\n#endif','''
// Clip the ray to each cube pyramid, then perform perspective-correct DDA
// within it. This includes terrain behind the eye and below the waterline.
bool opticsClip(float a,float b,inout float lo,inout float hi){
 if(abs(b)<0.0000001)return a>=0.0;
 float t=-a/b;if(b>0.0)lo=max(lo,t);else hi=min(hi,t);return hi>lo;
}
vec4 traceOpticalScene(vec3 origin,vec3 direction,vec3 interfaceNormal,int side,int quality,float maximum,bool cache,out float path){
 if(!cache)return traceOpticalSegment(origin,direction,interfaceNormal,side,quality,maximum,false,0.025,path);
 vec3 worldOrigin=mat3(gbufferModelViewInverse)*origin,worldDirection=mat3(gbufferModelViewInverse)*direction;
 vec4 best=vec4(0.0);float nearest=maximum+1.0;path=0.0;
 for(int face=0;face<6;face++){
  vec3 o=cubeCoordinates(worldOrigin,face),d=cubeCoordinates(worldDirection,face);
  float lo=0.025,hi=maximum;
  bool inside=opticsClip(o.z-0.05,d.z,lo,hi);
  inside=inside&&opticsClip(o.z-o.x,d.z-d.x,lo,hi)&&opticsClip(o.z+o.x,d.z+d.x,lo,hi);
  inside=inside&&opticsClip(o.z-o.y,d.z-d.y,lo,hi)&&opticsClip(o.z+o.y,d.z+d.y,lo,hi);
  if(!inside||hi<=lo||lo>=nearest)continue;
  opticsFace=face;float distance;
  vec4 hit=traceOpticalSegment(origin,direction,interfaceNormal,side,quality,hi,true,lo+0.0001,distance);
  if(hit.a>0.0&&distance<nearest){best=hit;nearest=distance;path=distance;}
 }
 return best;
}
#endif''')
p.write_text(s)
# Increase fine erosion and variation within connected large islands.
p=c/'ceiling.glsl';s=p.read_text();s=s.replace('vec3 point=vec3(xz.x*0.88,','vec3 point=vec3(xz.x*1.75,').replace('xz.y*0.88);','xz.y*1.75);');s=s.replace('mix(volume.g,volume.r,0.32)','mix(volume.g,volume.r,0.58)');s=s.replace('smoothstep(0.22,0.54,shape+island*0.25-cap*0.45)','smoothstep(0.37,0.70,shape+island*0.13-cap*0.52)');s=s.replace('point*3.17','point*4.37').replace('pores*(0.18+0.20*(1.0-bulk))','pores*(0.35+0.22*(1.0-bulk))');p.write_text(s)
print('Six-face scene cache and stronger porous cloud structure prepared.')
