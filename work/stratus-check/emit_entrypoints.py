from pathlib import Path

destination = Path('outputs/Stratus/shaders')
routes = {
    'gbuffers_basic': (0, 0),
    'gbuffers_textured': (1, 0),
    'gbuffers_textured_lit': (2, 0),
    'gbuffers_terrain': (3, 0),
    'gbuffers_block': (4, 0),
    'gbuffers_entities': (4, 0),
    'gbuffers_hand': (5, 0),
    'gbuffers_hand_water': (5, 1),
    'gbuffers_water': (6, 1),
    'gbuffers_weather': (7, 1),
    'gbuffers_skybasic': (8, 0),
    'gbuffers_skytextured': (8, 0),
    'gbuffers_clouds': (8, 0),
    'gbuffers_damagedblock': (9, 0),
    'gbuffers_armor_glint': (9, 0),
    'gbuffers_spidereyes': (10, 0),
    'gbuffers_beaconbeam': (1, 0),
}

for directory, dimension in (('', 0), ('world-1', -1), ('world1', 1)):
    folder = destination / directory
    folder.mkdir(exist_ok=True)
    for entry, (kind, late) in routes.items():
        definitions = f'#define DIMENSION_TYPE {dimension}\n#define PASS_KIND {kind}\n#define LATE_SURFACE {late}\n'
        for extension, part in (('vsh', 'vert'), ('fsh', 'frag')):
            (folder / f'{entry}.{extension}').write_text(
                '#version 330 compatibility\n' + definitions + f'#include "/core/raster.{part}.glsl"\n')
    for entry, core in (('deferred', 'resolve'), ('composite', 'lake'), ('final', 'output')):
        definitions = f'#define DIMENSION_TYPE {dimension}\n'
        (folder / f'{entry}.vsh').write_text('#version 330 compatibility\n' + definitions + '#include "/core/screen.vert.glsl"\n')
        (folder / f'{entry}.fsh').write_text('#version 330 compatibility\n' + definitions + f'#include "/core/{core}.frag.glsl"\n')

properties = '''# Stratus: a standalone implementation of the attached visual specification.
clouds=off
sky=false
sun=false
moon=false
stars=false
vignette=false
underwaterOverlay=false
oldLighting=false
separateAo=false

screen=<profile> [SURFACES] [CEILING] [ATMOSPHERE] [LAKE]
screen.SURFACES=SKY_AMBIENT ambientOcclusionLevel WHITE_BALANCE SURFACE_SATURATION LAMP_LEVEL LAMP_HEAT
screen.CEILING=CLOUD_AMOUNT CLOUD_SPAN CLOUD_DISTORTION CLOUD_RELIEF CLOUD_DRIFT CLOUD_LAYERS
screen.ATMOSPHERE=MIST_AMOUNT MIST_Y MIST_THICKNESS MIST_CLEAR MIST_DETAIL
screen.LAKE=REFLECT_LEVEL REFLECTION_MODE REFLECT_RANGE WATER_VISIBILITY WATER_EXTINCTION RIPPLE_HEIGHT RIPPLE_SIZE RIPPLE_RATE
sliders=SKY_AMBIENT ambientOcclusionLevel WHITE_BALANCE SURFACE_SATURATION LAMP_LEVEL LAMP_HEAT CLOUD_AMOUNT CLOUD_SPAN CLOUD_DISTORTION CLOUD_RELIEF CLOUD_DRIFT MIST_AMOUNT MIST_Y MIST_THICKNESS MIST_CLEAR REFLECT_LEVEL REFLECT_RANGE WATER_VISIBILITY WATER_EXTINCTION RIPPLE_HEIGHT RIPPLE_SIZE RIPPLE_RATE
profile.FAST=CLOUD_LAYERS:1 MIST_DETAIL:1 REFLECTION_MODE:0
profile.REFERENCE=CLOUD_LAYERS:2 MIST_DETAIL:2 REFLECTION_MODE:1
profile.HIGH=CLOUD_LAYERS:3 MIST_DETAIL:3 REFLECTION_MODE:2
blend.deferred=off
blend.composite=off
blend.final=off
'''
for entry, (kind, late) in routes.items():
    if late:
        for target in (0, 1):
            properties += f'blend.{entry}.colortex{target}=SRC_ALPHA ONE_MINUS_SRC_ALPHA ONE ONE_MINUS_SRC_ALPHA\n'
    elif kind not in (8, 9):
        properties += f'blend.{entry}.colortex1=off\nblend.{entry}.colortex2=off\n'
