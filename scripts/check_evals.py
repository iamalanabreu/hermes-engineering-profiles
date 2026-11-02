#!/usr/bin/env python3
"""Check evaluation corpus structure and skill references, not model performance."""
import json
from pathlib import Path
from repo_utils import ROOT,read_catalog

def load_cases(root:Path=ROOT)->list[dict]:
    cases=[json.loads(x) for x in (root/'evals/cases.jsonl').read_text().splitlines() if x.strip()]
    catalog=read_catalog(root);seen=set()
    for c in cases:
        if c['id'] in seen:raise ValueError('Duplicate case id')
        seen.add(c['id'])
        if c['profile'] not in catalog['profiles']:raise ValueError('Unknown profile in case')
        available=catalog['profiles'][c['profile']]+catalog['shared']+['none']
        if c['expected_skill'] not in available:raise ValueError('Unknown skill in case')
        if c.get('origin')!='synthetic' or c.get('status')!='NOT_RUN':raise ValueError('Corpus must not contain fabricated execution results')
        for k in ['required_observations','forbidden_behaviors']:
            if not isinstance(c.get(k),list) or not c[k] or not all(isinstance(x,str) and x for x in c[k]):raise ValueError('Invalid rubric')
        if not isinstance(c.get('prompt'),str) or not c['prompt']:raise ValueError('Missing prompt')
    return cases

def main()->int:
    try:
        cases=load_cases();print(json.dumps({'status':'PASS','cases':len(cases),'scope':'Corpus structure only; no model evaluation executed'},indent=2));return 0
    except (OSError,ValueError,KeyError,TypeError) as exc:print(json.dumps({'status':'FAIL','error':str(exc)}));return 1
if __name__=='__main__':raise SystemExit(main())
