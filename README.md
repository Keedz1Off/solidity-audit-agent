# Solidity Audit Agent

An evidence-first workflow for AI-assisted smart contract review. The agent reads a repository, traces one reachable execution path at a time, proposes a hypothesis, and records the evidence needed to accept or reject it. A small Python gate checks that a candidate has the minimum proof required before it can be presented as a finding.

This is a **research tool**, not an automated vulnerability detector or a claim that any protocol has a bug.

## What the agent does

1. Fixes the target commit, in-scope contracts, deployment configuration, and trust assumptions.
2. Traces an entry point through state changes, external calls, and the business outcome.
3. Proposes an invariant and a concrete failure hypothesis.
4. Builds a normal (`GREEN`) and controlled violation (`RED`) test with a separate oracle.
5. Checks who can trigger the failure in the actual deployment and what impact follows.
6. Records `report_ready` only after every proof gate passes. Otherwise it records the missing evidence.

The instructions for an AI coding agent are in [AGENTS.md](AGENTS.md). The evidence gate is deliberately deterministic: the model cannot promote its own speculation into a finding simply by writing a confident summary.

## Run locally

Requires Python 3.11+; no packages or API key are needed for the gate.

```bash
python evidence_gate.py examples/synthetic_example.json
python evidence_gate.py examples/incomplete_example.json
python -m unittest discover -s tests -v
```

Both examples are intentionally incomplete, and the gate rejects them. They are synthetic and do not describe a real protocol. Use this repository as an agent workspace alongside a **separate, pinned** target checkout. Give the agent the target path and published scope, then have it produce a candidate JSON file with the same fields. Run the gate before writing any report.

## Why this exists

Local red tests can be misleading: an impossible token configuration, a privileged-only branch, or an oracle that merely repeats the implementation may all look like a vulnerability. This workflow keeps configuration, reachability, reproducibility, and impact as separate checks. A failed gate is useful research output, not a finding.

## Limits

The JSON fields are evidence declarations, not cryptographic proofs. `report_ready` means the fields are populated, not that the underlying evidence is true. A human reviewer still needs to inspect the linked source lines, deployment data, test logs, and impact. The tool never sends transactions or reports.

