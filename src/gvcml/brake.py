"""Fail-safe release interlock: missing mandatory evidence never passes."""
from .schemas import BrakeState, Disposition

class SafetyBrake:
    def __init__(self):
        self.state = BrakeState.HOLD
        self.reason = "No release decision has been evaluated."

    def evaluate(self, decision, evidence, approval, min_confidence=0.70):
        if evidence.critical_findings > 0:
            return self._set(BrakeState.STOP, "Critical security finding.")
        if decision.disposition == Disposition.STOP:
            return self._set(BrakeState.STOP, decision.rationale)
        if decision.disposition == Disposition.HOLD:
            return self._set(BrakeState.HOLD, decision.rationale)
        if decision.confidence < min_confidence:
            return self._set(BrakeState.HOLD, "Guardian confidence is insufficient.")
        gates = {
            "functional validation": evidence.functional_passed,
            "security validation": evidence.security_passed,
            "signed artifact": evidence.signed_artifact,
            "complete attack-surface assessment": evidence.full_attack_surface_assessed,
            "sandbox validation": evidence.sandbox_passed,
        }
        missing = [name for name, passed in gates.items() if not passed]
        if missing:
            return self._set(BrakeState.HOLD, "Missing/failed gates: " + ", ".join(missing))
        if approval is None or not approval.approved or not approval.reviewer or not approval.ticket:
            return self._set(BrakeState.HOLD, "Explicit human release approval is required.")
        return self._set(BrakeState.RUN, "Guardian allowed; all evidence and human release gates passed.")

    def _set(self, state, reason):
        self.state, self.reason = state, reason
        return state
