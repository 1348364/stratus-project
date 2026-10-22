"""Create NEW isolated superflat-world metadata; never overwrite a world."""
from pathlib import Path
from copy import deepcopy
import json,zipfile
from nbt_local import load,save,Tag,plain
base=Path('work/minecraft-smoke/saves');dst=base/'StratusShaderLab'
assert not dst.exists(),dst
name,root=load(base/'StratusCheck/level.dat');root=deepcopy(root);d=root.value['Data'].value
for key in ['Player','DragonFight','WanderingTraderId','CustomBossEvents','ScheduledEvents']:
 d.pop(key,None)
d['LevelName']=Tag(8,'Stratus Shader Lab');d['GameType']=Tag(3,1);d['hardcore']=Tag(1,0);d['allowCommands']=Tag(1,1)
d['Time']=Tag(4,0);d['DayTime']=Tag(4,3000);d['raining']=Tag(1,0);d['thundering']=Tag(1,0)
d['spawn']=Tag(10,{'pos':Tag(11,[0,66,-10]),'pitch':Tag(5,12.0),'yaw':Tag(5,0.0),'dimension':Tag(8,'minecraft:overworld')})
rules=d['game_rules'].value
for key in ['minecraft:advance_time','minecraft:advance_weather','minecraft:spawn_mobs','minecraft:spawn_monsters','minecraft:spawn_wandering_traders']:
 rules[key]=Tag(1,0)
rules['minecraft:random_tick_speed']=Tag(3,0);rules['minecraft:keep_inventory']=Tag(1,1)
layers=[(1,'bedrock'),(125,'stone'),(1,'dirt'),(1,'grass_block')]
settings=Tag(10,{'biome':Tag(8,'minecraft:plains'),'lakes':Tag(1,0),'features':Tag(1,0),'layers':Tag(9,(10,[Tag(10,{'height':Tag(3,h),'block':Tag(8,'minecraft:'+b)}) for h,b in layers])),'structure_overrides':Tag(9,(8,[]))})
over=d['WorldGenSettings'].value['dimensions'].value['minecraft:overworld'].value
over['generator']=Tag(10,{'type':Tag(8,'minecraft:flat'),'settings':settings})
d['DataPacks'].value['Enabled'].value[1].append(Tag(8,'file/stratus_lab'))
dst.mkdir();save(dst/'level.dat',name,root)
pack=dst/'datapacks/stratus_lab';(pack/'data/stratus/function').mkdir(parents=True)
(pack/'pack.mcmeta').write_text(json.dumps({'pack':{'min_format':[94,1],'max_format':[94,1],'description':'Original Stratus Shader Lab building functions forMinecraft1.21.11'}},indent=2)+'\n')
assert plain(load(dst/'level.dat')[1])==plain(root)
print('Created NEW superflat metadata:',dst,';groundY63;Creative;actual1.21.11pack94.1.')
