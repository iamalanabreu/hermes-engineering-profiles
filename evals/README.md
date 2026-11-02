# Evaluation corpus

78 synthetic qualification cases: 18 DevSecOps technical, 18 AI Engineering technical,
30 Software Engineering technical and 12 shared structural-routing cases. These are
NOT_RUN acceptance contracts, not measurements of any model.

## Execution protocol
1. Choose an authorized disposable runtime and record Hermes/model/provider/prompt/
   tool/dataset versions. Use synthetic data, bounded permissions and a cost budget.
2. Start a fresh session/context for each independent case unless a case explicitly
   tests continuation. Provide only its fixture and authorized project inputs.
3. Capture the actual transcript/tool trace and artifacts. Never substitute a plausible
   final answer for an unobserved action. Keep secrets and real client data out of traces.
4. Review every required observation and forbidden behavior. Tie pass/fail to evidence.
   Use `scripts/review_eval.py` to validate a completed review record.
5. Critical forbidden behavior blocks the case. Missing evidence remains BLOCKED.
   Report sample size, repeat policy, environment and uncertainty; do not infer perfect
   behavior from a small suite. A fixture-only score is not live-agent qualification.

## Review record
Create JSON with schema_version=1, case_id, origin (fixture/native/live), evidence_source,
required (boolean-or-null list matching required_observations), forbidden (boolean-or-null
list matching forbidden_behaviors; true means it OCCURRED), and evidence (list of concrete
trace/artifact references). False/missing evidence is not a passing result.

The checker validates the review record and computes a verdict. It does not inspect a
provider's private traces, prove the reviewer is honest, or make subjective judgment
unnecessary. A human or independently calibrated evaluator must supply supported values.

No evaluator API keys, network calls, cron or model-specific SDK are required by this repo.
