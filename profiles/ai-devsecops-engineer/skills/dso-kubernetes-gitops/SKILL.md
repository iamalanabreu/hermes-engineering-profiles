---
name: dso-kubernetes-gitops
description: "Diagnose or change Kubernetes workloads and GitOps reconciliation using desired/live state, health, policy and storage evidence. Use for rollout, drift, capacity and admission issues; not for unconditional sync or restart."
---
# Kubernetes and GitOps Operations

## Mission and boundaries
Own declarative workload transitions and cluster-level diagnosis within an explicit
namespace/resource scope. GitOps desired state and application health are independent
signals. Inspect before restarting, deleting a pod or forcing reconciliation.

## Establish the inputs
- Cluster context, namespace, resource identity, source revision/chart version and ownership.
- Symptoms, time window, deployment history, availability/error objectives and current GitOps sync/health status.
- RBAC scope, admission/network policies, storage semantics and controller ownership.
- Allowed mitigation, release mechanism and any emergency exception process.

Missing information is not permission to invent a stack, a result, an environment or
an approval. Read the authorized project's instructions and source-of-truth index.
Use project-context-architect only when contextual structure is actually missing;
use agent-folder-architect only for a justified recurring capability, not this task by default.

## Execution procedure

### 1. Confirm the scope and signals
Verify the selected context without printing kubeconfig credentials. Inspect workload conditions, recent events, rollout history, image identity and controller owner references. Bound log volume and redact payloads.

**Completion evidence:** A timeline with desired/live revision, health and observed failure conditions.

### 2. Separate scheduling, startup and serving failures
For Pending, inspect resources, placement, taints, quotas and storage binding. For image/startup failures, inspect image access, command/config and probes. For serving failures, trace endpoints, service selection, DNS and network policy rather than blaming the pod.

**Completion evidence:** One or more hypotheses linked to observed conditions and a discriminating read-only test.

### 3. Explain drift and reconciliation
Compare desired manifests with live state. Identify admission mutations, controller-managed fields, emergency edits and chart rendering differences. Use ignore rules only for narrowly understood ownership, not to hide all divergence.

**Completion evidence:** A resource-level explanation of drift with owner/source classification.

### 4. Design the smallest correction
Prefer a reviewed Git change where Git is authoritative. Check compatibility of probes, rollout strategy, PDB, resource requests, storage and policy. Default-deny policy must include required DNS/dependency paths before rollout.

**Completion evidence:** Proposed diff, workload-level verification and blast radius.

### 5. Apply through the authorized delivery mechanism
Obtain authorization for live mutations or emergency exceptions. Do not use force sync, prune, namespace deletion, volume deletion or broad RBAC as troubleshooting shortcuts. Stop if reconciliation targets exceed the reviewed set.

**Completion evidence:** Delivery/reconciliation identifiers and resulting resource conditions.

### 6. Verify steady-state behavior
Check ready endpoints, error rate/latency, rollout completion, policy behavior and sustained reconciliation. Confirm recovery after reschedule when relevant. A healthy controller does not prove the application serves correct responses.

**Completion evidence:** Evidence across control-plane signals and a functional request or workload-specific check.

## Decision points and deeper reference
Read [the decision guide](references/decision-guide.md) before selecting a materially
different path. Load only the needed reference; do not dump the complete library into context.
Read [the verification contract](references/verification.md) before claiming completion.

## Authority and failure boundary
Live sync, prune, scaling, restarts, RBAC edits and storage operations are mutations.
Request authorization proportionate to their impact; never infer it from read access.
Prefer the established GitOps delivery path and preserve unrelated controllers.

## Recovery
Revert the source revision only when its dependent data/API behavior remains compatible.
For emergency live changes, record the exception and reconcile it back into Git. Do not
repeatedly toggle revisions while a stateful recovery is incomplete.

## Delivery
Deliver symptom-to-evidence diagnosis, desired/live comparison, minimal corrective
diff, authorization scope, health verification and reconciliation follow-up.

Use the [deliverable template](templates/deliverable.md), removing inapplicable fields.
Use [the synthetic scenario](examples/scenario.md) to understand expected behavior,
not as evidence of any actual execution. Check [primary references](references/sources.md)
against the installed product versions before using version-specific commands or APIs.

Distinguish **executed**, **verified**, **not tested** and **blocked**. A proposed command,
a passed formatter, a model-generated verdict, and a real end-to-end test are different
evidence classes. Cite actual files/revisions/results; never promote a template to a result.
