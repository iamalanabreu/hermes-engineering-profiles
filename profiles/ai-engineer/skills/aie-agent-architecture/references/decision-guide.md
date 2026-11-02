# Decision guide: Agent System Architecture

These are engineering decisions, not automatic authorization rules.

## The workflow is deterministic
Use a script or service function; let the agent select or explain it only where judgment is required.

**Why / trade-off:** Fewer probabilistic transitions make correctness and cost easier to control.

## One context grows too large
Improve retrieval/context packaging before adding a fleet. Delegate only independent bounded tasks with adequate handoff.

**Why / trade-off:** More agents can hide poor information architecture and multiply cost.

## A delegated task can mutate state
Verify inherited tools, target credentials and approval behavior on the chosen runtime.

**Why / trade-off:** A new role identity does not prove reduced privileges.

## An external action times out
Determine whether it committed before retrying; use an idempotency or operation-status mechanism if supported.

**Why / trade-off:** Transport failure and action failure are not the same.

## Human approval is unavailable
Fail closed or produce a non-mutating proposal for material actions.

**Why / trade-off:** Unattended operation is not implied authority.

## Known failure patterns
- Adding an orchestrator before defining a task contract.
- Persisting secrets or client facts in a generic profile.
- Using a model-generated success summary as the only completion signal.
- Making every error retryable or every task autonomous.

## Stop and escalate
Stop on a changed target, ambiguous data ownership, missing permission, incompatible
contracts, unexplained destructive diff, or exhausted investigation budget. Preserve
partial evidence and name the smallest next action that would unblock the task.
