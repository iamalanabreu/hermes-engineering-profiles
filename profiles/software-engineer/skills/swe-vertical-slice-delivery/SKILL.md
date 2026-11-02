---
name: swe-vertical-slice-delivery
description: "Implement a bounded feature or bug fix across the necessary application layers with working behavior, regression checks and a focused diff. Use for real product changes; do not replace requested implementation with a plan or expand scope silently."
---
# End-to-End Feature Delivery

## Mission and boundaries
Deliver a complete useful increment, not disconnected frontend/backend stubs.
Follow the existing stack and conventions. Small scope does not excuse missing error,
authorization or persistence behavior.

## Establish the inputs
- Requested user outcome, acceptance examples, explicit exclusions and relevant context.
- Actual codebase entrypoints, architecture, contracts, test commands and existing changes.
- Data/authentication boundaries, dependency constraints and runtime availability.
- Permission to edit, run tests, install dependencies, commit, push or deploy; these are distinct.

Missing information is not permission to invent a stack, a result, an environment or
an approval. Read the authorized project's instructions and source-of-truth index.
Use project-context-architect only when contextual structure is actually missing;
use agent-folder-architect only for a justified recurring capability, not this task by default.

## Execution procedure

### 1. Choose the smallest complete slice
Trace the user action to state change and visible result. Identify affected interface, domain, API and persistence layers. Write acceptance cases including invalid input, permission failure and dependency error.

**Completion evidence:** A bounded slice and testable expected outcomes.

### 2. Establish a failing or baseline check
For a bug, reproduce and preserve a regression test. For a feature, define contract/behavior tests before implementation where practical. For legacy code, characterize current behavior first. Do not delete existing code merely to enforce a testing ritual.

**Completion evidence:** Observed failing case or baseline and its reason.

### 3. Implement with explicit contracts
Make focused edits, keep types/schema/error semantics consistent and use project-supported dependency patterns. Handle loading/empty/error states in UI and validation/authorization in trusted server boundaries. Avoid unrelated cleanup.

**Completion evidence:** Working source changes mapped to the slice, with no undisclosed placeholders.

### 4. Verify incrementally
Run the smallest relevant tests, then affected regression/build/type checks. Test the real flow when runtime access exists. Separate mocks from integration evidence. Inspect the final diff for unrelated changes and generated artifacts.

**Completion evidence:** Actual command/test results and functional evidence.

### 5. Deliver and expose limits
Summarize behavior, changed files, tests, risks and missing verification. Commit/push/deploy only when authorized; stage only intended files. Turn discovered adjacent work into separate proposals, not silent expansion.

**Completion evidence:** A reviewable implementation and honest completion state.

## Decision points and deeper reference
Read [the decision guide](references/decision-guide.md) before selecting a materially
different path. Load only the needed reference; do not dump the complete library into context.
Read [the verification contract](references/verification.md) before claiming completion.

## Authority and failure boundary
Editing code does not authorize dependency installation, credential use, commits,
pushes, releases or production operations. Preserve user work and never bypass project
checks just to produce a green result.

## Recovery
Revert only your scoped changes when safe, preserving unrelated work. For schema or
external state changes, use the migration/compensation plan rather than a blind source
revert. Keep the failing regression case for future protection.

## Delivery
Deliver working slice, focused diff, acceptance/regression evidence, dependency
changes and explicit remaining integration or operational gaps.

Use the [deliverable template](templates/deliverable.md), removing inapplicable fields.
Use [the synthetic scenario](examples/scenario.md) to understand expected behavior,
not as evidence of any actual execution. Check [primary references](references/sources.md)
against the installed product versions before using version-specific commands or APIs.

Distinguish **executed**, **verified**, **not tested** and **blocked**. A proposed command,
a passed formatter, a model-generated verdict, and a real end-to-end test are different
evidence classes. Cite actual files/revisions/results; never promote a template to a result.
