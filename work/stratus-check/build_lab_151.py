"""Generate an original Creative shader showcase as a data-pack function."""
from pathlib import Path
import math,json,random
from nbt_local import load,save,Tag
world=Path('work/minecraft-smoke/saves/StratusShaderLab');pack=world/'datapacks/stratus_lab/data/stratus/function'
a=['forceload add -96 -96 95 95','gamemode creative @a','gamerule minecraft:advance_time false','gamerule minecraft:advance_weather false','gamerule minecraft:spawn_mobs false','gamerule minecraft:random_tick_speed 0','weather clear','time set 3000','kill @e[tag=stratus_lab]']
def cmd(s):a.append(s)
def fill(x,y,z,X,Y,Z,b):cmd(f'fill {x} {y} {z} {X} {Y} {Z} minecraft:{b}')
def block(x,y,z,b):cmd(f'setblock {x} {y} {z} minecraft:{b}')
def label(x,y,z,title,colour='gold'):
 text=json.dumps(title,ensure_ascii=False)
 cmd(f'summon minecraft:text_display {x} {y} {z} {{Tags:["stratus_lab"],billboard:"center",background:1073741824,view_range:1.0f,text:{{text:{text},color:"{colour}",bold:1b}},transformation:[0.7f,0f,0f,0f,0f,0.7f,0f,0f,0f,0f,0.7f,0f,0f,0f,0f,1f]}}')
def tree(x,z,kind='spruce',h=7):
 fill(x,64,z,x,63+h,z,kind+'_log')
 for dy,r in [(3,3),(5,2),(7,1)]:
  fill(x-r,63+dy,z-r,x+r,63+dy,z+r,kind+'_leaves[persistent=true]')
 block(x,64+h,z,kind+'_leaves[persistent=true]')
