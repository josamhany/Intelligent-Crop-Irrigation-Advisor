import os
import sys
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from src.utils import evaluate_model, save_object

@dataclass
class ModelTrainerConfig:
    trained_model_file_path:str = os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self,X_train, y_train, X_test, y_test):
        try:
            logging.info("loaded x/y train/test data from train pipeline")

            models = {
                "SVC": SVC(),
                "RandomForest": RandomForestClassifier(),
                "KNN": KNeighborsClassifier()
            }

            params = {
                "SVC": {"kernel": ["linear", "rbf"], "C": [1, 10]},
                "RandomForest": {"n_estimators": [50, 100], "max_depth": [5, 10]},
                "KNN": {"n_neighbors": [3, 5, 7]}
            }

            model_report = evaluate_model(X_train, y_train, X_test, y_test, models, params)

            # Extract the best model
            best_model_name = max(model_report, key=lambda k: model_report[k]["test_accuracy"])
            best_model = model_report[best_model_name]["best_model"]
            best_accuracy = model_report[best_model_name]["test_accuracy"]

            # Save model
            save_object(self.model_trainer_config.trained_model_file_path, best_model)

            logging.info(f"Best Model: {best_model_name} | Test Accuracy: {best_accuracy:.4f}")
            # print(model_report)
            print("Best Model is", best_model_name,"with", best_accuracy,"Test accuracy")
            return best_model_name, model_report[best_model_name]

        except Exception as e:
            raise CustomException(e,sys)

