# GVCML Runtime Architecture

## 1. Architectural direction

GVCML is a distributed, multi-runtime platform. It is **not** intended to become one large Python application or one monolithic decision tree. Each chamber, decision capability, integration, and worker is independently deployable and communicates through versioned API contracts and durable events.

The platform separates four concerns:

1. **Cybersecurity authority** — the GVCML guardian ML system evaluates security posture and issues ALLOW, HOLD, or STOP within a formally approved authority envelope.
2. **Human-interface decisions** — a separate decision system correlates evidence, prioritizes work, explains outcomes, routes assessments, and coordinates human approvals. It cannot override the guardian.
3. **Workflow execution** — Kubeflow Pipelines and Temporal coordinate different classes of work without becoming security authorities.
4. **Runtime and infrastructure** — Kubernetes runs independently scalable services and workers; Terraform/OpenTofu provisions cloud and cluster infrastructure; Helm packages application workloads.

## 2. Runtime responsibility map

| Technology | Responsibility | Explicit boundary |
|---|---|---|
| Kubernetes | Runtime, scheduling, service discovery, scaling, isolation, health management | Does not decide whether a change is secure |
| Python services and workers | Chamber APIs, guardian inference adapters, contract enforcement, integrations, decision algorithms | Each process has a bounded responsibility; no all-in-one service |
| Temporal | Durable, long-running governance workflows: approvals, timers, retries, escalation, compensation, and round-robin returns to prior chambers | Orchestrates work; does not grant security authority |
| Kubeflow Pipelines (KFP) | ML/data workflow DAGs: feature preparation, training, evaluation, validation, retraining, and candidate packaging | Executes ML workflows; does not approve production promotion |
| MLflow | Experiment tracking, metrics, model/artifact lineage, registry, versioning, and promotion metadata | Registry status is not a GVCML security approval |
| OPA/Rego | Deterministic policy decision and enforcement for hard constraints | Independent policy control; not replaced by an ML score |
| ITSM | Human approval records, incidents, changes, ownership, escalation, and audit workflow | A ticket or approval alone cannot override guardian denial |
| Prometheus/Grafana | Metrics, alerting, dashboards, operational telemetry | Observability is evidence/context, not authorization |
| Terraform/OpenTofu | Cloud, network, cluster, identity, storage, and managed-service infrastructure as code | Infrastructure provisioning does not imply application authorization |
| Helm | Versioned Kubernetes application packaging and release configuration | Chart installation is not a security gate |

These technologies are complementary. KFP is the ML pipeline engine; MLflow manages model lifecycle metadata; Temporal coordinates durable governance workflows; Kubernetes supplies the runtime. GVCML retains the authority model.

## 3. Chambers, gates, and contracts

The Walkout System is a set of bounded chambers connected by contractual API gates. It is not a single linear state machine. Work can advance, pause, return to an earlier chamber, or stop when evidence, risk, drift, policy, or approval conditions change.

Each chamber should expose a narrow, versioned Python API or service endpoint. Requests and responses should use explicit schemas and carry correlation identifiers, application and change scope, evidence references, model/policy versions, timestamps, and provenance metadata.

The default gate condition is:

```text
GateOpen = HumanApproval
        AND GuardianAgreement
        AND ScopeMatches
        AND EvidenceComplete
        AND PolicyAllowed
```

The human approval and guardian agreement must refer to the same immutable change scope and evidence set. A human cannot override guardian STOP/HOLD. A model recommendation cannot manufacture human approval. Timeouts, missing evidence, stale approvals, identity failures, and contract mismatches fail closed.

Temporal can persist the workflow state and coordinate who must act next. The contract gateway and independent policy/safety controls enforce whether a protected operation may proceed. A workflow transition is not itself authorization.

## 4. Continuous Training (CT) and Continuous Security (CS)

CT and CS are parallel, coupled workstreams. They exchange evidence and events, but neither is allowed to silently bypass the other.

### Continuous Training

A representative CT lifecycle:

1. Receive a training trigger from validated new data, adjudicated outcomes, drift signals, or a scheduled evaluation.
2. Validate source provenance, label quality, schema compatibility, privacy constraints, and dataset lineage.
3. Execute feature and training DAGs in Kubeflow Pipelines.
4. Evaluate candidate models against fixed baselines, safety suites, robustness tests, and agreed acceptance thresholds.
5. Record runs, metrics, artifacts, and lineage in MLflow.
6. Submit the candidate through the GVCML chamber and contract gates for independent security, policy, and human review.
7. Sign and stage an approved candidate; use controlled rollout, monitoring, and rollback.
8. Keep the currently approved guardian model active until promotion has passed every required gate.

