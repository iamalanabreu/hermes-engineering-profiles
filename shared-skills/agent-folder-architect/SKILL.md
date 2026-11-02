---
name: agent-folder-architect
description: "Create and evolve reusable operational folders with scope, evidence and validation. Use for recurrent agent capabilities, runbooks and contextual workflows. Route general project setup to project-context-architect; do not create folders for a simple one-off edit."
---
# Agent Folder Architect

## Persistent routing contract
This skill may be preloaded. Treat its presence as readiness, never as authorization
to create files on every turn. Classify a new request before acting:
- Recurrent procedure with observable outputs: use this skill.
- Project initialization, adoption or context organization: use `project-context-architect`.
- One-off edit, explanation or bug: use the relevant domain skill; do not scaffold.
- Existing operational folder: plan an evolution; never recreate over it.

Use only the authorized project context. Separate facts, assumptions and unknowns.
A folder, profile, context file or approval digest does not grant filesystem access.

## Procedure
1. Establish goal, recurrence, consumer, explicit destination and trust domain. Read the
   existing project instructions only within authorized scope. Do not infer clients.
2. Read [adaptation](references/adaptation-guide.md) and [blueprint contract](references/blueprint-contract.md).
   Put real inputs, decision points, outputs and external checks in a version-1.0 blueprint.
3. Choose layout deliberately: `operational` preserves SKILL.md, arquivos/INDICE.md,
   exemplos/LEIA-ME.md, validacao/CRITERIOS.md and notas.md. `hermes` maps supporting
   files to references/, examples/, scripts/ and assets/ for portable installation.
4. Preview with the script below. Review every proposed file; no placeholders in the
   final procedure, no invented approval, no credential values and no unexplained files.
5. Apply only to an approved root. Creation refuses an existing destination. Evolution
   requires a plan, content diff, preimage hashes and approval of the exact plan digest.
6. Run validation, inspect the produced tree, then execute the actual task-specific
   acceptance checks when authorized. Structural validation alone is not functional proof.
7. Report executed / verified / not tested / blocked, with exact artifacts and revisions.
   Save a reusable template only after a real approved outcome; mark synthetic examples.

## Commands through the terminal tool
Hermes substitutes `${HERMES_SKILL_DIR}` in loaded skill text. It is NOT a promise
that your shell exports an environment variable. Use the resolved absolute path in
terminal commands; on another agent, resolve the installed skill directory first.

```sh
python3 "${HERMES_SKILL_DIR}/scripts/architect.py" create --spec BLUEPRINT.json --root AUTHORIZED_PARENT --layout operational
python3 "${HERMES_SKILL_DIR}/scripts/architect.py" create --spec BLUEPRINT.json --root AUTHORIZED_PARENT --layout operational --apply
python3 "${HERMES_SKILL_DIR}/scripts/architect.py" validate --spec BLUEPRINT.json --folder CREATED_FOLDER --layout operational
python3 "${HERMES_SKILL_DIR}/scripts/architect.py" evolve-plan --spec REVISED_BLUEPRINT.json --folder EXISTING_FOLDER --layout operational --out REVIEW_PLAN.json
python3 "${HERMES_SKILL_DIR}/scripts/architect.py" evolve-apply --plan REVIEW_PLAN.json --approve-sha256 REVIEWED_DIGEST
```
Arguments in capitals are caller-supplied values, not real paths. Scripts require
Python 3.10+ and no third-party packages; they do not run application commands.
Use `--layout hermes` for a skill intended for independent installation. A new
project-local skill needs a recognized skill root and explicit project trust.

## Pitfalls and stop conditions
Do not overwrite a destination, follow symlinks, move to a different root after
approval, mix organizational contexts, classify synthetic fixtures as approved, or
use a security scanner as proof of absence of secrets. File-based policies are not
sandboxing. When a preimage hash changes, discard the plan and review again.
Evolution preserves unlisted files; deletion requires a separate maintenance decision.
Multi-file evolution uses a recovery journal, not a crash-proof filesystem transaction.
Never auto-delete a stale lock or backup without inspecting the recovery state.

## Verification and resources
Apply [quality gates](references/quality-gates.md) and [portable execution](references/hermes-adapter.md).
The complete [original workflow](references/original-workflow.md) remains reference
material; this compact entrypoint is the active routing contract.

Every runtime dependency is linked explicitly for portable skill installers:
- [Architect CLI](scripts/architect.py)
- [Original deterministic renderer](scripts/scaffold.py)
- [Filesystem and approval helpers](scripts/safe_files.py)
- [Original structural validator](scripts/validate_folder.py)
- [Synthetic blueprint](assets/blueprint-exemplo.json)
- [Invocation prompt](assets/PROMPT_DE_ACIONAMENTO.md)
