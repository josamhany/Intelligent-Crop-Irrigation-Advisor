# Models Directory

This directory contains all trained machine learning models for the Intelligent Crop Irrigation Advisor system.

## Directory Structure

### 📁 crop_recommendation/
Crop recommendation model that predicts the best crop based on soil nutrients, weather conditions, and soil type.

**Files:**
- `crop_model.pkl` - Main RandomForest model (8 features with soil_type)
- `crop_model_old.pkl` - Backup of previous model (7 features)
- `crop_model_with_soiltype.pkl` - Alternative model file
- `soil_type_encoder.pkl` - LabelEncoder for soil types (clay, petmos, sandy)
- `model_training.ipynb` - Training notebook with MLflow integration
- `README.md` - Detailed documentation

**Model Performance:**
- Accuracy: 99.32%
- Features: N, P, K, temperature, humidity, pH, rainfall, soil_type_encoded
- Crops: 22 different crops

---

### 📁 irrigation_optimization/
Irrigation optimization models including CatBoost classifiers and optimization algorithms.

**Files:**
- `catboost_irrigation_model.pkl` - Main irrigation optimization model
- `catboost_classifier.pkl` - Irrigation status classifier
- `catboost_root.pkl` - Additional CatBoost model
- `train.py` - Training script
- `train_classifier.py` - Classifier training script
- `model_accuracy.txt` - Model performance metrics
- `model_report.csv` - Detailed evaluation report
- `confusion_matrix.png` - Visualization of model performance
- `feature_importance.png` - Feature importance analysis
- `training.log` - Training logs

**Notebooks:**
- `train_notebook.ipynb` - Main training notebook
- `Irregation_optimization_notebook.ipynb` - Optimization experiments
- `Training_classification_wit_cmoparison.ipynb` - Model comparison

**Purpose:**
- Predict optimal irrigation amounts
- Classify irrigation status (Sufficient, Insufficient, Excessive)
- Optimize water usage based on soil moisture, weather, and crop needs

---

### 📁 soil_classification/
Soil type classification model using deep learning.

**Files:**
- `my_soil_model.h5` - Keras/TensorFlow model
- `class_labels.txt` - Soil type class labels
- `README.md` - Model documentation

**Supported Soil Types:**
- Clay
- Sandy
- Loamy
- Black
- Red

---

## Model Loading

All models are loaded in the Streamlit app (`frontend/streamlit_dashboard/app.py`) with proper error handling and status tracking.

### Usage Example:

```python
import joblib

# Load crop recommendation model
crop_model = joblib.load('models/crop_recommendation/crop_model.pkl')

# Load irrigation model
irrigation_model = joblib.load('models/irrigation_optimization/catboost_irrigation_model.pkl')

# Load soil type encoder
soil_encoder = joblib.load('models/crop_recommendation/soil_type_encoder.pkl')
```

## Model Training

Training notebooks are available in each subdirectory with MLflow integration for experiment tracking.

To train models:
1. Navigate to the specific model directory
2. Open the Jupyter notebook
3. Run all cells to train and save the model
4. Models are automatically logged to MLflow

## MLflow Integration

All models are tracked using MLflow. See `mlflow/` directory for experiment tracking and model registry.

Run MLflow UI:
```bash
cd mlflow
./QUICKSTART.sh
```

## Notes

- All models use Python 3.13.7 virtual environment
- Models are versioned and tracked in MLflow
- Backup models are kept with `_old` or `_root` suffixes
- Feature importance and performance metrics are logged for all models
