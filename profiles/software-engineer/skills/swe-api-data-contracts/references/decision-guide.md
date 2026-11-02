# Decision guide: API, Persistence and Data Contract Engineering

These are engineering decisions, not automatic authorization rules.

## An API change removes or changes a field
Identify consumer impact and version/deprecation strategy before shipping.

**Why / trade-off:** Compilation in one repository does not prove external compatibility.

## A webhook can be delivered twice
Use a verified authenticity check and idempotent processing tied to event/operation identity.

**Why / trade-off:** Exactly-once delivery should not be assumed.

## A migration rewrites large data
Bound batches, monitor locks/load and define restartable progress plus failure recovery.

**Why / trade-off:** A valid schema change can still cause prolonged outage or corruption.

## A client supplies tenant or owner ids
Bind authorization to authenticated context and validate ownership server-side.

**Why / trade-off:** Client-supplied identifiers are not authority.

## Rollback cannot restore lost data
Prefer a forward-compatible or restore-based plan with an explicit recovery point.

**Why / trade-off:** Down migrations are not universally safe.

## Known failure patterns
- Breaking contracts without consumer inventory.
- Testing migrations only on an empty database.
- Adding unbounded list endpoints.
- Using retries without idempotency or concurrency semantics.
- Equating valid JSON with valid API schema.

## Stop and escalate
Stop on a changed target, ambiguous data ownership, missing permission, incompatible
contracts, unexplained destructive diff, or exhausted investigation budget. Preserve
partial evidence and name the smallest next action that would unblock the task.
