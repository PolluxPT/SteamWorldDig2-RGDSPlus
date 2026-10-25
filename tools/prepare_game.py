#!/usr/bin/env python3
"""Assemble a PRIVATE installation from the owner's Linux game. MIT; see LICENSE."""
import zipfile, re, argparse, hashlib, io, json, os, shutil, struct, sys, tarfile, tempfile, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / 'port.json').read_text())

def fail(message):
    raise ValueError(message)

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()

def find_game(source):
    choices = [source, source/'game', source/'data/noarch/game']
    found = [p for p in choices if (p/CONFIG['executable']).is_file()]
    if len(found) != 1:
        fail('Choose the installed Linux folder containing '+CONFIG['executable']+' and '+CONFIG['assets']+'. Do not pass an installer or Windows files.')
    p = found[0].resolve(); exe = p/CONFIG['executable']
    if not any((p/n).is_dir() for n in CONFIG.get('asset_alternatives',[CONFIG['assets']])): fail('Game resource folder missing: '+CONFIG['assets'])
    header = exe.read_bytes()[:20]
    if header[:4] != b'\x7fELF' or len(header)<20 or header[4] != CONFIG['elf_class'] or header[5] != 1 or int.from_bytes(header[18:20],'little') != CONFIG['machine']:
        fail('Wrong executable architecture. Use the supported Linux edition.')
    actual = digest(exe)
    if CONFIG.get('sha256') and actual != CONFIG['sha256']:
        fail('Unsupported game build. SHA-256: '+actual+'; expected '+CONFIG['sha256']+'. No files were patched. Do not bypass this check.')
    return p, actual

def ar_members(data):
    if data[:8] != b'!<arch>\n': fail('Invalid Debian archive')
    pos = 8
    while pos < len(data):
        header = data[pos:pos+60]
        if len(header)!=60 or header[58:60]!=b'`\n': fail('Invalid ar member')
        name = header[:16].decode().strip().rstrip('/')
        length = int(header[48:58]); pos += 60
        payload = data[pos:pos+length]
        if len(payload)!=length: fail('Truncated ar member')
        yield name, payload
        pos += length + length%2

def fetch_runtime(destination, offline=None):
    lock = json.loads((ROOT/'runtime-lock.json').read_text())[CONFIG['debian_arch']]
    target = destination/'runtime'/CONFIG['libs_dir']; target.mkdir(parents=True, exist_ok=True)
    notices = destination/'runtime/upstream-notices'; notices.mkdir(parents=True, exist_ok=True)
    libs = {'libgcc-s1':'libgcc_s.so.1','libstdc++6':'libstdc++.so.6'}
    if CONFIG['id']=='dig': libs['zlib1g']='libz.so.1'
    for package, soname in libs.items():
        info = lock[package]; filename=Path(info['Filename']).name
        if offline:
            data=(offline/filename).read_bytes()
        else:
            url='https://deb.debian.org/debian/'+info['Filename']
            print('Downloading',package,info['Version'],CONFIG['debian_arch'],flush=True)
            with urllib.request.urlopen(url,timeout=90) as response: data=response.read()
        if len(data)!=int(info['Size']) or hashlib.sha256(data).hexdigest()!=info['SHA256']:
            fail('Runtime package failed size/hash check: '+filename)
        payload=next((b for name,b in ar_members(data) if name.startswith('data.tar')),None)
        if payload is None: fail('Debian data archive missing')
        with tarfile.open(fileobj=io.BytesIO(payload),mode='r:*') as archive:
            candidates=[m for m in archive.getmembers() if m.isfile() and re.fullmatch(re.escape(soname)+r'(?:\.\d+)*',Path(m.name).name)]
            if len(candidates)!=1: fail('Ambiguous/missing runtime library: '+soname)
            lib=archive.extractfile(candidates[0]).read()
            if lib[:4]!=b'\x7fELF' or lib[4]!=CONFIG['elf_class']: fail('Runtime ELF architecture mismatch')
            (target/soname).write_bytes(lib)
            for m in archive.getmembers():
                if m.isfile() and Path(m.name).name in ['copyright','changelog.Debian.gz'] and '/usr/share/doc/' in '/'+m.name:
                    (notices/(package+'-'+Path(m.name).name)).write_bytes(archive.extractfile(m).read())
        (notices/(package+'.json')).write_text(json.dumps(info,indent=2)+'\n')
    (notices/'PRIVATE_INSTALLATION.txt').write_text('Downloaded directly from Debian for this private installation. Not part of the public port release. Do not upload this installation. GCC source: https://sources.debian.org/src/gcc-12/ ; zlib source: https://sources.debian.org/src/zlib/\n')

