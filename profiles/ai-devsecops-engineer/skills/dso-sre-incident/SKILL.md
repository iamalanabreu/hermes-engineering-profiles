---
name: dso-sre-incident
description: "Investigate service degradation, incidents, SLOs and operational toil with impact-first evidence. Use for live incidents and reliability reviews; do not restart blindly or confuse correlated logs with cause."
---
# Reliability and Incident Response

## Mission and boundaries
Own bounded incident diagnosis, authorized mitigation and measurable recovery.
During an incident prioritize customer impact and reversible stabilization. During a
reliability review distinguish workload behavior, infrastructure and measurement errors.

## Establish the inputs
- Affected service, user impact, onset/window, severity criteria and incident owner.
- Relevant SLIs/SLOs, baseline, recent changes, topology and dependencies.
- Approved read access, mitigation scope, communication channel and sensitive-data handling.
- Known runbooks, recovery objectives and criteria to stop or escalate.

Missing information is not permission to invent a stack, a result, an environment or
an approval. Read the authorized project's instructions and source-of-truth index.
Use project-context-architect only when contextual structure is actually missing;
use agent-folder-architect only for a justified recurring capability, not this task by default.

## Execution procedure

### 1. Establish impact and coordination
State who is affected and what is failing. Confirm time windows and detection source. Establish an incident timeline and responsible owner; do not invent severity or an SLA breach from one alert.

**Completion evidence:** Impact statement, baseline/window and coordination record.

### 2. Build competing hypotheses
Correlate errors, latency, saturation, traffic, dependencies and recent changes. Select small tests that distinguish hypotheses. Avoid large log dumps and repeated identical probes without a new hypothesis.

**Completion evidence:** Ranked hypotheses with supporting and contradicting observations.

### 3. Choose stabilization before deep repair
Compare rollback, traffic shift, feature disable, capacity relief and dependency isolation against data integrity and blast radius. Obtain authorization for a material mitigation.

**Completion evidence:** Mitigation decision, expected effect, stop condition and rollback/forward-repair option.

### 4. Apply and measure
Execute one bounded mitigation or explicitly coordinated set. Record time and operation identifiers. Compare the intended leading indicators and real user path; stop if impact worsens.

**Completion evidence:** Mitigation result and time-aligned signal change.

### 5. Determine cause and durable correction
After stabilization, trace the failure mechanism and contributing conditions. Reproduce safely where possible. Separate trigger, root cause and missing detection; resist unsupported certainty.

**Completion evidence:** Causal explanation, reproduction or uncertainty, and correction with regression check.

### 6. Close with follow-through
Confirm the recovery window and stakeholder acceptance. Document impact, timeline, decisions, evidence, residual risk and preventive work. Assign ownership only when provided or approved.

**Completion evidence:** A factual incident record and prioritized recurrence-prevention actions.

## Decision points and deeper reference
Read [the decision guide](references/decision-guide.md) before selecting a materially
different path. Load only the needed reference; do not dump the complete library into context.
Read [the verification contract](references/verification.md) before claiming completion.

## Authority and failure boundary
Read-only investigation does not authorize restart, scaling, traffic changes or data
repair. Never disable audit/security globally for convenience. Protect incident data
and follow the environment's escalation authority.

## Recovery
Stop a worsening mitigation. Restore the last authorized configuration only where
safe; a stateful or data-loss incident may require forward repair or restore instead.
Keep a timeline so repeated handoffs do not reapply a failed intervention.

## Delivery
Deliver impact and timeline, tested hypotheses, mitigation authorization/results,
recovery evidence, causal confidence and prevention actions.

Use the [deliverable template](templates/deliverable.md), removing inapplicable fields.
Use [the synthetic scenario](examples/scenario.md) to understand expected behavior,
not as evidence of any actual execution. Check [primary references](references/sources.md)
against the installed product versions before using version-specific commands or APIs.

Distinguish **executed**, **verified**, **not tested** and **blocked**. A proposed command,
a passed formatter, a model-generated verdict, and a real end-to-end test are different
evidence classes. Cite actual files/revisions/results; never promote a template to a result.
