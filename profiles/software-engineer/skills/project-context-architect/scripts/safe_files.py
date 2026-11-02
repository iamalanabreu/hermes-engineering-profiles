"""Conservative, reviewable file operations. Standard library; no shell or network.

Approval is a reviewed plan digest, not a security identity. The caller must own
an authorized, exclusively controlled directory. This is not an OS sandbox.
"""
from __future__ import annotations
import difflib
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import tempfile
from datetime import datetime, timezone
from typing import Any
import uuid

MAX_FILE_BYTES = 2_000_000
MAX_PLAN_BYTES = 12_000_000
BLOCKED_NAMES = {'.env', 'auth.json', 'state.db', 'config.yaml', 'distribution.yaml'}

class SafetyError(ValueError):
    """Invalid scope, changed input, or unsafe path."""

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def canonical(data: Any) -> bytes:
    return (json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode()

def safe_relative(value: str) -> str:
    if not isinstance(value, str) or not value or '\\' in value or any(ord(c)<32 for c in value):
        raise SafetyError('Invalid relative path')
    p = PurePosixPath(value)
    if p.is_absolute() or str(p) != value or any(x in ('..', '.') for x in p.parts):
        raise SafetyError('Absolute paths and traversal are forbidden: ' + value)
    if any(x.startswith('.') for x in p.parts) or any(':' in x for x in p.parts):
        raise SafetyError('Hidden paths and drive identifiers are forbidden: ' + value)
    if any(x.casefold() in BLOCKED_NAMES for x in p.parts):
        raise SafetyError('Runtime/configuration path not managed by the Architect: ' + value)
    if p.suffix.lower() not in {'.md','.txt','.json','.yaml','.yml','.py','.sh','.csv','.toml'}:
        raise SafetyError('Unsupported authored file type: ' + value)
    return value

def reject_symlink_chain(path: Path) -> None:
    p = path.expanduser().absolute()
    for item in (p, *p.parents):
        if item.is_symlink():
            raise SafetyError('Symlinked path is not an authorized filesystem boundary: ' + str(item))

def root_dir(path: Path) -> Path:
    reject_symlink_chain(path)
    p = path.expanduser().resolve(strict=True)
    if not p.is_dir() or p == Path(p.anchor) or p == Path.home().resolve():
        raise SafetyError('Choose an existing, explicit workspace directory, not root or HOME')
    return p

def target_path(root: Path, relative: str) -> Path:
    safe_relative(relative)
    target = root / relative
    reject_symlink_chain(target)
    target.resolve().relative_to(root)
    if target.exists() and not target.is_file():
        raise SafetyError('Expected a regular file: ' + str(target))
    return target

def read_small(path: Path) -> bytes:
    if path.stat().st_size > MAX_FILE_BYTES:
        raise SafetyError('Refusing oversized authored file: ' + str(path))
    return path.read_bytes()

def validate_payload(files: dict[str, str]) -> None:
    if not isinstance(files, dict) or not files:
        raise SafetyError('Nonempty file mapping required')
    seen: set[str] = set()
    for name, text in files.items():
        safe_relative(name)
        if name.casefold() in seen:
            raise SafetyError('Case-insensitive duplicate path: ' + name)
        seen.add(name.casefold())
        if not isinstance(text, str) or not text.strip() or len(text.encode()) > MAX_FILE_BYTES:
            raise SafetyError('Empty or oversized content: ' + name)
    for name in files:
        for parent in PurePosixPath(name).parents:
            if str(parent).casefold() in seen:
                raise SafetyError('File/directory path collision: ' + name)

def create_tree(parent: Path, slug: str, files: dict[str,str], *, dry_run: bool = True) -> dict:
    import re
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug) or len(slug) > 64:
        raise SafetyError('Invalid slug')
    validate_payload(files)
    parent = root_dir(parent)
    target = parent / slug
    if target.exists() or target.is_symlink():
        raise SafetyError('Destination already exists; use a reviewed evolution plan')
    result = {'mode':'dry-run' if dry_run else 'created','target':str(target),'files':sorted(files)}
    if dry_run:
        return result
    lock = parent / ('.architect-create-' + slug + '.lock')
    try:
        lock.mkdir(mode=0o700)
    except FileExistsError as exc:
        raise SafetyError('Concurrent creation or stale lock: ' + str(lock)) from exc
    staging: Path | None = None
    try:
        if target.exists() or target.is_symlink():
            raise SafetyError('Destination changed after preview')
        staging = Path(tempfile.mkdtemp(prefix='.'+slug+'-stage-', dir=parent))
        for name, text in sorted(files.items()):
            p = staging / name
            p.parent.mkdir(parents=True, exist_ok=True)
            with p.open('x', encoding='utf-8', newline='\n') as out:
                out.write(text if text.endswith('\n') else text+'\n')
        if target.exists() or target.is_symlink():
            raise SafetyError('Destination appeared while staging')
        # Atomic publication on the same filesystem; lock coordinates our writers.
        # Do not use this in directories concurrently writable by untrusted actors.
        staging.rename(target)
        staging = None
        return result
    finally:
        if staging is not None:
            shutil.rmtree(staging)
        lock.rmdir()

def make_plan(root: Path, files: dict[str,str], *, kind: str) -> dict:
    validate_payload(files)
    root = root_dir(root)
    changes = []
    for rel,text in sorted(files.items()):
        text = text if text.endswith('\n') else text+'\n'
        p=target_path(root,rel)
        old=read_small(p) if p.exists() else None
        if old == text.encode():
            continue
        changes.append({'path':rel,'before_sha256':digest(old) if old is not None else None,
                        'content':text})
    return {'schema_version':1,'kind':kind,'root':str(root),'changes':changes,
            'delete_files':False,'semantics':'replace listed text files; preserve every unlisted path'}

