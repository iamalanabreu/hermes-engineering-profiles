"""Repository-local helpers; no Hermes or provider dependency."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
SKIP={'__pycache__','.git','.venv','.pytest_cache','.DS_Store'}

def read_catalog(root:Path=ROOT)->dict:
    data=json.loads((root/'catalog.json').read_text(encoding='utf-8'))
    if data.get('schema_version')!=1:raise ValueError('Unsupported catalog schema')
    if not isinstance(data.get('profiles'),dict) or not isinstance(data.get('shared'),list):raise ValueError('Invalid catalog')
    for name in [*data['profiles'],*data['shared'],*[x for a in data['profiles'].values() for x in a]]:
        if not isinstance(name,str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',name):raise ValueError('Unsafe catalog identifier')
    return data

def sha(path:Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()

def files(root:Path):
    for p in sorted(root.rglob('*')):
        rel=p.relative_to(root)
        if any(x in SKIP for x in rel.parts) or p.suffix=='.pyc':continue
        if p.is_symlink():raise ValueError('Symlink in authored tree: '+str(p))
        if p.is_file():yield p

def tree_hashes(root:Path)->dict[str,str]:
    if root.is_symlink():raise ValueError('Symlinked tree')
    if not root.exists():return {}
    return {p.relative_to(root).as_posix():sha(p) for p in files(root)}

def dump(path:Path,data:dict):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
