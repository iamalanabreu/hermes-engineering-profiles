# Kubernetes and GitOps Operations: delivery record

Template, not an executed result. Replace the marked inputs before issuing a report.

## Request and target
Context: {{context_id}}
Target / environment: {{authorized_target}}
Source revision: {{revision}}
Objective and explicit exclusions: {{scope}}

## Observed state
{{facts_with_sources}}

## Decision
{{chosen_approach_alternatives_and_tradeoffs}}

## Change and authority
{{diff_or_artifact_paths}}
{{required_approvals_and_actual_authorization}}

## Domain deliverable
Deliver symptom-to-evidence diagnosis, desired/live comparison, minimal corrective
diff, authorization scope, health verification and reconciliation follow-up.

## Verification
| Check | Actual result | Evidence | State |
|---|---|---|---|
| {{check_id}} | {{actual_result_or_not_executed}} | {{evidence_location}} | {{verified_not_tested_or_blocked}} |

## Recovery and residual risks
{{tested_recovery_or_explicit_limit}}
{{open_risks_and_owner_decisions}}
