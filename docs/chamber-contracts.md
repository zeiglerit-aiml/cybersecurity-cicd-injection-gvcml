# GVCML Chamber Contracts and Gate APIs

## Architecture

The Walkout System is organized as chambers connected by contractual gates. A chamber owns a bounded responsibility and exposes typed APIs. A gate is an authorization boundary: it validates a contract before allowing a request to enter the next chamber or invoke a protected operation.

The chamber model is not a simple linear pipeline. The round-robin control loop can route a request back to human review, evidence collection, ML triage, neural analysis, deep-learning analysis, AI orchestration, or the guardian security authority when conditions change.

## Dual agreement

For a governed chamber transition, the default authorization rule is conjunctive:

`HUMAN_APPROVAL AND GUARDIAN_AGREEMENT AND SCOPE_MATCH AND EVIDENCE_COMPLETE AND POLICY_ALLOWED`

All required conditions must be true. Human approval cannot override a guardian STOP, policy denial, incomplete evidence, or an out-of-scope contract. Guardian agreement does not manufacture human approval where the workflow requires it.

An approved standing contract may delegate a narrowly defined class of low-risk reversible operations. Each operation must still match the contract scope and pass current guardian, policy, evidence, and safety-brake checks. A standing contract is not a blanket approval for unrelated changes.

## Python API contract

`src/gvcml/contracts.py` provides:

- `GateContract`: immutable claims binding an approval to an application, exact change, source chamber, target chamber, human reviewer, guardian model version, scope, evidence, and policy result.
- `evaluate_gate(contract)`: returns a structured `GateReceipt` without executing the protected operation.
- `enforce_gate(contract)`: fails closed with `GateDenied` unless every required condition passes.
- `@requires_gate`: decorator for Python functions that must not run until the contract is enforced; the function receives the resulting gate receipt.

Example:

```python
from gvcml.contracts import GateContract, Chamber, requires_gate

@requires_gate
def promote_release(release_id: str, *, gate_receipt):
    # Invoke the separately protected deployment adapter here.
    return {"release_id": release_id, "contract": gate_receipt.contract_id}

contract = GateContract(
    contract_id="GVCML-CHG-42",
    application_id="payments-api",
    change_id="CHG-42",
    from_chamber=Chamber.HUMAN_GOVERNANCE,
    to_chamber=Chamber.BOUNDED_EXECUTION,
    human_approved=True,
    human_reviewer="reviewer-id",
    guardian_agreed=True,
    guardian_model_version="guardian-v1",
    scope_matches=True,
    evidence_complete=True,
    policy_allowed=True,
)

result = promote_release("release-42", contract=contract)
```

## Security boundary and production requirements

The Python contract object is an executable authorization interface, not proof that the claims are authentic. The current reference implementation trusts the caller-supplied booleans and identity/version strings. A production implementation must not accept those values directly from an untrusted API request.

Production adapters must:
1. Authenticate the human reviewer and service identities.
2. Verify signed, attributable approval and guardian decision assertions.
3. Bind approval to the exact application, change, artifact digest, policy version, model version, target chamber, permitted actions, and expiry.
4. Prevent replay and duplicate execution with unique contract IDs, nonces/idempotency keys, and durable state.
5. Verify current evidence and policy at execution time, not only when approval was first recorded.
6. Revoke or expire contracts when scope, evidence, model, policy, or risk context changes.
7. Emit tamper-evident audit events and preserve the gate receipt.
8. Keep the independent safety brake and deployment authorization checks in the final execution path.

Use JSON Schema or typed API models to validate payload shape at service boundaries. Use OPA/Rego or equivalent policy enforcement for independently evaluated deterministic constraints. Python function contracts orchestrate and enforce the application-level call boundary; they do not replace identity, cryptographic verification, policy evaluation, or infrastructure authorization.

## Contract states

A production workflow should distinguish at least:

- `PROPOSED`: a chamber requests a transition or operation.
- `AWAITING_HUMAN`: explicit human approval is pending.
- `AWAITING_GUARDIAN`: the guardian has not agreed or must reassess.
- `VALIDATING`: scope, evidence, policy, identity, and freshness are checked.
- `AUTHORIZED`: every required contractual condition passed.
- `DENIED`: a mandatory condition failed.
- `EXPIRED` / `REVOKED`: an earlier authorization is no longer valid.
- `EXECUTED`: the authorized action completed and its outcome was recorded.

Authorization and execution are separate events. A successful gate does not prove that the downstream action succeeded; execution must return evidence and an outcome to the round-robin governance loop.
