from gvcml.human_bridge import (
    HumanBridge, ReviewPriority, ReviewRoute, TriageContext,
)


def context(**overrides):
    values = dict(
        event_id="evt-1", application_id="inventory-api",
        guardian_disposition="ALLOW", guardian_confidence=0.98,
    )
    values.update(overrides)
    return TriageContext(**values)


def test_routine_triage_does_not_claim_release_authority():
    result = HumanBridge().triage(context())
    assert result.priority == ReviewPriority.ROUTINE
    assert result.route == ReviewRoute.AUTO_WORKFLOW
    assert result.guardian_disposition == "ALLOW"


def test_guardian_stop_routes_to_security_escalation():
    result = HumanBridge().triage(context(guardian_disposition="STOP"))
    assert result.priority == ReviewPriority.CRITICAL
    assert result.route == ReviewRoute.SECURITY_ESCALATION


def test_incomplete_evidence_routes_to_human():
    result = HumanBridge().triage(context(evidence_complete=False))
    assert result.route == ReviewRoute.HUMAN_REVIEW
    assert result.human_approval_required


def test_high_findings_route_to_human():
    result = HumanBridge().triage(context(high_findings=1))
    assert result.route == ReviewRoute.URGENT and result.human_approval_required


def test_custom_scorer_is_pluggable():
    class Scorer:
        def score(self, _context):
            return 0.8

    result = HumanBridge(Scorer()).triage(context())
    assert result.route == ReviewRoute.HUMAN_REVIEW
