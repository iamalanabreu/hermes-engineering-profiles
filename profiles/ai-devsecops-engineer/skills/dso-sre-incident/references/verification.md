# Verification contract: Reliability and Incident Response

Initial state: NOT EXECUTED. These are acceptance criteria, not a historical test report.

## V01 - Impact is bounded
**Method:** Compare affected and unaffected segments and the baseline window.

**Evidence to retain:** Impact scope and uncertainty.

## V02 - Hypothesis is tested
**Method:** Use a discriminating observation or controlled reproduction.

**Evidence to retain:** Test, result and alternative eliminated.

## V03 - Recovery is functional
**Method:** Verify the real user path and agreed stability interval.

**Evidence to retain:** Service outcomes plus telemetry.

## V04 - Prevention is concrete
**Method:** Link each follow-up to a contributing condition and measurable acceptance.

**Evidence to retain:** Follow-up record without invented owners or deadlines.

## Classification and evidence retention
A critical security, data-loss or authorization failure blocks release. An unavailable
integration is NOT TESTED, not PASS. A tool error is a failed attempt unless its output
proves the requested outcome. Record baseline versus changed revision, command or test id,
exit status and redacted results. Do not retain tokens, raw customer payloads or full prompts
when metrics and identifiers suffice. A reviewer may challenge every recorded claim.
