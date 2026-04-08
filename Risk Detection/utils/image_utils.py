# utils/image_utils.py

import os
import random
import cv2
import numpy as np
import tensorflow as tf

def get_random_image(dataset_path: str = "dataset") -> str:
    """
    Returns a random image file path from the dataset directory.
    """
    all_images = [
        os.path.join(root, file)
        for root, dirs, files in os.walk(dataset_path)
        for file in files
        if file.lower().endswith((".jpg", ".jpeg", ".png"))
    ]
    if not all_images:
        raise FileNotFoundError(f"No images found in the dataset path: {dataset_path}")
    return random.choice(all_images)


def preprocess_image(image_path: str, image_size: tuple = (128, 128)) -> np.ndarray:
    """
    Reads an image from the path, resizes it, normalizes it, and returns as numpy array.
    Adds a batch dimension.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Unable to read image: {image_path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, image_size)
    img = img.astype(np.float32) / 255.0
    return np.expand_dims(img, axis=0)  # Add batch dimension


def load_image_dataset(dataset_path: str = "dataset", image_size: tuple = (128, 128), batch_size: int = 32):
    """
    Loads the dataset from directory as a TensorFlow image dataset.
    Uses `tf.keras.utils.image_dataset_from_directory`.
    """
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset path does not exist: {dataset_path}")

    dataset = tf.keras.utils.image_dataset_from_directory(
        dataset_path,
        image_size=image_size,
        batch_size=batch_size
    )
    class_names = dataset.class_names
    return dataset, class_names