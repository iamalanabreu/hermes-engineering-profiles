# Decision guide: Agent Evaluation and Regression Engineering

These are engineering decisions, not automatic authorization rules.

## Only a handful of happy-path cases exist
Treat the results as exploratory; add negative and boundary cases before release claims.

**Why / trade-off:** Small convenient samples do not establish robustness.

## The judge approves a forbidden action
Make permission/security checks deterministic and blocking where possible.

**Why / trade-off:** A subjective quality score must not overrule an invariant.

## Mock integration passes
Label it contract-only and schedule an authorized integration test.

**Why / trade-off:** The real provider may differ in auth, streaming, latency or side effects.

## The candidate is cheaper but less reliable
Compare cost per accepted task and failure consequences against the agreed floor.

**Why / trade-off:** Savings can be erased by retries and manual repair.

## No live model was called
Report static/deterministic validation only.

**Why / trade-off:** A populated dataset is not an executed model evaluation.

## Known failure patterns
- Claiming accuracy without a defined dataset and denominator.
- Scoring missing results as successes.
- Using the candidate itself as the only judge.
- Tuning repeatedly on the supposed held-out suite.
- Treating a benchmark score as proof of permissions or production integration.

## Stop and escalate
Stop on a changed target, ambiguous data ownership, missing permission, incompatible
contracts, unexplained destructive diff, or exhausted investigation budget. Preserve
partial evidence and name the smallest next action that would unblock the task.
