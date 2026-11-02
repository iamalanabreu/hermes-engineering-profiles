# Decision guide: Model, Provider and Gateway Routing

These are engineering decisions, not automatic authorization rules.

## A route returns 401/403
Check configuration and entitlement; do not consume retries or switch to an unauthorized provider.

**Why / trade-off:** Retry cannot fix an account-level authorization error.

## Rate limits or transient 5xx occur
Use a bounded retry or an approved equivalent fallback, honoring latency and task budget.

**Why / trade-off:** Unbounded retries amplify outages and cost.

## A fallback lacks required tool/JSON support
Reject it for that task class or adapt through an explicitly tested compatibility layer.

**Why / trade-off:** Silent feature loss can corrupt downstream behavior.

## The cheapest model fails more often
Compare total spend and retries per accepted task at the required quality floor.

**Why / trade-off:** Unit token price does not measure delivered value.

## A provider change crosses a data boundary
Require explicit approval or keep the request blocked.

**Why / trade-off:** Availability does not override confidentiality.

## Known failure patterns
- Hardcoding current prices or model names as enduring facts.
- Logging full prompts and responses by default.
- Mixing gateway 200 responses with upstream semantic failure.
- Retrying an already committed tool side effect.

## Stop and escalate
Stop on a changed target, ambiguous data ownership, missing permission, incompatible
contracts, unexplained destructive diff, or exhausted investigation budget. Preserve
partial evidence and name the smallest next action that would unblock the task.
