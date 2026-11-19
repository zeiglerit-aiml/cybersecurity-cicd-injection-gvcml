"""Execution harness coordinating guardian, evidence, approval, and brake."""
from .brake import SafetyBrake

class DecisionHarness:
    def __init__(self, guardian, brake=None):
        self.guardian = guardian
        self.brake = brake or SafetyBrake()

    def evaluate(self, event, evidence, approval=None):
        decision = self.guardian.assess(event)
        state = self.brake.evaluate(decision, evidence, approval,
                                    self.guardian.min_confidence)
        return {
            "event_id": event.get("event_id", "unknown"),
            "component": event.get("component", "unspecified"),
            "guardian": {"disposition": decision.disposition.value,
                "confidence": round(decision.confidence, 4),
                "rationale": decision.rationale, "model_version": decision.model_version},
            "brake": {"state": state.value, "reason": self.brake.reason},
            "promotion_authorized": state.value == "RUN",
        }
