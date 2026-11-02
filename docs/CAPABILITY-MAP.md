# Mapa de capacidades

Escolha pela tarefa e pelo contexto, não por uma stack fixa.

## ai-devsecops-engineer

| Skill | Escopo |
|---|---|
| [dso-infrastructure-change](../profiles/ai-devsecops-engineer/skills/dso-infrastructure-change/SKILL.md) | Review or implement IaC and infrastructure changes with explicit target, plan, blast radius, approval and recovery. Use for Terraform, cloud resources and infrastructure migrations; not for a read-only conceptual question. |
| [dso-kubernetes-gitops](../profiles/ai-devsecops-engineer/skills/dso-kubernetes-gitops/SKILL.md) | Diagnose or change Kubernetes workloads and GitOps reconciliation using desired/live state, health, policy and storage evidence. Use for rollout, drift, capacity and admission issues; not for unconditional sync or restart. |
| [dso-cloud-security](../profiles/ai-devsecops-engineer/skills/dso-cloud-security/SKILL.md) | Review cloud architecture, network exposure and security controls with a threat model and evidence-backed findings. Use for hardening and cloud posture; do not claim compliance certification or run intrusive tests without scope. |
| [dso-identity-secrets](../profiles/ai-devsecops-engineer/skills/dso-identity-secrets/SKILL.md) | Design or troubleshoot IAM, workload identity, RBAC, OIDC and secret rotation with least privilege and safe recovery. Use for credential lifecycle and access boundaries; never request secret values in chat. |
| [dso-sre-incident](../profiles/ai-devsecops-engineer/skills/dso-sre-incident/SKILL.md) | Investigate service degradation, incidents, SLOs and operational toil with impact-first evidence. Use for live incidents and reliability reviews; do not restart blindly or confuse correlated logs with cause. |
| [dso-software-supply-chain](../profiles/ai-devsecops-engineer/skills/dso-software-supply-chain/SKILL.md) | Review CI/CD, dependencies, build provenance and artifact promotion with scoped permissions and verifiable release evidence. Use for pipeline and supply-chain changes; do not sign, publish or deploy without authorization. |

## ai-engineer

| Skill | Escopo |
|---|---|
| [aie-agent-architecture](../profiles/ai-engineer/skills/aie-agent-architecture/SKILL.md) | Design or evolve agent systems with explicit goals, tools, state, handoffs and stopping rules. Use for Hermes agents, tool-using workflows and orchestration; not to create extra agents for a simple deterministic task. |
| [aie-model-routing](../profiles/ai-engineer/skills/aie-model-routing/SKILL.md) | Design or diagnose LLM provider/gateway routes, fallbacks and compatibility with measurable quality, latency, cost and data boundaries. Use for routing policies and provider failures; do not silently change models or send data to another trust domain. |
| [aie-rag-memory](../profiles/ai-engineer/skills/aie-rag-memory/SKILL.md) | Design or diagnose RAG and persistent memory with provenance, access control, retention and retrieval evaluation. Use for knowledge ingestion and recall systems; do not treat memory as an unrestricted cross-client knowledge store. |
| [aie-agent-security](../profiles/ai-engineer/skills/aie-agent-security/SKILL.md) | Threat-model and harden agents, MCP tools and LLM applications against tool abuse, prompt injection and data leakage. Use before adding sensitive tools or autonomous execution; testing remains within explicit authorized scope. |
| [aie-agent-evaluation](../profiles/ai-engineer/skills/aie-agent-evaluation/SKILL.md) | Build and review evaluation suites for prompts, tools, models and agent workflows using baselines, held-out cases and observable evidence. Use before promotion or comparison; do not equate model judgments or mock tests with production proof. |
| [aie-llmops-observability](../profiles/ai-engineer/skills/aie-llmops-observability/SKILL.md) | Instrument, release and operate LLM/agent services with quality, latency, cost, traces and recovery evidence. Use for AI operations and model/prompt promotion; do not log sensitive prompts or assume model health proves task success. |

## software-engineer

| Skill | Escopo |
|---|---|
| [swe-codebase-discovery](../profiles/software-engineer/skills/swe-codebase-discovery/SKILL.md) | Inspect an unfamiliar repository and trace real execution/data paths before modifying it. Use for onboarding, impact analysis and legacy discovery; not for a speculative architecture diagram based only on folder names. |
| [swe-architecture-design](../profiles/software-engineer/skills/swe-architecture-design/SKILL.md) | Design application boundaries, contracts and data flows from requirements and quality attributes. Use for new products or consequential refactors; do not impose microservices, DDD or a framework without evidence. |
| [swe-vertical-slice-delivery](../profiles/software-engineer/skills/swe-vertical-slice-delivery/SKILL.md) | Implement a bounded feature or bug fix across the necessary application layers with working behavior, regression checks and a focused diff. Use for real product changes; do not replace requested implementation with a plan or expand scope silently. |
| [swe-api-data-contracts](../profiles/software-engineer/skills/swe-api-data-contracts/SKILL.md) | Design or evolve API and persistence contracts with validation, authorization, consistency and migration safety. Use for endpoints, schemas, integrations and data changes; do not assume a source rollback reverses data. |
| [swe-quality-verification](../profiles/software-engineer/skills/swe-quality-verification/SKILL.md) | Design and execute risk-based software checks, regression tests and code review with actual evidence. Use before claiming a change works or a release is ready; do not replace tests with model confidence or coverage percentages. |
| [swe-application-security](../profiles/software-engineer/skills/swe-application-security/SKILL.md) | Design, implement or review application security across authentication, authorization, input/data flows and session boundaries. Use for SaaS/web/API/local applications; do not claim a scanner or secure prompt replaces enforced controls. |
| [swe-release-maintenance](../profiles/software-engineer/skills/swe-release-maintenance/SKILL.md) | Prepare builds, packages, versioned changes and maintainable releases with compatibility and recovery evidence. Use for refactoring, dependencies and release readiness; do not publish or discard user changes automatically. |
| [swe-web-experience](../profiles/software-engineer/skills/swe-web-experience/SKILL.md) | Implement and verify web interfaces with real user flows, responsive layout, accessible interaction and explicit loading/error states. Use for frontend work; do not treat a screenshot, mock data or decorative polish as full functionality. |
| [swe-saas-engineering](../profiles/software-engineer/skills/swe-saas-engineering/SKILL.md) | Design or implement SaaS capabilities with tenant isolation, authorization, lifecycle and commercial rules when required. Use for multi-tenant products, entitlements and billing; do not add tenancy or subscriptions to every application. |
| [swe-local-crossplatform](../profiles/software-engineer/skills/swe-local-crossplatform/SKILL.md) | Develop local tools, CLI applications and desktop software with bounded OS integration, persistence and packaging. Use for offline or cross-platform products; do not assume web security, filesystem paths or packaging behave identically on every OS. |

## Compartilhadas

- [agent-folder-architect](../shared-skills/agent-folder-architect/SKILL.md)
- [project-context-architect](../shared-skills/project-context-architect/SKILL.md)

Nenhuma skill cria permissão, conta, provider, infraestrutura ou aplicação automaticamente.
