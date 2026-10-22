from pathlib import Path
S=Path('outputs/Stratus/shaders'); C=S/'core'
def edit(n,a,b):
 p=C/n;s=p.read_text();assert a in s,(n,a);p.write_text(s.replace(a,b))
edit('options.glsl','#define WATER_VISIBILITY 0.35','#define WATER_VISIBILITY 1.70')
edit('options.glsl','#define FACE_BLEND 0.50','#define FACE_BLEND 1.00')
edit('options.glsl','#define REFLECT_LEVEL 0.85','#define REFLECT_LEVEL 1.00')
edit('options.glsl','#endif','''#define CLOUD_STYLE 0 // [0 1 2]
#define SUN_STYLE 0 // [0 1]
#define WATER_TURBIDITY 1.00 // [0.00 0.50 1.00 1.50 2.00]
#define BIOME_WATER 1 // [0 1]
#endif''')
edit('frame.glsl','uniform int worldTime;','''uniform int worldTime;
uniform vec3 biomeWaterTint;
uniform float biomeSilt;
uniform float biomeHumidity;
uniform float biomeWarmth;
uniform ivec2 eyeBrightnessSmooth;''')
# Water tint uses its own late metadata attachment, so particles cannot erase it.
edit('raster.frag.glsl','/* RENDERTARGETS: 3,0,1,2 */','/* RENDERTARGETS: 3,0,1,2,8 */')
edit('raster.frag.glsl','#if PASS_KIND == 8\n    discard;','''#if PASS_KIND == 8 || (PASS_KIND == 12 && SUN_STYLE == 0) || (PASS_KIND == 13 && CLOUD_STYLE != 1)
    discard;''')
edit('raster.frag.glsl','#if PASS_KIND == 3 || BLOCK_SURFACE == 1\n    reflectable = float(category < 1.5);','#if PASS_KIND == 3 || PASS_KIND == 4 || PASS_KIND == 10 || BLOCK_SURFACE == 1\n    reflectable = 1.0;')
edit('raster.frag.glsl','    gl_FragData[0] = vec4(colour, surface.a);','''    gl_FragData[0] = vec4(colour, surface.a);
    gl_FragData[4] = vec4(0.0);
#if PASS_KIND == 6
    if(mark>0.5)gl_FragData[4]=vec4(tintAndOpacity.rgb,clamp((illuminationCoordinate.s*32.0-1.0)/30.0,0.0,1.0));
#endif''')
edit('raster.frag.glsl','    gl_FragData[2] = vec4(0.0);\n    gl_FragData[3] = vec4(0.0);','''    gl_FragData[2] = vec4(unitVector(orientedNormal),float(category>1.05&&category<1.5));
    gl_FragData[3] = vec4(wetMaterialProperties(material),0.0,0.0);''')
# Dampness is resolved with visible cavity geometry, rather than uniform coating.
edit('diffuse.glsl','float moisture = clamp(outdoorMoisture(skyExposure, kind), 0.0, 1.0);','float moisture = 0.0; // Contact-aware moisture is applied by the opaque resolve.')
for folder in [S,S/'world-1',S/'world1']:
 for name,kind in [('gbuffers_clouds',13),('gbuffers_skytextured',12)]:
  for ext in ['vsh','fsh']:
   p=folder/(name+'.'+ext);p.write_text(p.read_text().replace('#define PASS_KIND 8',f'#define PASS_KIND {kind}'))
 # Cache a small directional cloud environment before water, independent of view orientation.
 dim=0 if folder==S else (-1 if folder.name=='world-1' else 1)
 for ext,core in [('vsh','screen.vert'),('fsh','environment.frag')]:
  (folder/('deferred1.'+ext)).write_text(f'#version 330 compatibility\n#define DIMENSION_TYPE {dim}\n#include "/core/{core}.glsl"\n')
