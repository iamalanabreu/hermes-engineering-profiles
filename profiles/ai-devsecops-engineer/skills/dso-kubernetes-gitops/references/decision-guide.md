# Decision guide: Kubernetes and GitOps Operations

These are engineering decisions, not automatic authorization rules.

## Healthy and OutOfSync
Inspect drift origin; do not automatically sync merely to make the dashboard green.

**Why / trade-off:** Manual mitigations and mutating controllers can explain the mismatch.

## Degraded and OutOfSync
Prioritize impact and recoverability; a sync can help or worsen the incident depending on the desired revision.

**Why / trade-off:** Desired state is not necessarily healthy state.

## A stateful workload is failing
Check volume ownership, retention, snapshots and attach/mount events before any deletion.

**Why / trade-off:** Deleting a workload or volume can turn an availability issue into data loss.

## Admission blocks the change
Read the exact policy and failed field; propose a compliant change or an approved narrow exception.

**Why / trade-off:** Weakening admission globally amplifies risk beyond this workload.

## Capacity appears insufficient
Differentiate quota, scheduler constraints, requests/limits and physical capacity before scaling.

**Why / trade-off:** More nodes do not fix incompatible placement or unbound storage.

## Known failure patterns
- Treating a restart as a diagnosis.
- Ignoring all differences or disabling reconciliation to silence alerts.
- Using deprecated policy APIs from a copied example without verifying the cluster version.
- Concluding network policy works without checking the installed network implementation and traffic tests.

## Stop and escalate
Stop on a changed target, ambiguous data ownership, missing permission, incompatible
contracts, unexplained destructive diff, or exhausted investigation budget. Preserve
partial evidence and name the smallest next action that would unblock the task.
