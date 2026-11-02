# Decision guide: End-to-End Feature Delivery

These are engineering decisions, not automatic authorization rules.

## Only one layer is available
Implement the bounded contract and clearly mark the unavailable integration; do not pretend an end-to-end feature exists.

**Why / trade-off:** A mock UI or API stub cannot prove full workflow success.

## The test suite is already failing
Record baseline failures and isolate which failures your change introduces or fixes.

**Why / trade-off:** A red baseline must not hide a new regression or force unrelated repairs.

## A dependency must change
Justify necessity, compatibility, license and supply-chain impact before adding it.

**Why / trade-off:** Convenience imports create lifecycle obligations.

## A simple bug suggests a broad refactor
Deliver the minimal correct fix with tests; propose the refactor separately if useful.

**Why / trade-off:** Large diffs make causality and review harder.

## Known failure patterns
- Leaving buttons, endpoints or persistence as fake behavior while calling the feature done.
- Using git add -A in a workspace with unrelated changes.
- Editing tests to accept wrong behavior.
- Making a live production call during a local feature test without approval.

## Stop and escalate
Stop on a changed target, ambiguous data ownership, missing permission, incompatible
contracts, unexplained destructive diff, or exhausted investigation budget. Preserve
partial evidence and name the smallest next action that would unblock the task.
