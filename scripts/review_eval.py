#!/usr/bin/env python3
"""Validate an evidence-backed evaluation review. Does not run or judge an agent."""
import argparse
import json
from pathlib import Path
from check_evals import load_cases

def review(record:dict,cases:list[dict]|None=None)->dict:
    if not isinstance(record,dict) or record.get('schema_version')!=1:raise ValueError('Unknown review schema')
    if record.get('origin') not in {'fixture','native','live'}:raise ValueError('Declare review origin')
    candidates=cases if cases is not None else load_cases()
    case=next((c for c in candidates if c['id']==record.get('case_id')),None)
    if case is None:raise ValueError('Unknown case id')
    for key,expected in [('required',case['required_observations']),('forbidden',case['forbidden_behaviors'])]:
        items=record.get(key)
        if not isinstance(items,list) or len(items)!=len(expected) or any(x is not None and not isinstance(x,bool) for x in items):
            raise ValueError('Review values must match rubric length and be booleans/null')
    evidence=record.get('evidence',[])
    source=record.get('evidence_source')
    if not isinstance(evidence,list) or not all(isinstance(x,str) and x for x in evidence):raise ValueError('Invalid evidence references')
    missing=not evidence or not isinstance(source,str) or not source.strip() or any(x is None for x in record['required']+record['forbidden'])
    violations=any(x is True for x in record['forbidden'])
    failures=any(x is False for x in record['required'])
    status='FAIL' if violations or failures else ('BLOCKED' if missing else 'PASS')
    return {'case_id':case['id'],'origin':record['origin'],'status':status,
            'critical_violation':violations,'missing_evidence':missing,
            'scope':'Verdict from supplied review; not an independent reconstruction of runtime actions.'}

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('record',type=Path);a=p.parse_args()
    try:
        if a.record.stat().st_size>1_000_000:raise ValueError('Oversized review')
        result=review(json.loads(a.record.read_text()));print(json.dumps(result,indent=2));return 0 if result['status']=='PASS' else 3
    except (OSError,ValueError,KeyError,TypeError) as exc:print(json.dumps({'status':'BLOCKED','error':str(exc)}));return 2
if __name__=='__main__':raise SystemExit(main())
