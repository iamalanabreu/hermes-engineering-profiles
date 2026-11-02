#!/usr/bin/env python3
"""Static contract validator. Does not execute Hermes, cloud tools or a model."""
from __future__ import annotations
import argparse
import ast
import json
from pathlib import Path
import re
from urllib.parse import unquote
import yaml
from repo_utils import ROOT,read_catalog,files,dump
from build_distributions import synchronize

MANIFEST_FIELDS={'name','version','description','hermes_requires','author','license','env_requires','distribution_owned'}
APPROVAL_KEYS={'mode':'manual','cron_mode':'deny','single_query_mode':'deny','unattended_mode':'deny'}
SECRET_PATTERNS=[re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
                 re.compile(r'\b(?:AKIA|ASIA)[0-9A-Z]{16}\b'),re.compile(r'\bgh[pousr]_[A-Za-z0-9_]{20,}\b')]
LINK=re.compile(r'\]\(([^)]+)\)')

def skill_metadata(path:Path)->dict:
    text=path.read_text(encoding='utf-8')
    match=re.match(r'\A---\n(.*?)\n---(?:\n|$)',text,re.S)
    if not match:raise ValueError('Missing frontmatter: '+str(path))
    data=yaml.safe_load(match.group(1))
    if not isinstance(data,dict) or not isinstance(data.get('name'),str) or not isinstance(data.get('description'),str):raise ValueError('Invalid skill metadata: '+str(path))
    if data['name']!=path.parent.name or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',data['name']):raise ValueError('Skill name/path mismatch: '+str(path))
    if not data['description'].strip() or len(data['description'])>1024:raise ValueError('Invalid skill description')
    if len(text)>40_000:raise ValueError('Entrypoint exceeds repository context budget: '+str(path))
    return data

def validate(root:Path=ROOT)->dict:
    errors=[];warnings=[]
    try:catalog=read_catalog(root)
    except Exception as exc:return {'status':'FAIL','errors':[str(exc)],'warnings':[]}
    count=0
    for profile,specialized in catalog['profiles'].items():
        home=root/'profiles'/profile
        try:
            manifest=yaml.safe_load((home/'distribution.yaml').read_text())
            if not isinstance(manifest,dict) or set(manifest)-MANIFEST_FIELDS:raise ValueError('Unknown manifest fields: '+profile)
            if manifest['name']!=profile or manifest['version']!=catalog['profile_versions'][profile]:raise ValueError('Manifest identity/version mismatch')
            if manifest.get('hermes_requires')!='>=0.22.5':raise ValueError('Unexpected native feature floor')
            if manifest.get('env_requires')!=[]:raise ValueError('Generic profiles must not require a provider secret')
            expected=['SOUL.md','config.yaml','distribution.yaml']+['skills/'+s for s in catalog['shared']+specialized]
            if manifest['distribution_owned']!=expected:raise ValueError('Owned paths do not match explicit inventory: '+profile)
            config=yaml.safe_load((home/'config.yaml').read_text())
            if set(config)!={'approvals','skills','memory'}:raise ValueError('Unexpected generic configuration sections')
            if config['approvals']!=APPROVAL_KEYS:raise ValueError('Approval baseline drift')
            desired={'auto_load':['agent-folder-architect'],'write_approval':True,'project_discovery':True,'template_vars':True,'inline_shell':False}
            if config['skills']!=desired or config['memory']!={'write_approval':True}:raise ValueError('Skills/memory baseline drift')
            soul=(home/'SOUL.md').read_text()
            for required in ['agent-folder-architect','project-context-architect','not an OS sandbox','not tested','authorization']:
                if required not in soul:raise ValueError('SOUL missing invariant: '+required)
            for s in catalog['shared']+specialized:
                path=home/'skills'/s/'SKILL.md';skill_metadata(path);count+=1
                if not (path.parent/'agents/openai.yaml').exists():raise ValueError('Missing skill UI metadata: '+s)
                if s in specialized:
                    for part in ['references/decision-guide.md','references/verification.md','references/sources.md','templates/deliverable.md','examples/scenario.md']:
                        if not (path.parent/part).is_file():raise ValueError('Missing technical resource: '+s+'/'+part)
                if s=='agent-folder-architect' and len(path.read_text())>8_500:raise ValueError('Preloaded skill exceeds compact budget')
            actual={p.name for p in (home/'skills').iterdir() if p.is_dir() and not p.name.startswith('.')}
            if actual!=set(catalog['shared']+specialized):raise ValueError('Unexpected skill directories: '+profile)
        except (OSError,ValueError,KeyError,TypeError,yaml.YAMLError) as exc:errors.append(str(exc))
    try:synchronize(root)
    except (OSError,ValueError,KeyError) as exc:errors.append(str(exc))
    file_count=0;python_count=0
    try:
        for p in files(root):
            file_count+=1;rel=p.relative_to(root).as_posix()
            if p.name in {'.env','auth.json','state.db','projects.db'} or p.suffix in {'.pem','.p12','.key'}:
                errors.append('Forbidden runtime/credential file: '+rel)
            if p.suffix=='.py':
                python_count+=1
                try:ast.parse(p.read_text(encoding='utf-8'),filename=rel)
                except (SyntaxError,UnicodeError) as exc:errors.append(str(exc))
            if p.suffix not in {'.md','.yaml','.yml','.json','.jsonl','.py','.txt','.toml','.sh'}:continue
            text=p.read_text(encoding='utf-8')
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):errors.append('Possible secret in '+rel)
            if p.suffix=='.md':
                for link in LINK.findall(text):
                    if link.startswith(('http://','https://','mailto:','#','skills://')):continue
                    target=unquote(link.split('#',1)[0])
                    if not target or '{{' in target:continue
                    candidate=(p.parent/target).resolve()
                    try:candidate.relative_to(root.resolve())
                    except ValueError:errors.append('Link outside repository: '+rel+' -> '+link);continue
                    if not candidate.exists():errors.append('Broken local link: '+rel+' -> '+link)
                if p.name=='SKILL.md' and re.search(r'\b(?:TODO|TBD|PREENCHER AQUI)\b',text,re.I):
                    errors.append('Unresolved entrypoint marker: '+rel)
    except (OSError,ValueError,UnicodeError) as exc:errors.append(str(exc))
    warnings.extend(['Static validation is not native Hermes runtime qualification.',
                     'Pattern-based secret checks are limited; run a dedicated scanner before publication.',
                     'Live model behavior, provider integration and production permissions require separate evaluation.'])
    return {'status':'FAIL' if errors else 'PASS','profiles':len(catalog['profiles']),
            'canonical_skills':len(catalog['shared'])+sum(map(len,catalog['profiles'].values())),
            'installed_skill_copies':count,'files_checked':file_count,'python_files_parsed':python_count,
            'errors':sorted(set(errors)),'warnings':warnings}

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path);a=p.parse_args()
    result=validate()
    if a.out:dump(a.out,result)
    print(json.dumps(result,indent=2));return 0 if result['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
