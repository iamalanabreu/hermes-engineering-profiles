# Verification contract: Cloud Security Architecture and Review

Initial state: NOT EXECUTED. These are acceptance criteria, not a historical test report.

## V01 - Findings are reproducible
**Method:** Tie every material finding to a specific target, observation and safe verification method.

**Evidence to retain:** Redacted finding record.

## V02 - Remediation preserves functionality
**Method:** Test required consumers before and after a scoped change.

**Evidence to retain:** Success and denied-path results.

## V03 - Privileges remain bounded
**Method:** Compare effective permissions rather than policy labels alone.

**Evidence to retain:** Permission diff and scoped access checks.

## V04 - Residual risk is explicit
**Method:** List unverifiable assumptions, exceptions and deferred controls.

**Evidence to retain:** Risk decision log.

## Classification and evidence retention
A critical security, data-loss or authorization failure blocks release. An unavailable
integration is NOT TESTED, not PASS. A tool error is a failed attempt unless its output
proves the requested outcome. Record baseline versus changed revision, command or test id,
exit status and redacted results. Do not retain tokens, raw customer payloads or full prompts
when metrics and identifiers suffice. A reviewer may challenge every recorded claim.
