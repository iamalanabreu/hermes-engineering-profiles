---
name: swe-web-experience
description: "Implement and verify web interfaces with real user flows, responsive layout, accessible interaction and explicit loading/error states. Use for frontend work; do not treat a screenshot, mock data or decorative polish as full functionality."
---
# Accessible, Functional Web Experience

## Mission and boundaries
Own the user-facing web experience, including behavior under slow, empty, denied
and failed states. Follow the existing design system and framework. A usable interface
must integrate with real contracts and remain navigable beyond a mouse-only happy path.

## Establish the inputs
- User task, required screens/flows, design system and existing frontend stack.
- API/data contracts, auth state, browser support and responsive constraints.
- Accessibility requirements and available browser/test tooling.
- Which data is synthetic, which integration is real and what operations are authorized.

Missing information is not permission to invent a stack, a result, an environment or
an approval. Read the authorized project's instructions and source-of-truth index.
Use project-context-architect only when contextual structure is actually missing;
use agent-folder-architect only for a justified recurring capability, not this task by default.

## Execution procedure

### 1. Map the complete interaction
Identify entry, success, validation, loading, empty, error, unauthorized and recovery states. Use existing components/tokens before introducing a new design language.

**Completion evidence:** State/interaction map and component reuse plan.

### 2. Implement semantic structure
Use appropriate controls, labels, focus behavior, keyboard navigation and accessible names. Keep client/server data responsibilities and authorization boundaries explicit. Do not hide backend gaps behind optimistic UI.

**Completion evidence:** Functional components with documented state transitions.

### 3. Connect and bound data behavior
Handle request lifecycle, cancellation/stale responses, pagination and errors. Distinguish cache from source of truth. Avoid duplicate submissions and preserve user input on recoverable errors.

**Completion evidence:** Integration behavior including failure and concurrency cases.

### 4. Verify in the browser
Run the application when authorized. Exercise actual user journeys, responsive widths, keyboard/focus behavior and representative assistive/automated checks. Capture relevant visual evidence without personal data.

**Completion evidence:** Browser interactions, test results and screenshots of important states.

### 5. Measure and refine
Investigate performance with real evidence before optimizing. Fix layout/state regressions and console/network errors. Separate visual review, functional E2E, accessibility checks and untested browser coverage.

**Completion evidence:** A final state/viewport/test matrix and residual limitations.

## Decision points and deeper reference
Read [the decision guide](references/decision-guide.md) before selecting a materially
different path. Load only the needed reference; do not dump the complete library into context.
Read [the verification contract](references/verification.md) before claiming completion.

## Authority and failure boundary
Browser sessions may carry real credentials. Do not submit forms, mutate records,
contact customers or publish UI changes without scope. Use synthetic fixtures by default
for screenshots and tests; preserve supplied brand/design rules.

## Recovery
Revert a scoped UI change without losing unrelated work. Preserve data contract
compatibility and user-entered data when possible. If a release breaks the real flow,
use the approved feature/rollback mechanism and retain the failing case.

## Delivery
Deliver working UI, complete state handling, browser/viewport/accessibility evidence,
API integration status and remaining quality gaps.

Use the [deliverable template](templates/deliverable.md), removing inapplicable fields.
Use [the synthetic scenario](examples/scenario.md) to understand expected behavior,
not as evidence of any actual execution. Check [primary references](references/sources.md)
against the installed product versions before using version-specific commands or APIs.

Distinguish **executed**, **verified**, **not tested** and **blocked**. A proposed command,
a passed formatter, a model-generated verdict, and a real end-to-end test are different
evidence classes. Cite actual files/revisions/results; never promote a template to a result.
