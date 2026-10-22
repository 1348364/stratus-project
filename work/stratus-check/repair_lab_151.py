from pathlib import Path
p=Path('work/stratus-check/build_lab_151.py');s=p.read_text();a=s.index('# Submerged3D');b=s.index('# Three actual-biome',a)
s=s[:a]+'''# Submerged3D receivers follow the winding river's centre, not its bank.
fill(4,58,14,4,64,14,'oak_log')
fill(14,58,20,14,62,20,'spruce_log')
fill(4,60,14,17,60,14,'oak_log[axis=x]')
for i in range(5):block(9+i,58+i,18,'oak_stairs[facing=north,waterlogged=true]')
fill(15,60,23,19,60,23,'oak_slab[type=bottom,waterlogged=true]')
fill(8,59,24,11,61,24,'oak_fence[waterlogged=true]')
for x,b in [(6,'red_concrete'),(9,'yellow_concrete'),(12,'white_concrete'),(15,'blue_concrete')]:fill(x,58,33,x+1,61,34,b)
label(12,67,19,'SUBMERGED GEOMETRY','aqua')
label(12,65,36,'Look across the shore · then swim below','white')
'''+s[b:];s=s.replace("cmd('setworldspawn 0 66 -7 0 0')","cmd('setworldspawn -3 66 -7 0 0')").replace("cmd('tp @a 0 66 -7 0 12')","cmd('tp @a -3 66 -7 0 12')");s=s.replace("name,root=load(world/'level.dat');root.value['Data'].value['spawn'].value['pos']=Tag(11,[0,66,-7]);save(world/'level.dat',name,root)","# Runtime setworldspawn owns the live world metadata.")
s=s.replace("'spawn_bridge':[0,66,-7],'submerged_wood':[0,65,19]","'spawn_bridge':[-3,66,-7],'submerged_wood':[12,64,12]");p.write_text(s)
