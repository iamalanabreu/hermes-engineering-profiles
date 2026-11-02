#!/usr/bin/env python3
"""Preview an exact native installation command; execute only with --apply.

Does not clone a live profile, set credentials, or publish a repository.
"""
from __future__ import annotations
import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path
from repo_utils import ROOT,read_catalog,tree_hashes

def plan(profile:str,name:str,binary:str='hermes',alias:bool=False)->dict:
    catalog=read_catalog()
    if profile not in catalog['profiles']:raise ValueError('Unknown template')
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}',name) or name=='default':raise ValueError('Invalid instance name')
    source=(ROOT/'profiles'/profile).resolve()
    command=[binary,'profile','install',str(source),'--name',name]
    if alias:command.append('--alias')
    return {'template':profile,'instance':name,'source':str(source),'command':command,
            'source_files':len(tree_hashes(source)),
            'notes':['Native installer handles name conflicts and confirmation.','Keep this source path stable for native update.','Configure an approved provider separately in the new instance.','No credentials or live-state cloning is performed.']}

def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--profile',required=True,choices=sorted(read_catalog()['profiles']))
    p.add_argument('--name',required=True);p.add_argument('--hermes',default='hermes');p.add_argument('--alias',action='store_true');p.add_argument('--apply',action='store_true')
    a=p.parse_args()
    try:
        out=plan(a.profile,a.name,a.hermes,a.alias);print(json.dumps(out,indent=2))
        if not a.apply:return 0
        executable=shutil.which(a.hermes)
        if executable is None:raise ValueError('Hermes executable not found; nothing installed')
        command=out['command'];command[0]=executable
        # Interactive confirmation stays native. Never add --force or --yes here.
        return subprocess.run(command,check=False).returncode
    except (OSError,ValueError) as exc:print(json.dumps({'status':'blocked','error':str(exc)}));return 2
if __name__=='__main__':raise SystemExit(main())
