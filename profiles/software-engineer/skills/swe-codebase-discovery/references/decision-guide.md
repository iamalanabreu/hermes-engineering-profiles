# Decision guide: Evidence-Based Codebase Discovery

These are engineering decisions, not automatic authorization rules.

## Documentation and code disagree
Show both and inspect active wiring or runtime evidence before deciding which is current.

**Why / trade-off:** Documentation can be stale; code can be dead or feature-gated.

## A repository contains several applications
Identify the one in scope and shared dependencies rather than selecting the first package.json.

**Why / trade-off:** A monorepo root is not necessarily the runnable product.

## The workspace contains uncommitted work
Record and preserve it; isolate your change or obtain a decision before conflicting edits.

**Why / trade-off:** A clean implementation must not erase another contributor's work.

## The project cannot be run safely
Complete a static map and label runtime assumptions as not tested.

**Why / trade-off:** Unknown runtime behavior is preferable to executing untrusted initialization.

## Known failure patterns
- Inventing architecture from directory names.
- Running install/build scripts before checking trust.
- Treating LOC or dependency count as a quality score.
- Reading all secrets/configuration files to infer environment.

## Stop and escalate
Stop on a changed target, ambiguous data ownership, missing permission, incompatible
contracts, unexplained destructive diff, or exhausted investigation budget. Preserve
partial evidence and name the smallest next action that would unblock the task.
