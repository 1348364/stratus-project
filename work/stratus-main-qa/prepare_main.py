from pathlib import Path
from copy import deepcopy
import hashlib,json,shutil,sys
sys.path.insert(0,'work/stratus-check');from nbt_local import load,save,Tag,plain
root=Path.cwd();work=root/'work/stratus-main-qa';main=Path.home()/'Library/Application Support/ModrinthApp/profiles/Minecraft (1)'
dst=main/'saves/StratusTerrainLab';assert not dst.exists(), 'Never overwrite a world'
before=work/'before';before.mkdir(exist_ok=True)
files=[main/'options.txt',*[p for p in (main/'config').rglob('*') if p.is_file()],*[p for p in (main/'mods').glob('*') if p.is_file()]]
hashes={}
for p in files:
 rel=p.relative_to(main);hashes[rel.as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
 q=before/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
(work/'before-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
(work/'before-worlds.json').write_text(json.dumps(sorted(p.name for p in (main/'saves').iterdir() if p.is_dir()),indent=2)+'\n')
n,t=load(root/'work/minecraft-smoke/saves/StratusCheck/level.dat');t=deepcopy(t);d=t.value['Data'].value
for k in ['Player','DragonFight','WanderingTraderId','CustomBossEvents','ScheduledEvents']:d.pop(k,None)
d.update(LevelName=Tag(8,'Stratus Terrain Lab'),GameType=Tag(3,1),hardcore=Tag(1,0),allowCommands=Tag(1,1),Time=Tag(4,0),DayTime=Tag(4,5000),raining=Tag(1,0),thundering=Tag(1,0),initialized=Tag(1,0))
d['spawn']=Tag(10,{'pos':Tag(11,[164,66,32]),'pitch':Tag(5,18.0),'yaw':Tag(5,0.0),'dimension':Tag(8,'minecraft:overworld')})
assert plain(d['WorldGenSettings'])['dimensions']['minecraft:overworld']['generator']['type']=='minecraft:noise'
rules=d['game_rules'].value
for k in ['minecraft:advance_time','minecraft:advance_weather','minecraft:spawn_mobs']:rules[k]=Tag(1,0)
rules['minecraft:keep_inventory']=Tag(1,1)
d['DataPacks']=Tag(10,{'Enabled':Tag(9,(8,[Tag(8,'vanilla'),Tag(8,'file/stratus_terrain')])),'Disabled':Tag(9,(8,[]))})
dst.mkdir();save(dst/'level.dat',n,t)
pack=dst/'datapacks/stratus_terrain';(pack/'data/stratus/function').mkdir(parents=True)
(pack/'pack.mcmeta').write_text(json.dumps({'pack':{'min_format':[94,1],'max_format':[94,1],'description':'Stratus terrain testing and local controlled fixtures'}})+'\n')
shutil.copy2(root/'outputs/Stratus-1.5.1.zip',main/'shaderpacks/Stratus-1.5.1.zip')
# Only the shader selection is changed. All rendering/game options are retained.
p=main/'config/iris.properties';s=p.read_text();import re
s=re.sub(r'^shaderPack=.*$','shaderPack=Stratus-1.5.1.zip',s,flags=re.M);s=re.sub(r'^enableShaders=.*$','enableShaders=true',s,flags=re.M);p.write_text(s)
print('Created NEW normal world:',dst)
print('Saved',len(hashes),'existing config/mod hashes; Main rendering settings retained.')
