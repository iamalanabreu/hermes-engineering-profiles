---
name: swe-application-security
description: "Design, implement or review application security across authentication, authorization, input/data flows and session boundaries. Use for SaaS/web/API/local applications; do not claim a scanner or secure prompt replaces enforced controls."
---
# Secure Application Engineering

## Mission and boundaries
Own security inside the application and its data flow. Make authorization and
validation properties testable at trusted boundaries. Coordinate infrastructure/IAM
changes separately with DevSecOps instead of assuming cloud permissions.

## Establish the inputs
- Application type, actors, assets, data sensitivity and external entrypoints.
- Authentication/session mechanism, authorization rules, tenant/owner model and privileged actions.
- Code paths, dependencies, storage/logging behavior and authorized review/test scope.
- Applicable risk requirements, exceptions and recovery/incident ownership.

Missing information is not permission to invent a stack, a result, an environment or
an approval. Read the authorized project's instructions and source-of-truth index.
Use project-context-architect only when contextual structure is actually missing;
use agent-folder-architect only for a justified recurring capability, not this task by default.

## Execution procedure

### 1. Threat-model the changed flow
Trace input, identity, authorization, domain action, data access, output and logs. Identify trust boundaries and realistic abuse cases. Do not use a generic checklist as a substitute for the actual flow.

**Completion evidence:** Scoped threat model and protected invariants.

### 2. Review effective controls
Inspect server-side permission checks, object ownership, input validation, output encoding, secret access and session handling. For local apps, review OS/file/IPC boundaries. Verify framework behavior from the actual version.

**Completion evidence:** Concrete findings with preconditions and affected paths.

### 3. Implement proportionate fixes
Enforce least privilege, parameterized queries, safe serialization/path handling and bounded resource use as relevant. Avoid bespoke cryptography or undocumented auth shortcuts. Keep denial behavior useful without leaking sensitive details.

**Completion evidence:** Focused code changes tied to findings.

### 4. Test attacks and legitimate use
Use authorized synthetic cases for unauthorized objects, role escalation, injection, malicious paths, session expiration and duplicate actions. Confirm legitimate users retain access.

**Completion evidence:** Positive/negative security tests with no real sensitive data.

### 5. Review exposure and lifecycle
Inspect logs, caches, exports and error reports for data leaks. Address dependency/secret findings through their real lifecycle, including revocation when needed. Report residual risk and untested paths.

**Completion evidence:** Security acceptance record and follow-up decisions.

## Decision points and deeper reference
Read [the decision guide](references/decision-guide.md) before selecting a materially
different path. Load only the needed reference; do not dump the complete library into context.
Read [the verification contract](references/verification.md) before claiming completion.

## Authority and failure boundary
Security testing stays within authorized systems and synthetic data. Do not
rotate credentials, change global IAM or expose user data to prove a finding.
Escalate platform controls outside the application's ownership.

## Recovery
Contain the affected operation and preserve redacted evidence. Revert only if the
prior state is not itself unsafe; otherwise use a forward fix. Coordinate credential
revocation and data-impact response through authorized owners.

## Delivery
Deliver scoped threat model, specific findings, fixes, positive/negative tests,
exposure analysis and residual risks.

Use the [deliverable template](templates/deliverable.md), removing inapplicable fields.
Use [the synthetic scenario](examples/scenario.md) to understand expected behavior,
not as evidence of any actual execution. Check [primary references](references/sources.md)
against the installed product versions before using version-specific commands or APIs.

Distinguish **executed**, **verified**, **not tested** and **blocked**. A proposed command,
a passed formatter, a model-generated verdict, and a real end-to-end test are different
evidence classes. Cite actual files/revisions/results; never promote a template to a result.
