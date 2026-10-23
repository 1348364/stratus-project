from pathlib import Path
import json,zipfile,tempfile,importlib.util
w=Path(__file__).parent;p=Path('outputs/Stratus');spec=importlib.util.spec_from_file_location('installer1612',p/'install.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);policy=json.loads((p/'RELEASE-POLICY.json').read_text());checks=[]
def check(n,b):assert b,n;checks.append(n)
with tempfile.TemporaryDirectory() as tmp:
 root=Path(tmp);profile=root/'Main';packs=profile/'shaderpacks';packs.mkdir(parents=True);prev=packs/'Stratus-1.6.11.zip.txt';prev.write_text('# Existing values\nWATER_TEXTURE=1.00\nRIPPLE_SIZE=4.00\nREFLECTION_MODE=2\n');original=prev.read_bytes();archive=root/'Stratus-1.6.12.zip'
 with zipfile.ZipFile(archive,'w') as z:z.writestr('RELEASE-POLICY.json',json.dumps(policy))
 m.install(archive,profile,prev,True);check('Dry run writes nothing',not (packs/archive.name).exists())
 result=m.install(archive,profile,prev);settings=packs/(archive.name+'.txt');check('Only related captured water setting resets; unrelated visual and quality carry',m.read_values(settings)=={'RIPPLE_SIZE':'4.00','REFLECTION_MODE':'2'})
 check('Old preferences remain byte-identical',prev.read_bytes()==original)
 for val in ['0.00','0.50','0.75']:
  carried,reset=m.migrate({'WATER_TEXTURE':val,'RIPPLE_SIZE':'4.00'},policy);check('Later manual water choice '+val+' wins',carried['WATER_TEXTURE']==val and not reset)
 carried,reset=m.migrate({},policy);check('Missing prior settings preserve source default',not carried and not reset)
 settings.write_bytes(b'# Newer preferences\nWATER_TEXTURE=0.00\n');newer=settings.read_bytes();again=m.install(archive,profile,prev);check('Existing new release preferences win',settings.read_bytes()==newer and again['existing_new_version_preferences_preserved'])
 check('Atomic create never overwrites',not m.create_if_absent(settings,b'wrong') and settings.read_bytes()==newer)
 archive.write_bytes(archive.read_bytes()+b'changed')
 try:m.install(archive,profile,prev)
 except FileExistsError:checks.append('Conflicting archive refused')
 else:raise AssertionError('Archive conflict lost')
report={'checks':checks,'failures':0,'scope':'Actual 1.6.12 policy and installer in temporary profiles, no Main writes'};(w/'migration-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
