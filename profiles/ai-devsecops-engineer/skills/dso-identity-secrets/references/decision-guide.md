# Decision guide: Identity, Secrets and Credential Lifecycle

These are engineering decisions, not automatic authorization rules.

## Authentication succeeds but operation is denied
Inspect authorization and target resource, not another login loop.

**Why / trade-off:** Valid identity is not permission.

## A rotation must be zero-downtime
Use a verified overlap/switchover design if supported, then revoke only after consumer verification.

**Why / trade-off:** Immediate revocation can break services using cached credentials.

## An identity provider is unavailable
Apply documented emergency access procedures rather than weaken token validation.

**Why / trade-off:** Availability mitigation must not silently remove the trust boundary.

## A secret is committed to Git
Coordinate revoke/rotate and assess use; removal from the latest commit is only one cleanup step.

**Why / trade-off:** History cleanup is not credential invalidation.

## Known failure patterns
- Including raw JWTs or secrets in reports.
- Using wildcard roles as an incident shortcut.
- Rotating before identifying all consumers.
- Treating a masked UI field as proof that logs and subprocess environments are safe.

## Stop and escalate
Stop on a changed target, ambiguous data ownership, missing permission, incompatible
contracts, unexplained destructive diff, or exhausted investigation budget. Preserve
partial evidence and name the smallest next action that would unblock the task.
