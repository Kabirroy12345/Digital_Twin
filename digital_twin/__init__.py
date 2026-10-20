"""
Digital Twin Module for Cardiopulmonary Physiology.
Implements continuous physiological state modeling, wearable-EHR integration,
predictive adverse event forecasting, and counterfactual simulation.
"""

from .twin_engine import DigitalTwinEngine
from .wearable_sim import WearableTelemetryStream
from .ehr_connector import EHRConnector
from .counterfactual import CounterfactualSimulator

__all__ = [
    "DigitalTwinEngine",
    "WearableTelemetryStream",
    "EHRConnector",
    "CounterfactualSimulator"
]
