import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from support import ROOT,PCA,context_spec,module
import safe_files as safe
ctx=module('project_context','shared-skills/project-context-architect/scripts/context.py')

class ProjectContextTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.spec=context_spec()
    def specfile(self,data=None):
        p=self.root/'input.json';p.write_text(json.dumps(self.spec if data is None else data));return p
    def test_valid_spec_loads(self):
        self.assertEqual(ctx.load_spec(self.specfile())['slug'],self.spec['slug'])
    def test_unknown_kind_rejected(self):
        d=copy.deepcopy(self.spec);d['kind']='imaginary'
        with self.assertRaises(safe.SafetyError):ctx.load_spec(self.specfile(d))
    def test_incomplete_requirements_rejected(self):
        for key in ['scope','non_goals','constraints','acceptance']:
            d=copy.deepcopy(self.spec);d[key]=[]
            with self.subTest(key=key):
                with self.assertRaises(safe.SafetyError):ctx.load_spec(self.specfile(d))
    def test_invalid_sources_rejected(self):
        for value in [None,{},['bad']]:
            d=copy.deepcopy(self.spec);d['sources']=value
            with self.assertRaises(safe.SafetyError):ctx.load_spec(self.specfile(d))
    def test_secret_marker_rejected(self):
        d=copy.deepcopy(self.spec);d['purpose']='ghp_'+'a'*25
        with self.assertRaises(safe.SafetyError):ctx.load_spec(self.specfile(d))
    def test_new_context_does_not_invent_stack_or_application(self):
        d=copy.deepcopy(self.spec);d['stack']={};files=ctx.render(d)
        self.assertIn('No stack is selected',files['docs/context/'+d['slug']+'/CONTEXT.md'])
        self.assertEqual(len(files),6)
        self.assertFalse(any(p.startswith(('src/','app/','node_modules/')) for p in files))
    def test_adoption_preserves_existing_readme_and_source(self):
        (self.root/'AGENTS.md').write_text('Existing project conventions.\n')
        (self.root/'README.md').write_text('Existing product.\n');(self.root/'main.py').write_text('print(1)\n')
        plan=ctx.adoption_plan(self.root,self.spec);safe.apply_plan(plan)
        self.assertTrue((self.root/'AGENTS.md').read_text().startswith('Existing project conventions.'))
        self.assertEqual((self.root/'README.md').read_text(),'Existing product.\n')
        self.assertEqual((self.root/'main.py').read_text(),'print(1)\n')
    def test_adoption_is_idempotent(self):
        safe.apply_plan(ctx.adoption_plan(self.root,self.spec))
        again=ctx.adoption_plan(self.root,self.spec);self.assertEqual(again['changes'],[])
        self.assertEqual((self.root/'AGENTS.md').read_text().count('<!-- engineering-context:'),1)
    def test_contexts_do_not_share_declared_data(self):
        a=copy.deepcopy(self.spec);a['trust_domain']='synthetic-domain-a'
        b=copy.deepcopy(self.spec);b['slug']='other-context';b['trust_domain']='synthetic-domain-b'
        self.assertNotIn('synthetic-domain-a',json.dumps(ctx.render(b)))
        self.assertNotIn('synthetic-domain-b',json.dumps(ctx.render(a)))
    def test_precedence_warning_without_editing_existing_hermes_file(self):
        (self.root/'HERMES.md').write_text('Higher priority instructions.\n')
        proc=subprocess.run([sys.executable,str(PCA/'scripts/context.py'),'adopt-plan','--spec',str(self.specfile()),'--root',str(self.root),'--out',str(self.root/'plan.json')],capture_output=True,text=True)
        self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)
        self.assertTrue(json.loads(proc.stdout)['context_precedence_check_required'])
        self.assertEqual((self.root/'HERMES.md').read_text(),'Higher priority instructions.\n')
        self.assertFalse((self.root/'docs').exists())
    def test_cli_default_preview_from_other_directory(self):
        proc=subprocess.run([sys.executable,str(PCA/'scripts/context.py'),'create','--spec',str(self.specfile()),'--root',str(self.root)],cwd=self.root,capture_output=True,text=True)
        self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)
        self.assertEqual(json.loads(proc.stdout)['mode'],'dry-run')
        self.assertFalse((self.root/self.spec['slug']).exists())
    def test_adoption_refuses_symlinked_instructions(self):
        original=self.root/'original.md';original.write_text('original')
        try:(self.root/'AGENTS.md').symlink_to(original)
        except (OSError,NotImplementedError):self.skipTest('Symlink unavailable')
        with self.assertRaises(safe.SafetyError):ctx.adoption_plan(self.root,self.spec)

if __name__=='__main__':unittest.main()
