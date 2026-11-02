# Decision guide: Software Release and Sustainable Maintenance

These are engineering decisions, not automatic authorization rules.

## A refactor expands beyond the request
Split it or obtain a decision; keep the minimum safe change.

**Why / trade-off:** Maintenance should reduce future cost without obscuring current intent.

## A dependency upgrade changes behavior
Test impacted APIs and runtime assumptions, not just lockfile syntax.

**Why / trade-off:** SemVer and release notes are inputs, not integration proof.

## Only one OS was tested
Publish the scope of evidence and keep other platform gates open.

**Why / trade-off:** Cross-platform source does not prove cross-platform packaging.

## A release includes data migration
Bind recovery to schema/data compatibility and backup state.

**Why / trade-off:** A source tag alone cannot restore transformed data.

## Known failure patterns
- Publishing because the package was created.
- Committing unrelated files with broad staging.
- Assuming checkpoints replace Git or backups.
- Calling a skipped signing/notarization step successful.
- Editing dependency versions without regeneration/review of lockfiles.

## Stop and escalate
Stop on a changed target, ambiguous data ownership, missing permission, incompatible
contracts, unexplained destructive diff, or exhausted investigation budget. Preserve
partial evidence and name the smallest next action that would unblock the task.
