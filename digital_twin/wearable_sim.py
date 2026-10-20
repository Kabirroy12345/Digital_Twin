"""
Wearable Telemetry Stream Simulator & Ingestion Engine.
Emulates real-time BLE / Smartwatch / Smart Ring / Connected Inhaler sensor streams:
- Photoplethysmography (PPG): Heart Rate (HR), HRV (rMSSD), SpO2
- Respiratory rate derived from photoplethysmogram pulse wave
- Skin Temperature & Accelerometer METs activity
- Bluetooth Low Energy (BLE) Smart Inhaler puff counter and flow velocity
"""

import math
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

class WearableTelemetryStream:
    """
    Manages continuous wearable telemetry streams for the patient's Digital Twin.
    Generates physiological baseline + stress/exacerbation responses.
    """

    @staticmethod
    def generate_current_telemetry(patient_ehr: Dict[str, Any], stress_level: float = 0.2,
                                   ambient_pm25: float = 45.0) -> Dict[str, Any]:
        """
        Generates realistic instantaneous wearable telemetry calibrated to patient state and environment.
        stress_level: 0.0 (fully relaxed/controlled) to 1.0 (acute respiratory distress).
        """
        now = datetime.utcnow()

        # Environmental impact on autonomic tone
        pm_impact = min(0.4, ambient_pm25 / 300.0)
        total_stress = min(1.0, max(0.0, stress_level + pm_impact * 0.5))

        # Heart Rate: resting 68-76, tachycardic under distress up to 125 bpm
        hr = int(72 + 45 * total_stress + random.uniform(-2.5, 2.5))

        # HRV (rMSSD): high when relaxed (45-65ms), collapses under bronchial distress (12-22ms)
        hrv = max(14.0, round(54.0 - 36.0 * total_stress + random.uniform(-2.0, 2.0), 1))

        # SpO2: normal 97-99%, drops to 89-93% in severe exacerbation
        spo2 = max(88.0, min(99.5, round(98.5 - 7.5 * total_stress + random.uniform(-0.4, 0.4), 1)))

        # Respiratory Rate: normal 14-18 brpm, tachypneic up to 32 brpm
        rr = int(16 + 14 * total_stress + random.uniform(-1, 1))

        # Skin Temperature: 36.2 - 36.8 C
        skin_temp = round(36.4 + 0.5 * total_stress + random.uniform(-0.1, 0.1), 2)

        # Baseline PEF from EHR, degraded by stress & airway resistance
        base_pef = patient_ehr.get("baseline_spirometry", {}).get("baseline_pef_lpm", 390.0)
        personal_best = patient_ehr.get("baseline_spirometry", {}).get("personal_best_pef", 450.0)
        current_pef = max(110.0, round(base_pef * (1.0 - 0.55 * total_stress) + random.uniform(-5, 5), 1))
        pef_percent = round((current_pef / personal_best) * 100.0, 1)

        # Inhaler smart sensor connectivity
        inhaler_connected = True
        battery_level = 88

        # Zone classification according to GINA / Global Initiative for Asthma
        if pef_percent >= 80.0:
            clinical_zone = "GREEN (Controlled)"
            color = "#10B981"
        elif pef_percent >= 50.0:
            clinical_zone = "YELLOW (Caution - Airway Obstruction)"
            color = "#F59E0B"
        else:
            clinical_zone = "RED (Medical Emergency - Critical)"
            color = "#EF4444"

        return {
            "timestamp": now.isoformat() + "Z",
            "heart_rate_bpm": hr,
            "hrv_rmssd_ms": hrv,
            "spo2_percent": spo2,
            "respiratory_rate_brpm": rr,
            "skin_temperature_c": skin_temp,
            "current_pef_lpm": current_pef,
            "pef_percent_predicted": pef_percent,
            "clinical_zone": clinical_zone,
            "zone_color": color,
            "activity_state": "Sedentary" if total_stress < 0.5 else "Restricted (Shortness of Breath)",
            "smart_inhaler": {
                "connected": inhaler_connected,
                "battery": f"{battery_level}%",
                "canister_doses_remaining": 164,
                "last_actuation": (now - timedelta(hours=4, minutes=15)).strftime("%H:%M UTC")
            },
            "autonomic_stress_index": round(total_stress * 100.0, 1)
        }

    @staticmethod
    def generate_24h_telemetry_history(patient_ehr: Dict[str, Any], peak_pm25: float = 180.0) -> List[Dict[str, Any]]:
        """Generates continuous 24-hour historical telemetry log at 1-hour intervals."""
        history = []
        base_time = datetime.utcnow() - timedelta(hours=24)

        for h in range(25):
            t = base_time + timedelta(hours=h)
            hour_of_day = t.hour

            # Diurnal particulate exposure peak in morning & late evening
            diurnal_env = 0.5 + 0.5 * math.sin((hour_of_day - 6) / 24.0 * 2 * math.pi)
            ambient_pm = 35.0 + (peak_pm25 - 35.0) * diurnal_env
            stress = max(0.1, min(0.85, (ambient_pm / 240.0) * 0.75 + (0.1 if 2 <= hour_of_day <= 5 else 0.0)))

            telem = WearableTelemetryStream.generate_current_telemetry(patient_ehr, stress_level=stress, ambient_pm25=ambient_pm)
            telem["timestamp"] = t.isoformat() + "Z"
            telem["hour_label"] = f"{hour_of_day:02d}:00"
            telem["ambient_pm25"] = round(ambient_pm, 1)
            history.append(telem)

        return history
