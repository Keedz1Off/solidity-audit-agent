"""Deterministic evidence gate for AI-assisted smart contract review."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED = (
    "target_commit",
    "scope_source",
    "configuration_evidence",
    "external_actor_reachability",
    "green_test",
    "red_test",
    "branch_reached",
    "independent_oracle",
    "production_equivalent",
    "impact_evidence",
)


def evaluate(record: dict) -> dict:
    """Return a status and missing fields without trusting a model's verdict."""
    if not isinstance(record, dict):
        raise ValueError("Evidence record must be a JSON object")
    missing = [name for name in REQUIRED if not record.get(name)]
    if not missing:
        return {"status": "report_ready", "missing": []}
    if "configuration_evidence" in missing or "scope_source" in missing:
        status = "CONFIG_GATED"
    elif "external_actor_reachability" in missing:
        status = "REACHABILITY_UNVERIFIED"
    elif "impact_evidence" in missing:
        status = "IMPACT_UNVERIFIED"
    else:
        status = "NOT_REPRODUCIBLE"
    return {"status": status, "missing": missing}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python evidence_gate.py <candidate.json>", file=sys.stderr)
        return 2
    try:
        record = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
        result = evaluate(record)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Invalid evidence: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "report_ready" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
