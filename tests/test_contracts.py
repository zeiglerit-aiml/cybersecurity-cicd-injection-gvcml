import pytest

from gvcml.contracts import (
    Chamber, GateContract, GateDenied, enforce_gate, evaluate_gate, requires_gate,
)


def contract(**overrides):
    values = dict(
        contract_id="GVCML-CHG-42", application_id="payments-api",
        change_id="CHG-42", from_chamber=Chamber.HUMAN_GOVERNANCE,
        to_chamber=Chamber.BOUNDED_EXECUTION, human_approved=True,
        human_reviewer="reviewer@example.test", guardian_agreed=True,
        guardian_model_version="guardian-v1", scope_matches=True,
        evidence_complete=True, policy_allowed=True,
    )
    values.update(overrides)
    return GateContract(**values)


def test_valid_contract_opens_gate():
    receipt = enforce_gate(contract())
    assert receipt.authorized
    assert receipt.application_id == "payments-api"
    assert "guardian_agreement" in receipt.checks_passed


@pytest.mark.parametrize("override", [
    {"human_approved": False},
    {"human_reviewer": ""},
    {"guardian_agreed": False},
    {"guardian_model_version": ""},
    {"scope_matches": False},
    {"evidence_complete": False},
    {"policy_allowed": False},
    {"change_id": ""},
])
def test_missing_contract_condition_fails_closed(override):
    receipt = evaluate_gate(contract(**override))
    assert not receipt.authorized
    with pytest.raises(GateDenied):
        enforce_gate(contract(**override))


def test_guarded_api_does_not_run_without_contract():
    calls = []

    @requires_gate
    def execute(change_id, *, gate_receipt):
        calls.append(change_id)
        return gate_receipt.authorized

    with pytest.raises(GateDenied):
        execute("CHG-42", contract=contract(guardian_agreed=False))
    assert calls == []


def test_guarded_api_receives_gate_receipt():
    @requires_gate
    def execute(change_id, *, gate_receipt):
        return change_id, gate_receipt.contract_id

    assert execute("CHG-42", contract=contract()) == ("CHG-42", "GVCML-CHG-42")
