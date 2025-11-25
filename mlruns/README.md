# MLflow Runs Directory

This directory contains MLflow experiment tracking data.

## �� Contents
- Experiment metadata
- Model artifacts
- Training metrics and parameters
- Run histories

## 🚫 Why Not in Git?
This folder is excluded from version control because:
- Large size (80+ MB)
- Contains binary model files
- Generated during training
- User-specific experiment data

## ✅ How to Use
1. Train models locally:
   ```bash
   python mlflow_tools/train_all_models.py
   ```

2. View experiments:
   ```bash
   mlflow ui
   ```
   Then open http://localhost:5000

## 📝 Note
Each user will have their own `mlruns/` folder created during model training.
