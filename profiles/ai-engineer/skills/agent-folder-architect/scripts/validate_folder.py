#!/usr/bin/env python3
"""Validate a folder created by scaffold.py against the source blueprint."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from scaffold import BlueprintError, file_content, load_blueprint


REQUIRED = {"SKILL.md", "arquivos/INDICE.md", "exemplos/LEIA-ME.md", "validacao/CRITERIOS.md", "notas.md"}
LINK_PATTERN = re.compile(r"\]\(([^)]+)\)")


def validate_folder(folder: Path, spec: dict | None = None) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    if not folder.is_dir() or folder.is_symlink():
        return {"ok": False, "errors": [f"Pasta invalida: {folder}"], "warnings": []}
    files = list(folder.rglob("*"))
    rel_files = {str(path.relative_to(folder)) for path in files if path.is_file()}
    for rel in sorted(REQUIRED - rel_files):
        errors.append(f"Arquivo essencial ausente: {rel}")
    skill_path = folder / "SKILL.md"
    if skill_path.exists():
        skill_data = skill_path.read_text(encoding="utf-8")
        if not re.match(r"\A---\nname: [a-z0-9-]+\ndescription: .+\n---\n", skill_data):
            errors.append("SKILL.md: frontmatter name/description ausente ou invalido")
        if re.search(r"\b(?:TODO|TBD|PREENCHER AQUI)\b", skill_data, re.IGNORECASE):
            errors.append("SKILL.md: marcador generico nao resolvido")
    if spec is not None:
        if folder.name != spec["slug"]:
            errors.append("Nome do diretorio difere do slug do blueprint")
        expected = file_content(spec)
        for rel in sorted(set(expected) - rel_files):
            if rel not in REQUIRED:
                errors.append(f"Arquivo de blueprint ausente: {rel}")
        for extra in spec.get("files", []):
            path = folder / extra["path"]
            if path.is_file() and path.read_text(encoding="utf-8") != expected[extra["path"]]:
                warnings.append(f"Arquivo modificado desde o blueprint: {extra['path']}")
        index_path = folder / "arquivos/INDICE.md"
        if index_path.exists():
            index_text = index_path.read_text(encoding="utf-8")
            for extra in spec.get("files", []):
                if extra["path"] not in index_text:
                    errors.append(f"Indice nao referencia material: {extra['path']}")
    for file in files:
        if file.is_symlink():
            errors.append(f"Link simbolico nao permitido: {file.relative_to(folder)}")
            continue
        if not file.is_file() or file.suffix != ".md":
            continue
        content = file.read_text(encoding="utf-8")
        for candidate in LINK_PATTERN.findall(content):
            if candidate.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = (file.parent / candidate.split("#", 1)[0]).resolve()
            try:
                target.relative_to(folder.resolve())
            except ValueError:
                warnings.append(f"Link externo ao pacote: {file.relative_to(folder)} -> {candidate}")
                continue
            if not target.exists():
                errors.append(f"Link quebrado: {file.relative_to(folder)} -> {candidate}")
    if (folder / "PENDENCIAS.md").exists():
        warnings.append("Pendencias registradas; conferir antes de classificar como operacional")
    if (folder / "exemplos/LEIA-ME.md").exists():
        if "Nenhum exemplo aprovado" in (folder / "exemplos/LEIA-ME.md").read_text(encoding="utf-8"):
            warnings.append("Nenhum exemplo aprovado disponivel (nao e falha estrutural)")
    warnings.append("Verificacoes do processo e integracoes externas NAO foram executadas por este validador")
    return {"ok": not errors, "errors": sorted(set(errors)), "warnings": sorted(set(warnings)), "file_count": len(rel_files)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder", type=Path, required=True)
    parser.add_argument("--spec", type=Path)
    args = parser.parse_args()
    try:
        spec = load_blueprint(args.spec) if args.spec else None
        result = validate_folder(args.folder, spec)
    except (OSError, BlueprintError) as exc:
        result = {"ok": False, "errors": [str(exc)], "warnings": []}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
