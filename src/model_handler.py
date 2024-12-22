import tensorflow as tf
import numpy as np
from pathlib import Path
from PIL import Image


class ModelHandler:
    def __init__(self, model_path: str = "src/models/raw_model.h5"):
        self.model_path = Path(model_path)
        self.model = None
        self._load_model()

    def _load_model(self):
        self.model = tf.keras.models.load_model(self.model_path)

    def predict(self, image_input) -> float:
        """Process image (file path or NumPy array) through model and return prediction"""
        # Check if input is a NumPy array
        if isinstance(image_input, np.ndarray):
            image_array = image_input
        else:
            # Assume it's a file path, load and preprocess the image
            image = Image.open(image_input)
            image_array = np.array(image)

        # Convert to grayscale if RGB
        if len(image_array.shape) == 3:
            image_array = np.mean(image_array, axis=-1)

        # Add batch and channel dimensions
        image_array = np.expand_dims(image_array, axis=0)
        image_array = np.expand_dims(image_array, axis=-1)

        # Normalize to [0,1] if not already
        if image_array.max() > 1:
            image_array = image_array / 255.0

        return float(self.model.predict(image_array)[0][0])
