#!/usr/bin/env python3
"""Run local contract/fixture checks and write an honest qualification report.

No cloud, model or installed-user-profile access. --native invokes the separately
reviewable disposable-home smoke recipe; a missing runtime remains BLOCKED.
"""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
from repo_utils import ROOT,dump

def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--native',action='store_true',help='Try the optional native lifecycle probe in a disposable HOME')
    p.add_argument('--require-native',action='store_true',help='Block overall success unless the native probe passes')
    a=p.parse_args();reports=ROOT/'reports';reports.mkdir(exist_ok=True)
    jobs=[('shared-integrity',['scripts/build_distributions.py']),
          ('static-validation',['scripts/validate_distributions.py']),
          ('repository-tests',['-m','unittest','discover','-s','tests','-v']),
          ('original-architect-tests',['-m','unittest','discover','-s','shared-skills/agent-folder-architect/tests','-v']),
          ('evaluation-corpus',['scripts/check_evals.py'])]
    env=dict(os.environ);env['PYTHONUTF8']='1';results=[];test_count=0
    for label,args in jobs:
        run=subprocess.run([sys.executable,*args],cwd=ROOT,capture_output=True,text=True,env=env)
        output=run.stdout+run.stderr
        (reports/(label+'.log')).write_text(output,encoding='utf-8')
        match=re.search(r'Ran (\d+) tests?',output)
        count=int(match.group(1)) if match else None
        if count is not None and run.returncode==0:test_count+=count
        results.append({'check':label,'command':['python',*args],'status':'PASS' if run.returncode==0 else 'FAIL','exit_code':run.returncode,'tests':count,'evidence':label+'.log'})
    native={'status':'NOT_RUN','reason':'Pass --native to try the disposable-home lifecycle probe','tests_executed':0,'live_model_calls':0}
    if a.native or a.require_native:
        run=subprocess.run([sys.executable,'scripts/smoke_native.py','--out','reports/native-smoke.json'],cwd=ROOT,capture_output=True,text=True,env=env)
        (reports/'native-smoke.log').write_text(run.stdout+run.stderr,encoding='utf-8')
        try:native=json.loads(run.stdout)
        except ValueError:native={'status':'FAIL','reason':'Native probe returned no parseable report','tests_executed':0,'live_model_calls':0}
    else:dump(reports/'native-smoke.json',native)
    local_ok=all(x['status']=='PASS' for x in results)
    overall=('LOCAL_PASS_NATIVE_'+native['status']) if local_ok else 'LOCAL_FAIL'
    report={'schema_version':1,'generated_at_utc':datetime.now(timezone.utc).isoformat(),'status':overall,
            'environment':{'os':platform.system(),'machine':platform.machine(),'python':platform.python_version()},
            'local_checks':results,'local_tests_passed':test_count,'native_runtime':native,
            'live_model_evaluations':{'status':'NOT_RUN','cases_defined':78,'calls_made':0},
            'github_actions':{'status':'NOT_RUN','note':'Workflow authored; no remote execution or repository publication.'},
            'dedicated_secret_scanner':{'status':'NOT_RUN','note':'Only limited repository pattern checks were executed.'},
            'scope':'Local code/contracts/fixtures only. No production qualification, user-machine inspection, or provider integration claim.'}
    dump(reports/'qualification.json',report)
    rows='\n'.join('| '+x['check']+' | '+x['status']+' | '+str(x['tests'] if x['tests'] is not None else 'n/a')+' | ['+x['evidence']+']('+x['evidence']+') |' for x in results)
    text=f'''# Relatorio de qualificacao - v0.1.0

Estado: **{overall}**.
Gerado em UTC: `{report['generated_at_utc']}`.
Ambiente executado: {platform.system()} / {platform.machine()} / Python {platform.python_version()}.

## Executado e verificado

| Verificacao | Resultado | Testes | Evidencia |
|---|---|---:|---|
{rows}

Total de testes locais aprovados: **{test_count}**. Os testes usam fixtures sinteticas,
diretorios temporarios e injecao controlada de falhas. Nao sao testes de competencia de um LLM.

## Runtime nativo

Estado: **{native['status']}**. {native.get('reason','Ver detalhes no JSON.')}
Consulte [native-smoke.json](native-smoke.json). Uma instancia copiada para uma fixture
nao e uma instalacao feita pelo Hermes. A auditoria de arquivos nao prova auto_load real.

## Nao executado

- Avaliacoes comportamentais com modelos: **0 chamadas**. Os **78 casos** do corpus
  continuam NOT_RUN; o checker validou apenas estrutura, referencias e rubricas.
- Integracoes com providers, MCP, cloud, IAM, bancos e ambientes produtivos.
- Homologacao em macOS, Windows e outras versoes de Python/Hermes.
- Scanner dedicado de segredos/dependencias e execucao do workflow no GitHub.

## Escopo e limites

Nao houve acesso a maquina do usuario, clientes, credenciais ou profiles reais.
O relatorio nao certifica seguranca absoluta, comportamento perfeito, sandboxing ou
prontidao para producao. O status de runtime ausente nao e convertido em PASS.
Leia [KNOWN-LIMITS](../docs/KNOWN-LIMITS.md) e [SECURITY](../docs/SECURITY.md).

[Resultado estruturado](qualification.json)
'''
    (reports/'QUALIFICATION.md').write_text(text,encoding='utf-8')
    print(json.dumps({'status':overall,'local_tests_passed':test_count,'report':'reports/qualification.json'},indent=2))
    if not local_ok:return 1
    if a.require_native and native['status']!='PASS':return 77
    return 0

if __name__=='__main__':raise SystemExit(main())
