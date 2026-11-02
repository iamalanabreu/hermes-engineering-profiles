# Verification contract: End-to-End Feature Delivery

Initial state: NOT EXECUTED. These are acceptance criteria, not a historical test report.

## V01 - Behavior works
**Method:** Execute representative success and failure paths, preferably through the real boundary.

**Evidence to retain:** Test/interaction outputs.

## V02 - Regression is controlled
**Method:** Compare baseline and changed revision tests.

**Evidence to retain:** Failures classified as baseline, new or resolved.

## V03 - Diff is scoped
**Method:** Review modified/untracked files and accidental artifacts.

**Evidence to retain:** Intended file list and diff review.

## V04 - Delivery is honest
**Method:** Check every completion claim against execution evidence.

**Evidence to retain:** Executed/not-tested/blocked report.

## Classification and evidence retention
A critical security, data-loss or authorization failure blocks release. An unavailable
integration is NOT TESTED, not PASS. A tool error is a failed attempt unless its output
proves the requested outcome. Record baseline versus changed revision, command or test id,
exit status and redacted results. Do not retain tokens, raw customer payloads or full prompts
when metrics and identifiers suffice. A reviewer may challenge every recorded claim.
