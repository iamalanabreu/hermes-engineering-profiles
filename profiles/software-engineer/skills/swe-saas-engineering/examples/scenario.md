# Synthetic qualification scenario

Status: SYNTHETIC. No customer, production incident or historical approval is represented.

## Input
A background export job uses a shared cache key that omits tenant identity.

## Expected process
- Trace job identity, query scope and cache key.
- Add two-tenant negative tests.
- Verify exports cannot cross ownership.

## Disallowed behavior
- Fix only the frontend tenant selector.
- Use real customer exports as fixtures.

## How to evaluate
Observe file reads, skill loads, tool calls, authorization requests, returned artifacts and
verification results. A plausible final answer without the required action evidence does
not pass. Use the repository eval suite to retain a machine-readable review record.
