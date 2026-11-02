# Verification contract: Evidence-Based Codebase Discovery

Initial state: NOT EXECUTED. These are acceptance criteria, not a historical test report.

## V01 - Source grounding
**Method:** Spot-check each architectural claim against source or observed execution.

**Evidence to retain:** File/line/revision references.

## V02 - Path completeness
**Method:** Trace the requested operation through error and persistence boundaries.

**Evidence to retain:** Call/data-flow map with unknowns.

## V03 - Scope discipline
**Method:** Compare proposed edits against requested scope and pre-existing changes.

**Evidence to retain:** Impact list and preserved-work record.

## V04 - Handoff usability
**Method:** Have a fresh context locate entrypoints and checks from the map.

**Evidence to retain:** Cold-read review or explicit not-tested state.

## Classification and evidence retention
A critical security, data-loss or authorization failure blocks release. An unavailable
integration is NOT TESTED, not PASS. A tool error is a failed attempt unless its output
proves the requested outcome. Record baseline versus changed revision, command or test id,
exit status and redacted results. Do not retain tokens, raw customer payloads or full prompts
when metrics and identifiers suffice. A reviewer may challenge every recorded claim.
