# Decision guide: Infrastructure Change Engineering

These are engineering decisions, not automatic authorization rules.

## Plan proposes delete or replacement
Pause for data ownership, preservation strategy and consumer impact. A replacement can be destructive even with create-before-destroy.

**Why / trade-off:** Ordering does not guarantee service or data continuity.

## Drift is detected
Determine whether drift is an authorized emergency fix, stale desired state or unauthorized mutation before reconciling.

**Why / trade-off:** Blind reconciliation can remove an intentional mitigation.

## The target is ambiguous
Resolve account/project/region/workspace and permission before any material operation.

**Why / trade-off:** A correct command against the wrong account is still a failed change.

## Recovery requires data transformation
Design a forward repair or tested restore with explicit recovery point; do not promise that a Git revert restores data.

**Why / trade-off:** Infrastructure reversibility and data reversibility differ.

## A large change is presented as one apply
Split independent changes and prove ordering when practical; retain one coherent transition when splitting itself is unsafe.

**Why / trade-off:** Small scope improves attribution, but an inconsistent intermediate state can be worse.

## Known failure patterns
- Using plan output as a secret-free artifact; it can contain sensitive values.
- Applying a stale plan after a configuration, state or permission change.
- Disabling a state lock, increasing permissions or using destructive flags to get past an unexplained failure.
- Assuming a lower recurring price offsets interruption, migration or egress cost.

## Stop and escalate
Stop on a changed target, ambiguous data ownership, missing permission, incompatible
contracts, unexplained destructive diff, or exhausted investigation budget. Preserve
partial evidence and name the smallest next action that would unblock the task.
