import numpy as np
from src.model_handler import ModelHandler


def test_model_prediction():
    handler = ModelHandler()
    test_image = np.random.rand(256, 256)
    prediction = handler.predict(test_image)
    assert isinstance(prediction, float)
