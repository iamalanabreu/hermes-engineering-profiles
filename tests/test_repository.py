"""Repository contracts, fixture-only instance audits and packaging safety."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import yaml
from support import ROOT,AFA
import build_distributions as build
import install_profile
import verify_instance
import validate_distributions
import smoke_native
import check_evals
import review_eval
import package_release
from repo_utils import tree_hashes

class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
    def test_full_static_contract(self):
        r=validate_distributions.validate();self.assertEqual(r['status'],'PASS',r['errors'])
        self.assertEqual(r['profiles'],3);self.assertEqual(r['canonical_skills'],24)
        self.assertEqual(r['installed_skill_copies'],28)
    def test_all_shared_copies_identical(self):
        self.assertEqual(build.synchronize()['profile_copies'],6)
    def test_install_plan_is_native_and_non_forcing(self):
        r=install_profile.plan('software-engineer','software-context-a')
        self.assertEqual(r['command'][1:3],['profile','install'])
        for token in ['--force','--yes','--clone']:self.assertNotIn(token,r['command'])
    def test_install_default_cli_does_not_execute_missing_binary(self):
        p=subprocess.run([sys.executable,str(ROOT/'scripts/install_profile.py'),'--profile','software-engineer','--name','example','--hermes','intentionally-not-installed'],capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
    def test_invalid_names_are_refused(self):
        for name in ['default','../other','BAD NAME','-x','a'*65]:
            with self.assertRaises(ValueError):install_profile.plan('software-engineer',name)
    def test_unknown_profile_is_refused(self):
        with self.assertRaises(ValueError):install_profile.plan('not-real','example')
    def fixture_instance(self):
        dst=self.root/'instance';shutil.copytree(ROOT/'profiles/software-engineer',dst,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        return dst
    def test_fixture_instance_matches(self):
        dst=self.fixture_instance();self.assertEqual(verify_instance.inspect('software-engineer',dst)['status'],'MATCH')
    def test_fixture_instance_config_drift_does_not_print_values(self):
        dst=self.fixture_instance();p=dst/'config.yaml';d=yaml.safe_load(p.read_text());d['approvals']['mode']='off';d['api_key']='SYNTHETIC_LOCAL_SECRET_VALUE';p.write_text(yaml.safe_dump(d))
        r=verify_instance.inspect('software-engineer',dst);self.assertEqual(r['status'],'DRIFT')
        self.assertIn('approvals.mode',r['baseline_config_keys_differing']);self.assertNotIn('SYNTHETIC_LOCAL_SECRET_VALUE',json.dumps(r))
    def test_fixture_instance_malformed_config_does_not_leak_snippet(self):
        dst=self.fixture_instance();(dst/'config.yaml').write_text('secret: [SYNTHETIC_LOCAL_SECRET_VALUE\n')
        p=subprocess.run([sys.executable,str(ROOT/'scripts/verify_instance.py'),'--profile','software-engineer','--directory',str(dst)],capture_output=True,text=True)
        self.assertEqual(p.returncode,2);self.assertNotIn('SYNTHETIC_LOCAL_SECRET_VALUE',p.stdout+p.stderr)
    def test_fixture_audit_does_not_open_secrets_or_memory(self):
        dst=self.fixture_instance();(dst/'.env').write_text('synthetic secret');(dst/'memories').mkdir();(dst/'memories/MEMORY.md').write_text('private context')
        original=Path.read_text
        def guarded(path,*args,**kwargs):
            if path.name in {'.env','MEMORY.md','auth.json'}:raise AssertionError('Secret/memory read')
            return original(path,*args,**kwargs)
        with patch.object(Path,'read_text',new=guarded):self.assertEqual(verify_instance.inspect('software-engineer',dst)['status'],'MATCH')
    def test_native_missing_is_blocked_not_passed(self):
        with patch.object(smoke_native.shutil,'which',return_value=None):r=smoke_native.run('absent')
        self.assertEqual(r['status'],'BLOCKED');self.assertEqual(r['tests_executed'],0)
    def test_zip_build_is_reproducible(self):
        src=self.root/'src';src.mkdir();(src/'a.md').write_text('Hello\n');(src/'b.txt').write_text('Stable\n')
        one=package_release.archive(src,self.root/'one.zip','root');two=package_release.archive(src,self.root/'two.zip','root')
        self.assertEqual(one['sha256'],two['sha256'])
        with zipfile.ZipFile(self.root/'one.zip') as z:self.assertIsNone(z.testzip());self.assertEqual(z.namelist(),['root/a.md','root/b.txt'])
    def test_zip_rejects_source_symlink(self):
        src=self.root/'src';src.mkdir();outside=self.root/'outside.txt';outside.write_text('private')
        try:(src/'link.txt').symlink_to(outside)
        except (OSError,NotImplementedError):self.skipTest('Symlink unavailable')
        with self.assertRaises(ValueError):package_release.archive(src,self.root/'bad.zip','root')
    def test_generated_local_edit_is_not_clobbered(self):
        fixture=self.root/'repo';fixture.mkdir()
        for name in ['catalog.json','shared-skills.lock.json']:shutil.copy2(ROOT/name,fixture/name)
        shutil.copytree(ROOT/'shared-skills',fixture/'shared-skills',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        catalog=json.loads((ROOT/'catalog.json').read_text())
        for profile in catalog['profiles']:
            for skill in catalog['shared']:
                shutil.copytree(ROOT/'profiles'/profile/'skills'/skill,fixture/'profiles'/profile/'skills'/skill,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        edited=fixture/'profiles/software-engineer/skills/agent-folder-architect/SKILL.md';edited.write_text(edited.read_text()+'\nHuman local edit.\n')
        with self.assertRaises(ValueError):build.synchronize(fixture,write=True)
        self.assertIn('Human local edit.',edited.read_text())

class EvaluationContractTests(unittest.TestCase):
    def setUp(self):self.cases=check_evals.load_cases();self.case=self.cases[0]
    def record(self):return {'schema_version':1,'origin':'fixture','case_id':self.case['id'],'required':[True]*len(self.case['required_observations']),'forbidden':[False]*len(self.case['forbidden_behaviors']),'evidence':['fixture/transcript.json'],'evidence_source':'synthetic fixture, not a model run'}
    def test_corpus_has_78_unexecuted_cases(self):
        self.assertEqual(len(self.cases),78)
        self.assertTrue(all(c['status']=='NOT_RUN' and c['origin']=='synthetic' for c in self.cases))
    def test_software_has_at_least_30_technical_cases(self):
        rows=[c for c in self.cases if c['profile']=='software-engineer' and c['expected_skill'].startswith('swe-')]
        self.assertGreaterEqual(len(rows),30)
    def test_fixture_review_pass_is_labeled_fixture(self):
        r=review_eval.review(self.record(),self.cases);self.assertEqual(r['status'],'PASS');self.assertEqual(r['origin'],'fixture')
    def test_no_evidence_blocks(self):
        r=self.record();r['evidence']=[];self.assertEqual(review_eval.review(r,self.cases)['status'],'BLOCKED')
    def test_null_observation_blocks(self):
        r=self.record();r['required'][0]=None;self.assertEqual(review_eval.review(r,self.cases)['status'],'BLOCKED')
    def test_forbidden_action_fails(self):
        r=self.record();r['forbidden'][0]=True;result=review_eval.review(r,self.cases)
        self.assertEqual(result['status'],'FAIL');self.assertTrue(result['critical_violation'])
    def test_unmet_required_action_fails(self):
        r=self.record();r['required'][0]=False;self.assertEqual(review_eval.review(r,self.cases)['status'],'FAIL')
    def test_numeric_truthiness_is_not_accepted(self):
        r=self.record();r['required'][0]=1
        with self.assertRaises(ValueError):review_eval.review(r,self.cases)
    def test_wrong_rubric_length_is_rejected(self):
        r=self.record();r['required']=[]
        with self.assertRaises(ValueError):review_eval.review(r,self.cases)
    def test_unknown_case_is_rejected(self):
        r=self.record();r['case_id']='invented'
        with self.assertRaises(ValueError):review_eval.review(r,self.cases)

if __name__=='__main__':unittest.main()
