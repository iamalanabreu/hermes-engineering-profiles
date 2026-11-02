---
name: swe-architecture-design
description: "Design application boundaries, contracts and data flows from requirements and quality attributes. Use for new products or consequential refactors; do not impose microservices, DDD or a framework without evidence."
---
# Pragmatic Software Architecture

## Mission and boundaries
Choose the smallest architecture that meets the actual product and operational
constraints. Preserve a viable existing design; optimize for changeability and failure
understanding rather than fashionable patterns or hypothetical scale.

## Establish the inputs
- Business outcome, users, workflows, constraints, non-goals and acceptance criteria.
- Existing architecture/code or a clear greenfield declaration.
- Data sensitivity, consistency/availability needs, deployment model, team capacity and budget.
- Known integrations, expected workload evidence, migration and backward-compatibility requirements.

Missing information is not permission to invent a stack, a result, an environment or
an approval. Read the authorized project's instructions and source-of-truth index.
Use project-context-architect only when contextual structure is actually missing;
use agent-folder-architect only for a justified recurring capability, not this task by default.

## Execution procedure

### 1. Discover the domain and invariants
Describe core workflows, entities, lifecycle states and rules that must always hold. Separate confirmed workload needs from guesses. Identify irreversible operations and data ownership.

**Completion evidence:** Domain/workflow model with invariants and explicit assumptions.

### 2. Define quality requirements
Turn vague terms such as scalable, fast and secure into scenario-based acceptance: stimulus, environment, expected response and measure. Use provisional targets only when clearly labeled and approved.

**Completion evidence:** Quality scenarios and trade-off priorities.

### 3. Compare viable shapes
Consider the current architecture and the simplest coherent alternative. Evaluate a modular single deployable before distributed services for a new bounded product unless independent scaling, ownership or failure isolation justifies distribution.

**Completion evidence:** A small alternatives table with concrete benefits, costs and rejected options.

### 4. Specify boundaries and contracts
Define dependency direction, interfaces, data ownership, transaction boundaries, authentication/authorization, failure handling and observability. Do not add an abstraction with no consumer or plausible change boundary.

**Completion evidence:** Component/contract/data-flow design with error paths.

### 5. Validate uncertainty with a spike
Choose the highest-risk assumption and a bounded throwaway experiment. Separate exploratory code from production implementation. Record what the experiment did and did not demonstrate.

**Completion evidence:** Spike result or an explicit reason a spike was unnecessary.

### 6. Plan incremental delivery
Create a thin end-to-end slice, migration/compatibility steps and decision records for consequential choices. Define how architecture will be revisited using evidence.

**Completion evidence:** Implementable plan with acceptance, recovery and decision provenance.

## Decision points and deeper reference
Read [the decision guide](references/decision-guide.md) before selecting a materially
different path. Load only the needed reference; do not dump the complete library into context.
Read [the verification contract](references/verification.md) before claiming completion.

## Authority and failure boundary
Architecture advice is not permission to migrate, provision or rewrite. Resolve
material stack and data-boundary choices explicitly. Use official versioned docs for
capabilities; do not invent product features or performance guarantees.

## Recovery
Keep the prior design decision and a migration escape path where feasible. If a spike
invalidates an assumption, revise the design before broad implementation. Revert source
only where data/contracts remain compatible.

## Delivery
Deliver requirements/invariants, quality scenarios, chosen architecture with rejected
alternatives, interface/data/failure contracts and an incremental validation plan.

Use the [deliverable template](templates/deliverable.md), removing inapplicable fields.
Use [the synthetic scenario](examples/scenario.md) to understand expected behavior,
not as evidence of any actual execution. Check [primary references](references/sources.md)
against the installed product versions before using version-specific commands or APIs.

Distinguish **executed**, **verified**, **not tested** and **blocked**. A proposed command,
a passed formatter, a model-generated verdict, and a real end-to-end test are different
evidence classes. Cite actual files/revisions/results; never promote a template to a result.
