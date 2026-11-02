# Decision guide: LLMOps and Agent Observability

These are engineering decisions, not automatic authorization rules.

## Latency rises while model calls are normal
Inspect retrieval, tool waits, approval delays and retries by trace stage.

**Why / trade-off:** Model latency is only one component of an agent turn.

## Spend rises without traffic growth
Inspect route mix, input/context growth, cache behavior, retries, judge calls and fan-out.

**Why / trade-off:** Token count alone does not attribute the source of spend.

## Quality degrades with healthy endpoints
Check prompt/tool/data/index versions and real task outcomes.

**Why / trade-off:** Operational availability and semantic correctness are independent.

## Rollback changes the model but not tools
Verify schema/permission compatibility and re-evaluate the combined version set.

**Why / trade-off:** The deployed unit is a system, not just a model name.

## Trace data contains confidential payloads
Contain logging, minimize retention and treat exposure under the applicable process.

**Why / trade-off:** Observability must not become a secondary data leak.

## Known failure patterns
- Logging prompts, tokens or tool arguments without a data policy.
- Unbounded labels that include user input or tenant ids.
- Ignoring evaluation/judge/tool/retry costs.
- Using average latency without tail and failure analysis.

## Stop and escalate
Stop on a changed target, ambiguous data ownership, missing permission, incompatible
contracts, unexplained destructive diff, or exhausted investigation budget. Preserve
partial evidence and name the smallest next action that would unblock the task.
