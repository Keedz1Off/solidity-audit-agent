import unittest

from evidence_gate import REQUIRED, evaluate


class EvidenceGateTests(unittest.TestCase):
    def test_complete_record(self):
        record = {field: f"proof for {field}" for field in REQUIRED}
        self.assertEqual(evaluate(record), {"status": "report_ready", "missing": []})

    def test_missing_configuration_blocks_report(self):
        record = {field: "evidence" for field in REQUIRED}
        record["configuration_evidence"] = ""
        result = evaluate(record)
        self.assertEqual(result["status"], "CONFIG_GATED")
        self.assertIn("configuration_evidence", result["missing"])

    def test_unverified_reachability_blocks_report(self):
        record = {field: "evidence" for field in REQUIRED}
        del record["external_actor_reachability"]
        self.assertEqual(evaluate(record)["status"], "REACHABILITY_UNVERIFIED")

    def test_missing_impact_blocks_report(self):
        record = {field: "evidence" for field in REQUIRED}
        del record["impact_evidence"]
        self.assertEqual(evaluate(record)["status"], "IMPACT_UNVERIFIED")

    def test_wrong_shape_rejected(self):
        with self.assertRaises(ValueError):
            evaluate([])


if __name__ == "__main__":
    unittest.main()
