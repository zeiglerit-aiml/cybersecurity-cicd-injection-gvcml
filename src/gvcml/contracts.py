"""Machine-enforced approval contracts for chamber-to-chamber API calls.

These are technical authorization contracts, not legal agreements. A production
adapter must authenticate identities and verify signed approval/guardian
assertions before constructing a trusted GateContract.
"""
from dataclasses import dataclass
from enum import Enum
from functools import wraps
from typing import Callable, TypeVar, Any


class Chamber(str, Enum):
    HUMAN_GOVERNANCE = "HUMAN_GOVERNANCE"
    ML_TRIAGE = "ML_TRIAGE"
    NEURAL_ANALYSIS = "NEURAL_ANALYSIS"
    DEEP_LEARNING_ANALYSIS = "DEEP_LEARNING_ANALYSIS"
    AI_ORCHESTRATION = "AI_ORCHESTRATION"
    GUARDIAN_SECURITY_AUTHORITY = "GUARDIAN_SECURITY_AUTHORITY"
    BOUNDED_EXECUTION = "BOUNDED_EXECUTION"


@dataclass(frozen=True)
class GateContract:
    """Immutable authorization claim bound to one application change and gate."""
    contract_id: str
    application_id: str
    change_id: str
    from_chamber: Chamber
    to_chamber: Chamber
    human_approved: bool
    human_reviewer: str
    guardian_agreed: bool
    guardian_model_version: str
    scope_matches: bool
    evidence_complete: bool
    policy_allowed: bool


@dataclass(frozen=True)
class GateReceipt:
    contract_id: str
    application_id: str
    change_id: str
    from_chamber: Chamber
    to_chamber: Chamber
    authorized: bool
    checks_passed: tuple[str, ...]


class GateDenied(PermissionError):
    """Raised when a chamber contract fails any mandatory authorization check."""


def evaluate_gate(contract: GateContract) -> GateReceipt:
    """Evaluate the full conjunction of contract, human, guardian, and policy gates."""
    checks = {
        "contract_id": bool(contract.contract_id.strip()),
        "application_binding": bool(contract.application_id.strip()),
        "change_binding": bool(contract.change_id.strip()),
        "human_approval": contract.human_approved and bool(contract.human_reviewer.strip()),
        "guardian_agreement": (
            contract.guardian_agreed and bool(contract.guardian_model_version.strip())
        ),
        "scope_match": contract.scope_matches,
        "evidence_complete": contract.evidence_complete,
        "policy_allowed": contract.policy_allowed,
    }
    passed = tuple(name for name, ok in checks.items() if ok)
    return GateReceipt(
        contract_id=contract.contract_id,
        application_id=contract.application_id,
        change_id=contract.change_id,
        from_chamber=contract.from_chamber,
        to_chamber=contract.to_chamber,
        authorized=len(passed) == len(checks),
        checks_passed=passed,
    )


def enforce_gate(contract: GateContract) -> GateReceipt:
    """Fail closed unless every contractual gate condition is satisfied."""
    receipt = evaluate_gate(contract)
    if not receipt.authorized:
        failed = [
            name for name in (
                "contract_id", "application_binding", "change_binding",
                "human_approval", "guardian_agreement", "scope_match",
                "evidence_complete", "policy_allowed",
            )
            if name not in receipt.checks_passed
        ]
        raise GateDenied(
            f"Gate {contract.from_chamber.value}->{contract.to_chamber.value} denied: "
            + ", ".join(failed)
        )
    return receipt


F = TypeVar("F", bound=Callable[..., Any])


def requires_gate(function: F) -> F:
    """Decorator requiring a GateContract keyword argument before function execution.

    Example:
        @requires_gate
        def promote_release(release_id: str, *, contract: GateContract):
            return {"promoted": release_id}
    """
    @wraps(function)
    def guarded(*args, contract: GateContract, **kwargs):
        receipt = enforce_gate(contract)
        return function(*args, gate_receipt=receipt, **kwargs)
    return guarded  # type: ignore[return-value]
