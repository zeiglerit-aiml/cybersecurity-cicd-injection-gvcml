"""Trainable Random Forest guardian using human-adjudicated pipeline records."""
from pathlib import Path
import json
from .features import FEATURES, vectorize
from .schemas import Disposition, GuardianDecision

class GuardianModel:
    def __init__(self, estimator, model_version: str, min_confidence: float = 0.70):
        self.estimator = estimator
        self.model_version = model_version
        self.min_confidence = min_confidence

    @classmethod
    def train(cls, csv_path: str, output_path: str, min_confidence: float = 0.70):
        try:
            import csv
            import joblib
            from sklearn.ensemble import RandomForestClassifier
        except ImportError as exc:
            raise RuntimeError('Install the ML extra: pip install -e ".[ml]"') from exc
        with Path(csv_path).open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        if len(rows) < 12:
            raise ValueError("At least 12 labelled records are required.")
        labels = {row["label"].strip().upper() for row in rows}
        allowed = {item.value for item in Disposition}
        if not labels.issubset(allowed) or len(labels) < 2:
            raise ValueError(f"Labels must contain at least two of: {sorted(allowed)}")
        x = [[float(int(row[name])) for name in FEATURES] for row in rows]
        y = [row["label"].strip().upper() for row in rows]
        estimator = RandomForestClassifier(n_estimators=200, max_depth=8,
            class_weight="balanced", random_state=42, min_samples_leaf=1)
        estimator.fit(x, y)
        model = cls(estimator, "gvcml-rf-v1", min_confidence)
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({"estimator": estimator, "model_version": model.model_version,
            "features": list(FEATURES), "min_confidence": min_confidence}, destination)
        metadata = {"model_version": model.model_version, "algorithm": "RandomForestClassifier",
            "features": list(FEATURES), "training_records": len(rows),
            "labels": sorted(labels), "dataset": str(csv_path),
            "note": "Synthetic fixture only; validate on representative human-adjudicated data."}
        destination.with_suffix(".metadata.json").write_text(
            json.dumps(metadata, indent=2), encoding="utf-8")
        return model

    @classmethod
    def load(cls, model_path: str):
        try:
            import joblib
        except ImportError as exc:
            raise RuntimeError('Install the ML extra: pip install -e ".[ml]"') from exc
        bundle = joblib.load(model_path)
        if bundle.get("features") != list(FEATURES):
            raise ValueError("Model feature schema does not match this runtime.")
        return cls(bundle["estimator"], bundle["model_version"],
                   float(bundle.get("min_confidence", 0.70)))

    def assess(self, event: dict) -> GuardianDecision:
        probabilities = self.estimator.predict_proba([vectorize(event)])[0]
        index = int(probabilities.argmax())
        confidence = float(probabilities[index])
        predicted = str(self.estimator.classes_[index]).upper()
        if confidence < self.min_confidence:
            return GuardianDecision(Disposition.HOLD, confidence,
                "Model confidence is below the configured threshold.", self.model_version)
        return GuardianDecision(Disposition(predicted), confidence,
            "Guardian classification from pipeline feature evidence.", self.model_version)
