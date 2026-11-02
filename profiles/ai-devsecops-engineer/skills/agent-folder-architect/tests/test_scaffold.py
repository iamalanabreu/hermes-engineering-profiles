"""Deterministic tests for the meta-skill generator (stdlib unittest)."""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from scaffold import BlueprintError, create_folder, file_content, load_blueprint  # noqa: E402
from validate_folder import validate_folder  # noqa: E402


class TestFolderScaffold(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = load_blueprint(ROOT / "assets" / "blueprint-exemplo.json")

    def test_expected_files_and_metadata(self):
        rendered = file_content(self.spec)
        self.assertTrue({
            "SKILL.md", "arquivos/INDICE.md", "exemplos/LEIA-ME.md",
            "validacao/CRITERIOS.md", "notas.md", "PENDENCIAS.md"
        }.issubset(rendered))
        self.assertIn("name: revisao-documental-semanal", rendered["SKILL.md"])
        self.assertIn("NAO EXECUTADO", rendered["validacao/CRITERIOS.md"])
        self.assertIn("Nenhum exemplo aprovado", rendered["exemplos/LEIA-ME.md"])

    def test_dry_run_non_mutating_and_create_validate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan = create_folder(self.spec, root, dry_run=True)
            self.assertEqual(plan["mode"], "dry-run")
            self.assertFalse((root / self.spec["slug"]).exists())
            created = create_folder(self.spec, root, dry_run=False)
            self.assertEqual(created["mode"], "created")
            result = validate_folder(root / self.spec["slug"], self.spec)
            self.assertTrue(result["ok"], result)
            self.assertEqual(result["file_count"], 8)

    def test_never_overwrite_existing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / self.spec["slug"]
            target.mkdir()
            marker = target / "existing.txt"
            marker.write_text("protect", encoding="utf-8")
            with self.assertRaises(BlueprintError):
                create_folder(self.spec, root, dry_run=False)
            self.assertEqual(marker.read_text(encoding="utf-8"), "protect")

    def test_reject_path_traversal_and_absolute(self):
        for path in ("arquivos/../../outside.md", "arquivos/../x.md", "/tmp/attack.md", "arquivos/.env", "scripts/malware.exe", "arquivos/indice.md"):
            modified = copy.deepcopy(self.spec)
            modified["files"][0]["path"] = path
            with self.subTest(path=path), self.assertRaises(BlueprintError):
                file_content(modified)

    def test_reject_fabricated_approved_example(self):
        modified = copy.deepcopy(self.spec)
        modified["files"].append({
            "path": "exemplos/bom-1.md", "content": "Resultado inventado",
            "purpose": "Calibrar", "origin": "Aprovado sem evidencia", "status": "approved"
        })
        with self.assertRaises(BlueprintError):
            file_content(modified)

    def test_approved_example_requires_source_reference(self):
        modified = copy.deepcopy(self.spec)
        modified["files"].append({
            "path": "exemplos/bom-1.md", "content": "Modelo aprovado real",
            "purpose": "Calibrar", "origin": "Aprovado pelo responsavel da tarefa",
            "status": "approved", "source_ref": "docs/example-approved.md"
        })
        self.assertIn("exemplos/bom-1.md", file_content(modified))
        self.assertIn("docs/example-approved.md", file_content(modified)["exemplos/LEIA-ME.md"])

    def test_reject_missing_objective_checks(self):
        modified = copy.deepcopy(self.spec)
        modified["checks"] = []
        with self.assertRaises(BlueprintError):
            file_content(modified)

    def test_reject_private_keys_and_known_tokens(self):
        modified = copy.deepcopy(self.spec)
        modified["files"][0]["content"] = "-----BEGIN " + "PRIVATE KEY-----\ntest\n"
        with self.assertRaises(BlueprintError):
            file_content(modified)

    def test_optional_agents_file(self):
        modified = copy.deepcopy(self.spec)
        modified["agents_md"] = "# Instrucoes locais\n\nConsultar SKILL.md antes de executar."
        rendered = file_content(modified)
        self.assertIn("AGENTS.md", rendered)
        self.assertIn("AGENTS.md", rendered["arquivos/INDICE.md"])

    def test_validator_detects_deleted_required_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            create_folder(self.spec, root, dry_run=False)
            folder = root / self.spec["slug"]
            (folder / "notas.md").unlink()
            result = validate_folder(folder, self.spec)
            self.assertFalse(result["ok"])
            self.assertTrue(any("notas.md" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
