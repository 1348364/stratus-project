from pathlib import Path
import json,zipfile,tempfile,importlib.util
w=Path(__file__).parent;p=Path('outputs/Stratus');spec=importlib.util.spec_from_file_location('installer1611',p/'install.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);policy=json.loads((p/'RELEASE-POLICY.json').read_text());checks=[]
def check(n,b):assert b,n;checks.append(n)
original=(w/'Main-before-Stratus-1.6.10.zip.txt').read_bytes()
with tempfile.TemporaryDirectory() as tmp:
 root=Path(tmp);profile=root/'Main';packs=profile/'shaderpacks';packs.mkdir(parents=True);prev=packs/'Stratus-1.6.10.zip.txt';prev.write_bytes(original);archive=root/'Stratus-1.6.11.zip'
 with zipfile.ZipFile(archive,'w') as z:z.writestr('RELEASE-POLICY.json',json.dumps(policy))
 result=m.install(archive,profile,prev,True);check('Dry run writes no destination',not (packs/archive.name).exists())
 result=m.install(archive,profile,prev);settings=packs/(archive.name+'.txt');check('Captured related values reset to identical approved Reference defaults',m.read_values(settings)=={})
 check('Old preferences byte-identical',prev.read_bytes()==original)
 # A later user edit remains effective, including removing an old override.
 values=m.read_values(prev);values['SURFACE_DAMPNESS']='1.35';values['BLOOM_RADIUS']='6.00';values.pop('WATER_TEXTURE',None)
 carried,reset=m.migrate(values,policy)
 check('Later related manual edit preserved',carried['SURFACE_DAMPNESS']=='1.35' and 'SURFACE_DAMPNESS' not in reset)
 check('Later removal preserves old source default',carried['WATER_TEXTURE']==policy['previous_source_defaults']['WATER_TEXTURE'])
 check('Unrelated latest override preserved',carried['BLOOM_RADIUS']=='6.00')
 settings.write_bytes(b'# newer1.6.11 tuning\nRIPPLE_SIZE=4.00\n');newer=settings.read_bytes();again=m.install(archive,profile,prev);check('Existing new-version settings never overwritten',settings.read_bytes()==newer and again['existing_new_version_preferences_preserved'])
 check('Atomic create cannot overwrite',not m.create_if_absent(settings,b'bad') and settings.read_bytes()==newer)
 archive.write_bytes(archive.read_bytes()+b'changed')
 try:m.install(archive,profile,prev)
 except FileExistsError:checks.append('Conflicting archive refused')
 else:raise AssertionError('Archive conflict lost')
with tempfile.TemporaryDirectory() as tmp:
 root=Path(tmp);profile=root/'Main';archive=root/'Stratus-1.6.11.zip'
 with zipfile.ZipFile(archive,'w') as z:z.writestr('RELEASE-POLICY.json',json.dumps(policy))
 create=m.create_if_absent
 def race(path,data):
  if path.name==archive.name:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(b'other');return False
  return create(path,data)
 m.create_if_absent=race
 try:
  try:m.install(archive,profile)
  except FileExistsError:checks.append('Concurrent conflicting archive refused before preferences')
  else:raise AssertionError('Concurrent conflict lost')
 finally:m.create_if_absent=create
report={'checks':checks,'failures':0,'scope':'Temporary profiles, actual1.6.11 policy and installer. No Main writes.'};(w/'migration-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
