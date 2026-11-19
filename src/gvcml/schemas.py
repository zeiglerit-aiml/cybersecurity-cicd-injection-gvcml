"""Typed records for guardian decisions and release evidence."""
from dataclasses import dataclass
from enum import Enum

class Disposition(str, Enum):
    ALLOW = "ALLOW"
    HOLD = "HOLD"
    STOP = "STOP"

class BrakeState(str, Enum):
    RUN = "RUN"
    HOLD = "HOLD"
    STOP = "STOP"
    QUARANTINE = "QUARANTINE"
    ROLLBACK = "ROLLBACK"

@dataclass(frozen=True)
class GuardianDecision:
    disposition: Disposition
    confidence: float
    rationale: str
    model_version: str

@dataclass(frozen=True)
class ValidationEvidence:
    functional_passed: bool
    security_passed: bool
    signed_artifact: bool
    full_attack_surface_assessed: bool
    sandbox_passed: bool
    critical_findings: int = 0
    evidence_refs: tuple[str, ...] = ()

@dataclass(frozen=True)
class HumanApproval:
    reviewer: str
    scope: str
    ticket: str
    approved: bool
