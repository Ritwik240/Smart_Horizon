# tests/test_ml_models.py

import unittest
import numpy as np
import tensorflow as tf
from ml_models.anomaly_model import AnomalyDetectionModel
from ml_models.image_model import ImageClassificationModel

class TestMLModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize models once
        cls.anomaly_model = AnomalyDetectionModel()
        cls.image_model = ImageClassificationModel()
        # For testing, we can use a dummy image of correct shape
        cls.dummy_image = np.random.rand(1, 128, 128, 3).astype(np.float32)

    def test_anomaly_model_prediction(self):
        # Create dummy sensor data
        X_dummy = np.random.rand(5, 4)
        predictions = self.anomaly_model.predict(X_dummy)
        self.assertEqual(len(predictions), X_dummy.shape[0])
        self.assertTrue(all(p in [-1, 1] for p in predictions))  # IsolationForest outputs -1 (anomaly) or 1 (normal)

    def test_image_model_prediction_shape(self):
        # Test image model prediction returns expected shape
        preds = self.image_model.predict(self.dummy_image)
        self.assertEqual(preds.shape[0], 1)
        self.assertEqual(preds.shape[1], len(self.image_model.class_names))  # Number of classes

    def test_image_model_softmax(self):
        # Ensure predictions are probabilities that sum ~1
        preds = self.image_model.predict(self.dummy_image)
        total = np.sum(preds, axis=1)
        np.testing.assert_allclose(total, np.ones_like(total), rtol=1e-5)

if __name__ == "__main__":
    unittest.main()