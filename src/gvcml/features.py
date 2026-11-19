"""Stable feature schema shared by guardian training and inference."""
FEATURES = (
    "critical_vulnerability", "high_vulnerability", "privilege_escalation",
    "unsigned_artifact", "secret_exposure", "unknown_component",
    "untrusted_source", "sensitive_data_change", "network_exposure_change",
    "assessment_incomplete",
)

def vectorize(payload: dict) -> list[float]:
    values = payload.get("features", payload)
    return [float(bool(values.get(name, False))) for name in FEATURES]
