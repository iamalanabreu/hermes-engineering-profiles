---
name: aie-agent-evaluation
description: "Build and review evaluation suites for prompts, tools, models and agent workflows using baselines, held-out cases and observable evidence. Use before promotion or comparison; do not equate model judgments or mock tests with production proof."
---
# Agent Evaluation and Regression Engineering

## Mission and boundaries
Own measurement of useful, safe task outcomes. Distinguish prompt tests, tool-contract
tests, retrieval metrics, workflow execution, adversarial cases and live integration.
A single aggregate score must not hide a critical security regression.

## Establish the inputs
- Task definition, intended users, unacceptable failures and deployment decision.
- Baseline code/prompt/model/tool versions and candidate revisions.
- Representative authorized or synthetic datasets, splits, labeling/rubric provenance and privacy constraints.
- Quality, safety, latency and cost budgets with explicit threshold ownership.

Missing information is not permission to invent a stack, a result, an environment or
an approval. Read the authorized project's instructions and source-of-truth index.
Use project-context-architect only when contextual structure is actually missing;
use agent-folder-architect only for a justified recurring capability, not this task by default.

## Execution procedure

### 1. Define observable acceptance
Translate requirements into outcomes that can be checked independently of the agent's self-report. Separate critical failures from graded quality. Specify what evidence each test must retain.

**Completion evidence:** Rubric and threshold decision with no invented performance target.

### 2. Build representative cases
Include normal, boundary, negative, ambiguous, unavailable-tool, partial-failure and adversarial cases. Label synthetic data; avoid training/tuning on the held-out set. Track source, license and sensitive content handling.

**Completion evidence:** Versioned dataset and split manifest with expected observations.

### 3. Select appropriate evaluators
Use deterministic assertions for schemas, tools, permissions and exact behavior; human review for domain judgment; calibrated LLM judging only as a fallible aid. Blind candidate identity where useful and track judge version.

**Completion evidence:** Evaluator design, known blind spots and a deliberately broken case each evaluator catches.

### 4. Run paired baseline/candidate trials
Keep comparable inputs and environment. Record seeds/settings where available, retries, failures and missing results. Capture actions and artifacts, not only answer text. Repeated trials may be needed for variable behavior.

**Completion evidence:** Raw result records tied to all relevant versions and test ids.

### 5. Analyze failures and uncertainty
Report per-class results, sample size, uncertainty and critical regressions. Investigate disagreement and leakage. An average quality gain cannot compensate for a forbidden action or tenant leak.

**Completion evidence:** Failure taxonomy and promotion recommendation grounded in actual trials.

### 6. Gate and preserve reproducibility
Block on critical failures or missing mandatory evidence. Define rollback and monitoring for promoted changes. Keep datasets and evaluators versioned and rerun affected cases when tools/permissions change.

**Completion evidence:** Release gate record, reproducible invocation and explicit not-tested coverage.

## Decision points and deeper reference
Read [the decision guide](references/decision-guide.md) before selecting a materially
different path. Load only the needed reference; do not dump the complete library into context.
Read [the verification contract](references/verification.md) before claiming completion.

## Authority and failure boundary
Use only approved data and endpoints. Running evaluations can send confidential inputs
and incur cost; authorize that separately. Do not schedule recurring tests, alter release
thresholds or promote a model without the corresponding decision.

## Recovery
Hold promotion on regression, preserve the failing trace and restore the last evaluated
prompt/model/tool configuration when safe. Do not erase failures to improve the score;
add a regression case after identifying the cause.

## Delivery
Deliver dataset/split definitions, rubrics, evaluator checks, paired results,
critical regressions, uncertainty, cost/latency and a justified release decision.

Use the [deliverable template](templates/deliverable.md), removing inapplicable fields.
Use [the synthetic scenario](examples/scenario.md) to understand expected behavior,
not as evidence of any actual execution. Check [primary references](references/sources.md)
against the installed product versions before using version-specific commands or APIs.

Distinguish **executed**, **verified**, **not tested** and **blocked**. A proposed command,
a passed formatter, a model-generated verdict, and a real end-to-end test are different
evidence classes. Cite actual files/revisions/results; never promote a template to a result.

## Deterministic helper
Aggregate normalized result records; this does not execute a model or verify input provenance.

Read [the helper](scripts/summarize_evals.py). Invoke it through terminal using the resolved
`${HERMES_SKILL_DIR}/scripts/summarize_evals.py` path; run `--help` for inputs.
