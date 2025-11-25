import os
import sys
import pandas as pd
import numpy as np
from src.exception import CustomException
import dill
from sklearn.metrics import r2_score,accuracy_score
from sklearn.model_selection import GridSearchCV
from src.logger import logging

def save_object(file_path,obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)

    except Exception as e:
        raise CustomException(e,sys)


def evaluate_model(X_train,y_train,X_test,y_test,models,params):
    try:
        report = {}
        for model_name in models:
            model = models[model_name]
            param_grid = params[model_name]

            logging.info(f"Performing GridSearchCV for {model_name}...")
            grid_search = GridSearchCV(model, param_grid, cv=3)
            grid_search.fit(X_train, y_train)

            best_model = grid_search.best_estimator_
            logging.info(f"Best params for {model_name}: {grid_search.best_params_}")

            # Train best model again on full training data
            best_model.fit(X_train, y_train)

            # Predict and evaluate
            train_preds = best_model.predict(X_train)
            test_preds = best_model.predict(X_test)

            train_acc = accuracy_score(y_train, train_preds)
            test_acc = accuracy_score(y_test, test_preds)

            logging.info(f"{model_name} - Train Accuracy: {train_acc:.4f}, Test Accuracy: {test_acc:.4f}")

            report[model_name] = {
                "train_accuracy": train_acc,
                "test_accuracy": test_acc,
                "best_model": best_model
            }

        return report


    except Exception as e:
        raise CustomException(e,sys)


def load_object(file_path):
    try:
        with open(file_path,'rb') as file_obj:      
            return dill.load(file_obj)
        
    except Exception as e:
        raise CustomException(e,sys)