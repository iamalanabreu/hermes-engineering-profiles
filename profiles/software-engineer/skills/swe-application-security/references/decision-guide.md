# Decision guide: Secure Application Engineering

These are engineering decisions, not automatic authorization rules.

## The UI hides a privileged button
Still enforce authorization server-side or at the actual trusted operation.

**Why / trade-off:** Presentation is not a security boundary.

## A token is valid
Check action/resource/tenant authorization independently.

**Why / trade-off:** Authentication proves identity, not permission.

## A scanner flags a candidate issue
Trace exploit prerequisites and impact without dismissing or overstating it.

**Why / trade-off:** Tool results are evidence inputs, not final certification.

## An exposed secret is removed from code
Coordinate revoke/rotate and review history/log exposure; deletion alone is insufficient.

**Why / trade-off:** The old value can remain usable.

## A local app loads untrusted content
Constrain process/IPC/file capabilities and test the boundary.

**Why / trade-off:** Running on a personal device does not make content trustworthy.

## Known failure patterns
- Trusting client-supplied roles or tenant ids.
- Logging raw secrets or personal payloads.
- Writing custom security-sensitive primitives unnecessarily.
- Patching one endpoint while leaving an equivalent path unchecked.

## Stop and escalate
Stop on a changed target, ambiguous data ownership, missing permission, incompatible
contracts, unexplained destructive diff, or exhausted investigation budget. Preserve
partial evidence and name the smallest next action that would unblock the task.
