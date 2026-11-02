#!/usr/bin/env python3
"""Aggregate normalized outcome records. Does not run or judge an LLM.

Critical failures and missing mandatory results block a passing summary. A reported
metric proves nothing about the provenance of the input; preserve actual execution logs.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path

def number(value, name):
    if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or value<0:
        raise ValueError(name+' must be a finite nonnegative number or null')
    return float(value)

def summarize(data: dict, minimum_rate: float=1.0) -> dict:
    if not 0<=minimum_rate<=1:raise ValueError('Acceptance threshold must be between 0 and 1')
    if not isinstance(data,dict) or data.get('schema_version')!=1:raise ValueError('Unsupported result schema')
    if data.get('origin') not in {'synthetic','live','fixture'}:raise ValueError('Declare result origin')
    rows=data.get('results')
    if not isinstance(rows,list) or not rows:raise ValueError('Nonempty results required')
    seen=set();latencies=[];costs=[];accepted=0;unknown=0;critical=[]
    for row in rows:
        if not isinstance(row,dict) or not isinstance(row.get('case_id'),str) or not row['case_id']:raise ValueError('Missing case id')
        if row['case_id'] in seen:raise ValueError('Duplicate case result')
        seen.add(row['case_id'])
        outcome=row.get('accepted')
        if outcome is not None and not isinstance(outcome,bool):raise ValueError('accepted must be boolean or null')
        accepted+=outcome is True;unknown+=outcome is None
        failures=row.get('critical_failures',[])
        if not isinstance(failures,list) or not all(isinstance(x,str) and x for x in failures):raise ValueError('Invalid critical failures')
        critical.extend({'case_id':row['case_id'],'failure':x} for x in failures)
        for key,collection in [('latency_ms',latencies),('cost',costs)]:
            if row.get(key) is not None:collection.append(number(row[key],key))
    count=len(rows);rate=accepted/count
    status='BLOCKED' if unknown or critical else ('PASS' if rate>=minimum_rate else 'FAIL')
    latencies.sort()
    return {'schema_version':1,'origin':data['origin'],'status':status,'cases':count,
            'accepted':accepted,'not_evaluated':unknown,'acceptance_rate':rate,'required_rate':minimum_rate,
            'critical_failures':critical,'measured_latency_cases':len(latencies),
            'p95_latency_ms':latencies[math.ceil(.95*len(latencies))-1] if latencies else None,
            'measured_cost_cases':len(costs),'measured_cost_total':sum(costs) if costs else None,
            'limits':'Aggregation only; not model execution, statistical robustness, authorization proof or production certification.'}

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('results',type=Path)
    p.add_argument('--minimum-rate',type=float,default=1.0);a=p.parse_args()
    try:
        if a.results.stat().st_size>10_000_000:raise ValueError('Result input exceeds local budget')
        out=summarize(json.loads(a.results.read_text()),a.minimum_rate);print(json.dumps(out,indent=2))
        return 0 if out['status']=='PASS' else 3
    except (OSError,ValueError,TypeError,KeyError) as exc:
        print(json.dumps({'status':'blocked','error':str(exc)}));return 2
if __name__=='__main__':raise SystemExit(main())
