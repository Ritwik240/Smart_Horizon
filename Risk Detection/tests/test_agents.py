# tests/test_agents.py

import unittest
import os
from agents.risk_agent import RiskDetectionAgent
from config.crop_rules import CROP_RULES

class TestRiskDetectionAgent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize the agent once for all tests
        cls.agent = RiskDetectionAgent(image_dataset_path="dataset")  # Ensure this path exists for image tests

    def test_generate_random_input(self):
        # Test that generated random input has all required keys
        data = self.agent.generate_random_input()
        self.assertIn("crop", data)
        self.assertIn("temperature", data)
        self.assertIn("humidity", data)
        self.assertIn("soil_moisture", data)
        self.assertIn("ndvi", data)
        self.assertIn(data["crop"], CROP_RULES)

    def test_get_random_image(self):
        # Test that a random image path is returned
        img_path = self.agent.get_random_image()
        self.assertTrue(os.path.exists(img_path))

    def test_detect_risk_structure(self):
        # Test that detect_risk returns the correct structure
        sample_input = self.agent.generate_random_input()
        image_path = self.agent.get_random_image()
        result = self.agent.detect_risk(sample_input, image_path)
        self.assertIn("agent", result)
        self.assertIn("crop", result)
        self.assertIn("risks", result)
        self.assertIn("risk_score", result)
        self.assertIn("status", result)
        self.assertIsInstance(result["risks"], list)
        self.assertIsInstance(result["risk_score"], int)
        self.assertIn(result["status"], ["SAFE", "ALERT"])

if __name__ == "__main__":
    unittest.main()