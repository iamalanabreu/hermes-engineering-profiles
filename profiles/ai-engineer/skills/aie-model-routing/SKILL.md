---
name: aie-model-routing
description: "Design or diagnose LLM provider/gateway routes, fallbacks and compatibility with measurable quality, latency, cost and data boundaries. Use for routing policies and provider failures; do not silently change models or send data to another trust domain."
---
# Model, Provider and Gateway Routing

## Mission and boundaries
Own the route from application request to eligible inference service. Treat API
compatibility as a tested contract, not a label. Optimize for successful authorized
outcomes; low price per token is not automatically low cost per task.

## Establish the inputs
- Task classes, required modalities/tool calls/structured outputs, context needs and quality floor.
- Approved providers, data policy/residency restrictions, authentication source and endpoint configuration by logical reference.
- Latency/cost objectives, concurrency, rate limits, timeout/retry budget and acceptable fallback behavior.
- Baseline traces/evals with model version and observed response/error patterns.

Missing information is not permission to invent a stack, a result, an environment or
an approval. Read the authorized project's instructions and source-of-truth index.
Use project-context-architect only when contextual structure is actually missing;
use agent-folder-architect only for a justified recurring capability, not this task by default.

## Execution procedure

### 1. Inventory the route contract
Record protocol, endpoint origin, model identifiers, auth mechanism, supported request fields, streaming behavior, tool-call schema and output limits. Verify official docs and actual responses; do not infer all capabilities from an OpenAI-compatible base URL.

**Completion evidence:** A compatibility matrix with verified, unsupported and unknown fields.

### 2. Classify failures correctly
Separate authentication, permission/quota, rate limit, transient service/network, invalid request, context overflow and semantic quality failure. Read retry signals and distinguish provider errors from gateway transformation bugs.

**Completion evidence:** A failure taxonomy and observed examples without credential or prompt leakage.

### 3. Define eligible routes
Apply data and permission constraints before cost/latency preferences. Match capabilities to task class. Keep route identifiers and versions reproducible; refuse unsupported options instead of silently deleting request fields.

**Completion evidence:** Eligibility rules and an ordered route policy with explicit exclusions.

### 4. Design retries and fallback
Bound attempt count and total deadline. Use backoff/jitter where applicable. Prevent cycles and retry storms. Non-idempotent tool actions are not retried by swapping the model. Do not route around a 401 or quota policy as though it were transient.

**Completion evidence:** Failure-to-action decision table, budgets and side-effect semantics.

### 5. Test compatibility and degradation
Run fixtures for text, tool calls, structured outputs, streaming interruption, cancellation and negative errors. Compare provider change impact on evaluation cases, not one happy-path answer.

**Completion evidence:** Per-route outcomes, fallback reason and quality/cost/latency measurements.

### 6. Publish an observable policy
Version the routing policy, expose actual selected model/provider and failure classification, and keep a rollback route. Avoid hidden cross-provider data movement. Measure effective cost per successful task.

**Completion evidence:** Policy revision, redacted route traces, eligibility evidence and rollback decision.

## Decision points and deeper reference
Read [the decision guide](references/decision-guide.md) before selecting a materially
different path. Load only the needed reference; do not dump the complete library into context.
Read [the verification contract](references/verification.md) before claiming completion.

## Authority and failure boundary
No new provider, credential pool, endpoint, model entitlement or cross-region route
is enabled implicitly. Keep keys out of prompts and policy examples. A routing policy
is separate from native Hermes configuration; translate only documented fields.

## Recovery
Restore the last evaluated routing policy and preserve failure diagnostics. Do not
replay side effects. If no authorized route satisfies the contract, return a typed
unavailable result instead of silently weakening requirements.

## Delivery
Deliver the eligibility/compatibility matrix, error taxonomy, retry/fallback policy,
measured evaluation results and observable selected-route evidence.

Use the [deliverable template](templates/deliverable.md), removing inapplicable fields.
Use [the synthetic scenario](examples/scenario.md) to understand expected behavior,
not as evidence of any actual execution. Check [primary references](references/sources.md)
against the installed product versions before using version-specific commands or APIs.

Distinguish **executed**, **verified**, **not tested** and **blocked**. A proposed command,
a passed formatter, a model-generated verdict, and a real end-to-end test are different
evidence classes. Cite actual files/revisions/results; never promote a template to a result.
