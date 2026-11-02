---
name: swe-quality-verification
description: "Design and execute risk-based software checks, regression tests and code review with actual evidence. Use before claiming a change works or a release is ready; do not replace tests with model confidence or coverage percentages."
---
# Software Verification and Review

## Mission and boundaries
Own a credible answer to what was verified, how, on which revision and with which
limits. Match test layers to failure risks. Review can improve confidence but cannot
prove behavior in an environment that was never exercised.

## Establish the inputs
- Requested behavior, acceptance criteria, changed revision/diff and baseline state.
- Risky boundaries: auth, data, concurrency, external integrations, UI and packaging.
- Available test/build/type/lint tools, fixtures and authorized runtime.
- Required gates, known baseline failures and release decision owner.

Missing information is not permission to invent a stack, a result, an environment or
an approval. Read the authorized project's instructions and source-of-truth index.
Use project-context-architect only when contextual structure is actually missing;
use agent-folder-architect only for a justified recurring capability, not this task by default.

## Execution procedure

### 1. Build a verification map
Map requirements and changed boundaries to unit, integration, contract, E2E, exploratory or non-functional checks. Include failure/negative paths. Do not create every test layer for every trivial change.

**Completion evidence:** Risk-to-test matrix with critical gaps.

### 2. Establish baseline and test trust
Run or inspect baseline checks and fixture setup. Verify tests assert behavior, not implementation trivia or a mocked assertion that cannot fail. Detect skipped tests and missing dependencies.

**Completion evidence:** Baseline results and trustworthy assertions.

### 3. Execute the relevant suite
Run actual commands on the target revision. Capture exit statuses, failures and environment limitations. For UI, exercise user flows and inspect visual/responsive states. For local/desktop, test platform-specific packaging separately.

**Completion evidence:** Raw results and artifacts tied to revision and environment.

### 4. Review the diff independently where useful
Inspect security, logic, complexity, compatibility and error handling. Use a separate reviewer only when available and justified; otherwise label self-review honestly. Do not claim independence for another pass in the same context.

**Completion evidence:** Prioritized findings with file-level evidence and review provenance.

### 5. Resolve and reverify
Fix only justified findings, rerun affected checks and re-evaluate critical failures. Do not weaken tests to accept incorrect behavior or ignore a mandatory gate. Bound review loops and escalate unresolved questions.

**Completion evidence:** Final check matrix including baseline, resolved, remaining and not-tested items.

## Decision points and deeper reference
Read [the decision guide](references/decision-guide.md) before selecting a materially
different path. Load only the needed reference; do not dump the complete library into context.
Read [the verification contract](references/verification.md) before claiming completion.

## Authority and failure boundary
Do not modify release policy, skip mandatory checks, run destructive test fixtures
or publish artifacts without authorization. An evaluation verdict does not authorize
commit, push, merge or deploy.

## Recovery
Preserve failing artifacts, restore only authorized fixture state and revert an
unsafe change if appropriate. Keep a regression test. Escalate missing environments
instead of substituting guessed results.

## Delivery
Deliver a risk-based test matrix, actual results, review findings, critical gaps and
a qualified readiness decision, including what was not tested.

Use the [deliverable template](templates/deliverable.md), removing inapplicable fields.
Use [the synthetic scenario](examples/scenario.md) to understand expected behavior,
not as evidence of any actual execution. Check [primary references](references/sources.md)
against the installed product versions before using version-specific commands or APIs.

Distinguish **executed**, **verified**, **not tested** and **blocked**. A proposed command,
a passed formatter, a model-generated verdict, and a real end-to-end test are different
evidence classes. Cite actual files/revisions/results; never promote a template to a result.
