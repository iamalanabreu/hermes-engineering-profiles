"""Three filled domain blueprints, rendered in both supported layouts."""
import json
from pathlib import Path
import tempfile
import unittest
from support import ROOT
import architect
from scaffold import load_blueprint
from safe_files import create_tree

class DomainBlueprintTests(unittest.TestCase):
    def _verify(self,name):
        spec=load_blueprint(ROOT/'examples/capabilities'/name)
        for layout in ['operational','hermes']:
            with self.subTest(layout=layout),tempfile.TemporaryDirectory() as d:
                root=Path(d);create_tree(root,spec['slug'],architect.render(spec,layout),dry_run=False)
                result=architect.validate(root/spec['slug'],spec,layout)
                self.assertTrue(result['ok'],result)
                self.assertIn('NAO EXECUTADO','\n'.join(architect.render(spec,layout).values()))
    def test_infrastructure_blueprint(self):self._verify('dso-change-gate.json')
    def test_provider_blueprint(self):self._verify('aie-provider-qualification.json')
    def test_software_blueprint(self):self._verify('swe-release-verification.json')

if __name__=='__main__':unittest.main()
