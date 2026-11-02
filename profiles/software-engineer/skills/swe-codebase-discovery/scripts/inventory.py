#!/usr/bin/env python3
"""Bounded repository metadata inventory. No shell, network, dependency execution or secret reads."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path

SKIP={'.git','.hg','.svn','.venv','venv','node_modules','vendor','dist','build','coverage','__pycache__','target'}
MANIFESTS={'package.json':'javascript/typescript','pyproject.toml':'python','requirements.txt':'python',
 'go.mod':'go','Cargo.toml':'rust','pom.xml':'java','build.gradle':'jvm','build.gradle.kts':'jvm',
 'composer.json':'php','Gemfile':'ruby','CMakeLists.txt':'c/c++','Makefile':'build','Dockerfile':'container'}

def inventory(root:Path,max_files:int=5000,max_depth:int=8)->dict:
    root=root.expanduser()
    for p in (root.absolute(),*root.absolute().parents):
        if p.is_symlink():raise ValueError('Symlinked workspace is not accepted')
    root=root.resolve(strict=True)
    if not root.is_dir() or root==Path(root.anchor) or root==Path.home().resolve():raise ValueError('Explicit bounded workspace required')
    if max_files<1 or max_depth<0:raise ValueError('Invalid inventory limits')
    manifests=[];instructions=[];files=0;skipped_symlinks=0;truncated=False
    for current,dirs,names in os.walk(root,followlinks=False):
        cur=Path(current);depth=len(cur.relative_to(root).parts)
        kept=[]
        for d in sorted(dirs):
            p=cur/d
            if p.is_symlink():skipped_symlinks+=1;continue
            if d in SKIP or d.startswith('.'):continue
            if depth>=max_depth:truncated=True;continue
            kept.append(d)
        dirs[:]=kept
        for name in sorted(names):
            p=cur/name
            if p.is_symlink():skipped_symlinks+=1;continue
            if name.startswith('.'):continue
            files+=1
            if files>max_files:truncated=True;break
            rel=p.relative_to(root).as_posix()
            if name in {'AGENTS.md','HERMES.md','CLAUDE.md','README.md'}:instructions.append(rel)
            language=MANIFESTS.get(name)
            if name.endswith(('.csproj','.fsproj','.sln')):language='dotnet'
            if language:
                row={'path':rel,'ecosystem_hint':language,'execution':'not executed'}
                if name=='package.json' and p.stat().st_size<=100_000:
                    try:
                        obj=json.loads(p.read_text(encoding='utf-8'))
                        if not isinstance(obj,dict):raise ValueError('Manifest must be an object')
                        scripts=obj.get('scripts',{})
                        row['script_names']=sorted(scripts) if isinstance(scripts,dict) else []
                        row['dependency_count']=sum(len(obj.get(k,{})) for k in ['dependencies','devDependencies'] if isinstance(obj.get(k,{}),dict))
                    except (ValueError,OSError,UnicodeError):row['parse_status']='unreadable_or_invalid'
                manifests.append(row)
        if files>max_files:break
    return {'schema_version':1,'root':str(root),'files_seen':min(files,max_files),'truncated':truncated,
            'skipped_symlinks':skipped_symlinks,'manifests':manifests,'instruction_candidates':instructions,
            'limits':'Metadata hints only; does not identify active architecture, prove quality or authorize executing project scripts. Hidden instruction files need a separate scoped read.'}

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path)
    p.add_argument('--max-files',type=int,default=5000);p.add_argument('--max-depth',type=int,default=8);a=p.parse_args()
    try:print(json.dumps(inventory(a.root,a.max_files,a.max_depth),indent=2));return 0
    except (OSError,ValueError,TypeError) as exc:print(json.dumps({'status':'blocked','error':str(exc)}));return 2
if __name__=='__main__':raise SystemExit(main())
