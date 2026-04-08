# agents/risk_agent.py

import numpy as np
import cv2
import os
import random
from ml_models.anomaly_model import AnomalyModel
from ml_models.image_model import ImageModel
from config.crop_rules import CROP_RULES

class RiskDetectionAgent:
    """
    RiskDetectionAgent analyzes crop field data and images
    to detect environmental anomalies, stress, and diseases.
    """

    def __init__(self):
        # Initialize models
        self.anomaly_model = AnomalyModel()
        self.image_model = ImageModel()
        self.class_names = self.image_model.class_names

    def detect_risk(self, data: dict, image_path: str) -> dict:
        """
        Evaluate crop field data and image to detect risks.
        Returns a dictionary with agent name, risks, score, and status.
        """
        crop = data.get("crop")
        if crop not in CROP_RULES:
            raise ValueError(f"Crop '{crop}' not supported in crop rules.")

        rules = CROP_RULES[crop]
        risks = []

        # --------------------------
        # RULE-BASED CHECKS
        # --------------------------
        temp = data.get("temperature", 0)
        moisture = data.get("soil_moisture", 0)
        humidity = data.get("humidity", 0)
        ndvi = data.get("ndvi", 0)

        if not (rules["temp"][0] <= temp <= rules["temp"][1]):
            risks.append(("Temperature Stress", "HIGH"))

        if moisture < rules["moisture"]:
            risks.append(("Water Stress", "HIGH"))

        if humidity < rules["humidity"]:
            risks.append(("Pest Probability", "MEDIUM"))

        if ndvi < 0.4:
            risks.append(("Nutrient Deficiency", "HIGH"))

        # --------------------------
        # ML ANOMALY DETECTION
        # --------------------------
        X = np.array([[temp, humidity, moisture, ndvi]])
        if self.anomaly_model.predict(X)[0] == -1:
            risks.append(("Environmental Anomaly", "HIGH"))

        # --------------------------
        # IMAGE-BASED DISEASE DETECTION
        # --------------------------
        if os.path.exists(image_path):
            img = cv2.imread(image_path)
            img = cv2.resize(img, (128, 128))
            img = np.expand_dims(img, axis=0)
            pred = self.image_model.predict(img)
            label = self.class_names[np.argmax(pred)]
            if "healthy" not in label.lower():
                risks.append(("Disease Detected", "HIGH"))

        # --------------------------
        # RISK SCORING
        # --------------------------
        score_map = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}
        score = sum(score_map[r[1]] for r in risks)

        status = "SAFE" if score == 0 else "ALERT"

        return {
            "agent": "RiskDetectionAgent",
            "crop": crop,
            "risks": risks,
            "risk_score": score,
            "status": status
        }

    def get_random_image(self, dataset_path="dataset") -> str:
        """
        Return a random image path from the dataset folder.
        """
        all_images = []
        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                if file.endswith((".jpg", ".png", ".jpeg")):
                    all_images.append(os.path.join(root, file))
        if not all_images:
            raise FileNotFoundError(f"No images found in the dataset path: {dataset_path}")
        return random.choice(all_images)

    def generate_random_input(self) -> dict:
        """
        Generate random field data input for testing/demo purposes.
        """
        return {
            "crop": random.choice(list(CROP_RULES.keys())),
            "temperature": random.uniform(5, 45),
            "humidity": random.uniform(30, 90),
            "soil_moisture": random.uniform(20, 80),
            "ndvi": random.uniform(0.2, 0.9)
        }