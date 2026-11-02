#!/usr/bin/env python3
"""Scaffold a contextual, file-based agent skill folder from an audited JSON blueprint.

No third-party dependencies. Never overwrites an existing target folder.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any

SCHEMA_VERSION = "1.0"
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ALLOWED_PREFIXES = frozenset({
    "arquivos", "exemplos", "validacao", "scripts", "testes", "referencias", "assets"
})
RESERVED_PATHS = frozenset({
    "SKILL.md", "notas.md", "PENDENCIAS.md", "arquivos/INDICE.md",
    "exemplos/LEIA-ME.md", "validacao/CRITERIOS.md"
})
ALLOWED_STATUSES = frozenset({"draft", "verified", "approved", "synthetic"})
ALLOWED_SEVERITIES = frozenset({"critical", "major", "minor"})
SENSITIVE_SIGNATURES = [
    ("private-key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
    ("aws-access-key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("openai-key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
]


class BlueprintError(ValueError):
    pass


def text_value(value: Any, location: str, max_len: int = 20000) -> str:
    if not isinstance(value, str) or not value.strip():
        raise BlueprintError(f"{location}: texto nao vazio obrigatorio")
    if len(value) > max_len:
        raise BlueprintError(f"{location}: comprimento excede {max_len} caracteres")
    if "\x00" in value:
        raise BlueprintError(f"{location}: NUL nao permitido")
    return value.strip()


def get_strings(data: dict, key: str, *, minimum: int = 0) -> list[str]:
    items = data.get(key, [])
    if not isinstance(items, list) or len(items) < minimum:
        raise BlueprintError(f"{key}: lista com ao menos {minimum} item(ns) obrigatoria")
    return [text_value(item, f"{key}[{i}]", max_len=6000) for i, item in enumerate(items)]


def get_objects(data: dict, key: str, mandatory: tuple[str, ...], minimum: int = 0) -> list[dict]:
    items = data.get(key, [])
    if not isinstance(items, list) or len(items) < minimum:
        raise BlueprintError(f"{key}: lista com ao menos {minimum} item(ns) obrigatoria")
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            raise BlueprintError(f"{key}[{i}]: objeto obrigatorio")
        for field in mandatory:
            text_value(item.get(field), f"{key}[{i}].{field}")
    return items


def safe_path(path_str: str) -> str:
    text_value(path_str, "files[].path", max_len=240)
    if "\\" in path_str or path_str.startswith("/") or "\n" in path_str or "\r" in path_str:
        raise BlueprintError(f"Caminho nao permitido: {path_str!r}")
    path = PurePosixPath(path_str)
    if (
        len(path.parts) < 2
        or path.is_absolute()
        or any(part in (".", "..") or part.startswith(".") for part in path.parts)
        or path.parts[0] not in ALLOWED_PREFIXES
        or path_str.casefold() in {item.casefold() for item in RESERVED_PATHS}
        or str(path) != path_str
    ):
        raise BlueprintError(f"Caminho fora das pastas permitidas/reservado: {path_str!r}")
    if path.suffix not in {".md", ".txt", ".json", ".yaml", ".yml", ".py", ".sh", ".csv", ".toml"}:
        raise BlueprintError(f"Extensao nao permitida para arquivo de texto: {path_str!r}")
    return path_str


def scan_secrets(content: str, location: str) -> None:
    for name, pattern in SENSITIVE_SIGNATURES:
        if pattern.search(content):
            raise BlueprintError(f"{location}: possivel segredo ({name}); use referencia externa")


def load_blueprint(spec_path: Path) -> dict:
    try:
        data = json.loads(spec_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise BlueprintError(f"Nao foi possivel ler o JSON: {exc}") from exc
    validate_blueprint(data)
    return data


def validate_blueprint(data: Any) -> None:
    if not isinstance(data, dict):
        raise BlueprintError("Blueprint deve ser um objeto JSON")
    if data.get("version") != SCHEMA_VERSION:
        raise BlueprintError(f"version deve ser {SCHEMA_VERSION!r}")
    slug = text_value(data.get("slug"), "slug", max_len=64)
    if len(slug) < 2 or not SLUG.fullmatch(slug) or "anthropic" in slug or "claude" in slug:
        raise BlueprintError("slug deve ser kebab-case de 2 a 64 caracteres e nao conter nomes reservados")
    for key in ("title", "purpose", "description"):
        text_value(data.get(key), key, max_len=1024 if key == "description" else 6000)
    get_strings(data, "triggers", minimum=1)
    get_strings(data, "constraints", minimum=1)
    for key in ("prerequisites", "approvals", "assumptions", "pending"):
        get_strings(data, key)
    for key in ("source_of_truth", "project_context"):
        if key in data:
            text_value(data[key], key)
    inputs = get_objects(data, "inputs", ("name", "source", "validation"), minimum=1)
    for i, item in enumerate(inputs):
        if not isinstance(item.get("required"), bool):
            raise BlueprintError(f"inputs[{i}].required deve ser booleano")
    get_objects(data, "outputs", ("name", "acceptance"), minimum=1)
    get_objects(data, "steps", ("action", "evidence"), minimum=2)
    decisions = get_objects(data, "decisions", ("when", "then"))
    for i, d in enumerate(decisions):
        if "otherwise" in d and d["otherwise"] != "":
            text_value(d["otherwise"], f"decisions[{i}].otherwise")
    checks = get_objects(data, "checks", ("id", "criterion", "method", "evidence", "severity"), minimum=2)
    check_ids = set()
    for i, item in enumerate(checks):
        if item["severity"] not in ALLOWED_SEVERITIES:
            raise BlueprintError(f"checks[{i}].severity deve ser critical/major/minor")
        cid = item["id"].casefold()
        if cid in check_ids:
            raise BlueprintError(f"checks[{i}].id duplicado")
        check_ids.add(cid)
    files = get_objects(data, "files", ("path", "content", "purpose", "origin", "status"))
    paths_seen = set()
    for i, item in enumerate(files):
        path = safe_path(item["path"])
        if path.casefold() in paths_seen:
            raise BlueprintError(f"files[{i}]: caminho duplicado (inclusive maiusculas/minusculas)")
        paths_seen.add(path.casefold())
        if item["status"] not in ALLOWED_STATUSES:
            raise BlueprintError(f"files[{i}].status invalido")
        if item["status"] in {"approved", "verified"}:
            text_value(item.get("source_ref"), f"files[{i}].source_ref")
        if item["status"] == "synthetic" and path.startswith("exemplos/"):
            if "sintetico" not in item["origin"].casefold() and "sintético" not in item["origin"].casefold():
                raise BlueprintError(f"files[{i}]: exemplo sintetico exige origem rotulada")
        if item["status"] == "approved" and path.startswith("exemplos/"):
            if "aprov" not in item["origin"].casefold():
                raise BlueprintError(f"files[{i}]: exemplo aprovado exige origem com aprovacao explicita")
        scan_secrets(item["content"], f"files[{i}].content")
    scan_secrets(json.dumps(data, ensure_ascii=False), "blueprint")
    if "agents_md" in data:
        text_value(data["agents_md"], "agents_md", max_len=12000)


def safe_inline(value: Any) -> str:
    return str(value).strip().replace("\n", " ").replace("|", "\\|").replace("\r", "")


def bullets(items: list[str], empty: str = "Nenhum item especificado.") -> str:
    if not items:
        return empty
    return "\n".join(f"- {item}" for item in items)


def file_content(data: dict) -> dict[str, str]:
    """Pure deterministic rendering, with no filesystem writes."""
    validate_blueprint(data)
    slug, title = data["slug"], data["title"]
    extras = {f["path"]: f["content"].rstrip() + "\n" for f in data.get("files", [])}
    inputs = "\n".join(
        f"| {safe_inline(x['name'])} | {'Sim' if x['required'] else 'Nao'} | {safe_inline(x['source'])} | {safe_inline(x['validation'])} |"
        for x in data["inputs"]
    )
    outputs = "\n".join(
        f"| {safe_inline(x['name'])} | {safe_inline(x['acceptance'])} |"
        for x in data["outputs"]
    )
    steps = "\n".join(
        f"{i}. **Executar:** {x['action'].strip()}\n   - **Comprovar por:** {x['evidence'].strip()}"
        for i, x in enumerate(data["steps"], 1)
    )
    decisions = (
        "\n".join(
            f"| {safe_inline(x['when'])} | {safe_inline(x['then'])} | {safe_inline(x.get('otherwise', 'Interromper e esclarecer'))} |"
            for x in data.get("decisions", [])
        ) or "| Nao ha desvio conhecido | Executar a sequencia, respeitando bloqueios | Registrar o caso para revisao |"
    )
    links = [
        "- [Indice de arquivos](arquivos/INDICE.md)",
        "- [Guia de exemplos](exemplos/LEIA-ME.md)",
        "- [Criterios objetivos](validacao/CRITERIOS.md)",
        "- [Notas e aprendizado](notas.md)",
    ]
    if data.get("pending") or data.get("assumptions"):
        links.append("- [Pendencias e suposicoes](PENDENCIAS.md)")
    if extras:
        links.extend(f"- [{path}]({path})" for path in sorted(extras))
    if data.get("agents_md"):
        links.append("- [Instrucoes locais de descoberta](AGENTS.md)")
    intro = (
        f"# {title}\n\n"
        "> Instrucao operacional versionavel. Textos e exemplos nao conferem permissoes de execucao.\n\n"
        f"## Proposito\n\n{data['purpose'].strip()}\n\n"
        f"## Contexto e fonte de verdade\n\n"
        f"- Contexto: {data.get('project_context', 'Nao informado; consultar o escopo da solicitacao.')}\n"
        f"- Fonte principal: {data.get('source_of_truth', 'Nao definida; exigir confirmacao antes de afirmar fatos externos.')}\n\n"
        "## Acionamento\n\n"
        f"{bullets(data['triggers'])}\n\n"
        "## Precondicoes\n\n"
        f"{bullets(data.get('prerequisites', []), 'Nenhuma precondicao adicional comprovada.')}\n\n"
        "## Entradas e validacao inicial\n\n"
        "| Entrada | Obrigatoria | Origem | Como validar |\n|---|---|---|---|\n"
        f"{inputs}\n\n"
        "## Sequencia de execucao\n\n"
        f"{steps}\n\n"
        "## Decisoes condicionais\n\n"
        "| Se | Entao | Caso contrario |\n|---|---|---|\n"
        f"{decisions}\n\n"
        "## Limites operacionais\n\n"
        f"{bullets(data['constraints'])}\n\n"
        "## Acoes sujeitas a aprovacao\n\n"
        f"{bullets(data.get('approvals', []), 'Nenhuma aprovacao especifica declarada; ainda assim respeitar permissoes reais das ferramentas.')}\n\n"
        "## Entregaveis e aceite\n\n"
        "| Artefato | Criterio de aceite |\n|---|---|\n"
        f"{outputs}\n\n"
        "## Prova e conclusao\n\n"
        "Aplicar cada criterio em [validacao/CRITERIOS.md](validacao/CRITERIOS.md). "
        "Para cada verificacao, reportar metodo, evidencia e estado (aprovado, reprovado ou nao executado). "
        "Nao alegar sucesso sem verificacao. Falha critica impede concluir como operacional. "
        "Se diversas verificacoes falharem, revisar processo e fontes antes de corrigir apenas o output.\n\n"
        "## Tratamento de falhas e evolucao\n\n"
        "Classificar: erro de processo (alterar SKILL.md), ferramenta/fonte (alterar arquivos, scripts, exemplos) "
        "ou prova (alterar criterios/testes). Documentar falhas reais, causa e revalidacao em notas.md. "
        "Nao alterar arquivos mestres ou executar acoes externas sem autorizacao.\n\n"
        "## Recursos\n\n"
        + "\n".join(links) + "\n"
    )
    skill_md = "---\n" + f"name: {slug}\n" + "description: " + json.dumps(data["description"], ensure_ascii=False) + "\n---\n\n" + intro

    extra_rows = [
        ("SKILL.md", "Contrato operacional e processo", "Gerador a partir do blueprint", "draft"),
        ("validacao/CRITERIOS.md", "Conferencias objetivas", "Gerador a partir do blueprint", "draft"),
        ("exemplos/LEIA-ME.md", "Controle de procedencia dos exemplos", "Gerador a partir do blueprint", "draft"),
        ("notas.md", "Registro de mudanças e aprendizados reais", "Gerador, sem historico anterior", "draft"),
    ]
    extra_rows.extend((f["path"], f["purpose"], f["origin"], f["status"]) for f in data.get("files", []))
    if data.get("agents_md"):
        extra_rows.append(("AGENTS.md", "Instrucoes locais para descoberta de agentes", "Texto fornecido no blueprint", "draft"))
    index_lines = [
        "# Indice da caixa de ferramentas", "",
        "Este indice apresenta os arquivos disponiveis e sua procedencia. Nao presume revisao, homologacao ou validade eterna.", "",
        "| Arquivo | Finalidade | Origem | Status |", "|---|---|---|---|",
    ]
    for path, purpose, origin, status in extra_rows:
        link = "../" + path
        index_lines.append(f"| [{safe_inline(path)}]({link}) | {safe_inline(purpose)} | {safe_inline(origin)} | {status} |")
    index_lines.extend(["", "Ao atualizar um material, revisar origem/status e atualizar este indice. Aprovacao requer evidencia rastreavel.", ""])

    example_files = [f for f in data.get("files", []) if f["path"].startswith("exemplos/")]
    approved = [f for f in example_files if f["status"] == "approved"]
    example_intro = [
        "# Exemplos e calibracao", "",
        "Nunca tratar um exemplo sintetico ou nao verificado como resultado aprovado.", "",
    ]
    if approved:
        example_intro.append("## Exemplos aprovados e verificaveis")
        example_intro.append("")
        example_intro.extend(f"- [{f['path']}](../{f['path']}) — referencia de aprovacao: {f['source_ref']}" for f in approved)
    else:
        example_intro.extend(["**Nenhum exemplo aprovado foi fornecido ou verificado.**", "", "Adicionar apenas apos aprovacao humana rastreavel."])
    if example_files and len(approved) < len(example_files):
        example_intro.extend(["", "## Exemplos nao aprovados / sinteticos", ""])
        for f in example_files:
            if f["status"] != "approved":
                example_intro.append(f"- [{f['path']}](../{f['path']}) — status: {f['status']}; origem: {f['origin']}")
    example_intro.extend(["", "Se houver retrabalho por estilo ou conteudo, guardar exemplos contrastivos com explicacao objetiva.", ""])

    checks_lines = [
        "# Criterios objetivos de validacao", "",
        "Estado inicial: **NAO EXECUTADO**. Estes itens sao contratos de verificacao, nao evidencias de testes realizados.", "",
        "| ID | Criterio | Metodo externo/observavel | Evidencia exigida | Severidade | Estado inicial |",
        "|---|---|---|---|---|---|",
    ]
    for x in data["checks"]:
        checks_lines.append(
            f"| {safe_inline(x['id'])} | {safe_inline(x['criterion'])} | {safe_inline(x['method'])} | {safe_inline(x['evidence'])} | {x['severity']} | NAO EXECUTADO |"
        )
    checks_lines.extend([
        "", "## Protocolo de execucao", "",
        "1. Recolher dados autorizados e preservar referencia das fontes.",
        "2. Executar criterios com prova observavel; registrar falhas e nao executados.",
        "3. Interromper se um criterio `critical` falhar; nao declarar entrega operacional.",
        "4. Corrigir processo, materiais ou validacao conforme a causa e repetir os testes afetados.",
        "5. Entregar resultados com status e links para evidencias; nao inventar capturas ou logs.", ""
    ])

    notes = (
        "# Notas e aprendizado operacional\n\n"
        "Estado inicial: **sem execucoes e sem historico comprovado de falhas**.\n\n"
        "## Registros reais\n\n"
        "Acrescentar registros apenas depois de um evento efetivamente observado:\n\n"
        "- Data/hora de observacao e identificador da execucao.\n"
        "- Sintoma e evidencia verificavel.\n"
        "- Camada de causa: processo, caixa ou prova.\n"
        "- Correcao versionada e responsavel pela aprovacao, quando aplicavel.\n"
        "- Evidencia de regressao/reexecucao e limitacoes.\n\n"
        "Nao armazenar dados sensiveis, segredos ou logs completos quando bastar referenciar local protegido.\n"
    )
    result = {
        "SKILL.md": skill_md,
        "arquivos/INDICE.md": "\n".join(index_lines),
        "exemplos/LEIA-ME.md": "\n".join(example_intro),
        "validacao/CRITERIOS.md": "\n".join(checks_lines),
        "notas.md": notes,
    }
    if data.get("pending") or data.get("assumptions"):
        result["PENDENCIAS.md"] = (
            "# Pendencias e suposicoes declaradas\n\n"
            "## Informacoes pendentes\n\n"
            f"{bullets(data.get('pending', []), 'Nenhuma pendencia relatada.')}\n\n"
            "## Suposicoes nao verificadas\n\n"
            f"{bullets(data.get('assumptions', []), 'Nenhuma suposicao declarada.')}\n\n"
            "**Importante:** nao usar suposicoes como fatos e nao validar automaticamente pendencias.\n"
        )
    if data.get("agents_md"):
        result["AGENTS.md"] = data["agents_md"].rstrip() + "\n"
    # Render a polished PT-BR version without modifying the user-authored extras.
    words = {
        "Instrucao": "Instrução", "Proposito": "Propósito", "Indice": "Índice",
        "versionavel": "versionável", "permissoes": "permissões", "contrario": "contrário",
        "Nao": "Não", "Precondicoes": "Pré-condições", "Obrigatoria": "Obrigatória",
        "Sequencia": "Sequência", "Decisoes": "Decisões", "Entao": "Então",
        "Acoes": "Ações", "Criterios": "Critérios", "Criterio": "Critério",
        "Entregaveis": "Entregáveis", "executavel": "executável",
        "verificacao": "verificação", "evidencia": "evidência", "aprovacao": "aprovação",
        "operacao": "operação", "conclusao": "conclusão", "execucao": "execução",
        "nao": "não", "metodo": "método", "criterio": "critério", "historico": "histórico",
        "critica": "crítica", "verificacoes": "verificações", "evolucao": "evolução",
        "autorizacao": "autorização", "execucoes": "execuções", "Pendencias": "Pendências",
        "suposicoes": "suposições", "conferencias": "conferências", "Conferencias": "Conferências",
        "revalidacao": "revalidação", "mudancas": "mudanças", "calibracao": "calibração",
        "nenhuma": "nenhuma", "Nenhuma": "Nenhuma", "acoes": "ações"
    }
    for rel, content in list(result.items()):
        if rel.endswith(".md"):
            if rel == "SKILL.md":
                content = content.replace("Entradas e validacao inicial", "Entradas e validação inicial")
            for original, accent in words.items():
                content = re.sub(r"\b" + re.escape(original) + r"\b", accent, content)
            result[rel] = content
    result.update(extras)
    return result


def create_folder(spec: dict, root: Path, dry_run: bool) -> dict:
    if not root.exists() or not root.is_dir():
        raise BlueprintError(f"Root inexistente ou nao e diretorio: {root}")
    root = root.resolve(strict=True)
    target = root / spec["slug"]
    if target.exists() or target.is_symlink():
        raise BlueprintError(f"Destino ja existe; nao sobrescrever: {target}")
    result = file_content(spec)
    if dry_run:
        return {"mode": "dry-run", "target": str(target), "files": sorted(result)}
    temp_path = Path(tempfile.mkdtemp(prefix=f".{spec['slug']}-tmp-", dir=root))
    try:
        for relative, content in result.items():
            path = temp_path / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("x", encoding="utf-8", newline="\n") as fh:
                fh.write(content if content.endswith("\n") else content + "\n")
        if target.exists() or target.is_symlink():
            raise BlueprintError(f"Conflito detectado antes de publicar: {target}")
        temp_path.rename(target)
    except Exception:
        if temp_path.exists():
            shutil.rmtree(temp_path)
        raise
    return {"mode": "created", "target": str(target), "files": sorted(result)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, required=True, help="Blueprint JSON validado")
    parser.add_argument("--root", type=Path, required=True, help="Pasta pai autorizada, ja existente")
    parser.add_argument("--dry-run", action="store_true", help="Imprimir plano sem gravar nada")
    args = parser.parse_args()
    try:
        spec = load_blueprint(args.spec)
        outcome = create_folder(spec, args.root, args.dry_run)
    except (BlueprintError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(outcome, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
