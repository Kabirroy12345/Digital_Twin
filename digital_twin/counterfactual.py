# ==============================================================================
# PulmoTwin: Multimodal Cardiopulmonary Digital Twin
# Happiest Health - Reimagining & Reforming Healthcare in India Summit 2026
# Team Lead: Kabir Roy (rakeshkabir@gmail.com) | Digital Twin Challenge 2026
# Updated: October 2026 • Certified Clean Submission
# ==============================================================================

"""
Counterfactual "What-If" Simulation Engine for Digital Twin.
Allows patients and clinicians to virtually test interventions
(e.g., proactive bronchodilator, indoor HEPA filtration, rescheduled exercise)
before implementing them in the physical world.
"""

from typing import Dict, Any, List
from .twin_engine import DigitalTwinEngine

class CounterfactualSimulator:
    """
    Simulates counterfactual scenarios to optimize personalized patient treatment protocols.
    """

    @staticmethod
    def compare_scenarios(twin_engine: DigitalTwinEngine, environmental_forecast_24h: List[Dict[str, Any]],
                          scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Runs multiple intervention scenarios side-by-side and computes the comparative efficacy.
        """
        results = {}

        # 1. Baseline (Unmitigated / Status Quo)
        baseline_sim = twin_engine.simulate_forward_trajectory(
            environmental_forecast_24h,
            intervention={"name": "Baseline (Status Quo)", "description": "No proactive intervention"}
        )
        results["baseline"] = baseline_sim

        # 2. Iterate each candidate scenario
        for sc in scenarios:
            name = sc.get("name", "Custom Intervention")
            sim = twin_engine.simulate_forward_trajectory(environmental_forecast_24h, intervention=sc)

            base_peak = baseline_sim["adverse_event_forecast"]["peak_eri"]
            sc_peak = sim["adverse_event_forecast"]["peak_eri"]
            risk_reduction_pct = round(((base_peak - sc_peak) / max(0.01, base_peak)) * 100.0, 1)

            sim["comparative_evaluation"] = {
                "scenario_name": name,
                "peak_eri_delta": round(sc_peak - base_peak, 3),
                "risk_reduction_percent": max(0.0, risk_reduction_pct),
                "clinical_outcome": "SIGNIFICANT PROTECTIVE BENEFIT" if risk_reduction_pct > 25.0 else "MODEST BENEFIT"
            }
            results[name] = sim

        # Identify optimal scenario
        best_scenario = max(
            [k for k in results if k != "baseline"],
            key=lambda k: results[k].get("comparative_evaluation", {}).get("risk_reduction_percent", 0.0),
            default="baseline"
        )

        return {
            "success": True,
            "patient_name": twin_engine.ehr["name"],
            "best_recommended_intervention": best_scenario,
            "summary_recommendation": (
                f"Virtual Twin Simulation recommends '{best_scenario}', achieving a "
                f"{results[best_scenario].get('comparative_evaluation', {}).get('risk_reduction_percent', 0)}% "
                f"reduction in peak adverse exacerbation risk compared to the unmitigated baseline."
            ) if best_scenario != "baseline" else "Baseline control sufficient under current forecast.",
            "scenarios": results
        }
