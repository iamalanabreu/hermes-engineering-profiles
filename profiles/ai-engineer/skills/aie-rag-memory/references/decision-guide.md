# Decision guide: Retrieval, Knowledge and Memory Engineering

These are engineering decisions, not automatic authorization rules.

## Relevant context is missing
Inspect ingestion, filters, chunking and retrieval before changing the system prompt.

**Why / trade-off:** Generation cannot recover evidence it never received.

## A user asks about another tenant
Reject retrieval before documents enter the model context.

**Why / trade-off:** Output redaction is not a substitute for authorization.

## Sources conflict
Preserve source versions and authority, explain the contradiction and seek resolution.

**Why / trade-off:** Blending conflicting evidence produces unsupported certainty.

## The source is deleted or access revoked
Invalidate derived chunks, caches and recall as required by policy.

**Why / trade-off:** Deleting only the original document leaves derived exposure.

## The task is not evidence-backed
Abstain or provide an explicitly labeled hypothesis.

**Why / trade-off:** Retrieval similarity is not truth.

## Known failure patterns
- Sharing a semantic cache across tenants without authorization-aware keys.
- Measuring answer fluency while ignoring retrieval recall and permissions.
- Storing client secrets or ephemeral task details as permanent generic memory.
- Showing citations that reference old or inaccessible source revisions.

## Stop and escalate
Stop on a changed target, ambiguous data ownership, missing permission, incompatible
contracts, unexplained destructive diff, or exhausted investigation budget. Preserve
partial evidence and name the smallest next action that would unblock the task.
