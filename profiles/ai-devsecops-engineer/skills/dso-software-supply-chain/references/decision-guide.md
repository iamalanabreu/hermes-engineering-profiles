# Decision guide: Secure Build and Release Supply Chain

These are engineering decisions, not automatic authorization rules.

## A dependency has a vulnerability finding
Assess reachability, severity, exploit prerequisites and remediation availability without dismissing the finding by popularity.

**Why / trade-off:** A scanner label needs context, but uncertainty cannot become silent acceptance.

## Untrusted pull requests run CI
Separate read-only validation from privileged publish/sign/deploy jobs.

**Why / trade-off:** Pipeline code can be a credential execution path.

## An artifact is rebuilt for promotion
Compare inputs and digests; prefer promotion of the already verified output.

**Why / trade-off:** A second build may not be the artifact that passed the checks.

## A scanner is unavailable
Block the gate if required; otherwise report an explicit exception and owner decision.

**Why / trade-off:** No scan result is not a negative result.

## Known failure patterns
- Mutable references in privileged pipelines.
- Signing an artifact without verifying its source and build identity.
- Treating an SBOM as proof of vulnerability absence.
- Publishing because local unit tests passed while mandatory gates were skipped.

## Stop and escalate
Stop on a changed target, ambiguous data ownership, missing permission, incompatible
contracts, unexplained destructive diff, or exhausted investigation budget. Preserve
partial evidence and name the smallest next action that would unblock the task.
