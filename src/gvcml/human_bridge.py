"""Human-facing triage bridge; never replaces the GVCML security authority."""
from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class ReviewPriority(str, Enum):
    ROUTINE = "ROUTINE"
    ELEVATED = "ELEVATED"
    URGENT = "URGENT"
    CRITICAL = "CRITICAL"


class ReviewRoute(str, Enum):
    AUTO_WORKFLOW = "AUTO_WORKFLOW"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    SECURITY_ESCALATION = "SECURITY_ESCALATION"


@dataclass(frozen=True)
class TriageContext:
    event_id: str
    application_id: str
    guardian_disposition: str
    guardian_confidence: float
    critical_findings: int = 0
    high_findings: int = 0
    impact_score: float = 0.0
    urgency_score: float = 0.0
    telemetry_anomaly_score: float = 0.0
    evidence_complete: bool = True
    model_disagreement: bool = False
    itsm_record_id: str | None = None
    telemetry_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class TriageResult:
    event_id: str
    application_id: str
    priority: ReviewPriority
    route: ReviewRoute
    rationale: str
    guardian_disposition: str
    guardian_confidence: float
    itsm_record_id: str | None
    telemetry_refs: tuple[str, ...]
    human_approval_required: bool


class TriageScorer(Protocol):
    """Plug-in contract for separately evaluated ML triage algorithms."""

    def score(self, context: TriageContext) -> float:
        """Return a normalized review-priority score in [0, 1]."""


class BaselineTriageScorer:
    """Deterministic bootstrap scorer; not a trained ML model."""

    def score(self, context: TriageContext) -> float:
        return max(
            0.0,
            min(
                1.0,
                0.35 * min(context.impact_score, 1.0)
                + 0.20 * min(context.urgency_score, 1.0)
                + 0.20 * min(context.telemetry_anomaly_score, 1.0)
                + 0.15 * (1.0 - context.guardian_confidence)
                + 0.10 * min(context.high_findings / 5.0, 1.0),
            ),
        )


class HumanBridge:
    """Turns guardian outcomes into readable review/ITSM routing decisions."""

    def __init__(self, scorer: TriageScorer | None = None):
        self.scorer = scorer or BaselineTriageScorer()

    def triage(self, context: TriageContext) -> TriageResult:
        if not 0.0 <= context.guardian_confidence <= 1.0:
            raise ValueError("guardian_confidence must be between 0 and 1")
        if any(not 0.0 <= value <= 1.0 for value in (
            context.impact_score, context.urgency_score,
            context.telemetry_anomaly_score,
        )):
            raise ValueError("context scores must be between 0 and 1")

        score = self.scorer.score(context)
        if not 0.0 <= score <= 1.0:
            raise ValueError("triage scorer must return a score between 0 and 1")

        disposition = context.guardian_disposition.upper()
        if context.critical_findings > 0 or disposition == "STOP":
            priority, route = ReviewPriority.CRITICAL, ReviewRoute.SECURITY_ESCALATION
            reason = "Critical finding or guardian STOP: escalate; triage cannot override."
        elif (not context.evidence_complete or context.model_disagreement
              or disposition == "HOLD"):
            priority, route = ReviewPriority.URGENT, ReviewRoute.HUMAN_REVIEW
            reason = "Evidence gap, model disagreement, or guardian HOLD requires review."
        elif disposition != "ALLOW":
            priority, route = ReviewPriority.URGENT, ReviewRoute.HUMAN_REVIEW
            reason = "Unrecognized guardian disposition requires human review."
        elif score >= 0.70 or context.high_findings > 0:
            priority, route = ReviewPriority.URGENT, ReviewRoute.HUMAN_REVIEW
            reason = "Elevated triage score or high-severity finding requires review."
        elif score >= 0.40:
            priority, route = ReviewPriority.ELEVATED, ReviewRoute.HUMAN_REVIEW
            reason = "Elevated operational risk; human review requested."
        else:
            priority, route = ReviewPriority.ROUTINE, ReviewRoute.AUTO_WORKFLOW
            reason = "Routine triage only; GVCML policy and release gates still apply."

        return TriageResult(
            event_id=context.event_id,
            application_id=context.application_id,
            priority=priority,
            route=route,
            rationale=reason,
            guardian_disposition=disposition,
            guardian_confidence=context.guardian_confidence,
            itsm_record_id=context.itsm_record_id,
            telemetry_refs=context.telemetry_refs,
            human_approval_required=route != ReviewRoute.AUTO_WORKFLOW,
        )
