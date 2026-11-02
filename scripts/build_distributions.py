#!/usr/bin/env python3
"""Synchronize generated shared skills. Default checks only; --write updates known generated copies."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import tempfile
from repo_utils import ROOT,read_catalog,sha,tree_hashes,dump

LOCK='shared-skills.lock.json'

def synchronize(root:Path=ROOT,*,write:bool=False)->dict:
    catalog=read_catalog(root)
    lock_path=root/LOCK
    previous=json.loads(lock_path.read_text()) if lock_path.exists() else {'generated':{},'helper_sha256':None}
    canonical=root/'shared-skills/agent-folder-architect/scripts/safe_files.py'
    helper=root/'shared-skills/project-context-architect/scripts/safe_files.py'
    if helper.is_symlink():raise ValueError('Refusing symlinked generated helper')
    helper_mismatch=not helper.exists() or sha(helper)!=sha(canonical)
    if helper_mismatch:
        if not write:raise ValueError('Generated project helper differs from canonical helper; run build --write')
        if helper.exists() and previous.get('helper_sha256') not in (None,sha(helper)):
            raise ValueError('Generated helper was edited; preserve/resolve that diff before building')
        shutil.copy2(canonical,helper)
    operations=[];expected={}
    for profile in catalog['profiles']:
        for skill in catalog['shared']:
            src=root/'shared-skills'/skill; rel='profiles/'+profile+'/skills/'+skill; dst=root/rel
            hashes=tree_hashes(src);current=tree_hashes(dst)
            expected[rel]=hashes
            if current!=hashes:
                if dst.exists() and current!=previous.get('generated',{}).get(rel):
                    raise ValueError('Generated skill has local edits or no provenance: '+rel)
                operations.append((src,dst,rel))
    if operations and not write:
        raise ValueError('Shared skill drift: '+', '.join(r for _,_,r in operations))
    if write:
        for src,dst,rel in operations:
            dst.parent.mkdir(parents=True,exist_ok=True)
            staging=Path(tempfile.mkdtemp(prefix='.shared-stage-',dir=dst.parent))
            candidate=staging/'content';backup=staging/'previous'
            try:
                shutil.copytree(src,candidate,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.DS_Store'))
                if dst.exists():dst.rename(backup)
                try:candidate.rename(dst)
                except Exception:
                    if backup.exists():backup.rename(dst)
                    raise
            finally:shutil.rmtree(staging)
        dump(lock_path,{'schema_version':1,'helper_sha256':sha(canonical),'generated':expected})
    elif not lock_path.exists() or previous.get('generated')!=expected or previous.get('helper_sha256')!=sha(canonical):
        raise ValueError('Generated lock is stale; run build --write and review the diff')
    return {'status':'PASS','mode':'write' if write else 'check','shared_skills':len(catalog['shared']),
            'profile_copies':len(expected),'updated':[r for _,_,r in operations]}

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');a=p.parse_args()
    try:print(json.dumps(synchronize(write=a.write),indent=2));return 0
    except (OSError,ValueError,KeyError) as exc:print(json.dumps({'status':'FAIL','error':str(exc)}));return 1
if __name__=='__main__':raise SystemExit(main())
