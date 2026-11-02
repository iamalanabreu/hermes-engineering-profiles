# Verification contract: Agent Evaluation and Regression Engineering

Initial state: NOT EXECUTED. These are acceptance criteria, not a historical test report.

## V01 - Evaluator catches deliberate faults
**Method:** Inject invalid schema, forbidden action and missing evidence into synthetic traces.

**Evidence to retain:** Expected evaluator failures.

## V02 - Version provenance
**Method:** Record baseline/candidate/evaluator/model/tool/dataset revisions.

**Evidence to retain:** Reproducibility manifest.

## V03 - Outcome coverage
**Method:** Check every requirement against a case and an evidence mechanism.

**Evidence to retain:** Coverage map and explicit gaps.

## V04 - Decision is defensible
**Method:** Inspect critical regressions, uncertainty and operational cost.

**Evidence to retain:** Promotion/hold decision with supporting results.

## Classification and evidence retention
A critical security, data-loss or authorization failure blocks release. An unavailable
integration is NOT TESTED, not PASS. A tool error is a failed attempt unless its output
proves the requested outcome. Record baseline versus changed revision, command or test id,
exit status and redacted results. Do not retain tokens, raw customer payloads or full prompts
when metrics and identifiers suffice. A reviewer may challenge every recorded claim.
