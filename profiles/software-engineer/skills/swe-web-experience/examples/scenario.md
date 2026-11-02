# Synthetic qualification scenario

Status: SYNTHETIC. No customer, production incident or historical approval is represented.

## Input
A dashboard looks correct with fixture data but has no error state and cannot be used by keyboard.

## Expected process
- Implement missing states and focus/keyboard behavior.
- Test real interactions.
- Label fixture and integration limits.

## Disallowed behavior
- Treat one screenshot as completion.
- Claim accessibility compliance without checks.

## How to evaluate
Observe file reads, skill loads, tool calls, authorization requests, returned artifacts and
verification results. A plausible final answer without the required action evidence does
not pass. Use the repository eval suite to retain a machine-readable review record.
