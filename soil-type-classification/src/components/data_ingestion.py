import os
import sys
import pandas as pd
from src.exception import  CustomException
from src.logger import logging
from dataclasses import dataclass


@dataclass
class DataIngestionConfig:
    raw_data_dir: str = os.path.join('data', 'raw', 'soil-types')
    processed_data_dir: str = os.path.join('data', 'processed')
    dataset_info_file: str = os.path.join('data', 'dataset.csv')  # write image paths and labels


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def create_dataset_csv(self):
        logging.info("Entered the create dataset csv method")
        try:
            image_paths = []
            labels = []
            logging.info("walk throughout data folder and extract all the images path")
            for root, dirs, files in os.walk(self.ingestion_config.raw_data_dir):
                for file in files:
                    if file.endswith(('.png', '.jpg', '.jpeg')):
                        full_path = os.path.join(root, file)
                        label = os.path.basename(os.path.dirname(full_path))
                        image_paths.append(full_path)
                        labels.append(label)

            logging.info("making dataframe using fetched image path and labels")

            df = pd.DataFrame({'image_path': image_paths, 'label': labels})
            os.makedirs(os.path.dirname(self.ingestion_config.dataset_info_file), exist_ok=True)
            df.to_csv(self.ingestion_config.dataset_info_file, index=False)
            print(f"Dataset CSV saved to {self.ingestion_config.dataset_info_file}")

            logging.info("Ingestion of data is completed")
            return df
        
        except Exception as e:
            raise CustomException(e,sys)

