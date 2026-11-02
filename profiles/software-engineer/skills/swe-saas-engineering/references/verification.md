# Verification contract: SaaS Product and Tenant Engineering

Initial state: NOT EXECUTED. These are acceptance criteria, not a historical test report.

## V01 - Tenant isolation
**Method:** Run cross-tenant object, cache, file, job and export attempts.

**Evidence to retain:** Denied-path evidence across boundaries.

## V02 - Role and entitlement rules
**Method:** Exercise role/plan/state combinations and quota limits.

**Evidence to retain:** Business rule matrix.

## V03 - Async correctness
**Method:** Replay duplicate, reordered and delayed synthetic events.

**Evidence to retain:** Idempotency/reconciliation results.

## V04 - Lifecycle integrity
**Method:** Verify suspension, membership removal and deletion/retention behavior.

**Evidence to retain:** State transition and data-lifecycle evidence.

## Classification and evidence retention
A critical security, data-loss or authorization failure blocks release. An unavailable
integration is NOT TESTED, not PASS. A tool error is a failed attempt unless its output
proves the requested outcome. Record baseline versus changed revision, command or test id,
exit status and redacted results. Do not retain tokens, raw customer payloads or full prompts
when metrics and identifiers suffice. A reviewer may challenge every recorded claim.
