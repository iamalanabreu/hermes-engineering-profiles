# Decision guide: Reliability and Incident Response

These are engineering decisions, not automatic authorization rules.

## Metrics disagree with customer reports
Check telemetry coverage, aggregation, sampling and the affected user segment.

**Why / trade-off:** A global average can hide a severe regional or tenant issue.

## Rollback is low-risk and causally plausible
Propose an early bounded rollback with observed recovery criteria.

**Why / trade-off:** Stabilization may be more valuable than proving every causal detail first.

## Data integrity may be compromised
Escalate and consider an authorized write freeze or containment before retries.

**Why / trade-off:** A successful retry can amplify duplicated or corrupt writes.

## Investigation stops producing new evidence
Summarize hypotheses, stop repeated probes and request the missing access or decision.

**Why / trade-off:** Tool activity is not diagnostic progress.

## Known failure patterns
- Using restart as the first diagnostic step.
- Declaring root cause because the last log line looks suspicious.
- Mixing time zones or observation windows.
- Using synthetic metrics or inferred recovery in a postmortem.

## Stop and escalate
Stop on a changed target, ambiguous data ownership, missing permission, incompatible
contracts, unexplained destructive diff, or exhausted investigation budget. Preserve
partial evidence and name the smallest next action that would unblock the task.
