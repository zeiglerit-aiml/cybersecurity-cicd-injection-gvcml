import pytest

from gvcml.walkout import (
    RiskTier, TransitionEvidence, WalkoutAction, WalkoutRequest,
    WalkoutStage, authorize_stage_transition, evaluate_walkout,
)


def request(**overrides):
    values = dict(
        application_id="payments-api", application_type="cloud_native",
        change_id="change-42", stage=WalkoutStage.ML_ASSISTED,
        risk_tier=RiskTier.LOW, guardian_disposition="ALLOW",
        policy_allowed=True, evidence_complete=True, action_reversible=True,
    )
    values.update(overrides)
    return WalkoutRequest(**values)


def test_human_bridge_required_before_bounded_autonomy():
    result = evaluate_walkout(request())
    assert result.action == WalkoutAction.HOLD
    assert result.next_actor == "human_reviewer"


def test_guardian_stop_cannot_be_overridden_by_human_approval():
    result = evaluate_walkout(request(guardian_disposition="STOP", human_approved=True))
    assert result.action == WalkoutAction.STOP


def test_policy_denial_cannot_be_overridden_by_ai_recommendation():
    result = evaluate_walkout(request(
        stage=WalkoutStage.BOUNDED_AUTONOMY, policy_allowed=False,
        ai_recommendation="ALLOW",
    ))
    assert result.action == WalkoutAction.STOP


def test_bounded_autonomy_is_low_risk_reversible_and_guardian_allowed():
    result = evaluate_walkout(request(
        stage=WalkoutStage.BOUNDED_AUTONOMY, ai_recommendation="ALLOW",
    ))
    assert result.action == WalkoutAction.EXECUTE
    assert not result.human_approval_required


@pytest.mark.parametrize("changes", [
    {"risk_tier": RiskTier.HIGH},
    {"risk_tier": RiskTier.CRITICAL},
    {"action_reversible": False},
    {"ai_recommendation": "HOLD"},
])
def test_outside_autonomy_envelope_returns_to_human(changes):
    result = evaluate_walkout(request(
        stage=WalkoutStage.BOUNDED_AUTONOMY, **changes,
    ))
    assert result.action == WalkoutAction.HOLD
    assert result.next_actor == "human_reviewer"


def test_stage_transition_requires_all_human_governance_evidence():
    evidence = TransitionEvidence(True, "CHG-42", True, True, True)
    assert authorize_stage_transition(
        WalkoutStage.HUMAN_LED, WalkoutStage.ML_ASSISTED, evidence
    )
    assert not authorize_stage_transition(
        WalkoutStage.HUMAN_LED, WalkoutStage.AI_ASSISTED, evidence
    )
    assert not authorize_stage_transition(
        WalkoutStage.HUMAN_LED,
        WalkoutStage.ML_ASSISTED,
        TransitionEvidence(False, "", True, True, True),
    )