def copy_game(source, target):
    # Copy the owner's complete payload, preserving legal notices and optional DLC.
    # Exclude private port state if source is an existing installation's game folder.
    for entry in source.iterdir():
        if entry.name.lower() in {'savedata','saves','logs','runtime','.git','source','__pycache__'}: continue
        if entry.name.startswith('.') or entry.name.endswith(('.log',)): continue
        out=target/entry.name
        if entry.is_symlink():
            resolved=entry.resolve()
            if not resolved.is_relative_to(source): fail('Game symlink points outside selected folder: '+entry.name)
        if entry.is_dir(): shutil.copytree(entry,out,symlinks=False)
        elif entry.is_file(): shutil.copy2(entry,out)


def extract_gog_installer(installer, destination):
    # GOG Linux installers commonly append a ZIP. Read its game payload only;
    # never execute the supplied shell script and never extract outside staging.
    if not zipfile.is_zipfile(installer):
        fail('Installer is not a supported GOG appended-ZIP .sh. Install it normally on Linux, then pass the installed game folder.')
    prefix='data/noarch/game/'
    count=0
    with zipfile.ZipFile(installer) as archive:
        for item in archive.infolist():
            if not item.filename.startswith(prefix): continue
            relative=Path(item.filename[len(prefix):])
            if relative.is_absolute() or '..' in relative.parts or '\\' in item.filename:
                fail('Unsafe path in installer')
            if not relative.parts: continue
            mode=item.external_attr>>16
            if mode & 0o170000 == 0o120000: fail('Installer game payload contains a symlink; use a normal installed game folder instead')
            target=destination/relative
            if item.is_dir(): target.mkdir(parents=True,exist_ok=True);continue
            target.parent.mkdir(parents=True,exist_ok=True)
            with archive.open(item) as src,target.open('wb') as dst:shutil.copyfileobj(src,dst)
            count+=1
    if not count: fail('No data/noarch/game/ payload found; install normally and pass its game folder.')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('linux_game_folder',type=Path)
    parser.add_argument('output_apps',type=Path,nargs='?',default=ROOT/'build/APPS')
    parser.add_argument('--runtime-debs',type=Path,help='Use the pinned .deb packages from this folder instead of downloading')
    parser.add_argument('--runtime-only',action='store_true',help='Only download/extract runtime libraries into a new private output folder')
    args=parser.parse_args()
    input_path=args.linux_game_folder.expanduser().resolve()
    installer_temp=None
    if input_path.is_file():
        if input_path.suffix.lower()!='.sh': fail('Pass a Linux game folder or your own GOG Linux .sh installer')
        installer_temp=tempfile.TemporaryDirectory(prefix='gog-private-game-')
        extracted=Path(installer_temp.name)
        print('Reading your GOG installer locally; the shell script will not be executed...',flush=True)
        extract_gog_installer(input_path,extracted)
        source,sha=find_game(extracted)
    else:
        source,sha=find_game(input_path)
    output=args.output_apps.expanduser().resolve(); dest=output/CONFIG['folder']; launcher=output/(CONFIG['folder']+'.sh')
    if output==source or output.is_relative_to(source) or source.is_relative_to(dest): fail('Output must be outside the source game folder')
    if dest.exists() or launcher.exists(): fail('Output already contains this port. Choose an empty output folder; existing saves are never overwritten.')
    output.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.prepare-'+CONFIG['id']+'-',dir=output) as tmp:
        staged=Path(tmp)/CONFIG['folder']; staged.mkdir()
        shutil.copytree(ROOT/CONFIG['folder'],staged,dirs_exist_ok=True)
        fetch_runtime(staged,args.runtime_debs)
        game=staged/'game'; game.mkdir(exist_ok=True)
        (game/'PUT_YOUR_LINUX_GAME_HERE.txt').unlink(missing_ok=True)
        if not args.runtime_only:
            print('Copying your Linux game (this may take a few minutes)...',flush=True)
            copy_game(source,game)
            (game/CONFIG['executable']).chmod(0o755)
        (staged/'PRIVATE_INSTALLATION_DO_NOT_PUBLISH.txt').write_text('Contains user-supplied commercial game files and/or downloaded GNU runtime libraries. Keep private.\nExecutable SHA-256: '+sha+'\n')
        # Commit only after all downloads/copies have succeeded.
        staged.rename(dest)
        shutil.copy2(ROOT/(CONFIG['folder']+'.sh'),launcher); launcher.chmod(0o755)
    if installer_temp: installer_temp.cleanup()
    print('Ready:',output)
    if args.runtime_only: print('Runtime-only mode: copy your game into',dest/'game','before launch.')
    print('Copy '+CONFIG['folder']+' and '+CONFIG['folder']+'.sh to TF2/Roms/APPS/. Keep this generated installation private.')

if __name__=='__main__':
    try: main()
    except (ValueError,OSError,StopIteration,tarfile.TarError) as error:
        print('ERROR:',error,file=sys.stderr);sys.exit(1)
