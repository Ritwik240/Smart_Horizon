# tests/test_utils.py

import unittest
import os
import numpy as np
from utils import image_utils, input_utils, scoring_utils

class TestUtils(unittest.TestCase):

    def setUp(self):
        # Setup a dummy image array for image_utils tests
        self.dummy_image = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
        self.dataset_path = "dataset"  # dummy path for get_random_image test
        os.makedirs(self.dataset_path, exist_ok=True)

        # Create a dummy image file for get_random_image
        self.dummy_file = os.path.join(self.dataset_path, "dummy.jpg")
        from cv2 import imwrite
        imwrite(self.dummy_file, self.dummy_image)

    def tearDown(self):
        # Cleanup dummy files/folders
        try:
            os.remove(self.dummy_file)
            os.rmdir(self.dataset_path)
        except Exception:
            pass

    # ---------- image_utils tests ----------
    def test_preprocess_image_shape(self):
        processed = image_utils.preprocess_image(self.dummy_file)
        self.assertEqual(processed.shape, (1, 128, 128, 3))
        self.assertTrue((processed >= 0.0).all() and (processed <= 1.0).all())

    # ---------- input_utils tests ----------
    def test_generate_random_input_keys(self):
        record = input_utils.generate_random_input()
        expected_keys = {"crop", "temperature", "humidity", "soil_moisture", "ndvi"}
        self.assertSetEqual(set(record.keys()), expected_keys)

    def test_load_input_data_fallback(self):
        # Provide invalid paths to ensure fallback is triggered
        data = input_utils.load_input_data(api_url="http://invalid", json_path="nonexistent.json")
        self.assertEqual(len(data), 1)
        self.assertIn("crop", data[0])

    # ---------- scoring_utils tests ----------
    def test_compute_risk_score(self):
        risks = [("Temp Stress", "LOW"), ("Water Stress", "HIGH")]
        score = scoring_utils.compute_risk_score(risks)
        # LOW=1, HIGH=3 => total 4
        self.assertEqual(score, 4)

if __name__ == "__main__":
    unittest.main()