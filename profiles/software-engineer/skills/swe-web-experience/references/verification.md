# Verification contract: Accessible, Functional Web Experience

Initial state: NOT EXECUTED. These are acceptance criteria, not a historical test report.

## V01 - Flow completeness
**Method:** Exercise success, invalid, empty, loading, failed and denied states.

**Evidence to retain:** Interaction/test evidence.

## V02 - Accessibility
**Method:** Check keyboard, focus, semantics, contrast and applicable automated/manual requirements.

**Evidence to retain:** Accessibility findings and fixes; no unearned compliance claim.

## V03 - Responsive behavior
**Method:** Test representative narrow/wide layouts and content extremes.

**Evidence to retain:** Viewport evidence.

## V04 - Integration truth
**Method:** Distinguish fixture-backed behavior from real API persistence.

**Evidence to retain:** Data-source and E2E qualification record.

## Classification and evidence retention
A critical security, data-loss or authorization failure blocks release. An unavailable
integration is NOT TESTED, not PASS. A tool error is a failed attempt unless its output
proves the requested outcome. Record baseline versus changed revision, command or test id,
exit status and redacted results. Do not retain tokens, raw customer payloads or full prompts
when metrics and identifiers suffice. A reviewer may challenge every recorded claim.
