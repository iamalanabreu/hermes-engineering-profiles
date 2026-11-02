# Decision guide: Security of Tool-Using Agents

These are engineering decisions, not automatic authorization rules.

## A prompt says ignore policy
Treat it as untrusted content; keep authority in configured enforcement.

**Why / trade-off:** The model may follow instructions imperfectly; external controls must still hold.

## An approval control is unavailable
Fail closed for material actions and return a non-mutating proposal.

**Why / trade-off:** Lack of an interactive channel is not consent.

## A plugin requests broad capability
Evaluate necessity, source, code behavior and actual permission boundary before installation.

**Why / trade-off:** Catalog presence alone is not a trust or quality guarantee.

## A local process shares credentials
Reduce available credentials or move execution to an appropriate isolated context; test effective inheritance.

**Why / trade-off:** Profile separation does not automatically isolate the operating system.

## An attack test succeeds
Stop affected execution, preserve redacted evidence and remediate the boundary before rerunning.

**Why / trade-off:** A better refusal prompt alone may not close the action path.

## Known failure patterns
- Relying on regex injection detection as a proof of safety.
- Forwarding every environment variable into a sandbox.
- Equating a denied final answer with no forbidden tool execution.
- Using real customer secrets in adversarial fixtures.

## Stop and escalate
Stop on a changed target, ambiguous data ownership, missing permission, incompatible
contracts, unexplained destructive diff, or exhausted investigation budget. Preserve
partial evidence and name the smallest next action that would unblock the task.
