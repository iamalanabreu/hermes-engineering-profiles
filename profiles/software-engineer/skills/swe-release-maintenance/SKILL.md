---
name: swe-release-maintenance
description: "Prepare builds, packages, versioned changes and maintainable releases with compatibility and recovery evidence. Use for refactoring, dependencies and release readiness; do not publish or discard user changes automatically."
---
# Software Release and Sustainable Maintenance

## Mission and boundaries
Own software artifact readiness and safe evolution. Distinguish preparing a release
from publishing it, source recovery from data recovery, and a local build from platform
qualification. Favor focused maintenance with measurable benefit.

## Establish the inputs
- Change scope/revision, intended users/platforms and release contract.
- Existing build/package/versioning conventions, dependency locks and signing requirements.
- Compatibility/migration needs, required gates and known baseline failures.
- Authority for commit, push, tagging, signing, publishing and deployment.

Missing information is not permission to invent a stack, a result, an environment or
an approval. Read the authorized project's instructions and source-of-truth index.
Use project-context-architect only when contextual structure is actually missing;
use agent-folder-architect only for a justified recurring capability, not this task by default.

## Execution procedure

### 1. Inspect change and baseline
Review the precise diff, uncommitted work, public contracts, migrations and dependencies. Determine whether the change is bug fix, feature, breaking behavior or internal refactor.

**Completion evidence:** Scoped release inventory and baseline evidence.

### 2. Verify maintainability and compatibility
Remove unjustified complexity only within scope. For refactoring, preserve observable behavior and characterization tests. For dependency upgrades, inspect API/runtime/platform changes and security/license implications.

**Completion evidence:** Compatibility/risk analysis and focused maintenance justification.

### 3. Build the actual artifact
Use the supported toolchain and lockfiles. Produce an identified package/binary/container with a revision/digest. Confirm expected files and exclude secrets, caches and developer-only state.

**Completion evidence:** Artifact identity, contents and build result.

### 4. Qualify intended platforms and upgrades
Run required tests and installation/upgrade cases. Check data migrations and older consumers. If another OS/signing service is unavailable, record that platform as not tested instead of inferring parity.

**Completion evidence:** Platform/upgrade qualification matrix.

### 5. Prepare a controlled release
Write factual release notes, compatibility warnings and recovery instructions. Obtain authorization for each external publication step. Stage intended files only; never auto-label a change verified without evidence.

**Completion evidence:** Ready-to-review release package or authorized publication record.

## Decision points and deeper reference
Read [the decision guide](references/decision-guide.md) before selecting a materially
different path. Load only the needed reference; do not dump the complete library into context.
Read [the verification contract](references/verification.md) before claiming completion.

## Authority and failure boundary
No commit, push, tag, sign, publish, force reset or deployment without appropriate
explicit authority. Do not use cleanup to remove unfamiliar files. Package source is
not an instruction to execute arbitrary hooks or network installers.

## Recovery
Return to a known artifact/source state only when compatible with current data.
Retain failed artifacts and diagnostics where safe. For a bad published release,
follow the registry/update-channel revocation process instead of silently replacing it.

## Delivery
Deliver focused change summary, build/artifact evidence, compatibility matrix,
release notes, publication state and realistic recovery instructions.

Use the [deliverable template](templates/deliverable.md), removing inapplicable fields.
Use [the synthetic scenario](examples/scenario.md) to understand expected behavior,
not as evidence of any actual execution. Check [primary references](references/sources.md)
against the installed product versions before using version-specific commands or APIs.

Distinguish **executed**, **verified**, **not tested** and **blocked**. A proposed command,
a passed formatter, a model-generated verdict, and a real end-to-end test are different
evidence classes. Cite actual files/revisions/results; never promote a template to a result.
