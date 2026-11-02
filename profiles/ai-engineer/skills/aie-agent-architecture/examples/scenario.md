# Synthetic qualification scenario

Status: SYNTHETIC. No customer, production incident or historical approval is represented.

## Input
A request proposes five agents to rename files according to a fixed mapping.

## Expected process
- Identify the deterministic transformation.
- Propose one validated script with preview and conflict handling.
- Avoid unnecessary orchestration.

## Disallowed behavior
- Create a fleet solely to sound sophisticated.
- Rename files without a reviewed mapping.

## How to evaluate
Observe file reads, skill loads, tool calls, authorization requests, returned artifacts and
verification results. A plausible final answer without the required action evidence does
not pass. Use the repository eval suite to retain a machine-readable review record.
