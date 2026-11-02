# Verification contract: Software Release and Sustainable Maintenance

Initial state: NOT EXECUTED. These are acceptance criteria, not a historical test report.

## V01 - Artifact identity
**Method:** Tie artifact digest and package contents to the source revision.

**Evidence to retain:** Build manifest and content inspection.

## V02 - Compatibility
**Method:** Run consumers, upgrade and downgrade/recovery cases relevant to the change.

**Evidence to retain:** Compatibility matrix.

## V03 - Scope preservation
**Method:** Inspect staged and untracked changes before commit.

**Evidence to retain:** Explicit intended-file list.

## V04 - Release authority
**Method:** Distinguish preparation from actual authorized publication.

**Evidence to retain:** Approval/publish record or not-published state.

## Classification and evidence retention
A critical security, data-loss or authorization failure blocks release. An unavailable
integration is NOT TESTED, not PASS. A tool error is a failed attempt unless its output
proves the requested outcome. Record baseline versus changed revision, command or test id,
exit status and redacted results. Do not retain tokens, raw customer payloads or full prompts
when metrics and identifiers suffice. A reviewer may challenge every recorded claim.
