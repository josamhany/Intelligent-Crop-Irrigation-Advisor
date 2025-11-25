# MLflow Tools

This directory contains all MLflow-related utilities for experiment tracking and model management.

## 📁 Files

- **`mlflow_config.py`** - Central MLflow configuration
- **`train_all_models.py`** - Train all models with MLflow tracking
- **`launch_mlflow.py`** - Launch MLflow UI
- **`mlflow_analysis.py`** - Compare and analyze experiments
- **`demo_mlflow.py`** - Quick demo to test MLflow integration
- **`setup_mlflow.sh`** - Automated setup script
- **`QUICKSTART.sh`** - Interactive quick start guide
- **`MLFLOW_GUIDE.md`** - Complete documentation

## 📦 Installation

Before using MLflow tools, install dependencies:

### Option 1: Virtual Environment (Recommended)
```bash
cd /path/to/project
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Option 2: System Package Manager (Arch Linux)
```bash
sudo pacman -S python-mlflow python-optuna
```

### Option 3: Using pipx
```bash
pipx install mlflow
pipx install optuna
```

### Verify Installation
```bash
python -c "import mlflow; print('MLflow:', mlflow.__version__)"
```

## 🚀 Quick Start

### 1. Train Models
```bash
# From project root
python mlflow_tools/train_all_models.py

# Or train specific model
python mlflow_tools/train_all_models.py --model crop_recommendation
```

### 2. Launch MLflow UI
```bash
python mlflow_tools/launch_mlflow.py
# Open: http://localhost:5000
```

### 3. Analyze Results
```bash
python mlflow_tools/mlflow_analysis.py --action all
```

### 4. Quick Demo
```bash
python mlflow_tools/demo_mlflow.py
```

## 📊 Tracked Experiments

1. **Crop-Recommendation-Model** - RandomForest Classifier
2. **Irrigation-Optimization-Model** - CatBoost Regressor
3. **Smart-Irrigation-Classifier-Model** - CatBoost Classifier + Optuna

## 🎯 What Gets Tracked

- Model hyperparameters
- Dataset information
- Performance metrics (Accuracy, R², MAE, RMSE, etc.)
- Feature importance
- Model artifacts (.pkl files)
- Classification reports and visualizations

## 📦 Model Registry

Models are registered with these names:
- `CropRecommendationModel`
- `IrrigationOptimizationModel`
- `SmartIrrigationClassifierModel`

## 🔧 Usage Tips

- All MLflow data is stored in `mlruns/` directory at project root
- Use MLflow UI to compare runs and select best models
- Export results to CSV using `mlflow_analysis.py`

For more details, see `MLFLOW_GUIDE.md` in project root.
