#!/usr/bin/env python3
"""Check the public release allowlist; never scan or package private build/."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKIP={'.git','build','dist','cache','__pycache__'}

def files():
    return {p.relative_to(ROOT).as_posix():p for p in ROOT.rglob('*') if p.is_file() and not any(part in SKIP for part in p.relative_to(ROOT).parts) and p.name!='PUBLIC_MANIFEST.json'}

def check():
    expected=json.loads((ROOT/'PUBLIC_MANIFEST.json').read_text())
    actual=files();errors=[]
    for name in sorted(set(expected)^set(actual)):errors.append('Unexpected/missing public file: '+name)
    for name in sorted(set(expected)&set(actual)):
        if hashlib.sha256(actual[name].read_bytes()).hexdigest()!=expected[name]:errors.append('Changed public file: '+name)
    # Files ignored on disk are still unsafe if someone explicitly staged them.
    result=subprocess.run(['git','-C',str(ROOT),'ls-files','-z'],capture_output=True)
    if result.returncode==0:
        for raw in result.stdout.split(b'\0'):
            if raw:
                name=raw.decode()
                if name not in expected and name!='PUBLIC_MANIFEST.json':errors.append('Unapproved Git-tracked file: '+name)
    if errors:
        print('\n'.join(errors),file=sys.stderr);return 1
    print('PASS:',len(expected),'approved public files; hashes verified. Private build/ is excluded.')
    return 0
if __name__=='__main__':sys.exit(check())
