---
name: dso-infrastructure-change
description: "Review or implement IaC and infrastructure changes with explicit target, plan, blast radius, approval and recovery. Use for Terraform, cloud resources and infrastructure migrations; not for a read-only conceptual question."
---
# Infrastructure Change Engineering

## Mission and boundaries
Own the transition from observed infrastructure state to a reviewed desired state.
Do not confuse a syntactically valid plan with a safe change. Prefer the project's
existing IaC tool, provider and release path; do not prescribe a cloud vendor.

## Establish the inputs
- Authorized account/project, environment, resource scope and intended outcome; distinguish production from an isolated fixture.
- Repository revision, IaC tool/provider versions, state location and locking model; never print the state or secret variables.
- Dependencies, availability objectives, deletion/replacement tolerance, backup evidence and maintenance constraints.
- Who can authorize apply, how approval is bound to the reviewed artifact, and where evidence may be retained.

Missing information is not permission to invent a stack, a result, an environment or
an approval. Read the authorized project's instructions and source-of-truth index.
Use project-context-architect only when contextual structure is actually missing;
use agent-folder-architect only for a justified recurring capability, not this task by default.

## Execution procedure

### 1. Discover without mutation
Inspect the selected configuration, modules, inputs, lockfiles, current identity and target. Use read-oriented commands only. Treat data sources, external provisioners and provider initialization as potentially active code. Explain any required network or credentials before invoking them.

**Completion evidence:** Inventory identifies the exact scope, versioned source, identity and unknowns without exposing secrets.

### 2. Establish a meaningful plan
Run the project-supported format, validation and plan sequence in an authorized workspace. Keep plan files protected. Review creates, updates, destroys, replacement order, unknown values, drift and lifecycle changes. A green plan can still contain outage-causing replacements.

**Completion evidence:** Plan reference/digest and a redacted resource-action summary tied to the source revision.

### 3. Analyze the operational transition
Trace dependents of each changed endpoint, identity, route, volume, database and shared service. Compare compatibility, quota, cost, rollout ordering and recovery prerequisites. Separate code revert from recovery of data or external state.

**Completion evidence:** Blast-radius narrative, affected consumers, stop thresholds and verified recovery prerequisites.

### 4. Make the change decision
Choose the smallest safe rollout, not a preferred pattern by habit. Flag deletions, force-new fields, broad IAM and shared networking as material. Require approval of the actual target and reviewed plan before apply; regenerate review if state or code changes.

**Completion evidence:** A decision record with concrete approval scope; no mutation has preceded it.

### 5. Execute a bounded rollout when authorized
Use the existing deployment path and approved artifact. Do not bypass state locks, use force flags, improvise a different target or retry a partial failure blindly. Capture operation identifiers and stop on unexpected diff or health degradation.

**Completion evidence:** Execution result, operation ids and updated state information, excluding sensitive payloads.

### 6. Verify state and service behavior
Check reconciliation and user-facing health separately. Confirm resources, policy/identity behavior, telemetry and an agreed stabilization window. Record residual drift or unverified downstream effects rather than treating apply exit code as acceptance.

**Completion evidence:** Post-change checks and explicit executed/verified/not-tested/blocked verdicts.

## Decision points and deeper reference
Read [the decision guide](references/decision-guide.md) before selecting a materially
different path. Load only the needed reference; do not dump the complete library into context.
Read [the verification contract](references/verification.md) before claiming completion.

## Authority and failure boundary
Reading state, initializing providers and contacting cloud APIs require authorized scope.
Do not apply, destroy, unlock, import state, rotate credentials or alter shared networking
without the relevant explicit authorization. No policy in this file replaces IAM.

## Recovery
Stop further mutations on unexpected failure. Preserve the reviewed plan and operation
ids. Diagnose partial application before replanning. Choose approved rollback, restore
or forward repair according to actual resource and data semantics.

## Delivery
Deliver a target-bound change plan, resource-action review, blast radius, approval
requirements, execution evidence, recovery path and residual risks.

Use the [deliverable template](templates/deliverable.md), removing inapplicable fields.
Use [the synthetic scenario](examples/scenario.md) to understand expected behavior,
not as evidence of any actual execution. Check [primary references](references/sources.md)
against the installed product versions before using version-specific commands or APIs.

Distinguish **executed**, **verified**, **not tested** and **blocked**. A proposed command,
a passed formatter, a model-generated verdict, and a real end-to-end test are different
evidence classes. Cite actual files/revisions/results; never promote a template to a result.

## Deterministic helper
Summarize an already authorized Terraform JSON plan; exit 3 means destructive review, not apply authorization.

Read [the helper](scripts/review_plan.py). Invoke it through terminal using the resolved
`${HERMES_SKILL_DIR}/scripts/review_plan.py` path; run `--help` for inputs.
