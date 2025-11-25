import os
import sys
from src.logger import logging
import pandas as pd
import numpy as np
import cv2
from dataclasses import dataclass
from src.exception import CustomException
from sklearn.preprocessing import LabelEncoder
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    transformed_data_dir: str = os.path.join('data', 'processed') # Stores transformed datasets ready for training/test
    image_size: tuple = (128, 128)  
    histogram_bins: tuple = (16, 16, 16)
    feature_extraction_method: str = "color_histogram"  
    label_Encoder = os.path.join("artifacts", "label_encoder.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def extract_color_histogram(self,image):
        try:
            # Convert image to HSV
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            bins = self.data_transformation_config.histogram_bins
            # Extract color histogram
            hist = cv2.calcHist([hsv], [0, 1, 2], None, bins, [0, 180, 0, 256, 0, 256])
            
            # Normalize and flatten
            cv2.normalize(hist, hist)
            return hist.flatten()
        
        except Exception as e:
            raise CustomException(e,sys)

    def transform_data(self, df: pd.DataFrame):
            logging.info("Initiate Transformation of data")
            try:
                features = []
                labels = []

                for idx, row in df.iterrows():
                    img_path = row['image_path']
                    label = row['label']

                    image = cv2.imread(img_path)
                    if image is None:
                        continue

                    image = cv2.resize(image, (self.data_transformation_config.image_size))
                    feature_vector = self.extract_color_histogram(image)
                    features.append(feature_vector)
                    labels.append(label)

                # Transform label into numerical data
                label_encoder = LabelEncoder()
                y = label_encoder.fit_transform(labels)  

                logging.info("Converting Transformed data into numpy array")       
                # Convert to NumPy arrays
                X = np.array(features)

                # Save label encoder
                os.makedirs(self.data_transformation_config.transformed_data_dir, exist_ok=True)
                save_object(self.data_transformation_config.label_Encoder, label_encoder)

                # Save feature and label arrays using your custom utility
                save_object(os.path.join(self.data_transformation_config.transformed_data_dir, "X.pkl"), X)
                save_object(os.path.join(self.data_transformation_config.transformed_data_dir, "y.pkl"), y)

                logging.info("Data Transformation Done")
                return X, y
            
            except Exception as e:
                raise CustomException(e,sys)