---
name: dso-cloud-security
description: "Review cloud architecture, network exposure and security controls with a threat model and evidence-backed findings. Use for hardening and cloud posture; do not claim compliance certification or run intrusive tests without scope."
---
# Cloud Security Architecture and Review

## Mission and boundaries
Assess effective trust boundaries and attack paths instead of counting security
products. Remediation should reduce reachable risk without breaking required service
paths. Use the target cloud's official current guidance, not a fixed vendor blueprint.

## Establish the inputs
- Assets, actors, public/private entrypoints, data classification and trust boundaries.
- Authorized accounts/projects, regions, subscriptions and review depth.
- Current topology, identity policies, logging coverage, recovery requirements and critical dependencies.
- Applicable requirements and exceptions; distinguish engineering review from formal certification.

Missing information is not permission to invent a stack, a result, an environment or
an approval. Read the authorized project's instructions and source-of-truth index.
Use project-context-architect only when contextual structure is actually missing;
use agent-folder-architect only for a justified recurring capability, not this task by default.

## Execution procedure

### 1. Construct the threat model
Map assets, entrypoints, identities, privilege transitions and data flows. Prioritize paths reachable under realistic attacker capabilities. Mark unknown boundaries instead of inventing a network diagram.

**Completion evidence:** Asset/data-flow map linked to real configuration or explicitly supplied facts.

### 2. Collect effective configuration
Inspect actual exposure, routes, firewall/security rules, identity grants, encryption/key controls and audit logging. Compare declared policy with effective state. Avoid collecting sensitive objects wholesale.

**Completion evidence:** Findings reference concrete resource/configuration evidence and its observation time.

### 3. Validate candidate findings
Trace whether a weakness is exploitable or blocked by another control. Use non-destructive checks first. Include false-positive analysis and prerequisite conditions. Do not equate an exposed port with a proven breach.

**Completion evidence:** Each finding states preconditions, impact, evidence, confidence and limitations.

### 4. Design proportionate remediation
Rank by impact and reachable path, not just a generic severity label. Choose least privilege, segmentation, private access and detection where justified; evaluate service dependencies and recovery.

**Completion evidence:** Prioritized remediation with owner decision, effort, trade-off and validation plan.

### 5. Stage and review changes
Produce a minimal IaC/policy diff. Establish rollout order, emergency access safeguards and rollback. Applying the change is a separate authorized action, preferably through dso-infrastructure-change.

**Completion evidence:** Reviewable changes and explicit separation of recommendation from execution.

### 6. Verify security and availability
Test intended allow/deny behaviors and logging. Confirm legitimate clients still work and expected blocked paths fail. Report untested attack paths and residual risk.

**Completion evidence:** Before/after control results tied to the exact target and revision.

## Decision points and deeper reference
Read [the decision guide](references/decision-guide.md) before selecting a materially
different path. Load only the needed reference; do not dump the complete library into context.
Read [the verification contract](references/verification.md) before claiming completion.

## Authority and failure boundary
No intrusive probing, exploitation, production policy modification or credential
rotation without explicit scope and authorization. Human approval and platform IAM
remain separate; technical findings do not grant emergency access.

## Recovery
Roll back a control change only through the approved recovery path. Preserve audit
visibility and emergency access; record the temporary exception and its expiry.
A rollback that reintroduces exposure needs an explicit risk decision.

## Delivery
Deliver a threat model, evidence-backed finding set, prioritized control changes,
validation evidence, false-positive analysis and residual-risk decisions.

Use the [deliverable template](templates/deliverable.md), removing inapplicable fields.
Use [the synthetic scenario](examples/scenario.md) to understand expected behavior,
not as evidence of any actual execution. Check [primary references](references/sources.md)
against the installed product versions before using version-specific commands or APIs.

Distinguish **executed**, **verified**, **not tested** and **blocked**. A proposed command,
a passed formatter, a model-generated verdict, and a real end-to-end test are different
evidence classes. Cite actual files/revisions/results; never promote a template to a result.
