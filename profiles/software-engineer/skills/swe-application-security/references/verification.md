# Verification contract: Secure Application Engineering

Initial state: NOT EXECUTED. These are acceptance criteria, not a historical test report.

## V01 - Authorization invariants
**Method:** Test role/object/tenant matrix at the trusted operation boundary.

**Evidence to retain:** Denied and allowed results.

## V02 - Input/output safety
**Method:** Exercise relevant injection, path, size and output cases.

**Evidence to retain:** Regression test evidence.

## V03 - Session/data lifecycle
**Method:** Test expiry/revocation and inspect cache/log/export behavior.

**Evidence to retain:** Lifecycle and exposure checks.

## V04 - Fix completeness
**Method:** Trace alternate call paths and rerun the original abuse case.

**Evidence to retain:** Before/after security finding record.

## Classification and evidence retention
A critical security, data-loss or authorization failure blocks release. An unavailable
integration is NOT TESTED, not PASS. A tool error is a failed attempt unless its output
proves the requested outcome. Record baseline versus changed revision, command or test id,
exit status and redacted results. Do not retain tokens, raw customer payloads or full prompts
when metrics and identifiers suffice. A reviewer may challenge every recorded claim.
