---
name: dso-identity-secrets
description: "Design or troubleshoot IAM, workload identity, RBAC, OIDC and secret rotation with least privilege and safe recovery. Use for credential lifecycle and access boundaries; never request secret values in chat."
---
# Identity, Secrets and Credential Lifecycle

## Mission and boundaries
Own identity and secret lifecycle, not secret collection. Distinguish authentication,
authorization, token audience/issuer, credential issuance and application consumption.
Prefer short-lived workload identities when the verified platform supports them.

## Establish the inputs
- Actors, identities, resources, required actions and trust relationships.
- Identity provider/protocol, issuer/audience, token lifetime and intended validation location.
- Secret stores by logical name, consumer rollout behavior, rotation overlap and revocation capability.
- Authorized test identities, emergency access owner and audit-retention rules.

Missing information is not permission to invent a stack, a result, an environment or
an approval. Read the authorized project's instructions and source-of-truth index.
Use project-context-architect only when contextual structure is actually missing;
use agent-folder-architect only for a justified recurring capability, not this task by default.

## Execution procedure

### 1. Map identity-to-action paths
Enumerate which principal performs which operation on which resource. Trace delegation, group/role inheritance and cross-service trust. Do not retrieve tokens merely to populate a diagram.

**Completion evidence:** An identity/action/resource matrix and trust-boundary map.

### 2. Diagnose the failing boundary
For access failure, distinguish missing credential, expired credential, wrong issuer/audience, insufficient scope/role, network reachability and consumer cache. Use redacted claims and error codes, not raw bearer tokens.

**Completion evidence:** The failing layer and a safe discriminating test.

### 3. Design least privilege
Choose the narrowest identity and scope that support required actions. Prefer explicit audiences, bounded lifetime and workload binding. Document bootstrap trust and recovery before eliminating old access.

**Completion evidence:** Proposed grants/trust policy plus negative access cases.

### 4. Plan rotation or migration
Inventory consumers, caching, restart needs, overlapping validity, verification and revocation. Distinguish issuing a new credential from confirming every consumer uses it.

**Completion evidence:** A staged rotation plan with dependency order and revocation gate.

### 5. Execute only authorized changes
Do not print, commit or pass secrets through model-visible arguments. Use the approved secret manager/provider path. Never broaden roles to bypass a diagnosis or rotate unrelated credentials.

**Completion evidence:** Operation ids and consumer rollout evidence without secret material.

### 6. Verify both access and denial
Test required access, explicitly denied operations, expiry/revocation and audit entries. Validate that old credentials no longer work when revocation is part of the goal.

**Completion evidence:** Positive/negative access matrix, revocation evidence and residual consumers.

## Decision points and deeper reference
Read [the decision guide](references/decision-guide.md) before selecting a materially
different path. Load only the needed reference; do not dump the complete library into context.
Read [the verification contract](references/verification.md) before claiming completion.

## Authority and failure boundary
Never ask for a secret to be pasted into chat. Issuance, revocation, role changes,
trust policy changes and emergency access require explicit authority. Avoid reading
credential stores through general file tools; use approved identity/secret integrations.

## Recovery
For a failed rotation, preserve the approved overlap window where safe. Revert a
consumer configuration only if the prior credential remains valid and authorized.
A compromised credential must not be restored merely to regain availability.

## Delivery
Deliver an identity/action/resource matrix, trust design or diagnosis, staged
credential lifecycle plan, access verification and remaining risk.

Use the [deliverable template](templates/deliverable.md), removing inapplicable fields.
Use [the synthetic scenario](examples/scenario.md) to understand expected behavior,
not as evidence of any actual execution. Check [primary references](references/sources.md)
against the installed product versions before using version-specific commands or APIs.

Distinguish **executed**, **verified**, **not tested** and **blocked**. A proposed command,
a passed formatter, a model-generated verdict, and a real end-to-end test are different
evidence classes. Cite actual files/revisions/results; never promote a template to a result.
