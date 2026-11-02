#!/usr/bin/env python3
"""Read-only baseline audit of an explicitly selected installed profile directory.

Reads only config.yaml, SOUL.md and shipped skill files. Never reads auth, memory,
sessions or .env. Does not print configuration values or claim active-session behavior.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import yaml
from repo_utils import ROOT,read_catalog,sha,tree_hashes

def inspect(profile:str,directory:Path)->dict:
    catalog=read_catalog()
    if profile not in catalog['profiles']:raise ValueError('Unknown template')
    for p in (directory.absolute(),*directory.absolute().parents):
        if p.is_symlink():raise ValueError('Refusing symlinked profile directory')
    directory=directory.resolve(strict=True)
    source=ROOT/'profiles'/profile
    config_path=directory/'config.yaml'
    if config_path.is_symlink():raise ValueError('Refusing symlinked configuration')
    if config_path.stat().st_size>1_000_000:raise ValueError('Unexpected configuration size')
    try:
        current=yaml.safe_load(config_path.read_text())
    except yaml.YAMLError as exc:
        raise ValueError('Invalid YAML in local configuration; values are not included in this report') from None
    expected=yaml.safe_load((source/'config.yaml').read_text())
    if not isinstance(current,dict):raise ValueError('Invalid configuration mapping')
    mismatches=[]
    for section,values in expected.items():
        for key,wanted in values.items():
            if not isinstance(current.get(section),dict) or current[section].get(key)!=wanted:
                mismatches.append(section+'.'+key)
    drift=[]
    soul=directory/'SOUL.md'
    if not soul.exists() or soul.is_symlink() or sha(soul)!=sha(source/'SOUL.md'):drift.append('SOUL.md')
    for skill in catalog['shared']+catalog['profiles'][profile]:
        actual=tree_hashes(directory/'skills'/skill);wanted=tree_hashes(source/'skills'/skill)
        if actual!=wanted:drift.append('skills/'+skill)
    return {'status':'DRIFT' if drift or mismatches else 'MATCH','template':profile,
            'baseline_config_keys_differing':mismatches,'content_drift':drift,
            'scope':'Files/configuration only. Does not prove skill discovery, session loading, IAM or sandboxing.'}

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--profile',required=True);p.add_argument('--directory',type=Path,required=True);a=p.parse_args()
    try:
        out=inspect(a.profile,a.directory);print(json.dumps(out,indent=2));return 0 if out['status']=='MATCH' else 3
    except (OSError,ValueError,TypeError,yaml.YAMLError) as exc:print(json.dumps({'status':'blocked','error':str(exc)}));return 2
if __name__=='__main__':raise SystemExit(main())
