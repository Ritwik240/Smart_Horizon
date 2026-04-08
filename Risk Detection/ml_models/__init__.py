# ml_models/__init__.py

"""
ML Models package for RiskDetectionAgent.

Includes:
- image_model.py: CNN model for plant disease detection.
- anomaly_model.py: IsolationForest model for environmental anomaly detection.
"""

from .image_model import ImageModel
from .anomaly_model import AnomalyModel

__all__ = ["ImageModel", "AnomalyModel"]