# Decision guide: Cloud Security Architecture and Review

These are engineering decisions, not automatic authorization rules.

## A finding depends on missing evidence
Label confidence and request the smallest read that resolves it.

**Why / trade-off:** An uncertain risk can be important without being a confirmed vulnerability.

## A control breaks a required consumer
Design a least-privilege exception with expiry and observation, not a broad disable.

**Why / trade-off:** Operational continuity and risk reduction must both be evaluated.

## The request asks for compliance
Map evidence to requirements and state review limits; do not certify from a checklist.

**Why / trade-off:** A technical scan does not constitute an organizational audit.

## A secret may have leaked
Do not echo the value. Treat it as potentially compromised and coordinate scoped revocation/rotation.

**Why / trade-off:** Deleting text alone does not revoke an exposed credential.

## Known failure patterns
- Confusing configured controls with effective controls.
- Claiming an attack succeeded from static evidence alone.
- Disabling public access without tracing dependent services.
- Exporting full policy or log payloads that contain personal or secret data.

## Stop and escalate
Stop on a changed target, ambiguous data ownership, missing permission, incompatible
contracts, unexplained destructive diff, or exhausted investigation budget. Preserve
partial evidence and name the smallest next action that would unblock the task.
