# Verification contract: Agent System Architecture

Initial state: NOT EXECUTED. These are acceptance criteria, not a historical test report.

## V01 - Contract coverage
**Method:** Map each state and side effect to an input/output and acceptance case.

**Evidence to retain:** State/transition coverage table.

## V02 - Tool availability
**Method:** Probe only authorized capabilities and mark unavailable tools explicitly.

**Evidence to retain:** Tool inventory and version evidence.

## V03 - Failure safety
**Method:** Exercise timeout, partial completion, denial and duplicate cases in a fixture.

**Evidence to retain:** Action log demonstrating no unauthorized or duplicate effects.

## V04 - Behavioral quality
**Method:** Compare the slice to a baseline across held-out tasks and record cost/latency.

**Evidence to retain:** Versioned evaluation results; no invented score.

## Classification and evidence retention
A critical security, data-loss or authorization failure blocks release. An unavailable
integration is NOT TESTED, not PASS. A tool error is a failed attempt unless its output
proves the requested outcome. Record baseline versus changed revision, command or test id,
exit status and redacted results. Do not retain tokens, raw customer payloads or full prompts
when metrics and identifiers suffice. A reviewer may challenge every recorded claim.
