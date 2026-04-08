# ml_models/anomaly_model.py

import numpy as np
from sklearn.ensemble import IsolationForest

class AnomalyModel:
    """
    IsolationForest-based environmental anomaly detection.
    Detects anomalies in sensor data (temperature, humidity, soil moisture, NDVI).
    """

    def __init__(self, contamination=0.1, random_state=42):
        self.contamination = contamination
        self.random_state = random_state
        self.model = IsolationForest(contamination=self.contamination, random_state=self.random_state)
        self.is_trained = False

    def fit(self, data: np.ndarray):
        """
        Fit the IsolationForest model to the input sensor data.
        data: np.ndarray of shape (n_samples, n_features)
        """
        if data.ndim != 2:
            raise ValueError("Input data must be a 2D numpy array (n_samples, n_features)")
        self.model.fit(data)
        self.is_trained = True

    def predict(self, sample: np.ndarray) -> int:
        """
        Predict if the input sample is normal or anomalous.
        Returns -1 for anomaly, 1 for normal.
        """
        if not self.is_trained:
            raise RuntimeError("Model must be trained before prediction.")
        if sample.ndim == 1:
            sample = sample.reshape(1, -1)
        return self.model.predict(sample)[0]

    def predict_batch(self, samples: np.ndarray) -> np.ndarray:
        """
        Predict anomalies for a batch of samples.
        Returns array of -1 (anomaly) or 1 (normal) values.
        """
        if not self.is_trained:
            raise RuntimeError("Model must be trained before prediction.")
        return self.model.predict(samples)