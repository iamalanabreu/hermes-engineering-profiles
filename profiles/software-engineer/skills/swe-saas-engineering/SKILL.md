---
name: swe-saas-engineering
description: "Design or implement SaaS capabilities with tenant isolation, authorization, lifecycle and commercial rules when required. Use for multi-tenant products, entitlements and billing; do not add tenancy or subscriptions to every application."
---
# SaaS Product and Tenant Engineering

## Mission and boundaries
Own SaaS application behavior and its tenant/data/commercial invariants. Separate
tenancy, authentication, authorization, entitlements, usage metering and billing.
Build only capabilities required by the product, not an automatic SaaS checklist.

## Establish the inputs
- Product workflows, tenant model, user/role relationships and data ownership.
- Commercial rules when applicable: plans, quotas, trials, cancellations, metering and billing authority.
- Async/webhook integrations, audit requirements, lifecycle and deletion/retention.
- Authorized synthetic tenants/accounts, acceptance scenarios and supported deployment model.

Missing information is not permission to invent a stack, a result, an environment or
an approval. Read the authorized project's instructions and source-of-truth index.
Use project-context-architect only when contextual structure is actually missing;
use agent-folder-architect only for a justified recurring capability, not this task by default.

## Execution procedure

### 1. Model tenant and product boundaries
Define tenant identity, membership, roles, resource ownership and cross-tenant administrative cases. Decide shared versus isolated storage based on actual risk and operations.

**Completion evidence:** Tenant/data/permission model with explicit exceptions.

### 2. Define lifecycle and entitlements
Specify invite/join/remove, activation/suspension, plan change and deletion flows. Separate a payment event from the authoritative entitlement state. Keep commercial features out of products that do not need them.

**Completion evidence:** State transitions and entitlement/usage rules.

### 3. Implement server-side isolation
Bind queries, writes, caches, files, jobs and exports to validated tenant context. Check authorization at the trusted resource operation. Include background tasks and administrative paths, not just HTTP handlers.

**Completion evidence:** Isolation implementation across all relevant storage/execution paths.

### 4. Handle async and billing semantics
Verify event authenticity, deduplicate, handle order/late delivery, retries and reconciliation. Do not assume exactly-once callbacks or use client state as billing truth. Keep provider-specific API behavior verified against docs.

**Completion evidence:** Idempotent workflow and reconciliation tests with synthetic events.

### 5. Verify lifecycle and business outcomes
Run two-tenant negative tests, role/ownership matrix, quota boundaries, suspension, deletion and recovery cases. Evaluate auditability and customer-facing failure behavior.

**Completion evidence:** Tenant/lifecycle/billing acceptance record and residual risks.

## Decision points and deeper reference
Read [the decision guide](references/decision-guide.md) before selecting a materially
different path. Load only the needed reference; do not dump the complete library into context.
Read [the verification contract](references/verification.md) before claiming completion.

## Authority and failure boundary
Do not charge cards, change live subscriptions, export customer data or modify tenant
permissions without authorization. Use test-mode providers and synthetic tenants; never
present a test payment as a live business result.

## Recovery
Contain cross-tenant exposure or billing inconsistency, preserve redacted evidence
and reconcile authoritative state. Compensating commercial actions require approval;
source rollback alone may not undo charges, events or exported data.

## Delivery
Deliver tenant/data/permission model, lifecycle and entitlement rules, implementation,
cross-tenant and async tests, reconciliation/recovery plan and remaining gaps.

Use the [deliverable template](templates/deliverable.md), removing inapplicable fields.
Use [the synthetic scenario](examples/scenario.md) to understand expected behavior,
not as evidence of any actual execution. Check [primary references](references/sources.md)
against the installed product versions before using version-specific commands or APIs.

Distinguish **executed**, **verified**, **not tested** and **blocked**. A proposed command,
a passed formatter, a model-generated verdict, and a real end-to-end test are different
evidence classes. Cite actual files/revisions/results; never promote a template to a result.
