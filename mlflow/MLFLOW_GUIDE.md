# MLflow Integration Guide

## 📊 MLflow Setup for Intelligent Crop Irrigation Advisor

This document explains the MLflow integration in the project.

## Overview

MLflow has been integrated into all three models in the project:
1. **Crop Recommendation Model** - RandomForest Classifier
2. **Irrigation Optimization Model** - CatBoost Regressor
3. **Smart Irrigation Classifier** - CatBoost Classifier with Optuna

## Installation

Install required packages:

```bash
pip install -r requirements.txt
```

## Project Structure

```
Intelligent-Crop-Irrigation-Advisor/
├── mlflow_config.py          # Central MLflow configuration
├── launch_mlflow.py           # MLflow UI launcher
├── train_all_models.py        # Train all models with tracking
├── mlflow_analysis.py         # Compare and analyze experiments
├── mlruns/                    # MLflow tracking data (auto-created)
└── models/
    ├── crop recommendation/
    │   └── model_training.py  # Updated with MLflow
    ├── irrigation_optimization_model/
    │   └── train.py           # Updated with MLflow
    └── Smart_Irrigation_Classifier/
        └── train_model.py     # Updated with MLflow + Optuna
```

## Usage

### 1. Train All Models with MLflow Tracking

Train all models in sequence:

```bash
python train_all_models.py
```

Train a specific model:

```bash
# Train crop recommendation only
python train_all_models.py --model crop_recommendation

# Train irrigation optimization only
python train_all_models.py --model irrigation_optimization

# Train smart classifier only
python train_all_models.py --model smart_irrigation_classifier
```

### 2. Launch MLflow UI

View experiment results in the MLflow UI:

```bash
python launch_mlflow.py
```

Or with custom host/port:

```bash
python launch_mlflow.py --host 0.0.0.0 --port 8080
```

Then open your browser to: `http://localhost:5000`

### 3. Analyze and Compare Experiments

Compare all experiments:

```bash
python mlflow_analysis.py --action compare
```

Show best models:

```bash
python mlflow_analysis.py --action best
```

Export results to CSV:

```bash
python mlflow_analysis.py --action export
```

Run all analyses:

```bash
python mlflow_analysis.py --action all
```

## What Gets Tracked?

### For All Models:
- ✅ Model parameters (hyperparameters)
- ✅ Training/test dataset sizes
- ✅ Feature names and counts
- ✅ Model artifacts (.pkl files)
- ✅ Performance metrics
- ✅ Feature importance scores

### Crop Recommendation Model:
- Accuracy, Precision, Recall, F1 Score
- Classification report
- Number of crops
- Feature importance per feature

### Irrigation Optimization Model:
- MAE, RMSE, R² Score, Adjusted R²
- Feature importance visualization
- CatBoost training metrics

### Smart Irrigation Classifier:
- All Optuna trials (30 trials)
- Best hyperparameters
- Accuracy, Precision, Recall, F1 Score
- Feature importance
- Classification report

## MLflow UI Features

In the MLflow UI, you can:

1. **Compare Runs**: Select multiple runs and compare metrics/parameters
2. **Visualize Metrics**: View metric trends over time
3. **Download Artifacts**: Download saved models and reports
4. **Filter Runs**: Filter by metrics, parameters, or tags
5. **Register Models**: Register best models to Model Registry

## Experiment Names

The following experiments are created:
- `Crop-Recommendation-Model`
- `Irrigation-Optimization-Model`
- `Smart-Irrigation-Classifier-Model`

## Model Registry

Models are automatically registered with these names:
- `CropRecommendationModel`
- `IrrigationOptimizationModel`
- `SmartIrrigationClassifierModel`

## Loading Trained Models

Load a model from MLflow:

```python
import mlflow

# Load by run ID
model = mlflow.sklearn.load_model("runs:/<run_id>/crop_recommendation_model")

# Load from registry
model = mlflow.pyfunc.load_model("models:/CropRecommendationModel/latest")
```

## Best Practices

1. **Run Names**: Each run has a descriptive name
2. **Nested Runs**: Optuna trials are logged as nested runs
3. **Signatures**: Models include input/output signatures
4. **Artifacts**: All important files are logged
5. **Metrics**: Comprehensive metrics are tracked

## Troubleshooting

### Issue: MLflow not found
```bash
pip install mlflow>=2.9.0
```

### Issue: Port already in use
```bash
python launch_mlflow.py --port 5001
```

### Issue: Can't see experiments
Make sure you're in the project root directory when running scripts.

## Next Steps

1. Train models: `python train_all_models.py`
2. View results: `python launch_mlflow.py`
3. Compare models in the UI
4. Select best model from Model Registry
5. Deploy selected model

## Additional Resources

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [MLflow Model Registry](https://mlflow.org/docs/latest/model-registry.html)
- [MLflow Tracking](https://mlflow.org/docs/latest/tracking.html)
