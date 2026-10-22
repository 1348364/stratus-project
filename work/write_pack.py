from pathlib import Path
root=Path('outputs/Willow-Mist/shaders')
programs={
'gbuffers_basic':['FOGGED','MASK'],
'gbuffers_textured':['TEXTURED','FOGGED','MASK'],
'gbuffers_textured_lit':['TEXTURED','LIT','FOGGED','MASK'],
'gbuffers_skybasic':['HIDE_SKY'],
'gbuffers_skytextured':['HIDE_SKY'],
'gbuffers_clouds':['HIDE_SKY'],
'gbuffers_terrain':['TEXTURED','LIT','FOGGED','MATERIAL','MASK'],
'gbuffers_block':['TEXTURED','LIT','FOGGED','ENTITY','MASK'],
'gbuffers_entities':['TEXTURED','LIT','FOGGED','ENTITY','MASK'],
'gbuffers_hand':['TEXTURED','LIT','ENTITY','HAND','MASK'],
'gbuffers_hand_water':['TEXTURED','LIT','ENTITY','HAND'],
'gbuffers_water':['TEXTURED','LIT','FOGGED','MATERIAL','WATER'],
'gbuffers_weather':['TEXTURED','LIT','FOGGED'],
'gbuffers_damagedblock':['TEXTURED'],
'gbuffers_armor_glint':['TEXTURED','EMISSIVE'],
'gbuffers_spidereyes':['TEXTURED','EMISSIVE'],
'gbuffers_beaconbeam':['TEXTURED','FOGGED','EMISSIVE'],
}
for folder,dimension in (('', 'OVERWORLD'),('world-1','NETHER'),('world1','END')):
    dest=root/folder;dest.mkdir(exist_ok=True)
    for name,features in programs.items():
        for stage in ('vsh','fsh'):
            source='#version 330 compatibility\n\n'
            source+=f'#define WM_{dimension}\n'
            source+=''.join(f'#define WM_{x}\n' for x in features)
            source+=f'#include "/lib/geometry.{stage}"\n'
            (dest/f'{name}.{stage}').write_text(source)
    for name in ('deferred','final'):
        for stage in ('vsh','fsh'):
            lib='fullscreen.vsh' if stage=='vsh' else f'{name}.fsh'
            (dest/f'{name}.{stage}').write_text(f'#version 330 compatibility\n#define WM_{dimension}\n#include "/lib/{lib}"\n')
properties='''# Willow Mist 2.0: reference-driven, shadowless, matte solid materials.
# AO is controlled independently by ambientOcclusionLevel; no separateAo bug.
oldLighting=false
separateAo=false
clouds=off
sun=false
moon=false
stars=false
sky=false
vignette=false
underwaterOverlay=false

screen=<profile> [LIGHTING] [CLOUDS] [FOG] [WATER]
screen.columns=2
screen.LIGHTING=AMBIENT_BRIGHTNESS ambientOcclusionLevel COLOUR_TEMPERATURE SATURATION BLOCKLIGHT_BRIGHTNESS BLOCKLIGHT_WARMTH
screen.CLOUDS=CLOUD_COVERAGE CLOUD_SCALE CLOUD_IRREGULARITY CLOUD_SHADING CLOUD_SPEED CLOUD_QUALITY
screen.FOG=FOG_DENSITY FOG_HEIGHT FOG_FALLOFF FOG_START FOG_QUALITY
screen.WATER=WATER_REFLECTION REFLECTION_QUALITY REFLECTION_DISTANCE WATER_TRANSPARENCY WATER_ABSORPTION RIPPLE_STRENGTH RIPPLE_SCALE RIPPLE_SPEED
sliders=AMBIENT_BRIGHTNESS ambientOcclusionLevel COLOUR_TEMPERATURE SATURATION BLOCKLIGHT_BRIGHTNESS BLOCKLIGHT_WARMTH CLOUD_COVERAGE CLOUD_SCALE CLOUD_IRREGULARITY CLOUD_SHADING CLOUD_SPEED FOG_DENSITY FOG_HEIGHT FOG_FALLOFF FOG_START WATER_REFLECTION REFLECTION_DISTANCE WATER_TRANSPARENCY WATER_ABSORPTION RIPPLE_STRENGTH RIPPLE_SCALE RIPPLE_SPEED

# All profiles retain exactly the same colour, AO, density, water and movement defaults.
profile.FAST=CLOUD_QUALITY:1 FOG_QUALITY:1 REFLECTION_QUALITY:0
profile.REFERENCE=CLOUD_QUALITY:2 FOG_QUALITY:2 REFLECTION_QUALITY:1
profile.HIGH=CLOUD_QUALITY:3 FOG_QUALITY:3 REFLECTION_QUALITY:2
blend.deferred=off
blend.final=off
'''
for program,features in programs.items():
    if 'MASK' in features: properties+=f'blend.{program}.colortex1=off\n'
