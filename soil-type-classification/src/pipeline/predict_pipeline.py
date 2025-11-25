import os
import sys
import cv2
import numpy as np
from src.logger import logging
from src.exception import CustomException
from src.utils import load_object
from sklearn.preprocessing import LabelEncoder


class PredictPipeline:
    def __init__(self):
        self.model_path = os.path.join('artifacts', 'model.pkl')
        self.label_encoder_path = os.path.join('artifacts', 'label_encoder.pkl')
        self.image_size = (128, 128)

        # Load model and label encoder
        self.model = load_object(self.model_path)
        self.label_encoder: LabelEncoder = load_object(self.label_encoder_path)

    def extract_color_histogram(self, image, bins=(16, 16, 16)):
        try:
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            hist = cv2.calcHist([hsv], [0, 1, 2], None, bins, [0, 180, 0, 256, 0, 256])
            cv2.normalize(hist, hist)
            return hist.flatten()
        except Exception as e:
            raise CustomException(e, sys)

    def predict(self, image_path: str):
        try:
            # Load and preprocess image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Image not found or corrupted: {image_path}")

            image = cv2.resize(image, self.image_size)
            features = self.extract_color_histogram(image)
            features = np.array([features])  # Shape (1, n_features)

            # Predict
            prediction = self.model.predict(features)
            predicted_label = self.label_encoder.inverse_transform(prediction)

            return predicted_label[0]

        except Exception as e:
            raise CustomException(e, sys)
