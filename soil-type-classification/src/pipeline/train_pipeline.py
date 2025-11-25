import os
import sys
from sklearn.model_selection import train_test_split
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.logger import logging
from src.exception import CustomException


class TrainPipeline:
    def __init__(self):
        self.data_ingestion = DataIngestion()
        self.data_transformation = DataTransformation()
        self.model_trainer = ModelTrainer()


    def run_pipeline(self):
        logging.info("Starting the training pipeline...")

        try:
            # STEP 1: Ingest the data
            logging.info("Running data ingestion...")
            df = self.data_ingestion.create_dataset_csv()

            # STEP 2: Transform the data
            logging.info("Running data transformation...")
            X, y = self.data_transformation.transform_data(df)

            # STEP 3: Train-test split
            logging.info("Splitting data into train/test sets...")
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

            logging.info(f"Data split complete. Train shape: {X_train.shape}, Test shape: {X_test.shape}")

            # STEP 4: Train the model
            logging.info("Model Training...")
            self.model_trainer.initiate_model_trainer(X_train, y_train, X_test, y_test)

            logging.info("Training Pipeline completed successfully.")

        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    pipeline = TrainPipeline()
    pipeline.run_pipeline()
