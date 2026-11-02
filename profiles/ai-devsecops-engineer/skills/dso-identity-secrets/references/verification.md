# Verification contract: Identity, Secrets and Credential Lifecycle

Initial state: NOT EXECUTED. These are acceptance criteria, not a historical test report.

## V01 - Least privilege
**Method:** Exercise required and forbidden actions with scoped test identities.

**Evidence to retain:** Access matrix and denied results.

## V02 - Protocol correctness
**Method:** Check issuer, audience, lifetime and signature verification against actual protocol configuration.

**Evidence to retain:** Redacted configuration/claims evidence.

## V03 - Rotation completeness
**Method:** Verify each consumer and then revoked-credential denial.

**Evidence to retain:** Consumer checklist and revoke result.

## V04 - No secret exposure
**Method:** Inspect changed artifacts and redacted outputs; use dedicated secret scanning when available.

**Evidence to retain:** Scanner scope/results plus known limitations.

## Classification and evidence retention
A critical security, data-loss or authorization failure blocks release. An unavailable
integration is NOT TESTED, not PASS. A tool error is a failed attempt unless its output
proves the requested outcome. Record baseline versus changed revision, command or test id,
exit status and redacted results. Do not retain tokens, raw customer payloads or full prompts
when metrics and identifiers suffice. A reviewer may challenge every recorded claim.
