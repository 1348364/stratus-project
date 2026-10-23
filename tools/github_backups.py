"""Coverage for authored work and immutable GitHub backup assets. No AI calls."""
from __future__ import annotations
import hashlib,json,os,re,tarfile,zipfile
from pathlib import Path

MEDIA_OMIT={'.git','node_modules','.wrangler','.sites-runtime','.history','.bridge',
            '__pycache__','.next','.vinext','.cache','.venv','venv','coverage',
            'minecraft-smoke','stratus-github','.agents','.codex'}
SITES={'stratus-public','stratus-studio-cloud'}
HISTORICAL_TAG='project-backup-2026-10-22'
SNAPSHOT_TAG='project-work-snapshots'


def walk(folder, omit=()):
    for directory,dirs,names in os.walk(folder):
        dirs[:]=[name for name in dirs if name not in MEDIA_OMIT and name not in omit]
        for name in names:
            path=Path(directory)/name
            if path.is_file() and not path.is_symlink():yield path


def augment_sources(sync,files):
    """Retain final runtime separately from settled, explicitly labelled WIP."""
    root=sync.ROOT
    for path in (root/'work').iterdir():
        if path.is_file() and not path.is_symlink() and path.suffix.lower() in sync.TEXT and sync.allowed(path.name):
            files[path.relative_to(root).as_posix()]=path.read_bytes()
    for folder in (root/'work').iterdir():
        if not folder.is_dir() or folder.name in MEDIA_OMIT|SITES|{'Custom instructions','stratus-studio'}:continue
        for path in walk(folder):
            relative=path.relative_to(root).as_posix()
            if sync.allowed(relative) and path.suffix.lower() in sync.TEXT:files[relative]=path.read_bytes()
    for path in walk(root/'outputs',omit={'Stratus'}):
        relative=path.relative_to(root).as_posix()
        curated=any(part.endswith('-showcase') for part in path.parts)
        if sync.allowed(relative) and (path.suffix.lower() in sync.TEXT or (curated and path.suffix.lower()=='.png')):
            files[relative]=path.read_bytes()
    for path in walk(root/'outputs/Stratus'):
        if sync.allowed(path.relative_to(root/'outputs/Stratus').as_posix()):
            files['development/Stratus/'+path.relative_to(root/'outputs/Stratus').as_posix()]=path.read_bytes()
    # Uncommitted web source is backed up explicitly as development, never as deployed source.
    for site in SITES:
        folder=root/'work'/site
        if not sync.command(['git','status','--porcelain'],folder).strip():continue
        for path in walk(folder,omit={'dist','outputs'}):
            relative=path.relative_to(folder).as_posix()
            if sync.allowed(relative):files['development/'+site+'/'+relative]=path.read_bytes()
    files['development/README.md']=(
        '# Development snapshots\n\nThese are settled working files, including unfinished or release-candidate work. '
        'They are not a verified final release. `outputs/Stratus/` contains the latest final documented package. '
        'The original workspace, release history and settings remain preserved.\n').encode()


def historical_catalog(sync):
    """Index exact contents of the already uploaded, immutable historical bundles."""
    cache=sync.STATE.parent/'.github-sync-catalog.json'
    if cache.exists():return json.loads(cache.read_text())
    release=json.loads(sync.gh('api',f'repos/{repository(sync)}/releases/tags/{HISTORICAL_TAG}'))
    assets={asset['name']:asset for asset in release['assets']}
    catalog={}
    for name in ('stratus-completed-releases.zip','stratus-development-evidence.zip'):
        path=sync.ROOT/'backups/github-release-assets'/name
        if not path.exists():raise ValueError('Original backup bundle is missing: '+name)
        with path.open('rb') as handle:archive_hash=hashlib.file_digest(handle,'sha256').hexdigest()
        if assets.get(name,{}).get('digest')!='sha256:'+archive_hash:
            raise ValueError('Historical backup checksum does not match GitHub: '+name)
        with zipfile.ZipFile(path) as archive:
            for entry in archive.infolist():
                if not entry.is_dir():
                    catalog[entry.filename]={'sha256':sync.digest(archive.read(entry)),
                        'tag':HISTORICAL_TAG,'asset':name,'bytes':entry.file_size}
    sync.atomic(cache,json.dumps(catalog).encode())
    return catalog


def repository(sync):
    config=json.loads(sync.CONFIG.read_text())
    return json.loads(sync.gh('api','repositories/'+str(config['repository_id'])))['full_name']


def inspect_archive(sync,path):
    """Inspect textual entries, including nested ZIPs, before public upload."""
    import io
    def inspect_zip(archive,depth=0):
        if depth>4:raise ValueError('Archive nesting needs manual review: '+str(path))
        for member in archive.infolist():
            if member.is_dir():continue
            name=member.filename
            if not sync.allowed(name):
                if Path(name).name=='resourceful-config-web.json' or Path(name).name.startswith(('.env','.dev.vars')) or Path(name).suffix in {'.pem','.key'}:
                    raise ValueError('Private file inside archive: '+str(path))
                continue
            if Path(name).suffix.lower() in sync.TEXT:sync.inspect_bytes(str(path)+'/'+name,archive.read(member))
            elif name.lower().endswith(('.zip','.jar')):
                with zipfile.ZipFile(io.BytesIO(archive.read(member))) as nested:inspect_zip(nested,depth+1)
    if path.suffix.lower() in {'.zip','.jar'}:
        with zipfile.ZipFile(path) as archive:inspect_zip(archive)


