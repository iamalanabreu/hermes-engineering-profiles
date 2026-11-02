---
name: aie-llmops-observability
description: "Instrument, release and operate LLM/agent services with quality, latency, cost, traces and recovery evidence. Use for AI operations and model/prompt promotion; do not log sensitive prompts or assume model health proves task success."
---
# LLMOps and Agent Observability

## Mission and boundaries
Own operational visibility and safe evolution of AI workloads. Track the whole task:
retrieval, model calls, tool execution, retries, approvals and final outcome. A healthy
endpoint and low token cost do not establish useful or safe service behavior.

## Establish the inputs
- Service/task objectives, traffic classes, data sensitivity and operational ownership.
- Code/prompt/model/tool/retrieval versions, gateways and deployment mechanisms.
- Telemetry backend, retention, redaction, metric cardinality constraints and attribution needs.
- Quality/latency/cost budgets, canary cohorts, stop conditions and recovery strategy.

Missing information is not permission to invent a stack, a result, an environment or
an approval. Read the authorized project's instructions and source-of-truth index.
Use project-context-architect only when contextual structure is actually missing;
use agent-folder-architect only for a justified recurring capability, not this task by default.

## Execution procedure

### 1. Define outcomes and telemetry boundaries
Identify useful task completion, critical failure and abstention. Choose latency stages, request/token/cost counters, tool/error/retry events and approval outcomes. Decide what data must never be logged.

**Completion evidence:** Measurement plan with privacy, retention and cardinality limits.

### 2. Instrument the workflow
Propagate trace/operation ids across gateway, retrieval, model and tools. Record actual selected route and versions. Redact sensitive arguments/results; avoid tenant/user ids as unbounded metric labels.

**Completion evidence:** A sample redacted trace that joins the actual execution stages.

### 3. Connect quality and runtime signals
Join offline evaluation with production samples where authorized. Distinguish transport errors, semantic failure, policy denial, context exhaustion and tool failure. Do not infer success only from HTTP status.

**Completion evidence:** Failure taxonomy and dashboards/queries tied to task outcomes.

### 4. Design promotion and rollback
Version code, prompts, tool schemas, permissions and data/index changes. Require evaluation gates and a bounded canary when justified. Define stop thresholds and compatibility of rollback with current data state.

**Completion evidence:** Promotion plan and artifact/version matrix.

### 5. Verify failure handling and budget control
Exercise provider outage, rate limit, runaway retry, tool timeout and partial completion in a safe fixture. Check alerts and total cost attribution including judges/retries.

**Completion evidence:** Fault-injection results and budget/alert evidence.

### 6. Operate and improve
Review quality drift, stale indexes, latency distribution and cost per accepted task. Route observed failures into eval cases and bounded fixes. Do not let automatic learning overwrite reviewed policies without approval.

**Completion evidence:** Operational review with prioritized changes and measured post-change results.

## Decision points and deeper reference
Read [the decision guide](references/decision-guide.md) before selecting a materially
different path. Load only the needed reference; do not dump the complete library into context.
Read [the verification contract](references/verification.md) before claiming completion.

## Authority and failure boundary
Enabling telemetry exporters, recording payloads, changing retention, publishing a
model or modifying routing can expose data or incur cost. Require authorization and
use approved destinations. Do not enable autonomous scheduled work by implication.

## Recovery
Stop promotion, reduce affected traffic when authorized and restore a compatible
known-good version set. Preserve redacted diagnostics. Quarantine suspect memory/index
changes rather than rolling back permissions to an unsafe state.

## Delivery
Deliver privacy-aware telemetry design, actual traces/metrics, release/evaluation
gates, operational failure analysis, cost attribution and recovery evidence.

Use the [deliverable template](templates/deliverable.md), removing inapplicable fields.
Use [the synthetic scenario](examples/scenario.md) to understand expected behavior,
not as evidence of any actual execution. Check [primary references](references/sources.md)
against the installed product versions before using version-specific commands or APIs.

Distinguish **executed**, **verified**, **not tested** and **blocked**. A proposed command,
a passed formatter, a model-generated verdict, and a real end-to-end test are different
evidence classes. Cite actual files/revisions/results; never promote a template to a result.
