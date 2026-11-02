# Decision guide: Pragmatic Software Architecture

These are engineering decisions, not automatic authorization rules.

## A team requests microservices for a small product
Ask which independent scaling, ownership or failure boundary requires them; otherwise recommend a simpler modular deployable.

**Why / trade-off:** Distributed transactions, deployment and debugging have real operational cost.

## An existing system is imperfect but viable
Prefer an incremental boundary improvement with characterization tests over a rewrite.

**Why / trade-off:** A rewrite loses undocumented behavior and expands delivery risk.

## Requirements conflict
Make the trade-off explicit and obtain a product/operational decision.

**Why / trade-off:** Architecture cannot silently satisfy mutually incompatible goals.

## A pattern is proposed without a use case
Keep direct code until a real boundary or repeated requirement supports abstraction.

**Why / trade-off:** Abstraction is a maintenance commitment, not a maturity badge.

## Known failure patterns
- Inventing throughput targets to justify complexity.
- Writing ADRs for decisions nobody made.
- Choosing technologies before data and deployment constraints.
- Describing only happy-path component boxes.

## Stop and escalate
Stop on a changed target, ambiguous data ownership, missing permission, incompatible
contracts, unexplained destructive diff, or exhausted investigation budget. Preserve
partial evidence and name the smallest next action that would unblock the task.
