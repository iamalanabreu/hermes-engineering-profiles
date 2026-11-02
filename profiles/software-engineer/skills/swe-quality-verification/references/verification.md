# Verification contract: Software Verification and Review

Initial state: NOT EXECUTED. These are acceptance criteria, not a historical test report.

## V01 - Actual execution
**Method:** Reconcile each reported check with a command/result or captured interaction.

**Evidence to retain:** Evidence ledger.

## V02 - Negative sensitivity
**Method:** Introduce a controlled fault or verify a known failing case is detected.

**Evidence to retain:** Expected failing-test evidence.

## V03 - Review traceability
**Method:** Tie findings and resolution to exact file/revision.

**Evidence to retain:** Review and recheck record.

## V04 - Release honesty
**Method:** Distinguish static checks, mock contracts, integration and platform tests.

**Evidence to retain:** Final qualification matrix.

## Classification and evidence retention
A critical security, data-loss or authorization failure blocks release. An unavailable
integration is NOT TESTED, not PASS. A tool error is a failed attempt unless its output
proves the requested outcome. Record baseline versus changed revision, command or test id,
exit status and redacted results. Do not retain tokens, raw customer payloads or full prompts
when metrics and identifiers suffice. A reviewer may challenge every recorded claim.
