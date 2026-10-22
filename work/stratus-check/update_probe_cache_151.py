from pathlib import Path
p=Path('work/stratus-check/probe_151.py');s=p.read_text()
s=s.replace("s+='''vec3 transmissionProbe", "s+='''vec3 cacheProbe(vec3 origin,vec3 direction,vec3 normal,int side){float path;vec4 h=traceOpticalScene(origin,normalize(direction),normal,side,2,100.,true,path);return vec3(h.a,path,h.r);}\nvec3 transmissionProbe")
s=s.replace("('face_side','formIrradiance(vec3(1,0,0),1.)',1),", """('face_side','formIrradiance(vec3(1,0,0),1.)',1),
('face_z','formIrradiance(vec3(0,0,1),1.)',1),
('face_bottom','formIrradiance(vec3(0,-1,0),1.)',1),
('cache_offscreen_floor','cacheProbe(vec3(0,-1,-1),vec3(0,-1,-.1),vec3(0,1,0),-1)',1),
('cache_behind_eye_reflection','cacheProbe(vec3(0,1,-.5),vec3(0,-.6,.8),vec3(0,-1,0),1)',1),
('cache_upward_air_refraction','cacheProbe(vec3(0,1,-2),vec3(.1,.8,-.6),vec3(0,-1,0),-1)',1),
('cache_wrong_medium_rejected','cacheProbe(vec3(0,-1,-1),vec3(0,1,0),vec3(0,1,0),-1)',1),
('cloud_stationary_world_error','vec3(abs(physicalCloudLayer(vec3(200,100,200),vec3(0,1,0),7000.).a-physicalCloudLayer(vec3(200,110,200),vec3(0,1,0),6990.).a))',1),""")
s=s.replace('integer(p,"depthtex1",2);','integer(p,"shadowcolor0",5);integer(p,"shadowcolor1",6);integer(p,"depthtex1",2);')
s=s.replace('static void texture2(int unit,int channels,const float* data){','static void texture2size(int unit,int channels,const float* data,int width,int height){').replace('GL_RGBA32F,256,256,0','GL_RGBA32F,width,height,0')
s=s.replace('static void scene(void){','static void texture2(int unit,int channels,const float* data){texture2size(unit,channels,data,256,256);}\nstatic void scene(void){')
needle=' const char* path="outputs/Stratus/shaders/volumes/weather.rgba8";'
cube=''' float *cacheColour=calloc(1024*512*4,sizeof(float)),*cacheNormal=calloc(1024*512*4,sizeof(float));
 const float fw[6][3]={{1,0,0},{-1,0,0},{0,1,0},{0,-1,0},{0,0,1},{0,0,-1}};
 const float rt[6][3]={{0,0,1},{0,0,1},{1,0,0},{1,0,0},{1,0,0},{1,0,0}};
 for(int face=0;face<6;face++)for(int y=0;y<256;y++)for(int x=0;x<256;x++){
  float up[3]={fw[face][1]*rt[face][2]-fw[face][2]*rt[face][1],fw[face][2]*rt[face][0]-fw[face][0]*rt[face][2],fw[face][0]*rt[face][1]-fw[face][1]*rt[face][0]};
  float r[3],n[3]={0};for(int j=0;j<3;j++)r[j]=fw[face][j]+rt[face][j]*(2*(x+.5)/256-1)+up[j]*(2*(y+.5)/256-1);
  float t=1e5;int cube=0;
  for(int j=0;j<3;j++){float limit=j==1?4:16;float hit=limit/fmaxf(fabsf(r[j]),.000001);if(hit<t){t=hit;n[0]=n[1]=n[2]=0;n[j]=r[j]>0?-1:1;}}
  float lo[3]={-1,-4,-5},hi[3]={1,-2,-3},entry=0,exit=100,an[3]={0};int possible=1;
  for(int j=0;j<3;j++){if(fabsf(r[j])<.000001){if(0<lo[j]||0>hi[j])possible=0;continue;}float a=lo[j]/r[j],b=hi[j]/r[j],near=fminf(a,b);if(near>entry){entry=near;an[0]=an[1]=an[2]=0;an[j]=a<b?-1:1;}exit=fminf(exit,fmaxf(a,b));}
  if(possible&&entry<exit&&entry>0&&entry<t){t=entry;memcpy(n,an,sizeof n);cube=1;}
  int i=((face/4)*256+y)*1024+(face%4)*256+x;
  for(int j=0;j<3;j++)cacheNormal[i*4+j]=n[j];cacheNormal[i*4+3]=t*sqrtf(r[0]*r[0]+r[1]*r[1]+r[2]*r[2]);
  cacheColour[i*4]=cube?.9:.12;cacheColour[i*4+1]=cube?.2:.4;cacheColour[i*4+2]=cube?.1:.9;cacheColour[i*4+3]=1;
 }
 texture2size(5,4,cacheColour,1024,512);texture2size(6,4,cacheNormal,1024,512);free(cacheColour);free(cacheNormal);
'''
s=s.replace(needle,cube+needle);p.write_text(s)
