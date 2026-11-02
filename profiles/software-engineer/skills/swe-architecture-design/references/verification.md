# Verification contract: Pragmatic Software Architecture

Initial state: NOT EXECUTED. These are acceptance criteria, not a historical test report.

## V01 - Requirement traceability
**Method:** Map critical requirements and invariants to components and acceptance checks.

**Evidence to retain:** Requirements-to-design map.

## V02 - Failure completeness
**Method:** Walk through dependency failure, partial commit, invalid input and permission denial.

**Evidence to retain:** Failure-mode review.

## V03 - Proportionality
**Method:** Identify each added service/framework/abstraction and its explicit benefit.

**Evidence to retain:** Complexity budget and alternatives.

## V04 - Migration feasibility
**Method:** Review coexistence, data transition and reversibility.

**Evidence to retain:** Incremental migration/rollout plan.

## Classification and evidence retention
A critical security, data-loss or authorization failure blocks release. An unavailable
integration is NOT TESTED, not PASS. A tool error is a failed attempt unless its output
proves the requested outcome. Record baseline versus changed revision, command or test id,
exit status and redacted results. Do not retain tokens, raw customer payloads or full prompts
when metrics and identifiers suffice. A reviewer may challenge every recorded claim.
