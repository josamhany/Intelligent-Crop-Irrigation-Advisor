#!/usr/bin/env python3
"""
Quick Demo: MLflow Integration
==============================
This script demonstrates the MLflow integration without training all models.
It creates a simple demo run to verify the setup.
"""

import mlflow
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from mlflow_config import setup_mlflow

def run_demo():
    """Run a quick demo of MLflow integration."""
    print("🎯 MLflow Integration Demo")
    print("=" * 80)
    print()
    
    # Setup MLflow
    setup_mlflow('crop_recommendation')
    
    # Create synthetic data
    print("📊 Creating synthetic dataset...")
    np.random.seed(42)
    n_samples = 1000
    
    X = np.random.randn(n_samples, 7)
    y = np.random.choice(['rice', 'wheat', 'maize'], n_samples)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"✅ Dataset created: {n_samples} samples, 7 features")
    print()
    
    # Start MLflow run
    print("🚀 Starting MLflow run...")
    with mlflow.start_run(run_name="Demo_Run"):
        
        # Log parameters
        mlflow.log_param("model_type", "RandomForestClassifier")
        mlflow.log_param("n_estimators", 10)
        mlflow.log_param("test_size", 0.2)
        mlflow.log_param("demo", True)
        
        # Train simple model
        print("🔄 Training model...")
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Log metric
        mlflow.log_metric("accuracy", accuracy)
        
        print(f"✅ Model trained with accuracy: {accuracy:.4f}")
        print()
        
        # Log model
        mlflow.sklearn.log_model(model, "demo_model")
        
        run_id = mlflow.active_run().info.run_id
        
        print("=" * 80)
        print("✅ Demo completed successfully!")
        print()
        print(f"🔗 Run ID: {run_id}")
        print(f"📊 Accuracy: {accuracy:.4f}")
        print()
        print("View results:")
        print("   python launch_mlflow.py")
        print()
        print("Then open: http://localhost:5000")
        print("=" * 80)

if __name__ == "__main__":
    try:
        run_demo()
    except ImportError as e:
        print("❌ Error: Missing dependencies")
        print(f"   {e}")
        print()
        print("Please install MLflow first:")
        print("   pip install mlflow")
        print()
        print("Or run the setup script:")
        print("   ./setup_mlflow.sh")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
