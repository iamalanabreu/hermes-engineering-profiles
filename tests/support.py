"""Test-only loaders for this repository; never connect to a real Hermes home."""
import importlib.util
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
AFA=ROOT/'shared-skills/agent-folder-architect'
PCA=ROOT/'shared-skills/project-context-architect'
sys.path.insert(0,str(AFA/'scripts'))
sys.path.insert(0,str(ROOT/'scripts'))

def module(name,relative):
    spec=importlib.util.spec_from_file_location(name,ROOT/relative)
    obj=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

def blueprint():
    return json.loads((AFA/'assets/blueprint-exemplo.json').read_text())

def context_spec():
    return json.loads((PCA/'assets/context-example.json').read_text())
