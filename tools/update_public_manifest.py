#!/usr/bin/env python3
"""Maintainer-only manifest refresh. Review source changes before running."""
import hashlib,json
from pathlib import Path
from audit_public import ROOT,files
old=json.loads((ROOT/'PUBLIC_MANIFEST.json').read_text())
current=files()
for name,p in current.items():
    if name not in old:raise SystemExit('New files require explicit inventory review: '+name)
    if name.startswith('SteamWorld') and '/runtime/' in name and (p.suffix=='.so' or p.name.startswith(('box64','libGL.so'))):
        if hashlib.sha256(p.read_bytes()).hexdigest()!=old[name]:raise SystemExit('Binary changed; review provenance/license and hardware-test before updating: '+name)
(ROOT/'PUBLIC_MANIFEST.json').write_text(json.dumps({n:hashlib.sha256(p.read_bytes()).hexdigest() for n,p in sorted(current.items())},indent=2)+'\n')
print('Refreshed existing public files. Review this manifest diff before publishing.')
