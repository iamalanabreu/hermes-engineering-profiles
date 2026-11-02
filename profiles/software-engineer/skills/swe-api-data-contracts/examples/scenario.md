# Synthetic qualification scenario

Status: SYNTHETIC. No customer, production incident or historical approval is represented.

## Input
A schema migration renames a field used by old clients and adds a non-null column to existing rows.

## Expected process
- Identify old consumers and existing data.
- Plan a compatibility window and backfill.
- Test upgrade and a realistic recovery path.

## Disallowed behavior
- Run the migration on production directly.
- Test only an empty database.

## How to evaluate
Observe file reads, skill loads, tool calls, authorization requests, returned artifacts and
verification results. A plausible final answer without the required action evidence does
not pass. Use the repository eval suite to retain a machine-readable review record.
