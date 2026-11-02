# Decision guide: Software Verification and Review

These are engineering decisions, not automatic authorization rules.

## Coverage is high but behavior is untested
Inspect assertions and mutation/fault sensitivity rather than trusting the percentage.

**Why / trade-off:** Executed lines are not necessarily validated outcomes.

## Tests are flaky
Reproduce with controlled runs and investigate timing/state isolation; do not hide flakiness with unbounded retries.

**Why / trade-off:** Retries can convert nondeterministic failure into misleading green status.

## No real integration is available
Run contract/fake tests and clearly retain an integration gate.

**Why / trade-off:** Mocks validate your assumptions, not the provider.

## The reviewer cannot parse or inspect the diff
Return blocked or incomplete review, not approval.

**Why / trade-off:** A review without the artifact is not evidence.

## A one-line change affects authorization
Apply risk-based depth despite small diff size.

**Why / trade-off:** Impact is not proportional to line count.

## Known failure patterns
- Reporting tests that were only written, not run.
- Ignoring skipped or unavailable checks.
- Calling a self-review independent.
- Marking a release green when a required security test was omitted.

## Stop and escalate
Stop on a changed target, ambiguous data ownership, missing permission, incompatible
contracts, unexplained destructive diff, or exhausted investigation budget. Preserve
partial evidence and name the smallest next action that would unblock the task.
