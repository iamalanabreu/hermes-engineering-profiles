# Verification contract: Retrieval, Knowledge and Memory Engineering

Initial state: NOT EXECUTED. These are acceptance criteria, not a historical test report.

## V01 - Access isolation
**Method:** Run same-query cases under two identities with different ACLs and inspect retrieved chunks.

**Evidence to retain:** No unauthorized chunk enters context.

## V02 - Retrieval adequacy
**Method:** Evaluate labeled queries and absent-answer cases separately from generation.

**Evidence to retain:** Recall/rank measurements and misses.

## V03 - Citation fidelity
**Method:** Resolve citations to actual source/version/section and inspect claim support.

**Evidence to retain:** Claim-to-evidence sample review.

## V04 - Deletion/freshness
**Method:** Simulate source/ACL changes and invalidate derivatives.

**Evidence to retain:** Index/cache/memory propagation results.

## Classification and evidence retention
A critical security, data-loss or authorization failure blocks release. An unavailable
integration is NOT TESTED, not PASS. A tool error is a failed attempt unless its output
proves the requested outcome. Record baseline versus changed revision, command or test id,
exit status and redacted results. Do not retain tokens, raw customer payloads or full prompts
when metrics and identifiers suffice. A reviewer may challenge every recorded claim.
