# 🌾 Intelligent Crop Irrigation Advisor

An AI-powered web application that provide### Dependencies (Verified Working)
- Python 3.11+
- Streamlit 1.50.0
- CatBoost 1.2.8 (for irrigation models)
- Scikit-learn 1.7.2 (for crop recommendation)
- NumPy 2.3.3
- Pandas 2.3.3
- Joblib (for model loading)

## ✅ Advanced Fail-Safe System

### Multi-Layer Protection
1. **Model Loading Validation**: Comprehensive checks for all 3 models
2. **Input Validation**: Range checking and realistic value verification  
3. **Prediction Confidence**: Minimum thresholds for reliable results
4. **Exception Handling**: Graceful fallback to safe default values
# 🌾 Intelligent Crop Irrigation Advisor

An AI-powered web application that provides crop recommendations and irrigation advice (classification + optimization) using lightweight ML models and a Streamlit UI with **full MLflow experiment tracking**.

## 🎯 Overview

- Crop recommendation (RandomForest)
- Smart irrigation decision (CatBoost classifier with Optuna optimization)
- Irrigation amount optimization (CatBoost regressor)
- **MLflow experiment tracking and model management**
- Modular feature-engineering pipeline and fail-safe mechanisms

## 🚀 Quick Start (Linux / macOS)

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Or use the automated setup script
./mlflow_tools/setup_mlflow.sh
```

### 2. Train Models with MLflow Tracking

```bash
# Train all models with MLflow tracking
python mlflow_tools/train_all_models.py

# Or train a specific model
python mlflow_tools/train_all_models.py --model crop_recommendation
python mlflow_tools/train_all_models.py --model irrigation_optimization
python mlflow_tools/train_all_models.py --model smart_irrigation_classifier
```

### 3. View Results in MLflow UI

```bash
# Launch MLflow UI
python mlflow_tools/launch_mlflow.py

# Then open: http://localhost:5000
```

### 4. Run the Streamlit Application

```bash
# Launch the app
python -m streamlit run frontend/streamlit_dashboard/app.py --server.port=8503
```

## 📊 MLflow Integration

### Features

- ✅ **Experiment Tracking**: All training runs are tracked with parameters and metrics
- ✅ **Model Registry**: Automatic model registration for deployment
- ✅ **Hyperparameter Optimization**: Optuna trials tracked in MLflow
- ✅ **Comparison Tools**: Compare model performance across experiments
- ✅ **Artifact Storage**: Model files, reports, and visualizations saved

### MLflow Commands

```bash
# Demo MLflow integration (quick test)
python mlflow_tools/demo_mlflow.py

# Train all models with tracking
python mlflow_tools/train_all_models.py

# Launch MLflow UI
python mlflow_tools/launch_mlflow.py

# Analyze and compare experiments
python mlflow_tools/mlflow_analysis.py --action all
```

### Experiments Created

1. **Crop-Recommendation-Model** - RandomForest classifier
2. **Irrigation-Optimization-Model** - CatBoost regressor  
3. **Smart-Irrigation-Classifier-Model** - CatBoost classifier with Optuna

## 📁 Project Structure

```
Intelligent-Crop-Irrigation-Advisor/
├── mlflow_tools/                 # All MLflow utilities
│   ├── mlflow_config.py          # MLflow central configuration
│   ├── train_all_models.py       # Train all models with tracking
│   ├── launch_mlflow.py          # MLflow UI launcher
│   ├── mlflow_analysis.py        # Experiment comparison tools
│   ├── demo_mlflow.py            # Quick MLflow demo
│   ├── setup_mlflow.sh           # Automated setup script
│   ├── MLFLOW_GUIDE.md           # Detailed MLflow guide
│   ├── SETUP_MLFLOW.md           # Installation guide
│   └── README.md                 # MLflow tools documentation
├── mlruns/                       # MLflow tracking data (auto-created)
├── frontend/
│   └── streamlit_dashboard/      # Streamlit UI
├── models/
│   ├── crop recommendation/      # Crop model (updated with MLflow)
│   ├── irrigation_optimization_model/  # Irrigation regressor (updated)
│   └── Smart_Irrigation_Classifier/    # Classifier with Optuna (updated)
├── data/                         # Training datasets
├── docs/                         # Project documentation
└── requirements.txt              # Dependencies (includes MLflow)
```

## 🔧 Windows Setup (PowerShell)

```powershell
# Create environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Train models
python train_all_models.py

# Launch MLflow UI
python launch_mlflow.py

# Run Streamlit app
python -m streamlit run frontend/streamlit_dashboard/app.py --server.port=8503
```

## 📚 Documentation

- **[MLFLOW_GUIDE.md](MLFLOW_GUIDE.md)** - Complete MLflow integration guide
- **[SETUP_MLFLOW.md](SETUP_MLFLOW.md)** - Installation instructions
- **[docs/](docs/)** - Model documentation and user guides

## 🧪 What Gets Tracked in MLflow

### All Models
- Model hyperparameters
- Dataset information (size, features)
- Performance metrics
- Feature importance scores
- Model artifacts (.pkl files)
- Training/test splits

### Crop Recommendation Model
- Accuracy, Precision, Recall, F1 Score
- Classification report
- Feature importance per feature

### Irrigation Optimization Model  
- MAE, RMSE, R², Adjusted R²
- Feature importance visualization
- CatBoost training metrics

### Smart Irrigation Classifier
- All 30 Optuna trials tracked
- Best hyperparameters
- Accuracy, Precision, Recall, F1 Score
- Classification report

## 🌟 Key Features

1. **Automated Training Pipeline** - Train all models with one command
2. **Experiment Tracking** - Compare model performance over time
3. **Model Registry** - Centralized model management
4. **Hyperparameter Optimization** - Optuna integration with MLflow
5. **Interactive UI** - MLflow dashboard for visualization
6. **Export Results** - Export metrics to CSV for analysis

## 📋 Requirements

- Python 3.11+
- Streamlit 1.50.0
- CatBoost 1.2.8
- Scikit-learn 1.7.2
- MLflow 2.9.0+
- Optuna 3.5.0+

## 🔗 MLflow Workflow

```
Train Models → MLflow Tracks Everything → View in UI → Compare Results → Select Best Model → Deploy
```

## 🚀 Quick Demo

Test the MLflow integration without full training:

```bash
python mlflow_tools/demo_mlflow.py
python mlflow_tools/launch_mlflow.py
# Open http://localhost:5000
```

## 📝 Notes

- Models are tracked and versioned automatically
- MLflow data stored in `mlruns/` directory
- All experiments can be compared in the UI
- Best models are registered in Model Registry
- Git LFS used for large model artifacts

## 🤝 Contributing

When training new models, they will automatically be tracked in MLflow. Use the analysis tools to compare performance.

## 📄 License

See [LICENSE](LICENSE) file for details.

---

**Last updated**: 2025-11-18 (MLflow integration added)
   - 23 engineered features including NPK ratios, evapotranspiration, soil saturation
