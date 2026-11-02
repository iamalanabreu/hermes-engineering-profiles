---
name: dso-software-supply-chain
description: "Review CI/CD, dependencies, build provenance and artifact promotion with scoped permissions and verifiable release evidence. Use for pipeline and supply-chain changes; do not sign, publish or deploy without authorization."
---
# Secure Build and Release Supply Chain

## Mission and boundaries
Own the trust path from reviewed source to promoted artifact. Distinguish dependency
integrity, build reproducibility, vulnerability status, provenance and runtime safety;
none of these alone proves the others.

## Establish the inputs
- Source revision, release target, build workflow, artifact registry and promotion path.
- Dependency lockfiles, runner trust model, signing/identity mechanism and token scopes.
- Required quality/security gates, allowed exceptions and evidence retention.
- Who can trigger privileged jobs, publish artifacts, approve promotion and revoke a release.

Missing information is not permission to invent a stack, a result, an environment or
an approval. Read the authorized project's instructions and source-of-truth index.
Use project-context-architect only when contextual structure is actually missing;
use agent-folder-architect only for a justified recurring capability, not this task by default.

## Execution procedure

### 1. Map trust transitions
Trace source checkout, dependency retrieval, scripts, build runner, secrets, artifact upload and deployment. Include untrusted contributions, reusable workflows and caches.

**Completion evidence:** A trust-flow inventory with privileged boundaries.

### 2. Review inputs and privilege
Inspect pinning, lockfiles, dependency sources, action/plugin versions, token scopes, environment protections and secret access. Untrusted branch code must not inherit privileged release credentials.

**Completion evidence:** Specific findings tied to workflow lines and effective permission scope.

### 3. Define gates and evidence
Select tests, scanners, SBOM/provenance and signing checks appropriate to the product. Define exception ownership/expiry and fail behavior. Report scanner absence as not run, not clean.

**Completion evidence:** Gate matrix with evidence artifacts and blocking criteria.

### 4. Build and verify in a safe context
Use the existing supported build path. Verify the source revision and final artifact identity/digest. Do not execute newly downloaded scripts or change runner permissions implicitly.

**Completion evidence:** Build/test/scanner results and artifact digest tied to revision.

### 5. Promote only the verified artifact
Avoid rebuilding differently per environment. Verify provenance/signature policy and environment approval before publish/deploy. Keep secrets out of artifacts and logs.

**Completion evidence:** Artifact-to-environment promotion record and actual approvals.

### 6. Plan revocation and lifecycle
Document rollback to known artifact, compromised dependency response, key/credential revocation and retention. Revalidate when build inputs or trust assumptions change.

**Completion evidence:** Release/recovery procedure with explicit untested paths.

## Decision points and deeper reference
Read [the decision guide](references/decision-guide.md) before selecting a materially
different path. Load only the needed reference; do not dump the complete library into context.
Read [the verification contract](references/verification.md) before claiming completion.

## Authority and failure boundary
Commit, push, release publication, signing, production deployment and permission
changes each require appropriate authorization. A passing pipeline is not that
authorization. Do not relax controls to make a pipeline green.

## Recovery
Halt promotion when evidence does not match the artifact. Use a reviewed known-good
artifact or a forward fix. On suspected compromise, preserve evidence and coordinate
revocation; do not merely rerun the same untrusted build.

## Delivery
Deliver a build trust map, concrete pipeline/dependency findings, gate policy,
artifact provenance, release decision and recovery limitations.

Use the [deliverable template](templates/deliverable.md), removing inapplicable fields.
Use [the synthetic scenario](examples/scenario.md) to understand expected behavior,
not as evidence of any actual execution. Check [primary references](references/sources.md)
against the installed product versions before using version-specific commands or APIs.

Distinguish **executed**, **verified**, **not tested** and **blocked**. A proposed command,
a passed formatter, a model-generated verdict, and a real end-to-end test are different
evidence classes. Cite actual files/revisions/results; never promote a template to a result.
