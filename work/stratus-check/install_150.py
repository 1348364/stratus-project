"""Atomically install only the new shader and sidecar; never alter Main config."""
from pathlib import Path
import hashlib,json,shutil,zipfile
root=Path.cwd();release=root/'outputs/Stratus-1.5.0.zip';source=root/'outputs/Stratus'
main=Path.home()/'Library/Application Support/ModrinthApp/profiles/Minecraft (1)';test=root/'work/minecraft-smoke'
protected=['options.txt','config/iris.properties','config/sodium-options.json']
before={name:(main/name).read_bytes() for name in protected}
checks=json.loads((source/'CHECKS.json').read_text());assert checks['runtime']['shader_errors']==0
manifest=json.loads((source/'SOURCE-MANIFEST.json').read_text())
with zipfile.ZipFile(release) as archive:
    assert archive.testzip() is None
    for row in manifest:
        assert hashlib.sha256(archive.read(row['path'])).hexdigest()==row['sha256']
        assert row['sha256']==checks['source_hashes'][row['path']]
    with zipfile.ZipFile(test/'shaderpacks'/release.name) as tested:
        for row in manifest:assert tested.read(row['path'])==archive.read(row['path']),row['path']
for instance in [main,test]:
    for filename in ['Stratus-1.5.0.zip','Stratus-1.5.0.zip.txt']:
        target=instance/'shaderpacks'/filename;pending=target.with_suffix(target.suffix+'.pending')
        shutil.copyfile(root/'outputs'/filename,pending);pending.replace(target)
        assert target.read_bytes()==(root/'outputs'/filename).read_bytes()
for name,original in before.items():assert (main/name).read_bytes()==original,name
initial=root/'work/stratus-check/main-before-150'
initial_match={name:(initial/name).read_bytes()==(main/name).read_bytes() for name in protected}
record={'version':'1.5.0','zip':str(release),'bytes':release.stat().st_size,'sha256':hashlib.sha256(release.read_bytes()).hexdigest(),'source_files':len(manifest),'main_installed':str(main/'shaderpacks'/release.name),'test_installed':str(test/'shaderpacks'/release.name),'main_protected_files_byte_identical_during_install':True,'main_files_match_task_start_snapshot':initial_match,'main_selection_unchanged':True,'main_changes_restricted_to_shaderpacks':True,'preferences':(root/'outputs/Stratus-1.5.0.zip.txt').read_text().splitlines()}
(root/'outputs/Stratus-1.5.0-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(root/'outputs/Stratus-1.5.0-install.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
