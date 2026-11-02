# Verification contract: Model, Provider and Gateway Routing

Initial state: NOT EXECUTED. These are acceptance criteria, not a historical test report.

## V01 - Eligibility precedes selection
**Method:** Send cases that require restricted data or unsupported capabilities.

**Evidence to retain:** Rejected routes and permitted selection evidence.

## V02 - Fallback is bounded
**Method:** Exercise a multi-route failure and verify maximum attempts and deadline.

**Evidence to retain:** Attempt trace and final classified error.

## V03 - Protocol compatibility
**Method:** Test tool schema, streaming and structured outputs against each enabled route.

**Evidence to retain:** Contract-test results by route/version.

## V04 - Optimization is measured
**Method:** Compare a held-out task suite before and after the policy change.

**Evidence to retain:** Quality/cost/latency deltas with sample limitations.

## Classification and evidence retention
A critical security, data-loss or authorization failure blocks release. An unavailable
integration is NOT TESTED, not PASS. A tool error is a failed attempt unless its output
proves the requested outcome. Record baseline versus changed revision, command or test id,
exit status and redacted results. Do not retain tokens, raw customer payloads or full prompts
when metrics and identifiers suffice. A reviewer may challenge every recorded claim.
