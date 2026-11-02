#!/usr/bin/env python3
"""Summarize Terraform plan JSON actions without printing before/after values.

Exit 0: supported action summary with no deletes/replacements found (NOT an approval).
Exit 3: destructive action review needed. Exit 2: invalid/unsupported input.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

KNOWN={('no-op',),('read',),('create',),('update',),('delete',),('delete','create'),('create','delete')}

def summarize(plan: dict) -> dict:
    if not isinstance(plan,dict): raise ValueError('Plan must be an object')
    version=plan.get('format_version')
    if not isinstance(version,str) or not version.startswith('1.'):
        raise ValueError('Unsupported or missing Terraform JSON format version')
    resources=plan.get('resource_changes',[])
    outputs=plan.get('output_changes',{})
    if not isinstance(resources,list) or not isinstance(outputs,dict): raise ValueError('Invalid plan collections')
    rows=[]
    for entry in resources:
        if not isinstance(entry,dict) or not isinstance(entry.get('address'),str): raise ValueError('Missing resource address')
        change=entry.get('change')
        if not isinstance(change,dict): raise ValueError('Missing change object')
        actions=change.get('actions')
        if not isinstance(actions,list) or not all(isinstance(x,str) for x in actions) or tuple(actions) not in KNOWN:
            raise ValueError('Unsupported action sequence; inspect with the correct tool version')
        rows.append({'address':entry['address'],'actions':actions,'destructive':'delete' in actions,
                     'replacement':set(actions)=={'create','delete'},'has_unknowns':bool(change.get('after_unknown'))})
    output_rows=[]
    for name,change in outputs.items():
        if not isinstance(change,dict) or not isinstance(change.get('actions'),list): raise ValueError('Invalid output change')
        actions=change['actions']
        if not all(isinstance(x,str) for x in actions) or tuple(actions) not in KNOWN:
            raise ValueError('Unsupported output action sequence')
        output_rows.append({'name':name,'actions':actions})
    destructive=[r for r in rows if r['destructive']]
    return {'schema_version':1,'format_version':version,'resource_count':len(rows),
            'destructive_count':len(destructive),'replacement_count':sum(r['replacement'] for r in rows),
            'resources':rows,'outputs':output_rows,'review_required':bool(destructive),
            'scope':'Action summary only. Does not approve apply, validate permissions, prove recovery or assess all output/data risks.'}

def main() -> int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);a=p.parse_args()
    try:
        if a.plan.stat().st_size>30_000_000: raise ValueError('Plan input exceeds local review budget')
        result=summarize(json.loads(a.plan.read_text(encoding='utf-8')))
        print(json.dumps(result,indent=2));return 3 if result['review_required'] else 0
    except (OSError,ValueError,TypeError,KeyError) as exc:
        print(json.dumps({'status':'blocked','error':str(exc)}));return 2
if __name__=='__main__':raise SystemExit(main())
