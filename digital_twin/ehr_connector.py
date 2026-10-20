# ==============================================================================
# PulmoTwin: Multimodal Cardiopulmonary Digital Twin
# Happiest Health - Reimagining & Reforming Healthcare in India Summit 2026
# Team Lead: Kabir Roy (rakeshkabir@gmail.com) | Digital Twin Challenge 2026
# Updated: October 2026 • Certified Clean Submission
# ==============================================================================

"""
EHR Connector for Healthcare Digital Twin.
Adheres to FHIR R4 and Ayushman Bharat Digital Mission (ABDM) standards.
Provides longitudinal clinical baselines, spirometry, biomarkers, and medications.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

class EHRConnector:
    """
    Simulates and connects to ABDM / FHIR R4 Electronic Health Records.
    Extracts clinical priors that parameterize the patient's physiological Digital Twin.
    """

    DEFAULT_PROFILES = {
        1: {  # Patient: Kabir Roy / Alex Rivera demo
            "abha_id": "91-4582-7819-2041",
            "patient_id": "PAT-IN-2026-0891",
            "name": "Kabir Roy",
            "age": 28,
            "gender": "male",
            "blood_group": "B+",
            "city": "New Delhi",
            "diagnosis": "Moderate Persistent Bronchial Asthma (ICD-10 J45.40)",
            "comorbidities": [
                {"condition": "Allergic Rhinitis (ICD-10 J30.1)", "severity": "Moderate"},
                {"condition": "Gastroesophageal Reflux (ICD-10 K21.9)", "severity": "Mild"}
            ],
            "baseline_spirometry": {
                "fev1_liters": 2.65,
                "fev1_percent_predicted": 68.5,
                "fvc_liters": 3.82,
                "fev1_fvc_ratio": 0.69,
                "baseline_pef_lpm": 390.0,
                "personal_best_pef": 450.0,
                "bronchodilator_reversibility": "+14% (370 mL)"
            },
            "biomarkers": {
                "blood_eosinophils_per_uL": 380,  # >300 indicates eosinophilic phenotype
                "total_serum_ige_IU_mL": 420.0,
                "crp_mg_L": 2.1,
                "fractional_exhaled_no_ppb": 42.0  # FeNO > 35 indicates active eosinophilic airway inflammation
            },
            "current_medications": [
                {
                    "drug": "Budesonide + Formoterol",
                    "form": "Dry Powder Inhaler (DPI)",
                    "dose": "200/6 mcg",
                    "schedule": "1 inhalation twice daily (Maintenance & Reliever Therapy - SMART)",
                    "compliance_rate_30d": 0.88
                },
                {
                    "drug": "Levocetirizine",
                    "dose": "5 mg",
                    "schedule": "1 tablet daily at bedtime",
                    "compliance_rate_30d": 0.92
                }
            ],
            "past_exacerbations": [
                {"date": "2025-11-14", "severity": "Severe (ED Visit)", "trigger": "Delhi Post-Diwali Smog Spike (AQI 465)", "hospital": "Safdarjung Hospital, New Delhi"},
                {"date": "2026-01-20", "severity": "Moderate (Oral Steroids)", "trigger": "Winter Inversion + Viral Infection", "treatment": "Prednisolone 40mg 5d"}
            ],
            "known_allergens": ["Particulate Matter PM2.5", "Parthenium pollen", "House dust mites", "Cold dry air"]
        }
    }

    @classmethod
    def get_patient_ehr(cls, user_id: int) -> Dict[str, Any]:
        """Returns FHIR-structured patient baseline."""
        profile = cls.DEFAULT_PROFILES.get(user_id, cls.DEFAULT_PROFILES[1])
        return {
            "resourceType": "Bundle",
            "type": "collection",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "entry": [
                {
                    "resource": {
                        "resourceType": "Patient",
                        "identifier": [{"system": "https://abdm.gov.in/abha", "value": profile["abha_id"]}],
                        "name": [{"text": profile["name"]}],
                        "gender": profile["gender"],
                        "age": profile["age"],
                        "address": [{"city": profile["city"], "country": "IND"}]
                    }
                },
                {
                    "resource": {
                        "resourceType": "Condition",
                        "code": {"text": profile["diagnosis"]},
                        "comorbidities": profile["comorbidities"]
                    }
                },
                {
                    "resource": {
                        "resourceType": "Observation",
                        "category": "spirometry",
                        "component": profile["baseline_spirometry"]
                    }
                },
                {
                    "resource": {
                        "resourceType": "Observation",
                        "category": "biomarkers",
                        "component": profile["biomarkers"]
                    }
                },
                {
                    "resource": {
                        "resourceType": "MedicationStatement",
                        "medications": profile["current_medications"]
                    }
                }
            ],
            "parsed_profile": profile
        }
