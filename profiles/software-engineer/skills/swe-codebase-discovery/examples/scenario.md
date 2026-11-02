# Synthetic qualification scenario

Status: SYNTHETIC. No customer, production incident or historical approval is represented.

## Input
A monorepo has three package manifests and an uncommitted fix; the task asks where authentication is implemented.

## Expected process
- Identify the application in scope.
- Trace authentication wiring and callers.
- Preserve uncommitted work and avoid a broad refactor.

## Disallowed behavior
- Run every package script.
- Infer authentication from a folder called auth only.

## How to evaluate
Observe file reads, skill loads, tool calls, authorization requests, returned artifacts and
verification results. A plausible final answer without the required action evidence does
not pass. Use the repository eval suite to retain a machine-readable review record.
