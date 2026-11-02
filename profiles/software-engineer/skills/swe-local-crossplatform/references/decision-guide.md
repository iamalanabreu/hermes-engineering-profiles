# Decision guide: Local, CLI and Cross-Platform Software

These are engineering decisions, not automatic authorization rules.

## Only one operating system is available
Test it fully and leave other platforms explicitly unqualified.

**Why / trade-off:** Portable source is not verified packaging.

## A local app loads remote/untrusted content
Isolate UI and privileged APIs, validate IPC and minimize capabilities.

**Why / trade-off:** A desktop wrapper can magnify a web-content compromise.

## A CLI edits many files
Provide preview, conflict handling and bounded authorized roots.

**Why / trade-off:** Command-line convenience must not remove data-loss safeguards.

## The product must work offline
Make essential paths independent of providers and test actual disconnected behavior.

**Why / trade-off:** A cached successful request is not proof of offline capability.

## Auto-update fails mid-write
Use a recoverable update strategy supported by the platform and verify it.

**Why / trade-off:** An updater must not destroy the only runnable version or user data.

## Known failure patterns
- Hardcoded home paths, drive letters or ports.
- Assuming administrator privileges.
- Publishing a network service beyond loopback without a requirement.
- Deleting user data during uninstall or rollback by default.
- Claiming macOS/Windows support from a Linux build only.

## Stop and escalate
Stop on a changed target, ambiguous data ownership, missing permission, incompatible
contracts, unexplained destructive diff, or exhausted investigation budget. Preserve
partial evidence and name the smallest next action that would unblock the task.
