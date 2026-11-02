#!/usr/bin/env python3
"""Portable front door for Agent Folder Architect; no network or shell execution."""
from __future__ import annotations
import argparse
import json
import posixpath
import re
from pathlib import Path
from urllib.parse import unquote
from scaffold import BlueprintError, file_content, load_blueprint, scan_secrets
from safe_files import SafetyError, apply_plan, create_tree, load_plan, make_plan, plan_diff, root_dir, safe_relative, target_path, write_plan

LAYOUT_MAP={'arquivos':'references/files','exemplos':'examples','validacao':'references/validation',
            'referencias':'references/domain','testes':'scripts/tests','notas.md':'references/notes.md',
            'PENDENCIAS.md':'references/pending.md','AGENTS.md':'references/project-guidance.md'}
LINK=re.compile(r'\]\(([^)]+)\)')

def mapped(path: str, layout: str) -> str:
    if layout=='operational': return path
    first,sep,rest=path.partition('/')
    return LAYOUT_MAP.get(first,first)+(('/'+rest) if sep else '')

def render(spec: dict, layout: str) -> dict[str,str]:
    if layout not in {'operational','hermes'}: raise SafetyError('Unknown layout')
    original=file_content(spec)
    if layout=='operational': return original
    result={}
    for old_path,text in original.items():
        new_path=mapped(old_path,layout)
        def rewrite(match):
            raw=match.group(1)
            if raw.startswith(('http://','https://','mailto:','#')): return match.group(0)
            name,sep,anchor=raw.partition('#')
            absolute=posixpath.normpath(posixpath.join(posixpath.dirname(old_path),name))
            dest=mapped(absolute,layout)
            relative=posixpath.relpath(dest,posixpath.dirname(new_path) or '.')
            return ']('+relative+('#'+anchor if sep else '')+')'
        result[new_path]=LINK.sub(rewrite,text)
    if layout=='hermes':
        # Explicit direct links ensure third-party skill installers see the full bundle.
        refs='\n## Portable resource manifest\n\n'+''.join('- ['+p+']('+p+')\n' for p in sorted(result) if p!='SKILL.md')
        result['SKILL.md']+=refs
    return result

def validate(folder: Path, spec: dict, layout: str) -> dict:
    root=root_dir(folder)
    expected=render(spec,layout)
    errors=[]; warnings=[]
    for rel,text in expected.items():
        try:
            p=target_path(root,rel)
            if not p.exists(): errors.append('Missing: '+rel); continue
            current=p.read_text(encoding='utf-8')
            if rel=='SKILL.md':
                front=re.match(r'\A---\nname: ([a-z0-9-]+)\ndescription: (.+)\n---\n',current)
                if not front or front.group(1)!=spec['slug']:
                    errors.append('Invalid generated skill frontmatter: '+rel)
            if current!=text: warnings.append('Changed since blueprint: '+rel)
            for match in LINK.findall(current):
                if match.startswith(('http://','https://','mailto:','#')): continue
                q=(p.parent/unquote(match.split('#',1)[0])).resolve()
                try: q.relative_to(root)
                except ValueError: errors.append('Link escapes package: '+rel); continue
                if not q.exists(): errors.append('Broken local link: '+rel+' -> '+match)
            scan_secrets(current,rel)
        except (SafetyError,BlueprintError,UnicodeError,OSError) as exc: errors.append(str(exc))
    for p in root.rglob('*'):
        if p.is_symlink(): errors.append('Symlink: '+str(p.relative_to(root)))
    warnings.append('Structure only: external workflows and model behavior were not executed')
    return {'ok':not errors,'errors':sorted(set(errors)),'warnings':sorted(set(warnings)),'expected_files':len(expected)}

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    for name in ('create','validate','evolve-plan'):
        p=sub.add_parser(name)
        p.add_argument('--spec',type=Path,required=True)
        p.add_argument('--layout',choices=['operational','hermes'],default='operational')
        p.add_argument('--root' if name=='create' else '--folder',type=Path,required=True)
        if name=='create': p.add_argument('--apply',action='store_true',help='Default is a non-mutating preview')
        if name=='evolve-plan': p.add_argument('--out',type=Path,required=True)
    p=sub.add_parser('evolve-apply'); p.add_argument('--plan',type=Path,required=True)
    p.add_argument('--approve-sha256',required=True)
    args=parser.parse_args()
    try:
        if args.command=='evolve-apply':
            plan=load_plan(args.plan,args.approve_sha256)
            if plan['kind']!='operational-capability': raise SafetyError('Not an operational-capability plan')
            for row in plan['changes']: scan_secrets(row['content'],row['path'])
            result=apply_plan(plan)
        else:
            spec=load_blueprint(args.spec)
            files=render(spec,args.layout)
            if args.command=='create': result=create_tree(args.root,spec['slug'],files,dry_run=not args.apply)
            elif args.command=='validate':
                result=validate(args.folder,spec,args.layout)
                print(json.dumps(result,ensure_ascii=False,indent=2)); return 0 if result['ok'] else 1
            else:
                plan=make_plan(args.folder,files,kind='operational-capability')
                for row in plan['changes']:
                    old=Path(plan['root'])/row['path']
                    if old.exists(): scan_secrets(old.read_text(encoding='utf-8'),row['path'])
                diff=plan_diff(plan)
                result=write_plan(plan,args.out)
                result['diff']=diff
        print(json.dumps(result,ensure_ascii=False,indent=2)); return 0
    except (BlueprintError,SafetyError,OSError,ValueError,KeyError,TypeError) as exc:
        print(json.dumps({'status':'blocked','error':str(exc)},ensure_ascii=False)); return 2

if __name__=='__main__': raise SystemExit(main())