def backup_inventory(sync,state,files):
    """Catalogue existing backups and collect missing assets in bounded groups."""
    original=historical_catalog(sync)
    stat_cache=state.setdefault('asset_stat_cache',{})
    published=state.setdefault('work_backups',{})
    index=dict(original);index.update(published);groups={};seen=set()
    for root in (sync.ROOT/'outputs',sync.ROOT/'work'):
        children=[p for p in root.iterdir() if p.name not in (SITES|{'stratus-studio','Custom instructions','stratus-github','minecraft-smoke'} if root.name=='work' else {'Stratus'})]
        paths=(path for child in children for path in (walk(child) if child.is_dir() else [child]))
        for path in paths:
            if path.is_symlink() or not path.is_file():continue
            relative=path.relative_to(sync.ROOT).as_posix()
            if not sync.allowed(relative) or relative in files:continue
            # Deployment bundles/build caches are reproducible from the saved website source.
            if path.name.endswith(('.tar.gz','.tgz')):continue
            seen.add(relative)
            stat=path.stat();marker=[stat.st_size,stat.st_mtime_ns]
            cached=stat_cache.get(relative,{})
            if cached.get('stat')==marker:checksum=cached['sha256']
            else:
                checksum=sync.digest(path.read_bytes())
                stat_cache[relative]={'stat':marker,'sha256':checksum}
            prior=original.get(relative)
            if prior and prior['sha256']==checksum:
                index[relative]=prior;state.setdefault('asset_settling',{}).pop(relative,None);continue
            known=published.get(relative)
            if known and known['sha256']==checksum:
                index[relative]=known;state.setdefault('asset_settling',{}).pop(relative,None);continue
            # Settle each new/changed asset independently; editing one file cannot starve others.
            settling=state.setdefault('asset_settling',{})
            candidate=settling.get(relative)
            import time
            if not candidate or candidate['sha256']!=checksum:
                settling[relative]={'sha256':checksum,'since':time.time()}
                if known:index[relative]=known
                continue
            if time.time()-candidate['since']<60:continue
            inspect_archive(sync,path)
            group=path.relative_to(sync.ROOT).parts[1] if relative.startswith('work/') else re.sub(r'(Stratus-\d+\.\d+\.\d+(?:-rc\d+)?).*',r'\1',path.relative_to(root).parts[0])
            groups.setdefault(group,[]).append((relative,path,checksum,stat.st_size))
    state['asset_settling']={name:item for name,item in state.get('asset_settling',{}).items() if name in seen}
    sync.state_save(state)
    return index,groups


def upload_backups(sync,repo,state,index,groups):
    if not groups:return index
    releases=json.loads(sync.gh('api',f'repos/{repo}/releases?per_page=100'))
    release=next((r for r in releases if r['tag_name']==SNAPSHOT_TAG),None)
    if release is None:
        sync.gh('release','create',SNAPSHOT_TAG,'--repo',repo,'--title','Project work and development backups',
                '--notes','Automatic immutable backups of project work. Includes unfinished QA/candidate work; these are not final shader releases. See WORK-BACKUP-INDEX.json in the repository.','--prerelease','--latest=false')
        release=json.loads(sync.gh('api',f'repos/{repo}/releases/tags/{SNAPSHOT_TAG}'))
    existing={asset['name']:asset for asset in release['assets']}
    for group,entries in sorted(groups.items()):
        chunks=[];chunk=[];size=0
        for entry in sorted(entries):
            if chunk and size+entry[3]>250_000_000:chunks.append(chunk);chunk=[];size=0
            chunk.append(entry);size+=entry[3]
        if chunk:chunks.append(chunk)
        for chunk in chunks:
            checksum=sync.digest(json.dumps([(x[0],x[2]) for x in chunk]).encode())[:16]
            name=re.sub('[^a-zA-Z0-9-]','-',group)+'-'+checksum+'.zip'
            out=sync.ROOT/'backups/github-auto-assets'/name;out.parent.mkdir(parents=True,exist_ok=True)
            with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=1) as archive:
                for relative,path,expected,_ in chunk:
                    data=path.read_bytes()
                    if sync.digest(data)!=expected:raise ValueError('Asset changed while backing up: '+relative)
                    info=zipfile.ZipInfo(relative,date_time=(1980,1,1,0,0,0))
                    info.create_system=3;info.external_attr=0o100644<<16
                    archive.writestr(info,data,compress_type=zipfile.ZIP_DEFLATED,compresslevel=1)
            asset_hash='sha256:'+sync.digest(out.read_bytes())
            if name in existing:
                if existing[name].get('digest')!=asset_hash or existing[name].get('state')!='uploaded':raise ValueError('Existing backup asset differs: '+name)
            else:
                sync.command([sync.GH,'release','upload',SNAPSHOT_TAG,str(out),'--repo',repo],timeout=1800)
                actual=json.loads(sync.gh('api',f'repos/{repo}/releases/tags/{SNAPSHOT_TAG}'))
                remote=next((a for a in actual['assets'] if a['name']==name),None)
                if not remote or remote.get('digest')!=asset_hash or remote.get('state')!='uploaded':raise ValueError('Backup upload could not be verified: '+name)
            for relative,_,expected,amount in chunk:
                record={'sha256':expected,'tag':SNAPSHOT_TAG,'asset':name,'bytes':amount}
                state['work_backups'][relative]=record;index[relative]=record
            sync.state_save(state)
            print('Verified backup asset: '+name,flush=True)
    return index
