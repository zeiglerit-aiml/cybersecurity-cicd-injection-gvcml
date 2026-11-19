# GVCML Walkout System

## Mission

GVCML addresses the security and governance risks created as AI becomes capable of building, modifying, testing, deploying, and operating software at increasing speed. The strategic direction is to let capable automation handle more routine engineering and security work while ensuring that the authority, controls, evidence, and recovery mechanisms are designed before autonomy is expanded.

No architecture can guarantee that AI is always correct or universally more capable than people. GVCML therefore treats autonomy as an engineered capability that must be demonstrated, scoped, monitored, and revocable—not as an assumption that AI should simply be trusted.

## Two distinct decision systems

### 1. GVCML guardian: cybersecurity authority

The guardian machine-learning model is the primary learned cybersecurity authority over the CI/CD pipeline and the application lifecycle governed through the GVCML injection architecture. It evaluates application and pipeline evidence across source, build, dependencies, infrastructure, identity, data, models, agents, deployment, and runtime.

The guardian's security disposition is authoritative within its formally approved scope. It is not replaced or overruled by the human-interface algorithms, ITSM, Prometheus, Grafana, or an AI orchestrator.

Deterministic policy constraints, provenance requirements, mandatory evidence gates, and the safety brake remain independent, non-bypassable controls. The guardian cannot expand its own authority, approve its own policy or model updates, or override the brake.

### 2. Human-interface decision system: triage and approval bridge

A separate decision system—initially human-led and progressively augmented by machine-learning decision algorithms—works with the human approval process. Its job is to make complex security and engineering decisions readable, prioritized, traceable, and actionable.

It can:
- Correlate guardian decisions with asset, application, change, incident, and operational context.
- Prioritize and route work using risk, impact, urgency, uncertainty, and model disagreement.
- Select additional assessments and request missing evidence.
- Present a readable explanation of the guardian's disposition and supporting evidence.
- Create and update ITSM incidents, changes, tasks, approvals, and escalations.
- Capture human approvals, rejections, exceptions, rationale, and outcomes as governed feedback.
- Route high-impact, irreversible, ambiguous, conflicting, or out-of-scope cases to qualified humans.

The human-interface decision system does not make the cybersecurity disposition. It helps the human interact with the authority that does.

## ITSM and observability bridge

ITSM is the workflow and audit system of record for ownership, incidents, changes, approval tasks, escalation, and review history. The human-interface decision system connects guardian findings to those workflows.

Prometheus supplies metrics and operational telemetry. Grafana presents dashboards and correlated signals for investigation and review. They are evidence and observability sources—not the security authority and not substitutes for an attributable human approval.

A typical cycle is:

1. A source, build, infrastructure, deployment, or runtime event enters the GVCML injection pipeline.
2. The guardian evaluates the event and returns its security disposition, confidence, rationale, and model version.
3. The independent policy gates and safety brake enforce mandatory constraints.
4. The human-interface decision system correlates the result with application context, telemetry, and prior adjudicated outcomes.
5. It routes the work and creates or updates the relevant ITSM record.
6. Prometheus/Grafana context and evidence references are presented to the reviewer.
7. A human approves, rejects, requests more evidence, or escalates when human authorization is required.
8. The decision and evidence are bound to the exact change, artifact, guardian version, policy version, and approval record.
9. Outcomes feed governed evaluation and learning datasets. Reassessment can reopen the workflow at any time.

## Pyramid triage and round-robin progression

The pyramid describes increasing analytical capability and decreasing routine human intervention. It is not a one-way removal of human governance.

1. **Human-led baseline:** people decide; the system records evidence, rationale, approval, rejection, and outcome.
2. **Classical ML decision algorithms:** models assist classification, correlation, prioritization, routing, and recommendation. Humans remain the approval bridge.
3. **Tensor and neural learning:** validated neural models add representation learning, sequence analysis, and multi-signal interpretation where justified by data and evaluation.
4. **Deep-learning capabilities:** deeper architectures can analyze complex telemetry, artifacts, relationships, and behavior. Outputs remain bounded and evaluated.
5. **AI orchestration:** AI can synthesize context, coordinate models and tools, request assessments, prepare ITSM work, and propose or prepare actions.
6. **Bounded autonomy:** explicitly delegated, low-risk, reversible actions may be executed automatically when the guardian allows them and every policy/evidence gate passes.

The levels operate as a round-robin feedback loop. Human adjudications become governed training/evaluation data; model outputs are checked against subsequent outcomes; telemetry can change risk; uncertainty or drift sends work back to earlier stages; and escalation remains available at every point. The system may move down the pyramid whenever risk rises or confidence falls.

## Walking the human out—without removing human governance

"Walking the human out" means reducing routine human intervention for well-understood, low-risk, reversible work as measured performance and controls justify it. It does not mean eliminating human accountability or making every decision autonomous.

Each increase in delegated authority requires:
- Explicit human authorization and a documented scope.
- Representative offline and operational evaluation.
- Policy and threat-model review.
- Provenance and model/policy version control.
- Monitoring, auditability, and rollback readiness.
- A tested path to stop, quarantine, revert, and return the decision to a human.

High-impact, irreversible, critical, uncertain, policy-sensitive, or conflicting cases remain subject to human review. Humans retain authority over the autonomy envelope, policy changes, model promotion/retraining, exceptions, and emergency governance.

## Application-aware, lifecycle-wide coverage

The same governance principles cover legacy on-premises systems, hybrid infrastructure, modernized applications, cloud-native software, and AI/ML or agentic applications. Their sensors, threat models, evidence sources, risk thresholds, and review paths are not identical.

The system selects assessments based on actual architecture and change context. Signals can include source-control events, CI/CD metadata, SBOMs, SAST/SCA, secrets and IaC scans, cloud and Kubernetes audit events, identity changes, runtime metrics, model/data lineage, agent tool permissions, API exposure, and legacy adapter or migration health.

## Governing invariants

- The GVCML guardian is the cybersecurity authority over the governed CI/CD/application lifecycle.
- The human-interface decision system is a separate triage, explanation, routing, and approval bridge.
- ITSM records workflow and approval; Prometheus and Grafana provide observability.
- Human approvals are explicit, attributable, scoped, time-bound where appropriate, and bound to the exact change/evidence.
- Mandatory policy, evidence, provenance, and safety-brake controls cannot be bypassed by ML, neural networks, deep learning, AI, ITSM, or observability systems.
- Autonomy is incremental, measured, bounded, reversible, and revocable.
- The feedback loop remains closed: evidence, decisions, outcomes, telemetry, learning, and reassessment continuously inform governance.

## Implementation status

This document defines the target architecture. The repository's initial code provides reference contracts and a local decision-flow demonstration; it does not yet provide production ML triage models, live ITSM connectors, Prometheus/Grafana integrations, neural/deep-learning models, or autonomous deployment adapters. Those integrations require separate implementation, security review, and validation.