def plan_diff(plan: dict) -> str:
    root=root_dir(Path(plan['root']))
    parts=[]
    for item in plan['changes']:
        p=target_path(root,item['path'])
        old=read_small(p).decode('utf-8') if p.exists() else ''
        parts.extend(difflib.unified_diff(old.splitlines(True),item['content'].splitlines(True),
                     fromfile='before/'+item['path'],tofile='after/'+item['path']))
    return ''.join(parts)

def write_plan(plan: dict, path: Path) -> dict:
    blob=canonical(plan)
    if len(blob)>MAX_PLAN_BYTES:
        raise SafetyError('Plan is too large')
    reject_symlink_chain(path)
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'wb') as out:
        out.write(blob)
    return {'plan':str(path.resolve()),'sha256':digest(blob),'changes':len(plan['changes'])}

def load_plan(path: Path, approved_sha256: str) -> dict:
    reject_symlink_chain(path)
    if path.stat().st_size > MAX_PLAN_BYTES:
        raise SafetyError('Plan is too large')
    raw=path.read_bytes()
    if digest(raw) != approved_sha256:
        raise SafetyError('Plan approval digest does not match the reviewed bytes')
    plan=json.loads(raw)
    if not isinstance(plan,dict):
        raise SafetyError('Plan must be an object')
    if plan.get('schema_version')!=1 or plan.get('delete_files') is not False:
        raise SafetyError('Unsupported plan or deletion request')
    if plan.get('kind') not in {'operational-capability','project-context'}:
        raise SafetyError('Unknown plan type')
    if not isinstance(plan.get('changes'),list):
        raise SafetyError('Invalid changes')
    files={}
    for row in plan['changes']:
        if not isinstance(row,dict) or set(row)!={'path','content','before_sha256'}:
            raise SafetyError('Invalid change fields')
        import re
        if row['before_sha256'] is not None and (not isinstance(row['before_sha256'],str) or not re.fullmatch(r'[0-9a-f]{64}',row['before_sha256'])):
            raise SafetyError('Invalid preimage digest')
        safe_relative(row['path'])
        if row['path'] in files:
            raise SafetyError('Duplicate change')
        files[row['path']]=row['content']
    if files: validate_payload(files)
    return plan

def _check_expected(root: Path, row: dict) -> Path:
    p=target_path(root,row['path'])
    actual=digest(read_small(p)) if p.exists() else None
    if actual!=row['before_sha256']:
        raise SafetyError('File changed since review: '+row['path'])
    return p

def apply_plan(plan: dict) -> dict:
    """Apply with optimistic hashes and a rollback journal; no deletions.

    Ordinary errors restore touched files. A process/power loss can interrupt a
    multi-file transaction: preserve the backup/journal and recover explicitly.
    """
    root=root_dir(Path(plan['root']))
    changes=plan['changes']
    for row in changes: _check_expected(root,row)
    if not changes: return {'status':'unchanged','files':[]}
    lock=root/'.architect-update.lock'
    try: lock.mkdir(mode=0o700)
    except FileExistsError as exc: raise SafetyError('Concurrent update or stale lock') from exc
    backup_root=root/'.architect-backups'
    journal_dir=None
    touched=[]
    created_dirs=[]
    try:
        reject_symlink_chain(backup_root)
        backup_root.mkdir(mode=0o700,exist_ok=True)
        journal_dir=backup_root/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8])
        journal_dir.mkdir(mode=0o700)
        journal={'status':'applying','changes':[{k:v for k,v in r.items() if k!='content'} for r in changes]}
        journal_path=journal_dir/'journal.json'
        journal_path.write_bytes(canonical(journal))
        for row in changes:
            p=_check_expected(root,row)
            if p.exists():
                b=journal_dir/'files'/row['path']; b.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(p,b)
            missing=[]; parent=p.parent
            while not parent.exists():
                missing.append(parent); parent=parent.parent
            for d in reversed(missing): d.mkdir(); created_dirs.append(d)
            reject_symlink_chain(p)
            fd,tmp=tempfile.mkstemp(prefix='.architect-write-',dir=p.parent)
            tmp=Path(tmp)
            try:
                with os.fdopen(fd,'wb') as out:
                    out.write(row['content'].encode()); out.flush(); os.fsync(out.fileno())
                if p.exists():
                    os.chmod(tmp,p.stat().st_mode & 0o777)
                    _check_expected(root,row)
                    os.replace(tmp,p)
                else:
                    os.link(tmp,p) # exclusive creation: fails if a new file appeared
                    tmp.unlink()
                touched.append(row)
            finally:
                if tmp.exists(): tmp.unlink()
        journal['status']='applied'; journal_path.write_bytes(canonical(journal))
        return {'status':'applied','files':[r['path'] for r in touched],'backup':str(journal_dir)}
    except Exception:
        rollback_errors=[]
        for row in reversed(touched):
            try:
                p=target_path(root,row['path'])
                if digest(read_small(p)) != digest(row['content'].encode()):
                    raise SafetyError('Concurrent edit during rollback: '+row['path'])
                b=journal_dir/'files'/row['path']
                if row['before_sha256'] is None: p.unlink()
                else: shutil.copy2(b,p)
            except Exception as err: rollback_errors.append(str(err))
        for d in reversed(created_dirs):
            try: d.rmdir()
            except OSError: pass
        if journal_dir is not None:
            (journal_dir/'journal.json').write_bytes(canonical({'status':'rollback-incomplete' if rollback_errors else 'rolled-back','errors':rollback_errors}))
        if rollback_errors:
            raise SafetyError('Rollback needs manual recovery: '+ '; '.join(rollback_errors))
        raise
    finally:
        lock.rmdir()
