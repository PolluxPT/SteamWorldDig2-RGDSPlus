#!/usr/bin/env python3
import os,hashlib,json,zipfile
from pathlib import Path
from audit_public import ROOT,check
if check():raise SystemExit(1)
config=json.loads((ROOT/'port.json').read_text())
out=ROOT/'dist'/(config['folder']+'_RGDSPlus_Public_Kit_v'+config['version']+'.zip')
out.parent.mkdir(exist_ok=True)
files=sorted(json.loads((ROOT/'PUBLIC_MANIFEST.json').read_text()))+['PUBLIC_MANIFEST.json']
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
    for name in files:archive.write(ROOT/name,name)
with out.open('rb') as durable: os.fsync(durable.fileno())
with zipfile.ZipFile(out) as archive:
    if archive.testzip():raise SystemExit('ZIP validation failed')
print(out)
print('SHA256:',hashlib.sha256(out.read_bytes()).hexdigest())
