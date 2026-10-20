"""
Integration Tests for Digital Twin API endpoints.
Verifies /api/digital-twin/state, /wearable-stream, /simulate, /what-if, and /ehr.
"""

import json
import pytest
from app import app, db
from models import User

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            # Ensure demo user exists
            user = User.query.get(1)
            if not user:
                user = User(
                    id=1,
                    name="Kabir Roy",
                    age=28,
                    gender="Male",
                    phone_no="+91-9876543210",
                    city="Delhi",
                    lat=28.6139,
                    lon=77.2090
                )
                db.session.add(user)
                db.session.commit()
        yield client

def test_api_digital_twin_state(client):
    res = client.get("/api/digital-twin/state/1")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data["success"] is True
    assert "digital_twin" in data
    dt = data["digital_twin"]
    assert dt["patient_name"] == "Kabir Roy"
    assert "physiological_metrics" in dt
    assert "wearable_telemetry" in dt
    assert "digital_twin_status" in dt

def test_api_digital_twin_wearables(client):
    res = client.get("/api/digital-twin/wearable-stream/1")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data["success"] is True
    assert "current_telemetry" in data
    assert "history_24h" in data
    assert len(data["history_24h"]) == 25

def test_api_digital_twin_simulate(client):
    res = client.get("/api/digital-twin/simulate/1")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data["success"] is True
    assert "hourly_trajectory" in data
    assert len(data["hourly_trajectory"]) == 24
    assert "adverse_event_forecast" in data

def test_api_digital_twin_what_if(client):
    payload = {
        "scenarios": [
            {"name": "Indoor HEPA Air Purifier", "use_hepa_filter": True},
            {"name": "Proactive Reliever Inhaler (2 Puffs)", "take_reliever": True, "doses": 2}
        ]
    }
    res = client.post("/api/digital-twin/what-if/1", json=payload)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data["success"] is True
    assert "best_recommended_intervention" in data
    assert "scenarios" in data

def test_api_digital_twin_ehr(client):
    res = client.get("/api/digital-twin/ehr/1")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data["success"] is True
    assert "fhir_bundle" in data
    assert data["fhir_bundle"]["resourceType"] == "Bundle"
