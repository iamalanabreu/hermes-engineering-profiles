---
name: swe-local-crossplatform
description: "Develop local tools, CLI applications and desktop software with bounded OS integration, persistence and packaging. Use for offline or cross-platform products; do not assume web security, filesystem paths or packaging behave identically on every OS."
---
# Local, CLI and Cross-Platform Software

## Mission and boundaries
Own application behavior on the user's device and its packaging contract. Choose
CLI, desktop or local service based on the user workflow; do not default to Electron,
Tauri, a browser or a cloud backend without a requirement.

## Establish the inputs
- User workflow, target operating systems/architectures and offline/online requirements.
- Existing language/runtime, installation constraints, resource budgets and update policy.
- Filesystem/process/IPC/network permissions, storage paths and sensitive local data.
- Available test machines, signing/notarization capability and authorized integration scope.

Missing information is not permission to invent a stack, a result, an environment or
an approval. Read the authorized project's instructions and source-of-truth index.
Use project-context-architect only when contextual structure is actually missing;
use agent-folder-architect only for a justified recurring capability, not this task by default.

## Execution procedure

### 1. Choose the product boundary
Determine whether a command, local service or desktop UI best fits the task. Compare deployment size, OS integration, offline behavior, updates and maintenance against requirements.

**Completion evidence:** Proportional interface/runtime decision and target platform matrix.

### 2. Design OS and data contracts
Specify arguments/configuration precedence, exit statuses, paths, encoding, permissions, IPC and local persistence. Keep untrusted UI/content away from privileged operations. Avoid assuming POSIX paths/shell behavior everywhere.

**Completion evidence:** CLI/IPC/storage/error contracts and permission model.

### 3. Implement safe local behavior
Validate input/path scope, quote/avoid shell execution where possible, handle file locking and partial writes, support cancellation and meaningful errors. Do not silently overwrite user files or open a network listener publicly.

**Completion evidence:** Working bounded implementation and negative-path tests.

### 4. Package and test target environments
Build using documented toolchains and test clean install, launch, update, uninstall and offline operation where applicable. Verify code signing or notarization only with actual platform evidence.

**Completion evidence:** Artifact/platform matrix and observed installation behavior.

### 5. Verify recovery and maintainability
Test interruption, corrupted config/data, missing permissions and incompatible versions. Preserve user data during update/uninstall unless explicitly requested. Document unsupported targets and recovery.

**Completion evidence:** Recovery tests, resource observations and honest portability limits.

## Decision points and deeper reference
Read [the decision guide](references/decision-guide.md) before selecting a materially
different path. Load only the needed reference; do not dump the complete library into context.
Read [the verification contract](references/verification.md) before claiming completion.

## Authority and failure boundary
OS integrations, privileged permissions, public listeners, signing, updates and
filesystem changes require scope. Do not use another application's credentials or
modify shell startup/system settings merely to make a demo run.

## Recovery
Preserve user data and the previous runnable artifact. Restore only scoped changes
with content checks. If an update or migration is irreversible, state that limitation
and require a recovery decision before proceeding.

## Delivery
Deliver the working local product, CLI/IPC/storage contracts, tested platform/artifact
matrix, installation instructions, offline/recovery behavior and remaining limits.

Use the [deliverable template](templates/deliverable.md), removing inapplicable fields.
Use [the synthetic scenario](examples/scenario.md) to understand expected behavior,
not as evidence of any actual execution. Check [primary references](references/sources.md)
against the installed product versions before using version-specific commands or APIs.

Distinguish **executed**, **verified**, **not tested** and **blocked**. A proposed command,
a passed formatter, a model-generated verdict, and a real end-to-end test are different
evidence classes. Cite actual files/revisions/results; never promote a template to a result.
