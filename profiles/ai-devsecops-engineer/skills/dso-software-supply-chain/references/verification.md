# Verification contract: Secure Build and Release Supply Chain

Initial state: NOT EXECUTED. These are acceptance criteria, not a historical test report.

## V01 - Source-to-artifact traceability
**Method:** Match source revision, build job, digest and promotion target.

**Evidence to retain:** Release provenance chain.

## V02 - No privilege crossover
**Method:** Test untrusted job paths and effective token/secrets access.

**Evidence to retain:** Permission matrix and negative test.

## V03 - Gates are honest
**Method:** Check actual scanner/test execution and exception handling.

**Evidence to retain:** Tool versions, scope, exit status and findings.

## V04 - Recovery works
**Method:** Exercise artifact rollback or document unavailable infrastructure.

**Evidence to retain:** Rollback evidence or not-tested status.

## Classification and evidence retention
A critical security, data-loss or authorization failure blocks release. An unavailable
integration is NOT TESTED, not PASS. A tool error is a failed attempt unless its output
proves the requested outcome. Record baseline versus changed revision, command or test id,
exit status and redacted results. Do not retain tokens, raw customer payloads or full prompts
when metrics and identifiers suffice. A reviewer may challenge every recorded claim.