(destination / 'shaders.properties').write_text(properties)
(destination / 'block.properties').write_text('''# Semantic material classification for the raster stage.
block.4100=minecraft:water
block.4101=minecraft:lantern
block.4102=minecraft:torch minecraft:wall_torch minecraft:glowstone minecraft:sea_lantern minecraft:shroomlight minecraft:lava
''')

controls = {
 'SKY_AMBIENT': ('Diffuse ambient brightness', 'Scales skylit surfaces, retaining the game lightmap and stable exposure.'),
 'ambientOcclusionLevel': ('Corner shading', 'Independent vanilla AO strength; does not raise exposure.'),
 'WHITE_BALANCE': ('Subtle white balance', 'Zero preserves neutral foreground colour.'),
 'SURFACE_SATURATION': ('Surface saturation', 'Fixed saturation adjustment, shared by every preset.'),
 'LAMP_LEVEL': ('Lantern and block light', 'Diffuse local brightness and emissive pixel interiors, without glow halos.'),
 'LAMP_HEAT': ('Local light warmth', 'A restrained amber bias where block lighting dominates.'),
 'CLOUD_AMOUNT': ('Overcast coverage', 'One keeps a complete soft grey-blue cloud ceiling.'),
 'CLOUD_SPAN': ('Cloud band size', 'Approximate world size of broad undulating cloud forms.'),
 'CLOUD_DISTORTION': ('Band irregularity', 'Varies curvature and spacing to break repeated stripes.'),
 'CLOUD_RELIEF': ('Cloud shade depth', 'Gentle internal light and dark bands; no storm towers.'),
 'CLOUD_DRIFT': ('Slow cloud drift', 'Zero freezes the world-anchored ceiling.'),
 'CLOUD_LAYERS': ('Cloud sampling', 'Adds low-frequency variation without changing colour controls.'),
 'MIST_AMOUNT': ('Valley mist density', 'Outdoor mist opacity. Cave surfaces without skylight reject valley mist.'),
 'MIST_Y': ('Lower mist altitude', 'World Y of the principal pale horizontal mist layer.'),
 'MIST_THICKNESS': ('Mist layer thickness', 'Vertical thickness of the two smooth density layers.'),
 'MIST_CLEAR': ('Clear foreground range', 'Near-camera ray length excluded from outdoor mist.'),
 'MIST_DETAIL': ('Mist spatial variation', 'Sampling detail for broad horizontal density patches.'),
 'REFLECT_LEVEL': ('Water reflection amount', 'Environment reflections apply only to top-facing water.'),
 'REFLECTION_MODE': ('Scenery reflection quality', 'Fast: sky only. Reference: 22 trace samples. High: 46 samples.'),
 'REFLECT_RANGE': ('Scenery trace distance', 'Misses fade to the procedural sky, including at screen borders.'),
 'WATER_VISIBILITY': ('Water clarity', 'Shore visibility decreases continuously with depth.'),
 'WATER_EXTINCTION': ('Depth absorption', 'Depth-dependent colour absorption; no blur or caustics.'),
 'RIPPLE_HEIGHT': ('Ripple strength', 'Shading normal amplitude. Water geometry remains vanilla.'),
 'RIPPLE_SIZE': ('Ripple spacing', 'Scale of the four unequal spectral wave components.'),
 'RIPPLE_RATE': ('Ripple speed', 'Zero freezes all surface movement.'),
}
language = '''profile.FAST=Fast
profile.REFERENCE=Reference
profile.HIGH=High
screen.SURFACES=Diffuse surfaces
screen.CEILING=Overcast ceiling
screen.ATMOSPHERE=Layered mist
screen.LAKE=Reflective water
value.REFLECTION_MODE.0=Sky only
value.REFLECTION_MODE.1=Reference
value.REFLECTION_MODE.2=High
'''
for key, (label, detail) in controls.items():
    language += f'option.{key}={label}\noption.{key}.comment={detail}\n'
(destination / 'lang/en_us.lang').write_text(language)
print('Stratus entry points generated: 60 program pairs, 25 controls, three quality presets.')
