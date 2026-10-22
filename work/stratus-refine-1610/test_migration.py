from pathlib import Path
import importlib.util,json,tempfile,zipfile,hashlib
spec=importlib.util.spec_from_file_location('stratus_install',Path('outputs/Stratus/install.py'));installer=importlib.util.module_from_spec(spec);spec.loader.exec_module(installer)
policy=json.loads(Path('outputs/Stratus/RELEASE-POLICY.json').read_text());checks=[]
def check(name,value):
 assert value,name
 checks.append(name)
with tempfile.TemporaryDirectory() as tmp:
 root=Path(tmp);profile=root/'Main';packs=profile/'shaderpacks';packs.mkdir(parents=True);(profile/'config').mkdir();previous=packs/'Stratus-1.6.9.zip.txt';before=b'# old tuning\nSURFACE_DAMPNESS=0.15\nWATER_TURBIDITY=3.00\nWATER_RENDER_QUALITY=1\nSKY_AMBIENT=1.00\nEXPOSURE=3.00\n';previous.write_bytes(before);(profile/'config/iris.properties').write_text('shaderPack=Stratus-1.6.9.zip\n');archive=root/'Stratus-1.6.10.zip'
 with zipfile.ZipFile(archive,'w') as z:z.writestr('RELEASE-POLICY.json',json.dumps(policy))
 dry=installer.install(archive,profile,dry_run=True);check('Dry run writes no archive or preferences',not (packs/archive.name).exists() and not (packs/(archive.name+'.txt')).exists())
 result=installer.install(archive,profile);new=packs/(archive.name+'.txt');values=installer.read_values(new);check('Related film/colour overrides reset',not {'SURFACE_DAMPNESS','EXPOSURE'}&values.keys());check('Unrelated optics/quality/ambient tuning preserved',values=={'WATER_TURBIDITY':'3.00','WATER_RENDER_QUALITY':'1','SKY_AMBIENT':'1.00'});check('Prior preferences remain byte-identical',previous.read_bytes()==before)
 new.write_bytes(b'# newer user tuning\nSURFACE_DAMPNESS=2.50\n');newer=new.read_bytes();again=installer.install(archive,profile);check('Existing new-version tuning wins',new.read_bytes()==newer and again['existing_new_version_preferences_preserved'])
 content=archive.read_bytes();archive.write_bytes(content+b'extra metadata');
 try:installer.install(archive,profile)
 except FileExistsError:checks.append('Conflicting same-version archive is refused')
 else:raise AssertionError('Conflicting archive overwritten')
 check('Atomic creation never overwrites an existing file',not installer.create_if_absent(new,b'overwrite') and new.read_bytes()==newer)
 check('Visual defaults explicitly apply to all four presets',all(set(row['presets'])=={'FAST','BALANCED','REFERENCE','HIGH'} for row in policy['classifications'] if row['type']=='visual'))

# Simulate an archive arriving after the initial existence check, before link.
with tempfile.TemporaryDirectory() as tmp:
 root=Path(tmp);profile=root/'Main';archive=root/'Stratus-1.6.10.zip'
 with zipfile.ZipFile(archive,'w') as z:z.writestr('RELEASE-POLICY.json',json.dumps(policy))
 original_create=installer.create_if_absent
 def racing_create(path,data):
  if path.name==archive.name:
   path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(b'concurrent different archive');return False
  return original_create(path,data)
 installer.create_if_absent=racing_create
 try:
  try:installer.install(archive,profile)
  except FileExistsError:checks.append('Concurrent conflicting archive rejected before creating preferences')
  else:raise AssertionError('Concurrent conflicting archive accepted')
  assert not (profile/'shaderpacks'/(archive.name+'.txt')).exists()
 finally:installer.create_if_absent=original_create

report={'checks':checks,'failures':0,'scope':'Installer policy integration with temporary profiles; no Main data used or changed'};Path('work/stratus-refine-1610/migration-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
