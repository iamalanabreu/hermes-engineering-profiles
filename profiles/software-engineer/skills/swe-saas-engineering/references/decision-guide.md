# Decision guide: SaaS Product and Tenant Engineering

These are engineering decisions, not automatic authorization rules.

## A feature needs no tenant/commercial model
Do not introduce one merely because the profile supports SaaS.

**Why / trade-off:** Unneeded complexity creates authorization and operational risk.

## A shared cache returns another tenant's object
Fix tenant-aware keys and authorization before release.

**Why / trade-off:** API checks alone do not protect derived data.

## A billing webhook is duplicated or late
Process idempotently and reconcile authoritative state.

**Why / trade-off:** Event transport semantics must not create duplicate charges or entitlements.

## A user changes tenant context
Revalidate membership and invalidate stale authorization/data state.

**Why / trade-off:** A UI switch must not reuse the previous tenant's permissions.

## A deletion request occurs
Trace primary and derived data, backups/retention and legal constraints; do not promise immediate erasure without evidence.

**Why / trade-off:** Deletion is a lifecycle contract, not one database delete.

## Known failure patterns
- Trusting a request header tenant id without membership checks.
- Ignoring jobs, caches and exports in tenant isolation.
- Treating payment success as permanent authorization.
- Testing only one tenant or one role.

## Stop and escalate
Stop on a changed target, ambiguous data ownership, missing permission, incompatible
contracts, unexplained destructive diff, or exhausted investigation budget. Preserve
partial evidence and name the smallest next action that would unblock the task.
