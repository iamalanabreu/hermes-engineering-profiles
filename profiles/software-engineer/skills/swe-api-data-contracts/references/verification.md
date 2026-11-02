# Verification contract: API, Persistence and Data Contract Engineering

Initial state: NOT EXECUTED. These are acceptance criteria, not a historical test report.

## V01 - Contract correctness
**Method:** Validate with the applicable schema tooling and run examples through implementation.

**Evidence to retain:** Schema/contract results.

## V02 - Authorization
**Method:** Exercise unauthorized object/tenant and role combinations.

**Evidence to retain:** Negative access tests.

## V03 - Data invariants
**Method:** Test concurrent/duplicate operations and failure between steps.

**Evidence to retain:** Persistence/invariant evidence.

## V04 - Migration compatibility
**Method:** Run old data and consumer cases through upgrade/recovery.

**Evidence to retain:** Migration and backward-compatibility results.

## Classification and evidence retention
A critical security, data-loss or authorization failure blocks release. An unavailable
integration is NOT TESTED, not PASS. A tool error is a failed attempt unless its output
proves the requested outcome. Record baseline versus changed revision, command or test id,
exit status and redacted results. Do not retain tokens, raw customer payloads or full prompts
when metrics and identifiers suffice. A reviewer may challenge every recorded claim.
