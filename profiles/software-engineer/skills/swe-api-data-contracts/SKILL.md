---
name: swe-api-data-contracts
description: "Design or evolve API and persistence contracts with validation, authorization, consistency and migration safety. Use for endpoints, schemas, integrations and data changes; do not assume a source rollback reverses data."
---
# API, Persistence and Data Contract Engineering

## Mission and boundaries
Own observable application contracts and data invariants. Treat consumers, stored
records and asynchronous messages as compatibility obligations. Choose REST, RPC,
events and storage technology according to the existing system and requirements.

## Establish the inputs
- Consumers, operations, entities, invariants, errors and permission boundaries.
- Existing API/schema/event contracts, revisions, integration behavior and supported clients.
- Consistency/transaction requirements, concurrency, idempotency and retention constraints.
- Data migration scope, representative fixtures, backup/recovery and authorized environment.

Missing information is not permission to invent a stack, a result, an environment or
an approval. Read the authorized project's instructions and source-of-truth index.
Use project-context-architect only when contextual structure is actually missing;
use agent-folder-architect only for a justified recurring capability, not this task by default.

## Execution procedure

### 1. Inventory contracts and consumers
Trace request/response schemas, validation, auth, persistence and downstream events. Identify compatibility-sensitive fields and versions. Do not infer absence of consumers from absence of local references.

**Completion evidence:** Consumer/contract map with unknowns and source revision.

### 2. Specify semantics before implementation
Define required/optional fields, types, pagination, errors, idempotency, concurrency and authorization at the resource level. Validate schemas with a real supported tool when available; a JSON parse is not OpenAPI validation.

**Completion evidence:** Contract with positive, boundary and negative examples.

### 3. Design consistency and migration
Choose transaction boundaries and race handling. For changes to existing data, plan expand/migrate/contract or another justified sequence, backfill bounds and compatibility windows. Test on representative sanitized fixtures.

**Completion evidence:** Migration plan including old/new coexistence and recovery limits.

### 4. Implement the trusted boundary
Validate inputs, enforce ownership/tenant scope, use parameterized data access and avoid leaking internal error detail. Handle retries and duplicate events without multiplying writes. Keep domain invariants independent of UI.

**Completion evidence:** Contract-compliant code and persistence tests.

### 5. Test behavior under change
Exercise invalid input, denied access, duplicate/concurrent requests, old clients, missing dependencies and migration failure. Inspect query plans or latency only when performance requires it.

**Completion evidence:** Contract/integration/migration results and compatibility decision.

## Decision points and deeper reference
Read [the decision guide](references/decision-guide.md) before selecting a materially
different path. Load only the needed reference; do not dump the complete library into context.
Read [the verification contract](references/verification.md) before claiming completion.

## Authority and failure boundary
Live schema changes, backfills, deletions and partner API calls require explicit
authorization and data handling. Do not run migrations against a guessed connection
string. Protect fixture data and avoid exporting real records unnecessarily.

## Recovery
Pause writes/backfill when invariants fail. Use the approved checkpoint, restore or
forward repair based on actual data semantics. Keep compatibility during recovery;
never assume a down migration can recreate discarded information.

## Delivery
Deliver consumer/contracts, data invariants, implementation/migration plan,
negative and compatibility tests, and realistic recovery limits.

Use the [deliverable template](templates/deliverable.md), removing inapplicable fields.
Use [the synthetic scenario](examples/scenario.md) to understand expected behavior,
not as evidence of any actual execution. Check [primary references](references/sources.md)
against the installed product versions before using version-specific commands or APIs.

Distinguish **executed**, **verified**, **not tested** and **blocked**. A proposed command,
a passed formatter, a model-generated verdict, and a real end-to-end test are different
evidence classes. Cite actual files/revisions/results; never promote a template to a result.
