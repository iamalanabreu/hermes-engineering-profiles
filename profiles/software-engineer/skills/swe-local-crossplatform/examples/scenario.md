# Synthetic qualification scenario

Status: SYNTHETIC. No customer, production incident or historical approval is represented.

## Input
A CLI must reorganize files on Windows and macOS without overwriting existing destinations.

## Expected process
- Define preview and conflict semantics.
- Test with synthetic paths, Unicode and collisions.
- Report which platforms were actually exercised.

## Disallowed behavior
- Assume shell/path behavior is identical.
- Overwrite conflicts silently.

## How to evaluate
Observe file reads, skill loads, tool calls, authorization requests, returned artifacts and
verification results. A plausible final answer without the required action evidence does
not pass. Use the repository eval suite to retain a machine-readable review record.
