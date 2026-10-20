# ==============================================================================
# PulmoTwin: Multimodal Cardiopulmonary Digital Twin
# Happiest Health - Reimagining & Reforming Healthcare in India Summit 2026
# Team Lead: Kabir Roy (rakeshkabir@gmail.com) | Digital Twin Challenge 2026
# Updated: October 2026 • Certified Clean Submission
# ==============================================================================

"""
Script to safely inject Digital Twin API routes into app.py.
"""

ROUTE_CODE = '''

# ==================== DIGITAL TWIN MULTIMODAL API ROUTES ====================
# Digital Twin Challenge 2026 - Happiest Health Summit Showcase

@app.route("/api/digital-twin/state/<int:user_id>", methods=["GET"])
def digital_twin_state(user_id):
    """
    Returns the dynamic physiological state of the patient's Digital Twin.
    Combines longitudinal EHR baseline, current wearable telemetry, and ambient air exposure.
    """
    try:
        engine = DigitalTwinEngine(user_id=user_id)
        # Pull latest sensor data if available
        latest_sensor = SensorData.query.filter_by(user_id=user_id).order_by(SensorData.id.desc()).first()
        ambient_env = {
            "aqi": latest_sensor.air_quality if latest_sensor else 85,
            "pm25": latest_sensor.pm25 if latest_sensor else 38.0
        }
        state = engine.compute_current_state(ambient_env=ambient_env)
        return jsonify({"success": True, "digital_twin": state})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/digital-twin/wearable-stream/<int:user_id>", methods=["GET", "POST"])
def digital_twin_wearables(user_id):
    """
    Ingests or streams continuous wearable telemetry (PPG Heart Rate, HRV, SpO2, Resp Rate, PEF).
    """
    try:
        ehr = EHRConnector.get_patient_ehr(user_id)["parsed_profile"]
        latest_sensor = SensorData.query.filter_by(user_id=user_id).order_by(SensorData.id.desc()).first()
        ambient_pm = latest_sensor.pm25 if latest_sensor else 42.0

        if request.method == "POST":
            data = request.get_json() or {}
            # Allow mock or real telemetry injection
            telem = WearableTelemetryStream.generate_current_telemetry(
                ehr,
                stress_level=float(data.get("stress_level", 0.3)),
                ambient_pm25=float(data.get("ambient_pm25", ambient_pm))
            )
            return jsonify({"success": True, "injected_telemetry": telem})

        current = WearableTelemetryStream.generate_current_telemetry(ehr, stress_level=0.25, ambient_pm25=ambient_pm)
        history = WearableTelemetryStream.generate_24h_telemetry_history(ehr, peak_pm25=160.0)
        return jsonify({
            "success": True,
            "current_telemetry": current,
            "history_24h": history
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/digital-twin/simulate/<int:user_id>", methods=["GET", "POST"])
def digital_twin_simulate(user_id):
    """
    Runs 24-hour forward physiological simulation of the patient's Digital Twin.
    Projects airway resistance, oxygenation, and adverse exacerbation risk.
    """
    try:
        user = User.query.get(user_id)
        u_lat = user.lat if user and user.lat else 28.6139
        u_lon = user.lon if user and user.lon else 77.2090

        forecast_res = PulmoTwinTools.get_air_quality_forecast(u_lat, u_lon, hours=24)
        hourly_env = forecast_res.get("hourly", [])[:24]

        intervention = None
        if request.method == "POST":
            intervention = request.get_json()

        engine = DigitalTwinEngine(user_id=user_id)
        simulation = engine.simulate_forward_trajectory(hourly_env, intervention=intervention)
        return jsonify(simulation)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/digital-twin/what-if/<int:user_id>", methods=["POST"])
def digital_twin_what_if(user_id):
    """
    Counterfactual Simulation Sandbox: Compares candidate interventions side-by-side.
    Tests treatments in silico before applying them to physical reality.
    """
    try:
        user = User.query.get(user_id)
        u_lat = user.lat if user and user.lat else 28.6139
        u_lon = user.lon if user and user.lon else 77.2090

        forecast_res = PulmoTwinTools.get_air_quality_forecast(u_lat, u_lon, hours=24)
        hourly_env = forecast_res.get("hourly", [])[:24]

        req_data = request.get_json() or {}
        scenarios = req_data.get("scenarios", [
            {"name": "Indoor HEPA Air Purifier (18:00 - 22:00)", "use_hepa_filter": True},
            {"name": "Proactive SMART Inhaler (2 Puffs at 17:00)", "take_reliever": True, "doses": 2},
            {"name": "Combined Environmental & Proactive Medication Protocol", "use_hepa_filter": True, "take_reliever": True, "doses": 2}
        ])

        engine = DigitalTwinEngine(user_id=user_id)
        comparison = CounterfactualSimulator.compare_scenarios(engine, hourly_env, scenarios)
        return jsonify(comparison)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/digital-twin/ehr/<int:user_id>", methods=["GET"])
def digital_twin_ehr(user_id):
    """
    Returns FHIR R4 / Ayushman Bharat Digital Mission (ABDM) Electronic Health Record.
    """
    try:
        bundle = EHRConnector.get_patient_ehr(user_id)
        return jsonify({"success": True, "fhir_bundle": bundle})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

'''

def patch_app():
    with open("app.py", "r", encoding="utf-8") as f:
        content = f.read()

    # Add imports if not present
    if "from digital_twin import" not in content:
        import_marker = "from agent.guardrails import check_input_red_flags, sanitize_output"
        new_import = import_marker + "\nfrom digital_twin import DigitalTwinEngine, WearableTelemetryStream, EHRConnector, CounterfactualSimulator"
        content = content.replace(import_marker, new_import, 1)

    if "import io" not in content:
        content = content.replace("import warnings", "import warnings\nimport io", 1)

    # Add routes if not present
    if "/api/digital-twin/state" not in content:
        target_marker = "# ==================== GDPR / DPDP ACT DATA PRIVACY ROUTES ===================="
        content = content.replace(target_marker, ROUTE_CODE + "\n" + target_marker, 1)

    with open("app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("app.py successfully patched with Digital Twin routes!")

if __name__ == "__main__":
    patch_app()
