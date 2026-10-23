"""Retain privacy-filtered public website source versions without model calls."""
from __future__ import annotations
import io,json,os,re,tarfile,tempfile,zipfile
from pathlib import Path

def archive_versions(sync):
    site=sync.ROOT/'work/stratus-public'
    target=sync.ROOT/'work/public-site-history'
    target.mkdir(parents=True,exist_ok=True)
    commits=sync.command(['git','rev-list','--reverse','HEAD'],site).decode().splitlines()
    records=[]
    # Never copy a Git bundle: older revisions can contain private seed content.
    for commit in commits:
        out=target/(commit+'.zip')
        if not out.exists():
            raw=sync.command(['git','archive',commit],site)
            fd,temporary=tempfile.mkstemp(dir=sync.ROOT/'backups',suffix='.partial');os.close(fd)
            with tarfile.open(fileobj=io.BytesIO(raw)) as archive,zipfile.ZipFile(temporary,'w',zipfile.ZIP_DEFLATED,compresslevel=3) as package:
                omitted=[];redacted=[]
                for entry in archive:
                    name=entry.name
                    if not entry.isfile():continue
                    if not sync.allowed(name) or name=='lib/seed.json' or name.startswith(('verification/','outputs/')):
                        omitted.append(name);continue
                    data=archive.extractfile(entry).read()
                    if Path(name).suffix.lower() in sync.TEXT:
                        text=data.decode('utf-8')
                        clean=re.sub(r'https://stratus-studio-developer0406\.[a-zA-Z0-9.-]+','/api/studio',text)
                        clean=re.sub(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', '[private email removed]',clean)
                        clean=re.sub(r'/Users/[^\s\x22\x27<>]+','[local path removed]',clean)
                        if clean!=text:redacted.append(name)
                        data=clean.encode()
                        sync.inspect_bytes(name,data)
                        if re.search(rb'\bre_[A-Za-z0-9_]{24,}',data):raise ValueError('Possible mail credential in archived site source.')
                    elif not name.startswith('public/assets/'):
                        omitted.append(name);continue
                    info=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0));info.external_attr=0o100644<<16
                    package.writestr(info,data,compress_type=zipfile.ZIP_DEFLATED)
                package.writestr('SOURCE-VERSION.json',json.dumps({'commit':commit,'privacy_filtered':True,'omitted_files':omitted,'redacted_files':redacted,'note':'Source snapshot, not proof that this revision was deployed. Private seed data, contact details, local paths and QA captures are intentionally excluded.'},indent=2))
            os.replace(temporary,out)
        records.append({'commit':commit,'archive':out.name,'sha256':sync.digest(out.read_bytes())})
    sync.atomic(target/'versions.json',json.dumps({'site':'stratus-public','versions':records,'privacy_filtered':True,'restore':'Each ZIP contains source for its named commit. See SOURCE-VERSION.json for privacy omissions. Deployment bundles are rebuilt from source; no credentials are included.'},indent=2).encode()+b'\n')
    return len(records)

if __name__=='__main__':
    import github_sync
    print('Public website source versions archived:',archive_versions(github_sync))
