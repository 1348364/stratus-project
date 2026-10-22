from pathlib import Path
r=Path('outputs/Stratus/shaders');c=r/'core'
# Insert a depth-aware water resolve before the independent atmosphere passes.
for folder in [r,r/'world-1',r/'world1']:
 for n in range(5,1,-1):
  for ext in ['fsh','vsh']:
   (folder/f'composite{n+1}.{ext}').write_bytes((folder/f'composite{n}.{ext}').read_bytes())
 dim=0 if folder==r else (-1 if folder.name=='world-1' else 1)
 (folder/'composite2.fsh').write_text(f'#version 330 compatibility\n#define DIMENSION_TYPE {dim}\n#include "/core/water-resolve.frag.glsl"\n')
 (folder/'composite2.vsh').write_bytes((folder/'composite1.vsh').read_bytes())
p=c/'lake.frag.glsl';s=p.read_text().replace('/* RENDERTARGETS: 3 */','/* RENDERTARGETS: 12 */').replace('vec3 overlay=image-originalOpaque;','').replace('image=mix(transmitted,reflected,weight)+overlay;','image=mix(transmitted,reflected,weight);');p.write_text(s)
p=c/'resolve.frag.glsl';s=p.read_text().replace('const int colortex11Format = RGBA16F;','const int colortex11Format = RGBA16F;\nconst int colortex12Format = RGBA16F;');p.write_text(s)
p=c/'options.glsl';s=p.read_text().replace('#define ATMOSPHERE_QUALITY 1 // [0 1 2]','#define ATMOSPHERE_QUALITY 1 // [0 1 2]\n#define WATER_RENDER_QUALITY 1 // [0 1 2]');p.write_text(s)
p=r/'shaders.properties';s=p.read_text().replace('screen.REFRACTION=WATER_DISTORTION','screen.REFRACTION=WATER_RENDER_QUALITY WATER_DISTORTION').replace('screen.PERFORMANCE=ATMOSPHERE_QUALITY','screen.PERFORMANCE=WATER_RENDER_QUALITY ATMOSPHERE_QUALITY').replace('blend.composite5=off','blend.composite5=off\nblend.composite6=off')
for name,val in [('FAST','0'),('BALANCED','1'),('REFERENCE','2'),('HIGH','2')]:s=s.replace('profile.'+name+'=','profile.'+name+'=WATER_RENDER_QUALITY:'+val+' ')
s+='\n# Water optics scale independently; opaque geometry and underwater receivers stay sharp.\n#if WATER_RENDER_QUALITY == 2\nsize.buffer.colortex12=1.0 1.0\n#elif WATER_RENDER_QUALITY == 1\nsize.buffer.colortex12=0.5 0.5\n#else\nsize.buffer.colortex12=0.35 0.35\n#endif\n';p.write_text(s)
p=r/'lang/en_us.lang';s=p.read_text();s+='\noption.WATER_RENDER_QUALITY=Water render quality\noption.WATER_RENDER_QUALITY.comment=Resolution of water surface optics. Balanced uses half resolution with depth and normal aware reconstruction. Opaque terrain and submerged blocks seen directly remain full resolution.\nvalue.WATER_RENDER_QUALITY.0=Fast\nvalue.WATER_RENDER_QUALITY.1=Balanced\nvalue.WATER_RENDER_QUALITY.2=Full resolution\n';p.write_text(s)
