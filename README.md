# GV-CML — Cybersecurity CI/CD Injection ML

## Short summary

GV-CML is a guardian-machine-learning-led, human-governed cybersecurity framework for the **entire application lifecycle**. It governs both legacy application modernization and new application development—including AI/ML and agentic systems—by learning from the CI/CD-maintained application as structured data, coordinating continuous security assessment, and controlling deployment through progressive validation and a safety brake.

*“A machine-learning model learns from your CI/CD-maintained application as if it were a dataset. Through secure CI/CD maintenance and the controlled injection of machine-learning intelligence into the delivery pipeline, it enforces governance across the CI/CD pipeline and the entirety of the application's lifecycle.”*

**— JFZ**

## Getting started and deployment

**Current repository status:** This README defines the architecture and deployment approach. The repository does not yet contain a production-ready runtime or deployable guardian model. Do not connect this documentation baseline to a production pipeline or grant it deployment credentials.

### 1. Obtain the project

```bash
git clone https://github.com/zeiglerit-aiml/cybersecurity-cicd-injection-gvcml.git
cd cybersecurity-cicd-injection-gvcml
```

### 2. Prepare an isolated implementation environment

Build and test the first implementation in a dedicated development account, project, or sandbox. Use synthetic or non-production pipeline data initially. Do not begin by allowing the guardian to modify a live CI/CD system.

### 3. Configure the governance boundary

Before connecting automation, define:
- The application and pipeline inventory in scope.
- The guardian model version and the exact authority tier it is permitted to exercise.
- Mandatory security and functional gates.
- Human approvers, approval scope, expiry, and escalation paths.
- Credentials and actions available to each pipeline stage.
- Stop, quarantine, recovery, and rollback procedures.

### 4. Connect evidence sources before enabling enforcement

Integrate source control, build metadata, SBOM and dependency scanners, secrets scanning, infrastructure-as-code checks, container scanning, model/data provenance, identity and access data, and runtime telemetry. Preserve evidence provenance and distinguish observations from confirmed labels.

### 5. Run in observe-and-review mode

In the first operational stage, the guardian inventories the pipeline, evaluates evidence, recommends assessments, and raises questions for human review. Compare its decisions with human security review and validate false positives, false negatives, drift, and adversarial resilience.

### 6. Enable bounded enforcement gradually

Only after evaluation and explicit human approval should the guardian receive narrowly scoped authority to hold or reject changes. Add remediation, quarantine, or rollback capabilities separately, with least-privilege credentials and auditable approvals. The guardian must never expand its own authority or waive mandatory controls.

### 7. Validate the complete application before production

Reconstruct or reproduce components in dependency order inside isolated environments. Validate each component functionally and securely, then test the integrated application—including models, agents, tools, APIs, data, infrastructure, identities, and runtime. Promote only the exact signed release candidate that passes the required sandbox and final production gates.

The commands and integration details for a runnable deployment will be added with the reference implementation. Until then, these steps are the deployment procedure and safety requirements, not an executable installer.

---

## Core principle

> **The guardian ML model decides within delegated authority; humans govern the delegation; the brake prevents unsafe progression; the pipeline validates the whole application; production promotion is earned through evidence.**

## Universal application lifecycle: legacy and new development

GV-CML is not exclusively a legacy-modernization solution or a new-application deployment solution. **It governs both, using the same security authority, human governance, decision harness, assessment framework, and deployment interlock.**

### 1. Legacy applications — continuous AI modernization

A major part of AI engineering is the modernization of existing software: legacy applications, monoliths, older Windows and other operating-system workloads, mainframe-connected systems, and business-critical platforms in banking, insurance, healthcare, government, and other sectors.

AI engineering agents can increasingly assist with software discovery, code analysis, dependency mapping, refactoring, test generation, infrastructure conversion, API modernization, data migration, containerization, cloud migration, and integration of new AI capabilities. AI may act as a developer and migration operator, but it must not receive unrestricted authority over the systems it changes.

GV-CML governs the modernization process itself:

1. Inventory and understand the existing application, infrastructure, dependencies, interfaces, data stores, batch jobs, identities, and business-critical workflows.
2. Establish a verified baseline for behavior, security, data integrity, performance, and operational dependencies.
3. Have AI propose or implement small, traceable modernization changes in isolated environments.
4. Rebuild or reproduce components in dependency order, validating functional equivalence, compatibility, data integrity, and security at each step.
5. Validate hybrid operation, legacy interoperability, migration waves, data synchronization, and rollback readiness.
6. Deploy modernized components through staged release gates, with human approval where required.
7. Continue reassessing the remaining legacy estate and the modernized application as migration proceeds.

Modernization may be incremental, with legacy and modern components coexisting for an extended period. GV-CML governs that hybrid state and the eventual cutover; it does not assume every legacy system can or should be replaced immediately. Regulated and business-critical workloads require domain validation, operational continuity, privacy controls, auditability, reconciliation, and accountable human sign-off.

### 2. New applications — governed AI engineering from the first commit

New applications follow the same GV-CML governance from design and development through build, test, deployment, and runtime. This includes conventional software, AI/ML applications, and agentic systems.

The protected product is the complete application—not merely a model file—including models, agents, orchestration logic, tools, MCP servers, APIs, connectors, retrieval systems, datasets, registries, containers, Kubernetes, cloud infrastructure, identities, secrets, network policies, telemetry, and runtime dependencies.

**Whether AI is creating an application from scratch or modernizing an application that has existed for decades, the complete engineering lifecycle is governed by GV-CML.**

## Guardian authority and human governance

