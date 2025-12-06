#!/usr/bin/env python3
"""
Train All Models with MLflow Tracking
=====================================
This script trains all models in the project with MLflow tracking enabled.
"""

import subprocess
import sys
from pathlib import Path
import time

# PROJECT_ROOT should be the project root, not mlflow_tools folder
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

MODELS = {
    "crop_recommendation": {
        "name": "Crop Recommendation Model",
        "path": PROJECT_ROOT / "models" / "crop recommendation" / "model_training.py",
        "description": "RandomForest classifier for crop recommendation based on soil and weather conditions"
    },
    "irrigation_optimization": {
        "name": "Irrigation Optimization Model",
        "path": PROJECT_ROOT / "models" / "irrigation_optimization_model" / "train.py",
        "description": "CatBoost regressor for optimal irrigation water amount prediction"
    },
    "smart_irrigation_classifier": {
        "name": "Smart Irrigation Classifier",
        "path": PROJECT_ROOT / "models" / "Smart_Irrigation_Classifier" / "train_model.py",
        "description": "CatBoost classifier with Optuna optimization for irrigation status classification"
    }
}

def print_header(text, char="="):
    """Print a formatted header."""
    print(f"\n{char * 80}")
    print(f"  {text}")
    print(f"{char * 80}\n")

def train_model(model_key, model_info):
    """Train a single model."""
    print_header(f"Training {model_info['name']}", "=")
    print(f"📝 Description: {model_info['description']}")
    print(f"📂 Script: {model_info['path']}")
    print()
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [sys.executable, str(model_info['path'])],
            cwd=model_info['path'].parent,
            capture_output=False,
            text=True
        )
        
        elapsed_time = time.time() - start_time
        
        if result.returncode == 0:
            print(f"\n✅ {model_info['name']} trained successfully!")
            print(f"⏱️  Training time: {elapsed_time:.2f} seconds")
            return True
        else:
            print(f"\n❌ {model_info['name']} training failed with return code {result.returncode}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error training {model_info['name']}: {e}")
        return False

def train_all_models():
    """Train all models in sequence."""
    print_header("Intelligent Crop Irrigation Advisor - MLflow Training Pipeline", "█")
    print("🎯 This script will train all models with MLflow tracking enabled")
    print(f"📊 Results will be saved to: {PROJECT_ROOT / 'mlruns'}")
    print(f"🔗 View results with: python launch_mlflow.py")
    print()
    
    results = {}
    total_start = time.time()
    
    for key, info in MODELS.items():
        success = train_model(key, info)
        results[key] = success
        
        if not success:
            print(f"\n⚠️  Warning: {info['name']} failed")
            response = input("Continue with next model? (y/n): ")
            if response.lower() != 'y':
                print("Training pipeline stopped.")
                break
    
    total_time = time.time() - total_start
    
    # Print summary
    print_header("Training Summary", "█")
    print(f"⏱️  Total time: {total_time:.2f} seconds ({total_time/60:.2f} minutes)")
    print()
    
    for key, success in results.items():
        status = "✅ Success" if success else "❌ Failed"
        print(f"{status}: {MODELS[key]['name']}")
    
    print()
    print("📊 View results in MLflow UI:")
    print("   python launch_mlflow.py")
    print()

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Train all models with MLflow tracking")
    parser.add_argument(
        "--model",
        choices=list(MODELS.keys()),
        help="Train a specific model only"
    )
    
    args = parser.parse_args()
    
    if args.model:
        # Train specific model
        train_model(args.model, MODELS[args.model])
    else:
        # Train all models
        train_all_models()

if __name__ == "__main__":
    main()
