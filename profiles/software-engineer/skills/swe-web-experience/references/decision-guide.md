# Decision guide: Accessible, Functional Web Experience

These are engineering decisions, not automatic authorization rules.

## The API is not available
Use an explicitly labeled fixture and retain the integration gate.

**Why / trade-off:** A mock display is not end-to-end acceptance.

## Visual requirements conflict with accessibility
Offer an accessible implementation or document the trade-off for decision.

**Why / trade-off:** Aesthetic preference does not remove interaction requirements.

## The project already has a component system
Reuse it unless a demonstrated gap justifies extension.

**Why / trade-off:** Inconsistent design systems multiply maintenance and accessibility risk.

## A state race overwrites fresh data
Fix request ownership/cancellation or stale-result handling.

**Why / trade-off:** A successful network response can still update the wrong UI state.

## Known failure patterns
- Placeholder buttons or fake success notifications.
- Mouse-only acceptance testing.
- Removing labels/focus indicators for visual neatness.
- Declaring responsive support from a single screenshot.
- Trusting client-side role checks as authorization.

## Stop and escalate
Stop on a changed target, ambiguous data ownership, missing permission, incompatible
contracts, unexplained destructive diff, or exhausted investigation budget. Preserve
partial evidence and name the smallest next action that would unblock the task.
