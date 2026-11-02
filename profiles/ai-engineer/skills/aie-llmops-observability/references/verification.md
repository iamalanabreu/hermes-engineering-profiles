# Verification contract: LLMOps and Agent Observability

Initial state: NOT EXECUTED. These are acceptance criteria, not a historical test report.

## V01 - Trace continuity
**Method:** Follow a task through all relevant stages and failures.

**Evidence to retain:** Redacted span/event chain with versions.

## V02 - Cost attribution
**Method:** Reconcile measured usage and route pricing assumptions without claiming bill precision.

**Evidence to retain:** Cost method, included/excluded components and reconciliation sample.

## V03 - Alert usefulness
**Method:** Trigger a safe failure and confirm a meaningful signal reaches the intended operator.

**Evidence to retain:** Alert test and response context.

## V04 - Release safety
**Method:** Run the promotion/rollback checks for the full version set.

**Evidence to retain:** Evaluation gate and recovery evidence.

## Classification and evidence retention
A critical security, data-loss or authorization failure blocks release. An unavailable
integration is NOT TESTED, not PASS. A tool error is a failed attempt unless its output
proves the requested outcome. Record baseline versus changed revision, command or test id,
exit status and redacted results. Do not retain tokens, raw customer payloads or full prompts
when metrics and identifiers suffice. A reviewer may challenge every recorded claim.
