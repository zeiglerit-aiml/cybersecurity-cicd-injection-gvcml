"""Command-line interface for the GVC_ML reference implementation."""
import argparse
import json
from pathlib import Path
from .engine import DecisionHarness
from .guardian import GuardianModel
from .schemas import HumanApproval, ValidationEvidence

def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def evidence_from(payload):
    return ValidationEvidence(
        functional_passed=bool(payload.get("functional_passed")),
        security_passed=bool(payload.get("security_passed")),
        signed_artifact=bool(payload.get("signed_artifact")),
        full_attack_surface_assessed=bool(payload.get("full_attack_surface_assessed")),
        sandbox_passed=bool(payload.get("sandbox_passed")),
        critical_findings=int(payload.get("critical_findings", 0)),
        evidence_refs=tuple(payload.get("evidence_refs", [])),
    )

def main():
    parser = argparse.ArgumentParser(prog="gvcml", description="GVC_ML guardian governance CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    train = sub.add_parser("train", help="Train from labelled pipeline data")
    train.add_argument("--dataset", required=True)
    train.add_argument("--output", required=True)
    train.add_argument("--min-confidence", type=float, default=0.70)
    evaluate = sub.add_parser("evaluate", help="Evaluate a pipeline event")
    evaluate.add_argument("--model", required=True)
    evaluate.add_argument("--event", required=True)
    evaluate.add_argument("--evidence", required=True)
    evaluate.add_argument("--approval")
    demo = sub.add_parser("demo", help="Run the synthetic demonstration")
    demo.add_argument("--model", default="artifacts/guardian.joblib")
    args = parser.parse_args()
    if args.command == "train":
        model = GuardianModel.train(args.dataset, args.output, args.min_confidence)
        print(f"Trained {model.model_version}; artifact: {args.output}")
        return
    model = GuardianModel.load(args.model)
    harness = DecisionHarness(model)
    if args.command == "demo":
        event = read_json("examples/events/clean_release.json")
        evidence = evidence_from(read_json("examples/evidence/passing_sandbox.json"))
        approval = HumanApproval("demo-reviewer", "demo-release", "DEMO-001", True)
    else:
        event = read_json(args.event)
        evidence = evidence_from(read_json(args.evidence))
        approval = None
        if args.approval:
            p = read_json(args.approval)
            approval = HumanApproval(p["reviewer"], p["scope"], p["ticket"], bool(p["approved"]))
    print(json.dumps(harness.evaluate(event, evidence, approval), indent=2))

if __name__ == "__main__":
    main()