# Walkable frame, then the winding natural-style river cross-sections.
for x in [-88,88]:fill(x,63,-88,x+1,63,88,'stone_bricks')
for z in [-88,88]:fill(-88,63,z,88,63,z+1,'stone_bricks')
for z in range(-78,79):
 centre=round(16*math.sin(z*.045));width=11+round(2*math.sin(z*.13))
 left,right=centre-width,centre+width
 fill(left,59,z,right,66,z,'air')
 floor=56+int((z//12)%3==0)
 fill(left,floor,z,right,58,z,'gravel')
 fill(left+1,59,z,right-1,62,z,'water')
 for x in [left,left+1,right-1,right]:
  block(x,62,z,'sand');block(x,61,z,'sand')
 if z%9==0:fill(centre-3,58,z,centre+3,58,z,'smooth_stone')
 if z%17==0:block(centre,58,z,'diorite')
# Central timber bridge and waterfront details.
fill(-34,65,-9,34,65,-5,'spruce_planks')
for z in [-10,-4]:fill(-34,66,z,34,66,z,'spruce_fence')
for x in [-30,-15,0,15,30]:
 for z in [-9,-5]:
  fill(x,58,z,x,67,z,'stripped_spruce_log');block(x,68,z,'lantern')
for x in [-35,35]:
 for i in range(3):fill(x-i if x<0 else x+i,64+i//2,-8,x-i if x<0 else x+i,64+i//2,-6,'spruce_planks')
label(0,70,-7,'STRATUS · WATER & LIGHT','aqua')
# Submerged3D receivers follow the winding river's centre, not its bank.
fill(4,58,14,4,64,14,'oak_log')
fill(14,58,20,14,62,20,'spruce_log')
fill(4,60,14,17,60,14,'oak_log[axis=x]')
for i in range(5):block(9+i,58+i,18,'oak_stairs[facing=north,waterlogged=true]')
fill(15,60,23,19,60,23,'oak_slab[type=bottom,waterlogged=true]')
fill(8,59,24,11,61,24,'oak_fence[waterlogged=true]')
for x,b in [(6,'red_concrete'),(9,'yellow_concrete'),(12,'white_concrete'),(15,'blue_concrete')]:fill(x,58,33,x+1,61,34,b)
label(12,67,19,'SUBMERGED GEOMETRY','aqua')
label(12,65,36,'Look across the shore · then swim below','white')
# Three actual-biome ponds with different environments and submerged detail.
for z0,biome,title in [(-48,'swamp','SWAMP · MUD & ROOTS'),(0,'warm_ocean','WARM OCEAN · SAND & CORAL'),(48,'frozen_ocean','COLD WATER · STONE & ICE')]:
 for dz in range(-15,16):
  radius=round(17*math.sqrt(max(0.0,1-(dz/16)**2)))
  fill(60-radius,55,z0+dz,60+radius,64,z0+dz,'air')
  fill(60-radius,54,z0+dz,60+radius,55,z0+dz,'mud' if biome=='swamp' else ('sand' if biome=='warm_ocean' else 'stone'))
  if radius>1:fill(61-radius,56,z0+dz,59+radius,62,z0+dz,'water')
  block(60-radius,62,z0+dz,'mud' if biome=='swamp' else 'sand');block(60+radius,62,z0+dz,'mud' if biome=='swamp' else 'sand')
 cmd(f'fillbiome 40 40 {z0-20} 80 100 {z0+20} minecraft:{biome}')
 fill(42,64,z0-2,57,64,z0+1,'spruce_planks')
 for x in [44,55]:fill(x,55,z0,x,65,z0,'spruce_log');block(x,66,z0,'lantern')
 fill(61,56,z0,61,60,z0,'oak_log')
 label(60,68,z0-17,title,'aqua')
 if biome=='swamp':
  fill(65,56,z0+4,67,59,z0+6,'muddy_mangrove_roots');block(64,63,z0+4,'lily_pad')
 elif biome=='warm_ocean':
  for x,b in [(63,'brain_coral_block'),(66,'tube_coral_block'),(69,'horn_coral_block')]:fill(x,56,z0+4,x,57,z0+5,b)
 else:fill(68,63,z0+7,71,64,z0+9,'blue_ice')
# Material gallery, all six faces visible on freestanding cubes.
materials=['dirt','spruce_planks','stone','iron_ore','polished_granite','iron_block','white_glazed_terracotta','sandstone']
for i,b in enumerate(materials):
 x=-80+(i%4)*9;z=-69+(i//4)*15
 fill(x,64,z,x+4,67,z+4,b)
 label(x+2,70,z+2,b.replace('_',' ').upper(),'yellow')
fill(-82,63,-75,-42,63,-35,'smooth_stone')
label(-62,73,-42,'MATERIALS · WET FILM · VANILLA FACES')
# Dampness paths and partial roof for shelter/sky comparison.
for i,b in enumerate(['dirt','spruce_planks','stone','iron_ore','polished_granite','iron_block','white_glazed_terracotta','sandstone']):
 x=-81+i*5;fill(x,63,-29,x+3,63,-9,b)
fill(-82,70,-28,-42,70,-20,'stone_bricks')
for x in [-82,-42]:
 for z in [-28,-20]:fill(x,64,z,x,69,z,'spruce_log')
label(-62,74,-18,'SHELTER / OUTDOOR DAMP COMPARISON')
# Ordinary entities and projectiles, lit and shaded, without artificial glow.
fill(-82,63,1,-43,63,24,'grass_block')
for z in [0,25]:fill(-83,64,z,-42,64,z,'oak_fence')
for x in [-83,-42]:fill(x,64,0,x,64,25,'oak_fence')
for x,kind in [(-76,'cow'),(-67,'pig'),(-58,'sheep'),(-49,'villager')]:
 cmd(f'summon minecraft:{kind} {x} 64 12 {{NoAI:1b,PersistenceRequired:1b,Tags:["stratus_lab"]}}')
for x,kind in [(-73,'snowball'),(-62,'egg'),(-51,'ender_pearl')]:
 cmd(f'summon minecraft:{kind} {x} 66 5 {{NoGravity:1b,Motion:[0.0d,0.0d,0.0d],Tags:["stratus_lab"]}}')
label(-62,71,4,'ENTITY & PROJECTILE SHADING')
# Cave tank with striped receiver and glowing lamp; open inspection entrance.
fill(-82,57,36,-43,72,65,'stone')
fill(-80,59,38,-45,69,63,'air')
for z in range(39,63):fill(-79,58,z,-46,58,z,'white_concrete' if z%4<2 else 'black_concrete')
fill(-79,59,39,-46,62,62,'water')
fill(-80,64,36,-75,68,39,'air')
block(-61,60,51,'sea_lantern')
fill(-55,70,43,-49,72,49,'glass')
label(-64,75,37,'CAVE WATER · LOCAL LIGHT','aqua')
# Waterfall falling into the river, lip and source-level transition.
fill(22,63,52,29,77,58,'stone_bricks')
fill(21,77,51,30,77,59,'stone_bricks')
fill(23,78,53,28,78,57,'water')
label(27,82,54,'FLOWING WATER & THIN SIDES','aqua')
# Small atmospheric gardens and lamps, with contrasting flora.
rng=random.Random(151)
for x,z in [(-36,-70),(35,-68),(-36,70),(36,72),(-86,35),(85,-75),(85,75)]:tree(x,z)
for i in range(48):
 x=rng.choice([-1,1])*rng.randint(34,39);z=rng.randint(-75,75)
 block(x,64,z,rng.choice(['poppy','dandelion','cornflower','oxeye_daisy']))
for x,z in [(-35,-60),(-35,-30),(-35,0),(-35,30),(-35,65),(35,-60),(35,-30),(35,0),(35,30),(35,65)]:
 block(x,64,z,'cobblestone_wall');block(x,65,z,'lantern')
for x in [-39,-36,-33]:
 for z in [67,70,73]:block(x,64,z,'firefly_bush')
label(-36,69,73,'NIGHT · BLOOM · FIREFLIES')
# Raised sightline platform for cloud/parallax inspections, away from water.
fill(-9,169,-86,9,169,-72,'glass')
for x in [-9,9]:fill(x,170,-86,x,170,-72,'oak_fence')
for z in [-86,-72]:fill(-9,170,z,9,170,z,'oak_fence')
label(0,174,-78,'CLOUD VIEW · FLY UP / DOWN','white')
cmd('setworldspawn -3 66 -7 0 0')
cmd('tp @a -3 66 -7 0 12')
cmd('forceload remove -96 -96 95 95')
cmd('say Stratus Shader Lab built. Creative mode; explore the river, ponds, materials, cave and cloud platform.')
(pack/'build.mcfunction').write_text('\n'.join(a)+'\n')
# Runtime setworldspawn owns the live world metadata.
zones={'spawn_bridge':[-3,66,-7],'submerged_wood':[12,64,12],'materials':[-62,70,-55],'dampness_shelter':[-62,67,-18],'entities':[-62,67,12],'cave_tank':[-61,64,51],'swamp':[60,65,-48],'warm_ocean':[60,65,0],'cold_water':[60,65,48],'waterfall':[27,79,54],'cloud_platform':[0,171,-78]}
Path('work/stratus-check/lab-blueprint-151.json').write_text(json.dumps({'world':'Stratus Shader Lab','function_commands':len(a),'zones':zones},indent=2)+'\n')
print('Generated',len(a),'build commands and',len(zones),'Creative showcase zones in NEW flat world only.')
