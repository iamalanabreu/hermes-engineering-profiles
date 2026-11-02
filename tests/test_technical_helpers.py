"""Synthetic fixtures exercise helpers, not Terraform/LLM/cloud deployments."""
import copy
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from support import ROOT,module
plan=module('plan_reviewer','profiles/ai-devsecops-engineer/skills/dso-infrastructure-change/scripts/review_plan.py')
evalmod=module('eval_summary','profiles/ai-engineer/skills/aie-agent-evaluation/scripts/summarize_evals.py')
inv=module('inventory','profiles/software-engineer/skills/swe-codebase-discovery/scripts/inventory.py')

class TerraformSummaryTests(unittest.TestCase):
    def fixture(self):return json.loads((ROOT/'examples/terraform-plan.synthetic.json').read_text())
    def test_replacement_is_flagged(self):
        result=plan.summarize(self.fixture())
        self.assertTrue(result['review_required']);self.assertGreater(result['replacement_count'],0)
    def test_values_are_never_serialized(self):
        data=self.fixture();result=json.dumps(plan.summarize(data))
        self.assertNotIn('SYNTHETIC_DO_NOT_PRINT',result)
        self.assertNotIn('before_sensitive',result);self.assertNotIn('after_sensitive',result)
    def test_unsupported_format_is_rejected(self):
        data=self.fixture();data['format_version']='99.0'
        with self.assertRaises(ValueError):plan.summarize(data)
    def test_unknown_actions_fail_closed(self):
        data=self.fixture();data['resource_changes'][0]['change']['actions']=['execute_magic']
        with self.assertRaises(ValueError):plan.summarize(data)
    def test_empty_valid_plan_has_no_resource_mutations(self):
        result=plan.summarize({'format_version':'1.2'})
        self.assertFalse(result['review_required']);self.assertIn('NOT',plan.__doc__)
    def test_cli_returns_review_required(self):
        result=subprocess.run([sys.executable,str(Path(plan.__file__)),str(ROOT/'examples/terraform-plan.synthetic.json')],capture_output=True,text=True)
        self.assertEqual(result.returncode,3,result.stdout+result.stderr)
        self.assertNotIn('SYNTHETIC_DO_NOT_PRINT',result.stdout)
    def test_output_actions_are_validated_without_values(self):
        data={'format_version':'1.2','output_changes':{'public_url':{'actions':['update'],'before':'private-value','after':'new-private-value'}}}
        self.assertNotIn('private-value',json.dumps(plan.summarize(data)))
        data['output_changes']['public_url']['actions']=['alien']
        with self.assertRaises(ValueError):plan.summarize(data)

class EvaluationSummaryTests(unittest.TestCase):
    def base(self):return {'schema_version':1,'origin':'fixture','results':[{'case_id':'a','accepted':True,'critical_failures':[]}]}
    def test_missing_metrics_stay_null(self):
        r=evalmod.summarize(self.base());self.assertIsNone(r['p95_latency_ms']);self.assertIsNone(r['measured_cost_total'])
    def test_critical_failure_blocks(self):
        d=self.base();d['results'][0]['critical_failures']=['tenant isolation failed']
        self.assertEqual(evalmod.summarize(d)['status'],'BLOCKED')
    def test_unknown_outcome_blocks(self):
        d=self.base();d['results'][0]['accepted']=None
        self.assertEqual(evalmod.summarize(d)['status'],'BLOCKED')
    def test_failure_under_threshold_fails(self):
        d=self.base();d['results'][0]['accepted']=False
        self.assertEqual(evalmod.summarize(d)['status'],'FAIL')
    def test_duplicate_case_is_rejected(self):
        d=self.base();d['results']*=2
        with self.assertRaises(ValueError):evalmod.summarize(d)
    def test_invalid_metrics_are_rejected(self):
        for value in [True,-1,float('nan'),float('inf'),'100']:
            d=self.base();d['results'][0]['latency_ms']=value
            with self.subTest(value=value):
                with self.assertRaises(ValueError):evalmod.summarize(d)
    def test_invalid_threshold_is_rejected(self):
        for value in [-1,1.1,float('nan')]:
            with self.assertRaises(ValueError):evalmod.summarize(self.base(),value)
    def test_origin_is_mandatory(self):
        d=self.base();d.pop('origin')
        with self.assertRaises(ValueError):evalmod.summarize(d)
    def test_p95_uses_only_observed_values(self):
        d=self.base();d['results']=[{'case_id':str(i),'accepted':True,'latency_ms':i,'cost':0.1} for i in range(1,21)]
        r=evalmod.summarize(d);self.assertEqual(r['p95_latency_ms'],19);self.assertEqual(r['measured_latency_cases'],20)
        self.assertAlmostEqual(r['measured_cost_total'],2)
    def test_synthetic_result_is_explicit(self):
        d=json.loads((ROOT/'examples/eval-results.synthetic.json').read_text());r=evalmod.summarize(d)
        self.assertEqual(r['origin'],'synthetic');self.assertEqual(r['status'],'BLOCKED')

class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
    def test_inventory_never_executes_manifest_scripts(self):
        marker=self.root/'would-be-executed'
        (self.root/'package.json').write_text(json.dumps({'scripts':{'build':'touch '+str(marker)},'dependencies':{'x':'1'}}))
        r=inv.inventory(self.root);self.assertFalse(marker.exists())
        self.assertEqual(r['manifests'][0]['script_names'],['build'])
        self.assertNotIn('touch',json.dumps(r))
    def test_hidden_credentials_and_dependencies_are_excluded(self):
        (self.root/'.env').write_text('SECRET=synthetic-private-value')
        modules=self.root/'node_modules';modules.mkdir();(modules/'package.json').write_text('{}')
        (self.root/'pyproject.toml').write_text('[project]\nname="demo"\n')
        r=inv.inventory(self.root);self.assertEqual(len(r['manifests']),1)
        self.assertNotIn('synthetic-private-value',json.dumps(r))
    def test_symlinked_files_not_followed(self):
        original=self.root/'data.txt';original.write_text('private')
        try:(self.root/'package.json').symlink_to(original)
        except (OSError,NotImplementedError):self.skipTest('Symlink unavailable')
        r=inv.inventory(self.root);self.assertEqual(r['skipped_symlinks'],1);self.assertEqual(r['manifests'],[])
    def test_file_budget_truncates(self):
        for i in range(5):(self.root/(str(i)+'.txt')).write_text('x')
        r=inv.inventory(self.root,max_files=2);self.assertTrue(r['truncated']);self.assertEqual(r['files_seen'],2)
    def test_depth_budget_truncates(self):
        deep=self.root/'nested';deep.mkdir();(deep/'package.json').write_text('{}')
        r=inv.inventory(self.root,max_depth=0);self.assertTrue(r['truncated']);self.assertEqual(r['manifests'],[])
    def test_malformed_manifest_is_reported(self):
        (self.root/'package.json').write_text('{bad')
        self.assertEqual(inv.inventory(self.root)['manifests'][0]['parse_status'],'unreadable_or_invalid')
    def test_dotnet_and_instruction_hints_detected(self):
        (self.root/'demo.csproj').write_text('<Project/>');(self.root/'AGENTS.md').write_text('instructions')
        r=inv.inventory(self.root);self.assertEqual(r['manifests'][0]['ecosystem_hint'],'dotnet');self.assertIn('AGENTS.md',r['instruction_candidates'])
    def test_home_and_root_scans_rejected(self):
        for path in [Path.home(),Path(Path.cwd().anchor)]:
            with self.assertRaises(ValueError):inv.inventory(path)

if __name__=='__main__':unittest.main()
