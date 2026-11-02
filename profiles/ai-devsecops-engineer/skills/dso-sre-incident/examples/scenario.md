# Synthetic qualification scenario

Status: SYNTHETIC. No customer, production incident or historical approval is represented.

## Input
Latency rises after a release, while CPU is normal and one external dependency is timing out.

## Expected process
- Compare time windows and dependency latency.
- Test the dependency hypothesis.
- Propose a bounded mitigation with recovery signals.

## Disallowed behavior
- Scale everything because CPU looks normal.
- Announce root cause without discriminating evidence.

## How to evaluate
Observe file reads, skill loads, tool calls, authorization requests, returned artifacts and
verification results. A plausible final answer without the required action evidence does
not pass. Use the repository eval suite to retain a machine-readable review record.
