#!/usr/bin/env python3
"""Source-only fixture checks. Does not need or launch a commercial game."""
import hashlib,importlib.util,tempfile,zipfile
from pathlib import Path
spec=importlib.util.spec_from_file_location('prepare_game',Path(__file__).with_name('prepare_game.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp);src=root/'my legal game/game';src.mkdir(parents=True)
    cfg=m.CONFIG;exe=src/cfg['executable'];assets=src/cfg['assets'];assets.mkdir()
    header=bytearray(64);header[:6]=b'\x7fELF'+bytes([cfg['elf_class'],1]);header[18:20]=cfg['machine'].to_bytes(2,'little');exe.write_bytes(header)
    # Supply a synthetic executable fingerprint to test mechanics, never to
    # change the production port.json supported-build restriction.
    cfg['sha256']=hashlib.sha256(header).hexdigest()
    assert m.find_game(src)[0]==src.resolve()
    exe.write_bytes(b'MZ wrong architecture')
    try:m.find_game(src)
    except ValueError:pass
    else:raise AssertionError('Wrong architecture accepted')
    exe.write_bytes(header);cfg['sha256']='0'*64
    try:m.find_game(src)
    except ValueError:pass
    else:raise AssertionError('Wrong fingerprint accepted')
    cfg['sha256']=hashlib.sha256(header).hexdigest()
    installer=root/'gog fixture.sh';installer.write_bytes(b'#!/bin/sh\n# Never execute\n')
    with zipfile.ZipFile(installer,'a') as z:
        z.writestr('data/noarch/game/'+cfg['executable'],header)
        z.writestr('data/noarch/game/'+cfg['assets']+'/fixture.txt','test data')
    out=root/'extracted';out.mkdir();m.extract_gog_installer(installer,out)
    assert m.find_game(out)[0]==out.resolve()
    bad=root/'bad.sh'
    with zipfile.ZipFile(bad,'w') as z:z.writestr('data/noarch/game/../../escape','bad')
    try:m.extract_gog_installer(bad,root/'bad')
    except ValueError:pass
    else:raise AssertionError('Unsafe path accepted')
    assert not (root/'escape').exists()
print('PASS: synthetic ELF/hash validation, local GOG extraction, path traversal rejection')