edit('resolve.frag.glsl','#include "/core/ceiling.glsl"','#include "/core/ceiling.glsl"\n#include "/core/diffuse.glsl"')
edit('resolve.frag.glsl','uniform sampler2D colortex0;','uniform sampler2D colortex0;\nuniform sampler2D colortex1;\nuniform sampler2D colortex2;\n#include "/core/moisture.glsl"')
edit('resolve.frag.glsl','const int colortex7Format = RGBA16F;','const int colortex7Format = RGBA16F;\nconst int colortex8Format = RGBA16F;\nconst int colortex9Format = RGBA16F;')
edit('resolve.frag.glsl','/* RENDERTARGETS: 3,4,0,1,2 */','/* RENDERTARGETS: 3,4,0,1,2,8 */')
edit('resolve.frag.glsl','layout(location = 4) out vec4 emptyWaterDepth;','layout(location = 4) out vec4 emptyWaterDepth;\nlayout(location = 5) out vec4 emptyWaterTint;')
edit('resolve.frag.glsl','    resolvedScene = vec4(radiance, 1.0);','''    if(geometry)radiance=retainedMoisture(radiance,viewPoint,rasterUV);
    emptyWaterTint=vec4(0.0);
    resolvedScene = vec4(radiance, 1.0);''')
p=S/'shaders.properties';s=p.read_text();s=s.replace('clouds=off','''#if CLOUD_STYLE == 1
clouds=fancy
#else
clouds=off
#endif''').replace('sun=false','''#if SUN_STYLE == 1
sun=true
moon=true
#else
sun=false
moon=false
#endif''').replace('\nmoon=false\nstars=false','\nstars=false')
a=s.index('screen=');b=s.index('sliders=')
s=s[:a]+'''# Familiar category/subcategory layout; every previous control remains accessible.
screen=<profile> <empty> [WATER] [LIGHTING] [ATMOSPHERE] [MATERIALS] [POST] [PERFORMANCE]
screen.columns=2
screen.WATER=WATER_VISIBILITY BIOME_WATER WATER_TURBIDITY WATER_EXTINCTION [REFLECTIONS] [WAVES]
screen.REFLECTIONS=REFLECT_LEVEL REFLECTION_MODE REFLECT_RANGE
screen.WAVES=WATER_DISTORTION RIPPLE_HEIGHT RIPPLE_SIZE RIPPLE_RATE
screen.LIGHTING=SKY_AMBIENT ambientOcclusionLevel FACE_SHADING FACE_BLEND GROUND_WARMTH LAMP_LEVEL LAMP_HEAT
screen.ATMOSPHERE=[CLOUDS] [SUN] [FOG]
screen.CLOUDS=CLOUD_STYLE CLOUD_LAYERS CLOUD_AMOUNT CLOUD_ALTITUDE CLOUD_THICKNESS CLOUD_SPAN CLOUD_DISTORTION CLOUD_RELIEF CLOUD_DRIFT CIRRUS_AMOUNT CIRRUS_ALTITUDE
screen.SUN=SUN_STYLE SUN_VISIBILITY SKY_LEAK
screen.FOG=MIST_AMOUNT MIST_Y MIST_THICKNESS MIST_CLEAR MIST_DETAIL
screen.MATERIALS=SURFACE_DAMPNESS WET_SHEEN
screen.POST=SURFACE_SATURATION WHITE_BALANCE BLOOM_STRENGTH BLOOM_RADIUS
screen.PERFORMANCE=CLOUD_LAYERS MIST_DETAIL REFLECTION_MODE REFLECT_RANGE
''' +s[b:]
s=s.replace('sliders=','sliders=WATER_TURBIDITY ')
s+='\nblend.deferred1=off\nsize.buffer.colortex9=192 96\n'
# Fixed tint attachment: non-water passes preserve it; water writes its nearest interface.
for name in ['gbuffers_basic','gbuffers_terrain','gbuffers_block','gbuffers_entities','gbuffers_item','gbuffers_hand','gbuffers_spidereyes','gbuffers_damagedblock','gbuffers_armor_glint','gbuffers_skytextured','gbuffers_clouds','gbuffers_water']:
 s+=f'blend.{name}.colortex8=off\n'
for name in ['gbuffers_textured','gbuffers_textured_lit','gbuffers_beaconbeam','gbuffers_hand_water','gbuffers_weather','gbuffers_particles','gbuffers_particles_translucent','gbuffers_entities_translucent','gbuffers_block_translucent']:
 s+=f'blend.{name}.colortex8=ZERO ONE ZERO ONE\n'
