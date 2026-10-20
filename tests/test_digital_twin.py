"""
Unit Tests for Digital Twin Module.
Verifies physiological state calculations, wearable telemetry streams,
EHR connector, 24h forward simulation, and counterfactual intervention engine.
"""

import pytest
from digital_twin.ehr_connector import EHRConnector
from digital_twin.wearable_sim import WearableTelemetryStream
from digital_twin.twin_engine import DigitalTwinEngine
from digital_twin.counterfactual import CounterfactualSimulator

def test_ehr_connector_fhir_structure():
    bundle = EHRConnector.get_patient_ehr(1)
    assert bundle["resourceType"] == "Bundle"
    assert len(bundle["entry"]) >= 4
    profile = bundle["parsed_profile"]
    assert profile["name"] == "Kabir Roy"
    assert "baseline_spirometry" in profile
    assert profile["baseline_spirometry"]["fev1_percent_predicted"] > 0
    assert "biomarkers" in profile

def test_wearable_telemetry_generation():
    ehr = EHRConnector.get_patient_ehr(1)["parsed_profile"]
    telem = WearableTelemetryStream.generate_current_telemetry(ehr, stress_level=0.1, ambient_pm25=30.0)
    assert 50 <= telem["heart_rate_bpm"] <= 140
    assert 85.0 <= telem["spo2_percent"] <= 100.0
    assert 10 <= telem["respiratory_rate_brpm"] <= 35
    assert telem["current_pef_lpm"] > 100
    assert telem["clinical_zone"] in ["GREEN (Controlled)", "YELLOW (Caution - Airway Obstruction)", "RED (Medical Emergency - Critical)"]

def test_wearable_24h_history():
    ehr = EHRConnector.get_patient_ehr(1)["parsed_profile"]
    history = WearableTelemetryStream.generate_24h_telemetry_history(ehr, peak_pm25=150.0)
    assert len(history) == 25
    assert history[0]["hour_label"] is not None

def test_digital_twin_engine_current_state():
    engine = DigitalTwinEngine(user_id=1)
    state = engine.compute_current_state()
    assert state["patient_name"] == "Kabir Roy"
    metrics = state["physiological_metrics"]
    assert 1.0 <= metrics["airway_resistance_cmH2O_L_s"] <= 15.0
    assert 15.0 <= metrics["dynamic_lung_compliance_mL_cmH2O"] <= 100.0
    assert 0.0 <= state["digital_twin_status"]["exacerbation_risk_index"] <= 1.0

def test_forward_trajectory_simulation():
    engine = DigitalTwinEngine(user_id=1)
    mock_forecast = [{"hour": f"{h:02d}:00", "pm25": 40 + h * 3, "temperature": 22, "humidity": 55} for h in range(24)]
    sim = engine.simulate_forward_trajectory(mock_forecast)
    assert sim["success"] is True
    assert len(sim["hourly_trajectory"]) == 24
    assert "adverse_event_forecast" in sim
    assert sim["adverse_event_forecast"]["risk_within_24h"] >= 0.0

def test_counterfactual_scenarios():
    engine = DigitalTwinEngine(user_id=1)
    mock_forecast = [{"hour": f"{h:02d}:00", "pm25": 120, "temperature": 20, "humidity": 60} for h in range(24)]
    scenarios = [
        {"name": "Indoor HEPA Air Purifier", "use_hepa_filter": True},
        {"name": "Proactive Reliever Inhaler (2 Puffs)", "take_reliever": True, "doses": 2}
    ]
    cf_res = CounterfactualSimulator.compare_scenarios(engine, mock_forecast, scenarios)
    assert cf_res["success"] is True
    assert "best_recommended_intervention" in cf_res
    assert "baseline" in cf_res["scenarios"]
    assert "Indoor HEPA Air Purifier" in cf_res["scenarios"]
