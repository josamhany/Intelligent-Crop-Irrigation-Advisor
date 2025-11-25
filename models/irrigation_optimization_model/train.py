# ===============================
# 📦 IMPORT LIBRARIES
# ===============================
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from catboost import CatBoostRegressor
import joblib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import mlflow
import mlflow.catboost
from mlflow.models.signature import infer_signature
import sys
import os

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../mlflow_tools'))
from mlflow_config import setup_mlflow, log_dataset_info

# ===============================
# 📂 LOAD DATA
# ===============================
import os
# Get the absolute path to the data file
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
data_path = os.path.join(project_root, 'data', 'Final_irregation_optimization_data_m2.csv')
print(f"Loading data from: {data_path}")
merged_df = pd.read_csv(data_path)

# ===============================
# 🎯 DEFINE FEATURES AND TARGET
# ===============================
features = [
    'soil_moisture', 'temperature', 'soil_humidity', 'air_temperature_(c)',
    'wind_speed_(km/h)', 'humidity', 'wind_gust_(km/h)', 'pressure_(kpa)',
    'ph', 'rainfall', 'n', 'p', 'k', 'soil_moisture_diff',
    'Relative_Soil_Saturation', 'temp_diff', 'wind_effect',
    'Evapotranspiration', 'rain_3days', 'rain_vs_soil',
    'np_ratio', 'nk_ratio', 'ph_encoded', 'crop_encoded',
    'moisture_temp_ratio', 'evapo_ratio', 'rain_effect',
    'moisture_change_rate', 'temp_scaled', 'npk_balance', 'wind_ratio'
]

target = 'recommended_water_mm'

X = merged_df[merged_df['status'] == True][features]
y = merged_df[merged_df['status'] == True][target]

# ===============================
# 📊 TRAINING DATA VISUALIZATION
# ===============================

# 1. Feature Distribution Example
plt.figure(figsize=(7,5))
plt.hist(merged_df['soil_moisture'], bins=30, color='skyblue', edgecolor='black')
plt.title('Soil Moisture Distribution')
plt.xlabel('Soil Moisture')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# 2. Feature Correlation Heatmap
corr = merged_df[features].corr()
plt.figure(figsize=(12,10))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Feature Correlation Heatmap')
plt.tight_layout()
plt.show()

# ===============================
# 🧠 SPLIT DATA
# ===============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Setup MLflow
setup_mlflow('irrigation_optimization')

# Start MLflow run
with mlflow.start_run(run_name="CatBoost_Irrigation_Optimization"):
    
    # Log parameters
    mlflow.log_param("model_type", "CatBoostRegressor")
    mlflow.log_param("iterations", 1000)
    mlflow.log_param("learning_rate", 0.05)
    mlflow.log_param("depth", 8)
    mlflow.log_param("loss_function", "RMSE")
    mlflow.log_param("eval_metric", "R2")
    mlflow.log_param("test_size", 0.2)
    mlflow.log_param("random_seed", 42)
    mlflow.log_param("num_features", len(features))
    
    # Log dataset info
    log_dataset_info(merged_df, "irrigation_dataset")
    mlflow.log_param("train_samples", X_train.shape[0])
    mlflow.log_param("test_samples", X_test.shape[0])
    mlflow.log_param("features", features)
    
    # ===============================
    # 🚀 TRAIN MODEL
    # ===============================
    model = CatBoostRegressor(
        iterations=1000,
        learning_rate=0.05,
        depth=8,
        loss_function='RMSE',
        eval_metric='R2',
        random_seed=42,
        verbose=200
    )
    
    model.fit(X_train, y_train, eval_set=(X_test, y_test), use_best_model=True)
    
    # ===============================
    # 💾 SAVE MODEL
    # ===============================
    joblib.dump(model, 'catboost_irrigation_model.pkl')
    print("✅ Model saved successfully as 'catboost_irrigation_model.pkl'")
    
    # ===============================
    # 📊 EVALUATION
    # ===============================
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    n = len(y_test)
    p = len(features)
    adj_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)
    
    print(f"\n📊 MAE: {mae:.3f}")
    print(f"📉 RMSE: {rmse:.3f}")
    print(f"🎯 R² Score: {r2:.3f}")
    print(f"🔧 Adjusted R²: {adj_r2:.3f}")
    
    # Log metrics to MLflow
    mlflow.log_metric("mae", mae)
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2_score", r2)
    mlflow.log_metric("adjusted_r2", adj_r2)
    
    # Log feature importance
    feature_importance = pd.DataFrame({
        'feature': X_train.columns,
        'importance': model.get_feature_importance()
    }).sort_values('importance', ascending=False)
    
    # Log feature importance with sanitized names (MLflow doesn't accept parentheses)
    for idx, row in feature_importance.iterrows():
        # Replace invalid characters: () becomes _
        sanitized_name = row['feature'].replace('(', '_').replace(')', '_').replace(' ', '_')
        mlflow.log_metric(f"importance_{sanitized_name}", row['importance'])

    # ===============================
    # 📊 DATA VISUALIZATION
    # ===============================
    
    # Predict on test set (already done above, use existing y_pred)
    
    # 1. Actual vs Predicted Scatter Plot
    plt.figure(figsize=(7,5))
    plt.scatter(y_test, y_pred, alpha=0.6, color='royalblue')
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Actual Water (mm)')
    plt.ylabel('Predicted Water (mm)')
    plt.title('Actual vs Predicted Irrigation Amount')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("actual_vs_predicted.png")
    mlflow.log_artifact("actual_vs_predicted.png")
    plt.show()
    
    # 2. Feature Importance Bar Plot
    importances = model.get_feature_importance()
    indices = np.argsort(importances)[::-1]
    plt.figure(figsize=(9,6))
    plt.barh(np.array(features)[indices], np.array(importances)[indices], color='seagreen')
    plt.xlabel('Importance')
    plt.title('Feature Importance (CatBoost)')
    plt.tight_layout()
    plt.savefig("feature_importance.png")
    mlflow.log_artifact("feature_importance.png")
    plt.show()
    
    # Log model with signature
    signature = infer_signature(X_train, model.predict(X_train))
    mlflow.catboost.log_model(
        model,
        "irrigation_optimization_model",
        signature=signature,
        registered_model_name="IrrigationOptimizationModel"
    )
    
    # Log local model artifact
    mlflow.log_artifact("catboost_irrigation_model.pkl")
    
    print("\n✅ Training completed successfully!")
    print(f"🔗 MLflow Run ID: {mlflow.active_run().info.run_id}")
    print("📊 View results: mlflow ui")
