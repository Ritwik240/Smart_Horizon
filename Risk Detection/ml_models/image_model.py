# ml_models/image_model.py

import tensorflow as tf
import numpy as np
import os

class ImageModel:
    """
    TensorFlow CNN model for plant disease detection.
    Includes model creation, compilation, training, and prediction methods.
    """

    def __init__(self, image_size=(128, 128), batch_size=32):
        self.image_size = image_size
        self.batch_size = batch_size
        self.model = self._build_model()
        self.class_names = []

    def _build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Rescaling(1./255, input_shape=(*self.image_size, 3)),
            tf.keras.layers.Conv2D(32, 3, activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(64, 3, activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(128, 3, activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(1, activation='softmax')  # placeholder, will adjust after dataset
        ])
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        return model

    def prepare_dataset(self, dataset_path="dataset"):
        """
        Loads and preprocesses image dataset from a directory.
        """
        dataset = tf.keras.preprocessing.image_dataset_from_directory(
            dataset_path,
            image_size=self.image_size,
            batch_size=self.batch_size
        )
        self.class_names = dataset.class_names
        # Update final Dense layer based on number of classes
        self.model.pop()  # Remove placeholder Dense
        self.model.add(tf.keras.layers.Dense(len(self.class_names), activation='softmax'))
        self.model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        return dataset

    def train(self, dataset, epochs=2):
        """
        Train the CNN on the provided dataset.
        """
        self.model.fit(dataset, epochs=epochs)

    def predict(self, img_array):
        """
        Predict disease class from a preprocessed image array.
        Returns the prediction probabilities.
        """
        if img_array.ndim == 3:  # Single image, add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
        preds = self.model.predict(img_array)
        return preds

    def predict_label(self, img_array):
        """
        Returns the class label with highest probability.
        """
        preds = self.predict(img_array)
        if self.class_names:
            return self.class_names[np.argmax(preds)]
        return "Unknown"