(root/'shaders.properties').write_text(properties)
(root/'block.properties').write_text('''# Water alone receives environmental reflections. Lava is not water.
block.1001=minecraft:water
# Lanterns are emissive but excluded from the reflection mask.
block.1002=minecraft:lantern
block.1003=minecraft:torch minecraft:wall_torch minecraft:glowstone minecraft:sea_lantern minecraft:shroomlight minecraft:lava
''')
labels={
'AMBIENT_BRIGHTNESS':('Ambient brightness','Scales sky-lit surfaces while retaining Minecraft lightmap levels.'),
'ambientOcclusionLevel':('Ambient occlusion','Independent amount of vanilla corner/contact shading; lower keeps foliage open.'),
'COLOUR_TEMPERATURE':('Colour temperature','Small fixed balance adjustment. Zero keeps neutral foreground colours.'),
'SATURATION':('Saturation','Subtle global colour saturation; all presets use the same value.'),
'CLOUD_COVERAGE':('Cloud coverage','One produces an unbroken grey ceiling. Lower values soften toward blue-grey sky.'),
'CLOUD_SCALE':('Cloud band scale','World size of broad cloud forms, in approximate blocks.'),
'CLOUD_IRREGULARITY':('Cloud irregularity','Broad domain warping breaks up the elongated cloud layers.'),
'CLOUD_SHADING':('Cloud shading','Contrast within the overcast ceiling; no sharp puffy clouds.'),
'CLOUD_SPEED':('Cloud movement','Slow world-anchored drift. Zero freezes movement.'),
'CLOUD_QUALITY':('Cloud samples','Additional low-frequency detail; does not alter the colour palette.'),
'FOG_DENSITY':('Valley mist density','Outdoor mist amount. Fluid and status fog remain controlled by Minecraft.'),
'FOG_HEIGHT':('Mist layer altitude','World Y of the lower mist layer; move this for high-altitude terrain.'),
'FOG_FALLOFF':('Mist height falloff','How slowly the mist density decreases above the valley.'),
'FOG_START':('Clear foreground distance','Mist starts gradually beyond this distance, in blocks.'),
'FOG_QUALITY':('Mist samples','Spatial integration accuracy, with the same density and layer settings.'),
'WATER_REFLECTION':('Water reflection strength','Reflection and sky sheen on water top faces only. Solids stay matte.'),
'REFLECTION_QUALITY':('Terrain reflection quality','Fast uses sky only; Reference traces 24 steps; High traces 48 steps.'),
'REFLECTION_DISTANCE':('Reflection ray distance','Maximum terrain ray length. Missing scenery fades to the procedural sky.'),
'WATER_TRANSPARENCY':('Shallow water clarity','Controls visibility at the shore; deeper water still absorbs colour.'),
'WATER_ABSORPTION':('Water absorption','Depth-dependent loss of visibility, strongest in the red channel.'),
'RIPPLE_STRENGTH':('Ripple strength','Small water normal changes; shorelines and block geometry stay fixed.'),
'RIPPLE_SCALE':('Ripple frequency','Spatial frequency of the three unequal ripple layers.'),
'RIPPLE_SPEED':('Ripple speed','Surface movement speed. Zero freezes water shading.'),
'BLOCKLIGHT_BRIGHTNESS':('Block-light brightness','Lightmap block light and emissive interiors; no large bloom halo.'),
'BLOCKLIGHT_WARMTH':('Block-light warmth','Amber light temperature, strongest away from daylight.'),
}
lang='''profile.FAST=Fast
profile.REFERENCE=Reference
profile.HIGH=High
screen.LIGHTING=Light and colour
screen.CLOUDS=Overcast sky
screen.FOG=Layered valley mist
screen.WATER=Water
value.REFLECTION_QUALITY.0=Sky only
value.REFLECTION_QUALITY.1=Reference (24 steps)
value.REFLECTION_QUALITY.2=High (48 steps)
'''
for key,(label,comment) in labels.items(): lang+=f'option.{key}={label}\noption.{key}.comment={comment}\n'
(root/'lang/en_us.lang').write_text(lang)
print('Wrote 19 program pairs in each of 3 dimension routes, properties, material mapping and 25 controls.')
