#!/usr/bin/env python3
"""Optional real Hermes CLI lifecycle smoke test in a disposable HOME.

No model requests, provider setup, production access or user profile inspection.
Exit 77 means prerequisites are unavailable; it is not a passing test.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from repo_utils import ROOT,read_catalog,dump

class NativeFailure(RuntimeError):pass

def run(binary:str)->dict:
    executable=shutil.which(binary)
    if not executable:
        return {'status':'BLOCKED','reason':'Hermes CLI is not installed/available','tests_executed':0,'live_model_calls':0}
    results=[]
    with tempfile.TemporaryDirectory(prefix='hermes-native-smoke-') as d:
        base=Path(d);home=base/'user';home.mkdir();hermes_home=home/'.hermes';hermes_home.mkdir()
        (base/'tmp').mkdir()
        env={k:v for k,v in os.environ.items() if k in {'PATH','SYSTEMROOT','WINDIR','COMSPEC','PATHEXT','LANG','LC_ALL'}}
        env.update({'HOME':str(home),'USERPROFILE':str(home),'HERMES_HOME':str(hermes_home),
                    'XDG_CONFIG_HOME':str(home/'config'),'XDG_DATA_HOME':str(home/'data'),
                    'XDG_CACHE_HOME':str(home/'cache'),'APPDATA':str(home/'appdata'),
                    'TMPDIR':str(base/'tmp'),'TEMP':str(base/'tmp'),'TMP':str(base/'tmp'),
                    'PYTHONIOENCODING':'utf-8','PYTHONUTF8':'1'})
        def cli(args):
            done=subprocess.run([executable,*args],cwd=base,env=env,capture_output=True,text=True,timeout=120)
            if done.returncode:raise NativeFailure('CLI failed: '+json.dumps(args)+'\n'+done.stderr[-2000:]+done.stdout[-2000:])
            return done.stdout
        try:
            version=cli(['--version'])
            if not re.search(r'\b0\.22\.5\b',version):
                return {'status':'BLOCKED','reason':'This smoke recipe is qualified only against the documentary v0.22.5 baseline; review a different runtime first','version_output':version.strip(),'tests_executed':0,'live_model_calls':0}
            for profile in read_catalog()['profiles']:
                name='probe-'+profile
                source=base/'sources'/profile
                shutil.copytree(ROOT/'profiles'/profile,source,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
                cli(['profile','install',str(source),'--name',name,'--yes'])
                target=hermes_home/'profiles'/name
                if not target.is_dir():raise NativeFailure('Native profile did not resolve inside the disposable HERMES_HOME')
                cli(['profile','info',name])
                listing=cli(['-p',name,'skills','list'])
                if 'agent-folder-architect' not in listing:raise NativeFailure('Shared skill not found in native list')
                config=target/'config.yaml';config.write_text(config.read_text()+'\n# native-smoke-local-choice\n')
                before=config.read_bytes()
                memory=target/'memories';memory.mkdir(exist_ok=True)
                marker=memory/'MEMORY.md';marker.write_text('Synthetic local preservation marker.\n')
                local=target/'skills/local-probe';local.mkdir(parents=True)
                (local/'SKILL.md').write_text('---\nname: local-probe\ndescription: Synthetic preservation check.\n---\n# Probe\n')
                (source/'SOUL.md').write_text((source/'SOUL.md').read_text()+'\nNative smoke synthetic revision.\n')
                cli(['profile','update',name,'--yes'])
                if config.read_bytes()!=before:raise NativeFailure('Local configuration was not preserved')
                if marker.read_text()!='Synthetic local preservation marker.\n':raise NativeFailure('Local memory marker changed')
                if not (local/'SKILL.md').exists():raise NativeFailure('Local added skill disappeared')
                if 'Native smoke synthetic revision.' not in (target/'SOUL.md').read_text():raise NativeFailure('Distribution update did not reach SOUL')
                results.append({'profile':profile,'status':'PASS','checks':['install','profile-info','skill-list','update','config-preservation','memory-preservation','local-skill-preservation']})
            return {'status':'PASS','version_output':version.strip(),'tests_executed':len(results)*7,'profiles':results,'live_model_calls':0,
                    'limits':['Does not prove auto-load in a model request, agent behavior, IAM or production integration.']}
        except (OSError,subprocess.TimeoutExpired,NativeFailure) as exc:
            return {'status':'FAIL','reason':str(exc),'profiles':results,'tests_executed':len(results)*7,'live_model_calls':0}

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--hermes',default='hermes');p.add_argument('--out',type=Path);a=p.parse_args()
    result=run(a.hermes)
    if a.out:dump(a.out,result)
    print(json.dumps(result,indent=2))
    return 0 if result['status']=='PASS' else (77 if result['status']=='BLOCKED' else 1)
if __name__=='__main__':raise SystemExit(main())
