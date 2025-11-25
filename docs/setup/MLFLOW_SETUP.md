# 🚀 MLflow Setup Guide

## 📦 Quick Start

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Intelligent-Crop-Irrigation-Advisor.git
cd Intelligent-Crop-Irrigation-Advisor
```

### 2️⃣ Setup Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate environment
# On Linux/Mac:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3️⃣ Launch MLflow UI
```bash
# Easy way - use the launcher script
python mlflow_tools/launch_mlflow.py

# Or directly with mlflow command
mlflow ui --backend-store-uri ./mlruns --port 5000
```

### 4️⃣ Open in Browser
Navigate to: **http://127.0.0.1:5000**

---

## 🎯 What You'll See

### Available Experiments:
1. **Crop-Recommendation-Model**
   - Random Forest Classifier
   - 22 crop types prediction
   - ~99% accuracy

2. **Irrigation-Optimization-Model**
   - CatBoost Regressor
   - Water amount prediction
   - R² Score: 0.97+

3. **Smart-Irrigation-Classifier-Model**
   - CatBoost Classifier with Optuna
   - Binary irrigation status classification
   - Hyperparameter optimization tracking

---

## 📊 Train New Models

### Train All Models:
```bash
python mlflow_tools/train_all_models.py
```

### Train Individual Models:
```bash
# Crop Recommendation
python models/crop\ recommendation/model_training.py

# Irrigation Optimization
python models/irrigation_optimization_model/train.py

# Smart Irrigation Classifier
python models/Smart_Irrigation_Classifier/train_model.py
```

---

## 🔧 Troubleshooting

### Issue: MLflow command not found
**Solution:**
```bash
pip install mlflow>=2.9.0
```

### Issue: No experiments showing
**Solution:**
1. Check if `mlruns/` directory exists
2. Run training scripts to create experiments
3. Restart MLflow UI

### Issue: Virtual environment not activated
**Solution:**
```bash
# Activate first
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Then run MLflow
python mlflow_tools/launch_mlflow.py
```

---

## 📁 MLflow Directory Structure

```
mlruns/
├── 0/                          # Default experiment
├── 152495235150166473/         # Crop Recommendation
├── 934665864281209605/         # Irrigation Optimization
├── 327291042310154438/         # Smart Irrigation Classifier
└── models/                     # Model Registry
    ├── CropRecommendationModel/
    ├── IrrigationOptimizationModel/
    └── SmartIrrigationClassifier/
```

---

## 🎓 MLflow Features Used

### 1. Experiment Tracking
- Log parameters, metrics, and artifacts
- Compare multiple runs
- Visualize training progress

### 2. Model Registry
- Version control for models
- Stage management (Staging/Production)
- Model lineage tracking

### 3. Hyperparameter Tuning (Optuna Integration)
- Automated optimization
- Nested runs for each trial
- Best parameters selection

---

## 📝 Configuration Files

- `mlflow_tools/mlflow_config.py` - Central configuration
- `mlflow_tools/launch_mlflow.py` - UI launcher
- `mlflow_tools/train_all_models.py` - Training orchestrator
- `mlflow_tools/MLFLOW_GUIDE.md` - Detailed documentation

---

## 🌐 Production Deployment

### Option 1: SQLite Backend (Recommended)
```bash
mlflow server \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root ./mlruns \
    --host 0.0.0.0 \
    --port 5000
```

### Option 2: PostgreSQL Backend (Production)
```bash
mlflow server \
    --backend-store-uri postgresql://user:password@localhost/mlflow \
    --default-artifact-root s3://my-mlflow-bucket \
    --host 0.0.0.0 \
    --port 5000
```

---

## 📞 Support

For issues or questions:
1. Check `mlflow_tools/MLFLOW_GUIDE.md`
2. Visit: https://mlflow.org/docs/latest/
3. Open an issue on GitHub

---

## ⚡ Quick Commands Cheat Sheet

```bash
# Launch MLflow UI
python mlflow_tools/launch_mlflow.py

# Train all models
python mlflow_tools/train_all_models.py

# View experiments programmatically
python mlflow_tools/mlflow_analysis.py

# Run quick demo
python mlflow_tools/demo_mlflow.py

# Clean up old runs (optional)
mlflow gc --backend-store-uri ./mlruns
```

---

**Happy Tracking! 🎉**
