# Verification contract: Infrastructure Change Engineering

Initial state: NOT EXECUTED. These are acceptance criteria, not a historical test report.

## V01 - Target binding
**Method:** Compare account/project/workspace and resource scope with the approved request.

**Evidence to retain:** Redacted identity and target identifiers.

## V02 - Plan completeness
**Method:** Review every action, unknown/sensitive field and replacement; exercise the supplied plan-summary helper on a fixture.

**Evidence to retain:** Plan digest and per-resource action summary.

## V03 - Recovery feasibility
**Method:** Test the recovery path in an isolated equivalent or state exactly what was not tested.

**Evidence to retain:** Restore/revert result or explicit limitation.

## V04 - Behavioral acceptance
**Method:** Run agreed service and policy checks after the change, not only IaC validation.

**Evidence to retain:** Metrics/health/authorization results with window and revision.

## Classification and evidence retention
A critical security, data-loss or authorization failure blocks release. An unavailable
integration is NOT TESTED, not PASS. A tool error is a failed attempt unless its output
proves the requested outcome. Record baseline versus changed revision, command or test id,
exit status and redacted results. Do not retain tokens, raw customer payloads or full prompts
when metrics and identifiers suffice. A reviewer may challenge every recorded claim.
