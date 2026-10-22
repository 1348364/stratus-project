from pathlib import Path
import json
w=Path('work/stratus-main-qa');a=[];O=4096;H=33
A=lambda s:a.append(s)
def f(x,y,z,X,Y,Z,b):
 for xx in range(x,X+1,16):
  for zz in range(z,Z+1,16):
   A(f'fill {O+xx} {H+y} {O+zz} {O+min(X,xx+15)} {H+Y} {O+min(Z,zz+15)} minecraft:{b}')
def b(x,y,z,name):A(f'setblock {O+x} {H+y} {O+z} minecraft:{name}')
def label(x,y,z,text):A(f'summon minecraft:text_display {O+x} {H+y} {O+z} {{Tags:["stratus_terrain_fixture"],billboard:"center",text:{{text:{json.dumps(text)},color:"aqua",bold:1b}}}}')
A(f'forceload add {O-48} {O-48} {O+47} {O+47}')

A('kill @e[tag=stratus_terrain_fixture]')
f(-48,64,-48,47,150,47,'air');f(-48,55,-48,47,62,47,'stone');f(-48,63,-48,47,63,47,'grass_block')
# Long six-block-deep pool, graded bank and walkable timber bridge.
f(-13,57,-40,13,65,40,'air');f(-13,56,-40,13,56,40,'gravel');f(-12,57,-39,12,62,39,'water')
for x in [-13,13]:f(x,57,-40,x,62,40,'sand')
f(-18,65,-8,18,65,-5,'spruce_planks')
for x in [-16,16]:
 for z in [-8,-5]:f(x,57,z,x,67,z,'spruce_log');b(x,68,z,'lantern')
f(-10,60,12,4,60,12,'oak_log[axis=x]');f(-10,57,12,-10,64,12,'oak_log')
for i in range(5):b(-5+i,58+i,18,'oak_stairs[facing=north,waterlogged=true]')
f(3,60,23,8,60,23,'oak_slab[type=bottom,waterlogged=true]');f(-7,58,25,-3,61,25,'oak_fence[waterlogged=true]')
for x,mat in [(-9,'red_concrete'),(-4,'yellow_concrete'),(1,'white_concrete'),(6,'blue_concrete')]:f(x,57,32,x+1,61,33,mat)
label(0,69,12,'SUBMERGED BLOCKS · STAIRS · SLABS · FENCES')
# Cubes and partial shelter, with absorbing and nonabsorbing material classes.
for i,mat in enumerate(['dirt','spruce_planks','stone','iron_ore','polished_granite','iron_block','white_glazed_terracotta','sandstone']):
 x=-44+(i%2)*10;z=-35+(i//2)*12;f(x,64,z,x+4,67,z+4,mat);label(x+2,70,z+2,mat.replace('_',' ').upper())
f(-47,71,16,-21,71,28,'stone_bricks');f(-46,63,16,-22,63,33,'spruce_planks')
for x in [-47,-21]:f(x,64,16,x,70,16,'spruce_log')
label(-34,74,24,'SHELTER / EXPOSED WET FILM')
# Regional colour ponds: explicit biomes kept inside this controlled area.
for z,biome in [(-30,'swamp'),(0,'warm_ocean'),(30,'frozen_ocean')]:
 f(22,56,z-9,42,64,z+9,'air');f(22,54,z-9,42,54,z+9,'stone');f(22,55,z-9,42,55,z+9,'sand');f(23,56,z-8,41,62,z+8,'water')
 A(f'fillbiome {O+20} {H+40} {O+z-11} {O+44} {H+100} {O+z+11} minecraft:{biome}')
 f(21,64,z-2,28,64,z+1,'spruce_planks');b(25,65,z,'lantern');label(32,68,z-10,biome.replace('_',' ').upper())
# Local dark tank and lamp, plus a waterfall lip and thin vertical sheet.
f(-44,56,35,-23,72,46,'stone');f(-43,58,36,-24,69,45,'air');f(-42,58,37,-25,62,44,'water');b(-34,59,41,'sea_lantern');f(-44,64,35,-39,68,37,'air')
f(12,63,28,17,77,35,'stone_bricks');f(11,77,27,18,77,36,'stone_bricks');f(13,78,29,16,78,34,'water')
for x,kind in [(-43,'cow'),(-36,'sheep'),(-29,'villager')]:A(f'summon minecraft:{kind} {O+x} {H+64} {O+9} {{NoAI:1b,PersistenceRequired:1b,Tags:["stratus_terrain_fixture"]}}')
for x in [-46,-44,-42]:b(x,64,3,'firefly_bush')
label(0,73,-6,'STRATUS · CONTROLLED TEST CLEARING')

A(f'forceload remove {O-48} {O-48} {O+47} {O+47}')
A('say Test clearing ready. Normal terrain beyond the clearing is unchanged. Water fixture: /tp @s 4096 98 4102')
(w/'build.mcfunction').write_text('\n'.join(a)+'\n')
zones={'bridge':[4096,100,4085],'wood_above':[4096,97,4101],'wood_underwater':[4096,92.8,4101],'material_cubes':[4060,105,4070],'shelter':[4062,100,4128],'cave_tank':[4062,97,4132],'cloud_view':[4096,180,4096]}
(w/'fixture-zones.json').write_text(json.dumps(zones,indent=2)+'\n');print('Prepared',len(a),'commands for a 96 by 96 test clearing in the NEW normal world.')