# Camera-biome properties are smoothed. Actual surface tint is per vertex across biome boundaries.
s+='''
uniform.float.biomeSilt=smooth(if(in(biome, BIOME_SWAMP, BIOME_MANGROVE_SWAMP), 1.0, in(biome, BIOME_RIVER), 0.32, in(biome, BIOME_LUSH_CAVES), 0.18, 0.05), 6, 6)
uniform.float.biomeHumidity=smooth(rainfall, 6, 6)
uniform.float.biomeWarmth=smooth(temperature, 6, 6)
variable.float.waterTintR=if(in(biome, BIOME_SWAMP), 0.38, in(biome, BIOME_MANGROVE_SWAMP), 0.227, in(biome, BIOME_WARM_OCEAN), 0.263, in(biome, BIOME_LUKEWARM_OCEAN, BIOME_DEEP_LUKEWARM_OCEAN), 0.271, in(biome, BIOME_COLD_OCEAN, BIOME_DEEP_COLD_OCEAN), 0.239, in(biome, BIOME_FROZEN_RIVER, BIOME_FROZEN_OCEAN, BIOME_DEEP_FROZEN_OCEAN), 0.224, 0.247)
variable.float.waterTintG=if(in(biome, BIOME_SWAMP), 0.482, in(biome, BIOME_MANGROVE_SWAMP), 0.478, in(biome, BIOME_WARM_OCEAN), 0.835, in(biome, BIOME_LUKEWARM_OCEAN, BIOME_DEEP_LUKEWARM_OCEAN), 0.678, in(biome, BIOME_COLD_OCEAN, BIOME_DEEP_COLD_OCEAN), 0.341, in(biome, BIOME_FROZEN_RIVER, BIOME_FROZEN_OCEAN, BIOME_DEEP_FROZEN_OCEAN), 0.22, 0.463)
variable.float.waterTintB=if(in(biome, BIOME_SWAMP), 0.392, in(biome, BIOME_MANGROVE_SWAMP), 0.416, in(biome, BIOME_WARM_OCEAN), 0.933, in(biome, BIOME_LUKEWARM_OCEAN, BIOME_DEEP_LUKEWARM_OCEAN), 0.949, in(biome, BIOME_COLD_OCEAN, BIOME_DEEP_COLD_OCEAN), 0.839, in(biome, BIOME_FROZEN_RIVER, BIOME_FROZEN_OCEAN, BIOME_DEEP_FROZEN_OCEAN), 0.788, 0.894)
uniform.vec3.biomeWaterTint=vec3(smooth(waterTintR,6,6),smooth(waterTintG,6,6),smooth(waterTintB,6,6))
'''
p.write_text(s)
p=S/'lang/en_us.lang';s=p.read_text();s+='''
screen.WATER=Water
screen.REFLECTIONS=Reflections
screen.WAVES=Waves and refraction
screen.LIGHTING=Lighting and shadows
screen.ATMOSPHERE=Atmosphere
screen.CLOUDS=Clouds
screen.SUN=Sun and moon
screen.FOG=Fog
screen.MATERIALS=Materials and dampness
screen.POST=Colour and bloom
screen.PERFORMANCE=Performance
option.CLOUD_STYLE=Cloud style
option.CLOUD_STYLE.comment=Stratus uses rounded world-space volumes. Vanilla uses Minecraft's actual fancy cloud geometry. Off hides both.
value.CLOUD_STYLE.0=Stratus volumetric
value.CLOUD_STYLE.1=Vanilla fancy
value.CLOUD_STYLE.2=Off
option.SUN_STYLE=Sun and moon style
option.SUN_STYLE.comment=Choose the soft overcast sun or Minecraft's original textured sun and moon.
value.SUN_STYLE.0=Stratus soft sun
value.SUN_STYLE.1=Vanilla textures
option.BIOME_WATER=Environment-aware water
option.BIOME_WATER.comment=Vanilla biome tint plus smoothed sediment, humidity, temperature, rain runoff and local cave lighting. These are visual approximations, not measured sediment data.
value.BIOME_WATER.0=Off
value.BIOME_WATER.1=On
option.WATER_TURBIDITY=Suspended sediment
option.WATER_TURBIDITY.comment=Scattering from suspended particles. Swamps and rainy rivers carry more sediment; sheltered cave water rejects rain runoff.
''';s=s.replace('Outdoor moisture','Retained surface moisture');p.write_text(s)
p=Path('outputs/Stratus/package.py');p.write_text(p.read_text().replace('Stratus-1.3.1.zip','Stratus-1.4.0.zip'))
