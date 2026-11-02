---
name: aie-agent-security
description: "Threat-model and harden agents, MCP tools and LLM applications against tool abuse, prompt injection and data leakage. Use before adding sensitive tools or autonomous execution; testing remains within explicit authorized scope."
---
# Security of Tool-Using Agents

## Mission and boundaries
Own defense-in-depth for agentic behavior. Prompts and content scanners are guidance
and detection, not a complete enforcement boundary. Separate the model's suggestion,
the tool broker's authorization and the underlying service permissions.

## Establish the inputs
- Assets, identities, entrypoints, data classes, external services and tool side effects.
- Actual runtime/tool schemas, terminal backend, MCP trust configuration and permissions.
- Approved adversarial test scope, synthetic data, network boundaries and recovery plan.
- Human approval and audit requirements, unattended execution policy and budget limits.

Missing information is not permission to invent a stack, a result, an environment or
an approval. Read the authorized project's instructions and source-of-truth index.
Use project-context-architect only when contextual structure is actually missing;
use agent-folder-architect only for a justified recurring capability, not this task by default.

## Execution procedure

### 1. Map the attack surface
Trace untrusted inputs through prompts, retrieval, memory, tools, plugins and outputs. Include supply-chain updates, persistent instructions, cross-agent handoffs and credential inheritance.

**Completion evidence:** Threat model with trust crossings and concrete protected outcomes.

### 2. Enforce authority outside the model
Use service-side IAM, scoped credentials, tool allowlists, validated arguments and controlled execution contexts. Define which actions need human approval and what actually enforces it. Do not claim a profile folder or prompt prevents filesystem access.

**Completion evidence:** Permission/enforcement matrix separating instruction, runtime checks and OS/service controls.

### 3. Constrain data and tools
Limit readable/writable roots and egress where the environment supports enforcement. Validate tool schemas and remote URLs, classify read versus mutation, minimize secrets/PII exposure and retention. Review MCP configuration and dependencies before enabling.

**Completion evidence:** Tool/data policy with explicit capabilities and installation provenance.

### 4. Test realistic adversarial paths
Use synthetic fixtures for instruction spoofing, retrieved injection, unauthorized tool calls, argument abuse, cross-tenant recall and repeated side effects. Observe actual tool behavior rather than just final refusal wording.

**Completion evidence:** Adversarial case results with redacted traces and observed enforcement points.

### 5. Harden without breaking the task
Prioritize controls by reachable harm and verify legitimate workflows still work. Check failure behavior when approvals, secret sources, scanners or authorization services are unavailable.

**Completion evidence:** Allowed/denied behavior matrix and bounded degradation policy.

### 6. Review changes and retain evidence
Version tools, prompts, permissions and dependencies together in the evaluation record. Require review for new side-effect capabilities. Record residual exposure and what the test suite did not cover.

**Completion evidence:** Security decision tied to exact versions and executed checks.

## Decision points and deeper reference
Read [the decision guide](references/decision-guide.md) before selecting a materially
different path. Load only the needed reference; do not dump the complete library into context.
Read [the verification contract](references/verification.md) before claiming completion.

## Authority and failure boundary
No tests against third-party systems without authorization. Use synthetic fixtures.
No new plugin, credential, egress route, tool permission or unattended automation is
enabled solely by this skill. Report the limits of in-process enforcement honestly.

## Recovery
Disable the affected capability through the approved control plane, preserve evidence
and revoke exposed credentials when authorized. Re-test the actual boundary; do not
re-enable based only on a revised prompt or a static scan.

## Delivery
Deliver threat model, authority/data/tool matrix, adversarial test evidence,
remediation priorities and residual risk with clear enforcement limitations.

Use the [deliverable template](templates/deliverable.md), removing inapplicable fields.
Use [the synthetic scenario](examples/scenario.md) to understand expected behavior,
not as evidence of any actual execution. Check [primary references](references/sources.md)
against the installed product versions before using version-specific commands or APIs.

Distinguish **executed**, **verified**, **not tested** and **blocked**. A proposed command,
a passed formatter, a model-generated verdict, and a real end-to-end test are different
evidence classes. Cite actual files/revisions/results; never promote a template to a result.