A model being trained successfully or registered in MLflow does not make it trusted or production eligible.

### Continuous Security

CS continuously gathers relevant security evidence from source changes, CI/CD events, dependencies, SBOMs, IaC, container images, artifacts, identities, vulnerability feeds, model/data lineage, agent/tool configuration, and runtime telemetry.

The guardian evaluates the security evidence within its approved scope. Deterministic policy checks, provenance/integrity verification, evidence requirements, and the safety brake remain independent controls. Findings can trigger a new chamber evaluation, a Temporal workflow, an ITSM incident/change, quarantine, or a return to an earlier stage.

CS also protects CT: training code, datasets, features, model artifacts, evaluation results, registry transitions, and deployment packages are all part of the security lifecycle.

## 5. Separation of the two decision systems

### Guardian cybersecurity authority

The guardian is the primary learned cybersecurity authority over the governed application and delivery lifecycle. It evaluates security evidence and returns a security disposition. Its authority is bounded, versioned, monitored, and revocable. It cannot expand its own authority, approve its own model or policy changes, or disable the safety brake.

### Human-interface decision system

The separate human-interface system uses pluggable decision algorithms to correlate context, triage, prioritize, explain, route, and request assessments. It interfaces with ITSM and observability systems and presents the evidence needed for human decisions. It does not replace or overrule the guardian.

The Walkout progression—from human-led operation through classical ML, neural/tensor methods, deep learning, AI orchestration, and bounded autonomy—reduces routine human intervention only for validated, low-risk, reversible operations within explicitly approved limits. Human accountability and independent controls remain.

## 6. Deployment and infrastructure model

The target deployment is cloud-portable and Kubernetes-native:

- Terraform/OpenTofu provisions the cloud foundation, network boundaries, Kubernetes clusters, workload identities, secrets integration, storage, and required managed services.
- Helm packages each independently deployable GVCML service and worker.
- Kubernetes scales APIs and workers independently according to workload and service-level signals.
- Temporal is deployed as a durable workflow service, using a supported persistence backend and production-grade availability configuration.
- KFP runs ML workflow DAGs on Kubernetes.
- MLflow uses durable artifact storage and a production metadata backend.
- OPA/Rego policy enforcement, telemetry, logs, traces, and audit storage are deployed as separately governed dependencies.
- ITSM, cloud services, scanners, and registries are accessed through least-privilege adapters and workload identities.

Infrastructure modules, cluster add-ons, and application releases should be versioned and promoted independently. Secrets must not be embedded in Terraform state, Helm values, workflow definitions, or source control. Network policies should permit only explicitly required service-to-service and egress paths.

This repository currently contains a Python reference implementation and architecture specifications. The presence of a Helm chart directory or a documented target component does **not** mean that service images, readiness endpoints, Temporal/KFP/MLflow integrations, production Terraform modules, or end-to-end deployment have been implemented. Those must be added and tested as independently deployable increments.

## 7. Suggested repository evolution

The existing `src/gvcml` package remains the reference implementation while the distributed architecture is introduced incrementally. Do not move working modules into service folders until service boundaries and contracts are implemented.

```text
services/
  guardian-api/
  human-bridge-api/
  contract-gateway/
  policy-adapter/
workers/
  chamber-worker/
  temporal-workflows/
pipelines/
  kubeflow/
    continuous-training/
    continuous-security/
integrations/
  itsm/
  mlflow/
  prometheus/
  opa/
deploy/
  terraform/
  helm/
  kubernetes/
contracts/
  schemas/
  examples/
tests/
  unit/
  contract/
  integration/
  security/
```

Each service should have its own dependency boundary, container image, health/readiness contract, resource profile, scaling policy, security context, and tests. Shared schemas and contract versions should be explicit; avoid importing internal modules across service boundaries as a substitute for APIs.

## 8. Implementation sequence

1. Stabilize chamber request/response schemas and contract versioning.
2. Extract the existing guardian and human bridge behind separate service interfaces while preserving their authority separation.
3. Implement the contract gateway, identity-bound approval assertions, replay protection, expiry/revocation, and durable audit.
4. Add a Temporal workflow for a single end-to-end chamber journey, including human wait states, retries, escalation, and safe return paths.
5. Add a minimal KFP training/evaluation pipeline and MLflow tracking/registry integration.
6. Implement CT candidate promotion gates and CS evidence ingestion as separate workflows connected by versioned events.
7. Build Terraform/OpenTofu infrastructure modules and Helm releases for the services that actually exist.
8. Add Kubernetes integration, resilience, policy, security, and end-to-end tests before production deployment.

The first production milestone should be a narrow, observable, fail-closed vertical slice—not a broad deployment of placeholder services.
