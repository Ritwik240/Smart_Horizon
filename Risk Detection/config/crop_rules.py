# config/crop_rules.py

"""
Crop-specific thresholds and rules for RiskDetectionAgent.
These values are aligned with the Data Ingestion Agent's schema
to ensure consistency across the pipeline.
"""

CROP_RULES = {
    "rice": {
        "temp": (20, 35),        # acceptable temperature range in °C
        "moisture": 60,          # minimum soil moisture percentage
        "humidity": 70           # minimum humidity percentage
    },
    "wheat": {
        "temp": (10, 25),
        "moisture": 40,
        "humidity": 50
    },
    "cotton": {
        "temp": (21, 30),
        "moisture": 35,
        "humidity": 60
    },
    "sugarcane": {
        "temp": (20, 38),
        "moisture": 65,
        "humidity": 65
    }
}