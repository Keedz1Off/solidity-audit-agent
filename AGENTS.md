# Agent workflow

You are reviewing smart contracts inside the target repository named by the user. Follow the published scope and test only local or permitted environments. Never call a hypothesis a vulnerability until the evidence gate returns `report_ready` and a human has checked its references.

For each root hypothesis:

1. Record the exact repository URL, commit SHA, contract addresses and chain if deployed, and source for configuration facts. Unknown configuration is a gate, not an assumed default.
2. Map the user or external actor entry point to the business outcome. Name every privileged role, external adapter, token behavior, and sequence requirement.
3. Write the invariant in plain language. Separate an invariant that must always hold (`LAW`) from exploratory stricter behavior (`STRICT`). Resolve uncertain assumptions before fuzzing.
4. Build a harness plan: actors, balances, approvals, time, call sequence, fixtures, branch reach proof, and an independent oracle.
5. Run a normal route (`GREEN`) and a controlled violation (`RED`). Check that the intended branch was reached and the oracle detected the injected violation.
6. Compare the failing test with the real deployment: allowed configuration, external-actor reachability, production-equivalent reproduction, and concrete impact.
7. Save one JSON evidence record using the example schema, run `python evidence_gate.py <file>`, and report the gate result faithfully.

The gate uses `CONFIG_GATED`, `REACHABILITY_UNVERIFIED`, `NOT_REPRODUCIBLE`, and `IMPACT_UNVERIFIED` when evidence is missing. Only use `TRUSTED_ROLE_ONLY` or `NO_SECURITY_IMPACT` after positively proving those facts. Cite exact source lines and test commands in the evidence record. Do not submit a bounty report or contact a project without the user's explicit instruction.
