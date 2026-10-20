"""
Digital Twin Engine: Cardiopulmonary Physiological Simulator.
Simulates dynamic patient airway resistance, alveolar ventilation,
cardiopulmonary stress, and predicts adverse exacerbation events up to 24 hours in advance.
"""

import math
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from .ehr_connector import EHRConnector
from .wearable_sim import WearableTelemetryStream

class DigitalTwinEngine:
    """
    Dynamic virtual replica of a patient's respiratory & autonomic physiology.
    Integrates longitudinal EHR baselines with streaming wearable telemetry and
    environmental exposure curves.
    """

    def __init__(self, user_id: int = 1):
        self.user_id = user_id
        self.ehr = EHRConnector.get_patient_ehr(user_id)["parsed_profile"]

    def compute_current_state(self, wearable_data: Optional[Dict[str, Any]] = None,
                              ambient_env: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Computes the complete multi-organ physiological twin state at the present moment.
        """
        if not wearable_data:
            ambient_pm25 = ambient_env.get("pm25", 48.0) if ambient_env else 48.0
            wearable_data = WearableTelemetryStream.generate_current_telemetry(self.ehr, stress_level=0.25, ambient_pm25=ambient_pm25)

        hr = wearable_data["heart_rate_bpm"]
        spo2 = wearable_data["spo2_percent"]
        pef = wearable_data["current_pef_lpm"]
        rr = wearable_data["respiratory_rate_brpm"]
        hrv = wearable_data["hrv_rmssd_ms"]

        # Baseline parameters from EHR
        fev1_pred = self.ehr["baseline_spirometry"]["fev1_percent_predicted"]
        feno = self.ehr["biomarkers"]["fractional_exhaled_no_ppb"]
        eos = self.ehr["biomarkers"]["blood_eosinophils_per_uL"]

        # 1. Airway Resistance Raw (normal: 1.5 - 2.5 cmH2O/(L/s))
        # Inverse relationship with instantaneous PEF
        pef_ratio = pef / max(100.0, self.ehr["baseline_spirometry"]["personal_best_pef"])
        airway_resistance = round(max(1.5, min(14.0, 1.8 / (pef_ratio ** 1.6))), 2)

        # 2. Dynamic Lung Compliance Cdyn (normal: 50 - 100 mL/cmH2O)
        lung_compliance = round(max(20.0, min(85.0, 70.0 * (pef_ratio ** 1.1) - (feno / 10.0))), 1)

        # 3. Alveolar-Arterial O2 Gradient (A-a DO2, normal < 15 mmHg)
        aa_gradient = round(max(8.0, min(45.0, 10.0 + (100.0 - spo2) * 3.2)), 1)

        # 4. Bronchial Hyperresponsiveness Index (BHR, 0 - 100%)
        bhr_index = round(min(100.0, max(15.0, (feno / 50.0) * 40.0 + (eos / 500.0) * 30.0 + (airway_resistance / 8.0) * 30.0)), 1)

        # 5. Autonomic Sympathetic / Parasympathetic Balance
        sympathetic_tone = round(min(1.0, max(0.1, (hr - 60.0) / 60.0 * 0.6 + (50.0 - min(50.0, hrv)) / 50.0 * 0.4)), 2)

        # 6. Composite Exacerbation Risk Index (ERI: 0.0 to 1.0)
        eri = round(min(0.99, max(0.05,
            (airway_resistance / 10.0) * 0.35 +
            ((100.0 - spo2) / 12.0) * 0.25 +
            ((rr - 14.0) / 16.0) * 0.15 +
            sympathetic_tone * 0.15 +
            (bhr_index / 100.0) * 0.10
        )), 3)

        if eri < 0.35:
            clinical_status = "STABLE / CONTROLLED"
            status_color = "#10B981"
            action_code = "MAINTAIN_REGIMEN"
        elif eri < 0.70:
            clinical_status = "ELEVATED VULNERABILITY (AIRWAY STRESS)"
            status_color = "#F59E0B"
            action_code = "PROPHYLACTIC_ACTION_RECOMMENDED"
        else:
            clinical_status = "IMPENDING ACUTE EXACERBATION"
            status_color = "#EF4444"
            action_code = "EMERGENCY_RESCUE_PROTOCOL"

        return {
            "patient_abha_id": self.ehr["abha_id"],
            "patient_name": self.ehr["name"],
            "age": self.ehr["age"],
            "diagnosis": self.ehr["diagnosis"],
            "computation_timestamp": datetime.utcnow().isoformat() + "Z",
            "physiological_metrics": {
                "airway_resistance_cmH2O_L_s": airway_resistance,
                "airway_resistance_normal_range": "1.5 - 2.5",
                "dynamic_lung_compliance_mL_cmH2O": lung_compliance,
                "aa_oxygen_gradient_mmHg": aa_gradient,
                "bronchial_hyperresponsiveness_pct": bhr_index,
                "sympathetic_autonomic_tone": sympathetic_tone,
                "work_of_breathing_index": round(airway_resistance * (rr / 15.0), 2)
            },
            "wearable_telemetry": wearable_data,
            "digital_twin_status": {
                "exacerbation_risk_index": eri,
                "clinical_status": clinical_status,
                "status_color": status_color,
                "recommended_action_code": action_code,
                "time_to_potential_decompensation_hours": round(max(1.5, (1.0 - eri) * 18.0), 1) if eri >= 0.50 else None
            }
        }

    def simulate_forward_trajectory(self, environmental_forecast_24h: List[Dict[str, Any]],
                                    intervention: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Runs forward physiological simulation across the next 24 hours.
        Applies mathematical differential equations representing airway bronchoconstriction,
        particulate clearance kinetics, and medication pharmacokinetics.
        """
        hours = len(environmental_forecast_24h)
        trajectory = []
        base_state = self.compute_current_state()

        curr_raw = base_state["physiological_metrics"]["airway_resistance_cmH2O_L_s"]
        curr_pef = base_state["wearable_telemetry"]["current_pef_lpm"]
        curr_spo2 = base_state["wearable_telemetry"]["spo2_percent"]
        curr_hr = base_state["wearable_telemetry"]["heart_rate_bpm"]
        curr_eri = base_state["digital_twin_status"]["exacerbation_risk_index"]

        # Pharmacokinetic factor if medication taken
        med_boost = 0.0
        if intervention and intervention.get("take_reliever", False):
            # Salbutamol / Formoterol rapid bronchodilation (onset 5-15 mins, peak 1-2 hours)
            med_boost = intervention.get("doses", 2) * 0.22

        hepa_active = intervention.get("use_hepa_filter", False) if intervention else False

        adverse_event_forecast = {
            "risk_within_4h": 0.0,
            "risk_within_12h": 0.0,
            "risk_within_24h": 0.0,
            "peak_risk_hour": "00:00",
            "peak_eri": 0.0,
            "primary_driver": "Ambient Particulate Exposure (PM2.5)"
        }

        cumulative_particulate_dose = 0.0

        for i, step in enumerate(environmental_forecast_24h):
            pm25 = float(step.get("pm25", 45.0))
            if hepa_active and i >= 2:  # Indoors with HEPA reduces effective exposure by 75%
                effective_pm25 = pm25 * 0.25
            else:
                effective_pm25 = pm25

            temp = float(step.get("temperature", 24.0))
            humidity = float(step.get("humidity", 60.0))

            # Particulate irritant stimulus on mast cell degranulation
            particulate_stimulus = max(0.0, (effective_pm25 - 35.0) / 120.0)
            cumulative_particulate_dose += effective_pm25

            # Thermal stimulus (cold dry air induces reflex bronchoconstriction)
            cold_stimulus = max(0.0, (18.0 - temp) / 15.0) if temp < 18.0 else 0.0

            # Medication decay curve (half-life of beta-2 agonist ~ 4-6 hours)
            decayed_med = med_boost * math.exp(-i / 5.5)

            # Airway resistance progression: differential drift
            delta_raw = (particulate_stimulus * 0.35 + cold_stimulus * 0.20) - (decayed_med * 0.8)
            curr_raw = max(1.6, min(13.5, curr_raw + delta_raw * 0.45))

            # PEF response
            personal_best = self.ehr["baseline_spirometry"]["personal_best_pef"]
            curr_pef = max(120.0, min(personal_best, personal_best * (1.8 / (curr_raw ** 0.65))))

            # SpO2 and Heart Rate response
            curr_spo2 = max(89.0, min(99.0, 98.8 - (curr_raw - 1.8) * 0.65))
            curr_hr = int(70 + (curr_raw - 1.8) * 4.5 + (0.5 if i % 2 == 0 else -0.5))

            # Exacerbation Risk Index
            sim_eri = round(min(0.99, max(0.06, (curr_raw / 9.0) * 0.5 + ((100.0 - curr_spo2) / 10.0) * 0.3 + (effective_pm25 / 250.0) * 0.2)), 3)

            time_str = step.get("hour", f"{i:02d}:00")

            if sim_eri > adverse_event_forecast["peak_eri"]:
                adverse_event_forecast["peak_eri"] = sim_eri
                adverse_event_forecast["peak_risk_hour"] = time_str

            if i <= 4:
                adverse_event_forecast["risk_within_4h"] = max(adverse_event_forecast["risk_within_4h"], sim_eri)
            if i <= 12:
                adverse_event_forecast["risk_within_12h"] = max(adverse_event_forecast["risk_within_12h"], sim_eri)
            adverse_event_forecast["risk_within_24h"] = max(adverse_event_forecast["risk_within_24h"], sim_eri)

            trajectory.append({
                "hour_step": i,
                "hour_label": time_str,
                "ambient_pm25": round(effective_pm25, 1),
                "airway_resistance": round(curr_raw, 2),
                "predicted_pef": round(curr_pef, 1),
                "predicted_spo2": round(curr_spo2, 1),
                "predicted_heart_rate": curr_hr,
                "exacerbation_risk_index": sim_eri,
                "clinical_zone": "GREEN" if sim_eri < 0.35 else ("YELLOW" if sim_eri < 0.70 else "RED")
            })

        adverse_event_forecast["cumulative_pm25_dose_ug_h"] = round(cumulative_particulate_dose, 1)

        return {
            "success": True,
            "patient_name": self.ehr["name"],
            "simulation_length_hours": hours,
            "intervention_applied": intervention or {"description": "Standard baseline (no proactive intervention)"},
            "adverse_event_forecast": adverse_event_forecast,
            "hourly_trajectory": trajectory
        }
