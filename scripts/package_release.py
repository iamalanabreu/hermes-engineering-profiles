#!/usr/bin/env python3
"""Build reproducible ZIPs from validated source; no signing or publishing."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import zipfile
from repo_utils import ROOT,read_catalog,files,dump
from validate_distributions import validate

STAMP=(2026,11,1,0,0,0)

def archive(source:Path,destination:Path,prefix:str,*,exclude:tuple[Path,...]=())->dict:
    items=[]
    for p in files(source):
        if any(p==x or x in p.parents for x in exclude):continue
        if 'dist' in p.relative_to(source).parts:continue
        items.append(p)
    destination.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(destination,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in items:
            rel=p.relative_to(source).as_posix()
            name=(prefix.rstrip('/')+'/'+rel) if prefix else rel
            info=zipfile.ZipInfo(name,STAMP);info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=(0o100644<<16);info.create_system=3
            z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    return {'file':destination.name,'files':len(items),'bytes':destination.stat().st_size,
            'sha256':hashlib.sha256(destination.read_bytes()).hexdigest()}

def package(out:Path,root:Path=ROOT)->dict:
    result=validate(root)
    if result['status']!='PASS':raise ValueError('Validation failed: '+json.dumps(result['errors']))
    out=out.resolve();out.mkdir(parents=True,exist_ok=True)
    catalog=read_catalog(root);version=catalog['version'];packages=[]
    packages.append(archive(root,out/('hermes-engineering-profiles-'+version+'.zip'),'hermes-engineering-profiles',exclude=(out,)))
    for profile in catalog['profiles']:
        version=catalog['profile_versions'][profile]
        packages.append(archive(root/'profiles'/profile,out/(profile+'-'+version+'.zip'),profile))
    data={'schema_version':1,'repository_version':catalog['version'],'packages':packages}
    dump(out/'SHA256SUMS.json',data)
    (out/'SHA256SUMS.txt').write_text(''.join(p['sha256']+'  '+p['file']+'\n' for p in packages))
    return data

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    try:print(json.dumps(package(a.out),indent=2));return 0
    except (OSError,ValueError,KeyError) as exc:print(json.dumps({'status':'FAIL','error':str(exc)}));return 1
if __name__=='__main__':raise SystemExit(main())
