"""
MLflow Configuration for Intelligent Crop Irrigation Advisor
===========================================================
This module provides centralized MLflow configuration and utilities
for tracking experiments across all models in the project.
"""

import mlflow
import os
from pathlib import Path

# Project root directory (go up one level from mlflow_tools)
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

# MLflow tracking URI (local file store)
MLFLOW_TRACKING_URI = f"file://{PROJECT_ROOT}/mlruns"

# Experiment names for different models
EXPERIMENTS = {
    'crop_recommendation': 'Crop-Recommendation-Model',
    'irrigation_optimization': 'Irrigation-Optimization-Model',
    'smart_irrigation_classifier': 'Smart-Irrigation-Classifier-Model'
}

def setup_mlflow(experiment_name: str):
    """
    Setup MLflow tracking for a specific experiment.
    
    Args:
        experiment_name: Name of the experiment (use EXPERIMENTS dict keys)
    
    Returns:
        experiment_id: The ID of the created/existing experiment
    """
    # Set tracking URI
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    
    # Get full experiment name
    full_experiment_name = EXPERIMENTS.get(experiment_name, experiment_name)
    
    # Set experiment
    mlflow.set_experiment(full_experiment_name)
    
    # Get experiment
    experiment = mlflow.get_experiment_by_name(full_experiment_name)
    
    print(f"✅ MLflow configured successfully!")
    print(f"📊 Experiment: {full_experiment_name}")
    print(f"🔗 Tracking URI: {MLFLOW_TRACKING_URI}")
    print(f"🆔 Experiment ID: {experiment.experiment_id}")
    
    return experiment.experiment_id

def log_dataset_info(df, dataset_name="dataset"):
    """Log dataset information to MLflow."""
    mlflow.log_param(f"{dataset_name}_shape", df.shape)
    mlflow.log_param(f"{dataset_name}_rows", df.shape[0])
    mlflow.log_param(f"{dataset_name}_cols", df.shape[1])
    mlflow.log_param(f"{dataset_name}_columns", list(df.columns))

def log_model_with_signature(model, X_train, y_train, model_name="model"):
    """
    Log model to MLflow with input/output signature.
    
    Args:
        model: Trained model object
        X_train: Training features for signature inference
        y_train: Training target for signature inference
        model_name: Name to save the model as
    """
    from mlflow.models.signature import infer_signature
    
    # Infer signature
    signature = infer_signature(X_train, y_train)
    
    # Log model
    mlflow.sklearn.log_model(
        model, 
        model_name,
        signature=signature
    )
    
    print(f"✅ Model '{model_name}' logged to MLflow with signature")

def compare_runs(experiment_name: str, metric_name: str = "accuracy", top_n: int = 5):
    """
    Compare top N runs for a given experiment.
    
    Args:
        experiment_name: Name of the experiment
        metric_name: Metric to sort by
        top_n: Number of top runs to return
    
    Returns:
        DataFrame with top runs
    """
    import pandas as pd
    
    # Get experiment
    full_experiment_name = EXPERIMENTS.get(experiment_name, experiment_name)
    experiment = mlflow.get_experiment_by_name(full_experiment_name)
    
    if experiment is None:
        print(f"❌ Experiment '{full_experiment_name}' not found!")
        return None
    
    # Search runs
    runs = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=[f"metrics.{metric_name} DESC"],
        max_results=top_n
    )
    
    return runs

if __name__ == "__main__":
    print("🚀 MLflow Configuration")
    print(f"📁 Project Root: {PROJECT_ROOT}")
    print(f"🔗 Tracking URI: {MLFLOW_TRACKING_URI}")
    print(f"📊 Available Experiments: {list(EXPERIMENTS.values())}")
