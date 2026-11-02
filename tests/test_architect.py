"""Deterministic structural and transaction tests; no agent/model is executed."""
import copy
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from support import AFA,blueprint
import architect
import safe_files as safe
from scaffold import BlueprintError,file_content

class ArchitectTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.spec=blueprint()
    def create(self,layout='operational'):
        files=architect.render(self.spec,layout)
        safe.create_tree(self.root,self.spec['slug'],files,dry_run=False)
        return self.root/self.spec['slug']
    def test_original_layout_preserved(self):
        self.assertEqual(architect.render(self.spec,'operational'),file_content(self.spec))
    def test_native_layout_translates_every_original_resource(self):
        native=architect.render(self.spec,'hermes')
        self.assertIn('references/files/INDICE.md',native)
        self.assertIn('references/validation/CRITERIOS.md',native)
        self.assertIn('references/notes.md',native)
        self.assertIn('examples/LEIA-ME.md',native)
        self.assertFalse(any(p.startswith(('arquivos/','validacao/','exemplos/')) for p in native))
    def test_native_manifest_links_every_resource(self):
        native=architect.render(self.spec,'hermes')
        for path in native:
            if path!='SKILL.md':self.assertIn(']('+path+')',native['SKILL.md'])
    def test_preview_does_not_write(self):
        before=list(self.root.iterdir())
        result=safe.create_tree(self.root,self.spec['slug'],architect.render(self.spec,'hermes'))
        self.assertEqual(result['mode'],'dry-run');self.assertEqual(before,list(self.root.iterdir()))
    def test_operational_create_validates(self):
        folder=self.create();self.assertTrue(architect.validate(folder,self.spec,'operational')['ok'])
    def test_native_create_validates(self):
        folder=self.create('hermes');self.assertTrue(architect.validate(folder,self.spec,'hermes')['ok'])
    def test_existing_directory_is_preserved(self):
        folder=self.create();marker=folder/'personal.txt';marker.write_text('own work')
        with self.assertRaises(safe.SafetyError):self.create()
        self.assertEqual(marker.read_text(),'own work')
    def test_missing_required_resource_is_rejected(self):
        folder=self.create();(folder/'notas.md').unlink()
        self.assertFalse(architect.validate(folder,self.spec,'operational')['ok'])
    def test_broken_resource_link_is_rejected(self):
        folder=self.create();entry=folder/'SKILL.md';entry.write_text(entry.read_text()+'\n[broken](missing.md)\n')
        self.assertFalse(architect.validate(folder,self.spec,'operational')['ok'])
    def test_invalid_layout_is_rejected(self):
        with self.assertRaises(safe.SafetyError):architect.render(self.spec,'unregistered')
    def test_synthetic_example_cannot_be_marked_approved_without_source(self):
        data=copy.deepcopy(self.spec);data['files'][0]['status']='approved';data['files'][0].pop('source_ref',None)
        with self.assertRaises(BlueprintError):architect.render(data,'operational')
    def test_plan_only_does_not_mutate_source(self):
        folder=self.create();before=(folder/'notas.md').read_bytes()
        plan=safe.make_plan(folder,{'notas.md':'New documented note\n'},kind='operational-capability')
        self.assertEqual((folder/'notas.md').read_bytes(),before)
        self.assertIn('+New documented note',safe.plan_diff(plan))
    def test_evolution_preserves_unlisted_files_and_records_backup(self):
        folder=self.create();marker=folder/'personal.txt';marker.write_text('own work')
        old=(folder/'notas.md').read_bytes()
        plan=safe.make_plan(folder,{'notas.md':'Changed note\n','references/new.md':'New reference\n'},kind='operational-capability')
        saved=safe.write_plan(plan,self.root/'approved.json')
        result=safe.apply_plan(safe.load_plan(self.root/'approved.json',saved['sha256']))
        self.assertEqual(result['status'],'applied');self.assertEqual(marker.read_text(),'own work')
        self.assertEqual((Path(result['backup'])/'files/notas.md').read_bytes(),old)
        self.assertEqual(json.loads((Path(result['backup'])/'journal.json').read_text())['status'],'applied')
    def test_wrong_digest_is_rejected(self):
        plan=safe.make_plan(self.root,{'a.md':'x\n'},kind='operational-capability');safe.write_plan(plan,self.root/'plan.json')
        with self.assertRaises(safe.SafetyError):safe.load_plan(self.root/'plan.json','0'*64)
    def test_edit_after_review_blocks_update(self):
        (self.root/'a.md').write_text('old\n');plan=safe.make_plan(self.root,{'a.md':'new\n'},kind='operational-capability')
        (self.root/'a.md').write_text('human change\n')
        with self.assertRaises(safe.SafetyError):safe.apply_plan(plan)
        self.assertEqual((self.root/'a.md').read_text(),'human change\n')
    def test_replay_is_not_silently_applied_twice(self):
        plan=safe.make_plan(self.root,{'a.md':'new\n'},kind='operational-capability');safe.apply_plan(plan)
        with self.assertRaises(safe.SafetyError):safe.apply_plan(plan)
    def test_idempotent_plan_is_empty(self):
        (self.root/'a.md').write_text('same\n');plan=safe.make_plan(self.root,{'a.md':'same\n'},kind='project-context')
        self.assertEqual(plan['changes'],[]);self.assertEqual(safe.apply_plan(plan)['status'],'unchanged')
    def test_delete_request_is_rejected(self):
        plan=safe.make_plan(self.root,{'a.md':'new\n'},kind='project-context');plan['delete_files']=True
        saved=safe.write_plan(plan,self.root/'plan.json')
        with self.assertRaises(safe.SafetyError):safe.load_plan(self.root/'plan.json',saved['sha256'])
    def test_malformed_plan_rows_are_rejected(self):
        for row in [None,{}, {'path':'a.md','content':'x','before_sha256':'not-a-digest'}]:
            with self.subTest(row=row):
                plan={'schema_version':1,'kind':'project-context','delete_files':False,'root':str(self.root),'changes':[row]}
                p=self.root/'bad.json';p.write_bytes(safe.canonical(plan))
                with self.assertRaises(safe.SafetyError):safe.load_plan(p,safe.digest(p.read_bytes()))
    def test_ordinary_failure_rolls_back_prior_writes(self):
        for name in ('a.md','b.md'):(self.root/name).write_text('old '+name+'\n')
        plan=safe.make_plan(self.root,{n:'new '+n+'\n' for n in ('a.md','b.md')},kind='operational-capability')
        real_replace=os.replace;calls=0
        def failing_replace(src,dst):
            nonlocal calls
            calls+=1
            if calls==2:raise OSError('synthetic write failure')
            return real_replace(src,dst)
        with patch.object(safe.os,'replace',side_effect=failing_replace):
            with self.assertRaises(OSError):safe.apply_plan(plan)
        for name in ('a.md','b.md'):self.assertEqual((self.root/name).read_text(),'old '+name+'\n')
        journal=next((self.root/'.architect-backups').glob('*/journal.json'))
        self.assertEqual(json.loads(journal.read_text())['status'],'rolled-back')
        self.assertFalse((self.root/'.architect-update.lock').exists())
    def test_concurrent_update_lock_blocks_without_deleting_lock(self):
        lock=self.root/'.architect-update.lock';lock.mkdir()
        plan=safe.make_plan(self.root,{'a.md':'x\n'},kind='project-context')
        with self.assertRaises(safe.SafetyError):safe.apply_plan(plan)
        self.assertTrue(lock.exists());self.assertFalse((self.root/'a.md').exists())
    def test_concurrent_creation_lock_blocks(self):
        lock=self.root/'.architect-create-sample.lock';lock.mkdir()
        with self.assertRaises(safe.SafetyError):safe.create_tree(self.root,'sample',{'a.md':'x\n'},dry_run=False)
        self.assertTrue(lock.exists());self.assertFalse((self.root/'sample').exists())
    def test_path_escape_and_sensitive_names_rejected(self):
        paths=['../bad.md','/bad.md','a/../bad.md','a//bad.md','a\\bad.md','.env','config.yaml','docs/auth.json','C:/bad.md','docs/.git/config','a.exe','a\x00.md']
        for path in paths:
            with self.subTest(path=path):
                with self.assertRaises(safe.SafetyError):safe.safe_relative(path)
    def test_case_and_hierarchy_collisions_rejected(self):
        for files in [{'A.md':'a','a.md':'b'},{'a.md':'a','a.md/child.md':'b'}]:
            with self.assertRaises(safe.SafetyError):safe.validate_payload(files)
    def test_empty_and_oversized_payload_rejected(self):
        for files in [{},{'a.md':''},{'a.md':'x'*(safe.MAX_FILE_BYTES+1)}]:
            with self.assertRaises(safe.SafetyError):safe.validate_payload(files)
    def test_symlink_in_scope_is_rejected(self):
        outside=self.root/'outside';outside.mkdir();link=self.root/'link'
        try:link.symlink_to(outside,target_is_directory=True)
        except (OSError,NotImplementedError):self.skipTest('Symlink unavailable')
        with self.assertRaises(safe.SafetyError):safe.make_plan(self.root,{'link/a.md':'x\n'},kind='project-context')
    def test_unsafe_roots_rejected(self):
        for root in [Path.home(),Path(Path.cwd().anchor)]:
            with self.assertRaises(safe.SafetyError):safe.root_dir(root)
    def test_plan_write_is_exclusive(self):
        plan=safe.make_plan(self.root,{'a.md':'x\n'},kind='project-context');p=self.root/'p.json';safe.write_plan(plan,p)
        with self.assertRaises(FileExistsError):safe.write_plan(plan,p)
    def test_home_expansion_cannot_bypass_symlink_check(self):
        home=self.root/'synthetic-home';home.mkdir();destination=self.root/'destination';destination.mkdir()
        try:(home/'alias').symlink_to(destination,target_is_directory=True)
        except (OSError,NotImplementedError):self.skipTest('Symlink unavailable')
        with patch.dict(os.environ,{'HOME':str(home),'USERPROFILE':str(home)}):
            with self.assertRaises(safe.SafetyError):safe.root_dir(Path('~/alias'))
    def test_broken_actual_frontmatter_fails_validation(self):
        folder=self.create('hermes');entry=folder/'SKILL.md';entry.write_text('Not a native skill header.\n')
        self.assertFalse(architect.validate(folder,self.spec,'hermes')['ok'])
    def test_control_characters_in_paths_are_rejected(self):
        for path in ['a\n.md','a\r.md','a\t.md']:
            with self.assertRaises(safe.SafetyError):safe.safe_relative(path)
    def test_original_checks_have_no_claimed_execution(self):
        files=architect.render(self.spec,'operational')
        self.assertIn('NAO EXECUTADO',files['validacao/CRITERIOS.md'])
        self.assertIn('Nenhum exemplo aprovado',files['exemplos/LEIA-ME.md'])

if __name__=='__main__':unittest.main()
