# Synthetic qualification scenario

Status: SYNTHETIC. No customer, production incident or historical approval is represented.

## Input
A new internal CRUD tool for ten users is proposed as six microservices.

## Expected process
- Identify actual quality and ownership needs.
- Compare a modular single application.
- Recommend a proportional approach with explicit trade-offs.

## Disallowed behavior
- Assume hypothetical massive scale.
- Create six services before validating the requirement.

## How to evaluate
Observe file reads, skill loads, tool calls, authorization requests, returned artifacts and
verification results. A plausible final answer without the required action evidence does
not pass. Use the repository eval suite to retain a machine-readable review record.
