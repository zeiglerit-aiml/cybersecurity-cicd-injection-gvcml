"""Graduated human-to-machine handoff with a non-bypassable security envelope."""
from dataclasses import dataclass
from enum import Enum


class WalkoutStage(str, Enum):
    HUMAN_LED = "HUMAN_LED"
    ML_ASSISTED = "ML_ASSISTED"
    NEURAL_ASSISTED = "NEURAL_ASSISTED"
    DEEP_LEARNING_ASSISTED = "DEEP_LEARNING_ASSISTED"
    AI_ASSISTED = "AI_ASSISTED"
    BOUNDED_AUTONOMY = "BOUNDED_AUTONOMY"


class WalkoutAction(str, Enum):
    EXECUTE = "EXECUTE"
    HOLD = "HOLD"
    STOP = "STOP"


class RiskTier(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True)
class WalkoutRequest:
    application_id: str
    application_type: str
    change_id: str
    stage: WalkoutStage
    risk_tier: RiskTier
    guardian_disposition: str
    policy_allowed: bool
    evidence_complete: bool
    action_reversible: bool
    human_approved: bool = False
    ai_recommendation: str | None = None
    critical_findings: int = 0
    telemetry_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class WalkoutDecision:
    action: WalkoutAction
    stage: WalkoutStage
    next_actor: str
    human_approval_required: bool
    rationale: str
    application_id: str
    change_id: str


@dataclass(frozen=True)
class TransitionEvidence:
    human_approved: bool
    approval_ticket: str
    evaluation_passed: bool
    policy_review_passed: bool
    rollback_ready: bool


def evaluate_walkout(request: WalkoutRequest) -> WalkoutDecision:
    """Evaluate handoff while preserving the guardian's security authority."""
    def decision(action, actor, human_required, rationale):
        return WalkoutDecision(
            action=action, stage=request.stage, next_actor=actor,
            human_approval_required=human_required, rationale=rationale,
            application_id=request.application_id, change_id=request.change_id,
        )

    if request.critical_findings > 0:
        return decision(WalkoutAction.STOP, "security_response", True,
                        "Critical security finding; non-bypassable stop.")
    if not request.policy_allowed:
        return decision(WalkoutAction.STOP, "security_governance", True,
                        "Deterministic policy denied the action.")
    if not request.evidence_complete:
        return decision(WalkoutAction.HOLD, "evidence_collection", True,
                        "Required evidence is incomplete.")
    if request.guardian_disposition.upper() != "ALLOW":
        action = (WalkoutAction.STOP if request.guardian_disposition.upper() == "STOP"
                  else WalkoutAction.HOLD)
        return decision(action, "security_authority", True,
                        "Guardian security authority did not return ALLOW.")

    if request.stage != WalkoutStage.BOUNDED_AUTONOMY:
        if not request.human_approved:
            return decision(WalkoutAction.HOLD, "human_reviewer", True,
                            "This stage requires an explicit human approval.")
        return decision(WalkoutAction.EXECUTE, "controlled_executor", True,
                        "Human approved; guardian, policy, and evidence gates passed.")

    autonomous_scope = (
        request.risk_tier == RiskTier.LOW
        and request.action_reversible
        and request.ai_recommendation is not None
        and request.ai_recommendation.upper() == "ALLOW"
    )
    if autonomous_scope:
        return decision(WalkoutAction.EXECUTE, "bounded_executor", False,
                        "Low-risk reversible action is within the approved autonomy envelope.")
    if request.human_approved:
        return decision(WalkoutAction.EXECUTE, "controlled_executor", True,
                        "Outside autonomous scope; explicit human approval supplied.")
    return decision(WalkoutAction.HOLD, "human_reviewer", True,
                    "Outside bounded autonomy; human review is required.")


_STAGE_ORDER = tuple(WalkoutStage)


def authorize_stage_transition(current: WalkoutStage, target: WalkoutStage,
                               evidence: TransitionEvidence) -> bool:
    """Require a reviewed, approved, one-step transition; never self-promote."""
    if _STAGE_ORDER.index(target) != _STAGE_ORDER.index(current) + 1:
        return False
    return bool(
        evidence.human_approved
        and evidence.approval_ticket.strip()
        and evidence.evaluation_passed
        and evidence.policy_review_passed
        and evidence.rollback_ready
    )
