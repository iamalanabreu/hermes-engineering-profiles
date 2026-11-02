# Verification contract: Local, CLI and Cross-Platform Software

Initial state: NOT EXECUTED. These are acceptance criteria, not a historical test report.

## V01 - CLI and error contract
**Method:** Test arguments, invalid input, cancellation and documented exit statuses.

**Evidence to retain:** Command results and failure cases.

## V02 - Data safety
**Method:** Exercise path traversal, conflicts, partial writes and permission denial in fixtures.

**Evidence to retain:** No unintended file mutation.

## V03 - Platform qualification
**Method:** Run clean install/launch/update on each claimed target.

**Evidence to retain:** Per-OS/architecture results; unavailable targets not tested.

## V04 - Offline and recovery
**Method:** Exercise disconnected operation and interrupted/corrupt state.

**Evidence to retain:** Recovery and offline evidence.

## Classification and evidence retention
A critical security, data-loss or authorization failure blocks release. An unavailable
integration is NOT TESTED, not PASS. A tool error is a failed attempt unless its output
proves the requested outcome. Record baseline versus changed revision, command or test id,
exit status and redacted results. Do not retain tokens, raw customer payloads or full prompts
when metrics and identifiers suffice. A reviewer may challenge every recorded claim.
