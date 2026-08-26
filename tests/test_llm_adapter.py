from __future__ import annotations

import unittest

from enterprise_orchestrator.llm_adapter import DeterministicPlanner
from enterprise_orchestrator.orchestrator_api import validate_model_output


class DeterministicPlannerTests(unittest.TestCase):
    def test_fallback_planner_produces_contract_valid_output(self) -> None:
        result = DeterministicPlanner().generate_plan(
            task="Check Nutanix storage latency",
            evidence=[{"source": "operator", "summary": "Latency spike observed"}],
        )

        validate_model_output(result.plan)
        self.assertEqual(result.provider, "deterministic")
        self.assertIn("nutanix", result.plan["domains"])
        self.assertIn("storage", result.plan["domains"])


if __name__ == "__main__":
    unittest.main()
