---
name: swe-codebase-discovery
description: "Inspect an unfamiliar repository and trace real execution/data paths before modifying it. Use for onboarding, impact analysis and legacy discovery; not for a speculative architecture diagram based only on folder names."
---
# Evidence-Based Codebase Discovery

## Mission and boundaries
Build a useful, evidence-backed model of an existing codebase. Code and executable
contracts outrank stale prose, but neither should be run blindly. Avoid whole-repository
summaries when a bounded call path answers the task.

## Establish the inputs
- Authorized repository/workspace, requested feature/problem and investigation scope.
- Existing project instructions, documentation, manifests, lockfiles and repository status.
- Execution permission, trusted tooling and data/credential limitations.
- Expected outcome: orientation, change-impact map, bug hypothesis or implementation plan.

Missing information is not permission to invent a stack, a result, an environment or
an approval. Read the authorized project's instructions and source-of-truth index.
Use project-context-architect only when contextual structure is actually missing;
use agent-folder-architect only for a justified recurring capability, not this task by default.

## Execution procedure

### 1. Establish safe context
Confirm the actual working directory and relevant instructions. Inspect uncommitted/untracked work without overwriting it. Identify nested repositories and generated/vendor areas. Do not execute package scripts, hooks or build files from an untrusted checkout.

**Completion evidence:** Scope and trust record plus the relevant pre-existing changes.

### 2. Identify the runtime and entrypoints
Read manifests, build configurations, service definitions and composition roots. Record versions and commands as declared, not yet executed. Use the optional inventory helper only for bounded metadata; file counts do not explain architecture.

**Completion evidence:** Manifest/toolchain map and entrypoint candidates linked to source.

### 3. Trace a representative path
Follow one user request, command, event or job through interface, domain, storage and external boundaries. Inspect call sites and error paths; distinguish runtime wiring from unused code.

**Completion evidence:** A source-linked execution/data path with unresolved links marked.

### 4. Map change impact
Find public contracts, shared types, migrations, tests, callers and operational dependencies affected by the request. Check backward compatibility and hidden side effects.

**Completion evidence:** A bounded impact map with likely edit/test locations.

### 5. Validate the model and hand off
Use a minimal authorized run/test or static trace to challenge assumptions. Summarize confirmed behavior, unknowns and next steps. Update existing context docs only when requested and useful.

**Completion evidence:** An actionable map that another engineer can verify without the original conversation.

## Decision points and deeper reference
Read [the decision guide](references/decision-guide.md) before selecting a materially
different path. Load only the needed reference; do not dump the complete library into context.
Read [the verification contract](references/verification.md) before claiming completion.

## Authority and failure boundary
Repository read access is not permission to run its scripts, install dependencies,
trust LSP servers, change files or contact production. Seek explicit authority where
needed. Do not copy client context into the generic profile.

## Recovery
Discovery is read-oriented. If a probe changes state, stop and disclose it. Preserve
observations, revert only your authorized changes, and refine the trust boundary before
continuing. Do not clean the repository to make exploration easier.

## Delivery
Deliver a concise source-grounded orientation map, representative flow, impact/test
locations, unknowns and the smallest justified implementation step.

Use the [deliverable template](templates/deliverable.md), removing inapplicable fields.
Use [the synthetic scenario](examples/scenario.md) to understand expected behavior,
not as evidence of any actual execution. Check [primary references](references/sources.md)
against the installed product versions before using version-specific commands or APIs.

Distinguish **executed**, **verified**, **not tested** and **blocked**. A proposed command,
a passed formatter, a model-generated verdict, and a real end-to-end test are different
evidence classes. Cite actual files/revisions/results; never promote a template to a result.

## Deterministic helper
Collect bounded metadata without executing project scripts. Trace architecture separately.

Read [the helper](scripts/inventory.py). Invoke it through terminal using the resolved
`${HERMES_SKILL_DIR}/scripts/inventory.py` path; run `--help` for inputs.