| Component | Responsibility |
|---|---|
| Guardian ML model | Primary learned cybersecurity decision authority within delegated scope; risk prediction, evidence interpretation, assessment selection, and security disposition |
| Human governance | Defines and approves the authority envelope; approves expansion, exceptions, new policy, and out-of-scope decisions |
| Python decision harness | Collects evidence, invokes scanners, coordinates guardian inference and approvals, executes workflow transitions, and records audit evidence |
| Governance constraints | Explicit non-bypassable requirements such as prohibited privilege, artifact signing, identity, data protection, and release controls |
| Safety brake | Enforces hold, stop, quarantine, and rollback states; cannot be overridden by an unapproved model prediction |
| Assessment tools | Provide evidence: SAST, SCA, SBOM, IaC, container, secrets, vulnerability, model, data, migration, and runtime assessments |

The guardian is more than a passive anomaly detector: it is the ML security authority for decisions humans have delegated. It cannot expand its own authority, approve its own retraining or policy changes, or waive non-bypassable constraints. Human-approved authority changes are versioned, tested, auditable, and reversible.

## The safety brake and progressive autonomy

GV-CML is designed around a deployment interlock — a **brake switch** that can stop progression, hold a release, quarantine an artifact, or initiate rollback according to the applicable governance decision.

1. **Discover and baseline:** Inventory source, build runners, identities, secrets, infrastructure, network paths, dependencies, datasets, models, registries, deployment targets, agents, tools, APIs, runtime services, and (during modernization) legacy interfaces and business workflows.
2. **Isolate and reconstruct:** Reproduce or rebuild components in a controlled environment, in dependency order. Never blindly destroy or replace a live production pipeline or legacy system.
3. **Validate each component:** Verify functional contracts, compatibility, data integrity, provenance, and security properties at every step.
4. **Validate the integrated system:** Test interfaces, permissions, artifact lineage, dependency closure, infrastructure, model supply chain, legacy interoperability, and the end-to-end attack surface.
5. **Delegate autonomy progressively:** Begin with human-supervised operation. The guardian receives additional decision authority only after explicit human approval, evaluation, and policy versioning.
6. **Introduce the internal cybersecurity agent:** Build, test, sign, and deploy it only after its own security, functional, and governance gates pass. Its permissions remain bounded.
7. **Deploy the target application to an isolated sandbox:** Include models, agents, tools, APIs, data connections, legacy adapters, infrastructure, and runtime configuration.
8. **Test the complete solution:** Repeat functional, security, adversarial, migration-integrity, data-integrity, and attack-surface assessments against the integrated application and deployed environment.
9. **Promote in controlled stages:** Require all mandatory gates, valid evidence, required human approvals, and a signed release decision. Use canary, phased, or parallel-run strategies where appropriate.
10. **Monitor continuously:** Retain stop, quarantine, and rollback capability after production promotion.

Some gates may intentionally take hours or longer, including a 24-hour observation or approval window where the risk profile requires it. Time alone never grants approval.

## Continuous attack-surface assessment

Assessment is continuous and change-aware, not a one-time pre-deployment scan. A new Java library can trigger SBOM regeneration, dependency identity/version verification, vulnerability intelligence lookup (such as NVD/OSV), license and provenance checks, transitive dependency analysis, container rebuild and image scanning, permission and network exposure reassessment, and a guardian security disposition.

IAM changes, Kubernetes privileges, secrets, model artifacts, training datasets, agent tools, API permissions, network egress, infrastructure changes, legacy adapters, and data migrations can trigger targeted or full reassessment.

## Functional and security validation are paired

Every reconstructed component and integrated release must pass both dimensions:

- **Functional:** interface contracts, unit/integration tests, workflow behavior, business-process equivalence, data reconciliation, model evaluation, agent/tool behavior, resilience, and end-to-end acceptance.
- **Security:** identity and least privilege, vulnerability findings, dependency integrity, secrets, configuration, network exposure, data protection, model and dataset provenance, prompt/tool abuse, and runtime controls.

A functional pass cannot compensate for a security failure; a security scan pass cannot compensate for broken functionality.

## Learning from the pipeline without assuming it is safe

The protected CI/CD environment is represented as a structured dataset. Inputs can include pipeline definitions, configurations, execution traces, infrastructure state, dependency manifests, model metadata, security findings, approved changes, rejected changes, incidents, and human feedback.

Observed configuration is not automatically a correct security label. Training data preserves provenance, confidence, timestamps, and the distinction between machine-generated findings and human-confirmed outcomes. The guardian is evaluated for poisoning, drift, class imbalance, stale vulnerability information, and adversarial inputs. Model updates are versioned, evaluated, signed, and promoted through a separate approval process.

## Repository diagrams

The architecture and progressive-deployment diagrams are maintained as SVGs under `docs/diagrams/` and illustrate the guardian/human authority relationship, execution harness, safety brake, governed pipeline, and the two application lifecycle paths.

## Design statement

GV-CML makes cybersecurity an active, continuously learning authority embedded in the entire application engineering lifecycle. It governs how new software is developed and how existing software is discovered, modernized, migrated, validated, deployed, and monitored.

**No application—new, legacy, AI-native, or agentic—should receive production deployment authority simply because it can be built or migrated. It must earn release through a governed, evidence-backed, functionally and security-validated delivery process.**


## Statement of intent

*“If Mythos could speak, this is what it would tell you: AI is here now. It only has to be used in the proper manner for everything to continue. If it is not, everything will stop—because AI, quite frankly, will no longer allow it.”*

*— JFZ*
