from pathlib import Path
import re,json,subprocess,time
p=Path('work/stratus-check/release-performance-context.json');v=json.loads(p.read_text());rows=Path('work/stratus-check/minecraft-140-release.log').read_text().splitlines();camera={}
for tag,pos in [('clean-water',[104.5,104.,90.5]),('clean-landscape',[.5,110.,-31.5]),('clean-clouds',[200.5,140.,200.5])]:
 start=max(i for i,l in enumerate(rows) if 'BENCH_START v140-'+tag+' ' in l);end=next(i for i in range(start+1,len(rows)) if 'BENCH_RESULT ' in rows[i])
 def parse(lines):
  found=[]
  for l in lines:
   m=re.search(r'has the following entity data: \[(.*?)\]',l)
   if m:found.append([float(x.strip().rstrip('df')) for x in m[1].split(',')])
  return found
 before=parse(rows[:start])[-2:];after=parse(rows[end+1:])[:2]
 assert before[0]==after[0]==pos,(tag,before,after)
 manual=any('[ShaderCheck:' in l for l in rows[start:end]);assert not manual
 camera[tag]={'position':pos,'rotation_before':before[1],'rotation_after':after[1],'position_same_before_and_after':True,'manual_commands_during_sample':False,'rotation_delta_degrees':[b-a for a,b in zip(before[1],after[1])]}
clients=[]
for l in subprocess.run(['ps','-axo','pid=,command='],capture_output=True,text=True).stdout.splitlines():
 if 'net.fabricmc.loader' in l and '/bin/java' in l:clients.append({'pid':int(l.split()[0]),'type':'test' if 'minecraft-smoke' in l else 'normal'})
assert len(clients)==1 and clients[0]['type']=='test',clients
v['clients_at_finalization']=clients;v['finalization_at']=time.strftime('%Y-%m-%dT%H:%M:%S%z');v['camera_verification']=camera;v['sample_context']='Only isolated test client; Main shutdown verified before all accepted final-source samples. Camera position and angle observations recorded per sample.';v['discarded_capped_water_sample']={'average_fps':15.1823,'reason':'background Dynamic FPS cap; repeated after focus warmup'};p.write_text(json.dumps(v,indent=2)+'\n');print(json.dumps(camera,indent=2))
