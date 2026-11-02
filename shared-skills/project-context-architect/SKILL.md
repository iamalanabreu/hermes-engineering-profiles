---
name: project-context-architect
description: "Initialize or adopt a project/context with explicit scope, source-of-truth files and trust boundaries. Use for repository onboarding, context maps and portable project guidance. Do not replace an existing application or create a skill for a one-off task."
---
# Project Context Architect

## Decision contract
Own contextual structure, not the application's architecture or Hermes' project database.
Use the smallest useful context package. If the user only asks for a code edit, do it
through a domain skill instead. A recurring procedure is delegated to
`agent-folder-architect`; a context document is not automatically a skill.

## Workflow
1. Establish the actual authorized project and desired outcome. Distinguish greenfield,
   existing application, reusable operational procedure and knowledge-only context.
2. Read existing instructions and context within scope. Identify authoritative documents,
   contradictory constraints, trust domain and prohibited data flows. Preserve conventions.
3. Fill the [context contract](references/context-contract.md) from explicit inputs.
   Leave technology undecided unless supplied or justified by project evidence.
4. Preview creation of a new context directory, or plan adoption into an existing project.
   Adoption preserves existing README/source files and appends one contextual link to
   AGENTS.md. Review instruction precedence before making that link effective.
5. Review the complete file plan. Apply only after authorization; an adoption plan requires
   the digest of the reviewed bytes. Reject stale preimages, symlinks and broad roots.
6. Validate the files and then verify the effective context in a fresh Hermes session.
   `.hermes.md`/HERMES.md may outrank AGENTS.md; do not silently edit a higher-priority file.
7. Optionally register the existing directories using native `hermes project` commands
   after authorization. Do not create an alternative registry or edit Hermes databases.
8. Revisit the map when real architecture changes. Record decisions, not imaginary history.

## Terminal commands
The installed directory below is substituted by Hermes at skill-load time, not assumed
as a shell environment variable. Python 3.10+ is required.

```sh
python3 "${HERMES_SKILL_DIR}/scripts/context.py" create --spec CONTEXT.json --root AUTHORIZED_PARENT
python3 "${HERMES_SKILL_DIR}/scripts/context.py" create --spec CONTEXT.json --root AUTHORIZED_PARENT --apply
python3 "${HERMES_SKILL_DIR}/scripts/context.py" adopt-plan --spec CONTEXT.json --root EXISTING_PROJECT --out REVIEW_PLAN.json
python3 "${HERMES_SKILL_DIR}/scripts/context.py" adopt-apply --plan REVIEW_PLAN.json --approve-sha256 REVIEWED_DIGEST
python3 "${HERMES_SKILL_DIR}/scripts/context.py" validate --spec CONTEXT.json --root PROJECT_ROOT
```
This generator creates documentation and contextual instructions, not a working app.
Do not claim deployability, project trust, provider setup or test completion from it.
The adoption plan may replace this context's own documents but never deletes unrelated
files. The shared helper uses optimistic hashes and a recovery journal; see its caveats.

## Acceptance
The objective, non-goals, authoritative sources, data boundaries and validation
requirements must be locatable from one context index. A fresh authorized agent
must locate them without relying on the conversation that created them. Registering
a skill, trusting a repository and enforcing process isolation are separate actions.

## Resources
- [Context contract and taxonomy](references/context-contract.md)
- [Adoption and precedence checks](references/adoption.md)
- [Context CLI](scripts/context.py)
- [Filesystem helper](scripts/safe_files.py)
- [Synthetic context example](assets/context-example.json)
