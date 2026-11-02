# Verification contract: Kubernetes and GitOps Operations

Initial state: NOT EXECUTED. These are acceptance criteria, not a historical test report.

## V01 - Scope safety
**Method:** Confirm every mutation belongs to the authorized context and namespace.

**Evidence to retain:** Resource allowlist and reviewed diff.

## V02 - Causal diagnosis
**Method:** Perform a test that distinguishes the leading hypothesis from alternatives.

**Evidence to retain:** Conditions/events and before/after signals.

## V03 - Policy and identity
**Method:** Test allowed and denied paths in an authorized fixture.

**Evidence to retain:** RBAC/admission/network results without secrets.

## V04 - Service recovery
**Method:** Check readiness plus representative application behavior through its normal route.

**Evidence to retain:** Health, errors, latency and stabilization evidence.

## Classification and evidence retention
A critical security, data-loss or authorization failure blocks release. An unavailable
integration is NOT TESTED, not PASS. A tool error is a failed attempt unless its output
proves the requested outcome. Record baseline versus changed revision, command or test id,
exit status and redacted results. Do not retain tokens, raw customer payloads or full prompts
when metrics and identifiers suffice. A reviewer may challenge every recorded claim.
