# GVC_ML — Cybersecurity CI/CD Injection ML

## Executive summary

GVC_ML is a guardian-machine-learning-led, human-governed cybersecurity framework for the **entire application lifecycle**. It governs legacy modernization and new application development—including AI/ML and agentic systems—by learning from the CI/CD-maintained application as structured data, coordinating continuous security assessment, and controlling delivery through progressive validation and a safety brake.

*“A machine-learning model learns from your CI/CD-maintained application as if it were a dataset. Through secure CI/CD maintenance and controlled injection of machine-learning intelligence into the delivery pipeline, it enforces governance across the CI/CD pipeline and the entirety of the application's lifecycle.”*

**— JFZ**

## Installation

Requirements: Python 3.10+, Git, and an isolated environment.

```bash
git clone https://github.com/zeiglerit-aiml/cybersecurity-cicd-injection-gvcml.git
cd cybersecurity-cicd-injection-gvcml
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[ml,dev]"
```

## Quick start

Train the guardian using the included synthetic, illustrative, human-labelled fixture:

```bash
gvcml train --dataset data/guardian_training.csv --output artifacts/guardian.joblib
gvcml demo --model artifacts/guardian.joblib
```

Evaluate an event:

```bash
gvcml evaluate --model artifacts/guardian.joblib \
  --event examples/events/unknown_agent_tool.json \
  --evidence examples/evidence/passing_sandbox.json
```

Run tests: `python -m pytest`.

**Important:** the included training data is a demonstration fixture, not production training data. Do not use this initial model to authorize real deployments.

## Configuration and authority

Configuration: `config/governance.json`. The reference implementation starts in human-supervised mode. The guardian predicts ALLOW, HOLD, or STOP from structured pipeline features. The decision harness enforces mandatory evidence and explicit human release approval.

- Guardian ML is the primary learned cybersecurity decision authority within a human-approved scope.
- Humans define, expand, and revoke that authority.
- Python is the execution and orchestration harness, not the source of security authority.
- Mandatory controls cannot be bypassed by model predictions.
- The safety brake holds or stops progression when evidence or approval is missing.

Do not connect production credentials or live deployment systems until the model, labels, policy, scanner adapters, threat model, identity controls, and recovery procedures have been independently evaluated.

## Deployment model

GVC_ML governs both lifecycle paths:

1. **Legacy modernization:** inventory and baseline the existing application, infrastructure, data, interfaces, and business workflows; apply AI-assisted changes in isolated environments; validate functional equivalence, data integrity, compatibility, and security; migrate in controlled waves.
2. **New application development:** govern design, source, dependencies, build, infrastructure, model/data pipelines, agents, tools, APIs, deployment, and runtime from the first commit.

For either path, components are reproduced in dependency order in isolated environments, validated functionally and securely, integrated, tested as a complete application in a sandbox, and promoted only after required evidence and approvals pass. Never destructively rebuild a live production environment in place.

## Architecture

![GVC_ML architecture](docs/diagrams/gvcml-architecture.svg)

![GVC_ML progressive deployment](docs/diagrams/progressive-deployment.svg)

The guardian learns from pipeline definitions, configurations, execution metadata, security findings, artifact provenance, and human-validated outcomes. Existing pipeline state is not automatically ground truth. Training data must distinguish observations, scanner output, confirmed vulnerabilities, policy compliance, and human-adjudicated labels.

## Project structure

```text
config/                 Governance configuration
data/                   Synthetic labelled training fixture
docs/                   Architecture and SVG diagrams
examples/               Sample pipeline events and evidence
policies/               Rego policy example
src/gvcml/              Guardian, feature extraction, brake, harness, CLI
tests/                  Unit and safety-invariant tests
.github/workflows/      Continuous integration
```

## Current implementation scope

The initial reference implementation includes a trainable Random Forest guardian, versioned feature schema, confidence-based HOLD behavior, human approval gate, fail-safe brake, evidence requirements for functional/security/signing/sandbox validation, CLI training/evaluation/demo, unit tests, and GitHub Actions CI.

Scanner, cloud, identity, artifact-signing, sandbox, and production deployment integrations are extension points, not yet live integrations. The Rego example is illustrative and is not yet connected to an OPA server.

## Security and operations

Treat training data, model artifacts, event payloads, and scanner output as untrusted until provenance is verified. Separate training, policy-promotion, and production credentials. Use least privilege and isolated runners. Log model/policy versions, evidence references, approvals, and decisions. Test poisoning, drift, false positives, false negatives, and adversarial inputs. Keep rollback and quarantine paths available. A timeout is never an approval.

## Testing and troubleshooting

```bash
python -m pytest -q
gvcml --help
gvcml train --help
gvcml evaluate --help
```

If the command is missing, activate the virtual environment and reinstall with `python -m pip install -e ".[ml,dev]"`. If model loading fails, retrain it against the current feature schema.

## Roadmap

1. Signed SBOM and provenance ingestion.
2. SAST, SCA, secrets, IaC, container, model, and runtime scanner adapters.
3. OPA/Rego execution and signed policy bundles.
4. Pipeline inventory and dependency-ordered reconstruction adapters.
5. Human approval service and tiered guardian authority management.
6. Isolated sandbox and immutable production promotion adapters.
7. Guardian evaluation, drift monitoring, poisoning defenses, and retraining governance.
8. AWS, Azure, and GCP integrations.

## Contributing

Include tests, security rationale, and provenance for contributed training data. Changes to governance policy, guardian authority, or labels require explicit review. Never submit credentials, production secrets, private customer data, or proprietary pipeline exports.

## License

No license has been selected. Until one is added, all rights are reserved; do not assume unrestricted reuse.

## Statement of intent

*“If Mythos could speak, this is what it would tell you: AI is here now. It only has to be used in the proper manner for everything to continue. If it is not, everything will stop—because AI, quite frankly, will no longer allow it.”*

*— JFZ*
