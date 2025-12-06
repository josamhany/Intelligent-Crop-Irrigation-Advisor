# ===============================
# 📦 IMPORT REQUIRED LIBRARIES
# ===============================
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score, f1_score
from catboost import CatBoostClassifier
import optuna
import joblib
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
# 📂 LOAD YOUR DATA
# ===============================
# Make sure your dataset (merged_df) is loaded before training
# Example:
# merged_df = pd.read_csv("your_dataset.csv")

# ===============================
# 🧩 DEFINE IMPORTANT FEATURES
# ===============================
important_features = [ 
    'soil_moisture', 'temperature', 'soil_humidity', 'Relative_Soil_Saturation',
    'temp_diff', 'Evapotranspiration', 'rain_vs_soil', 'rainfall', 'ph_encoded',
    'n', 'p', 'k', 'np_ratio', 'nk_ratio', 'crop_encoded', 'rain_3days',
    'moisture_temp_ratio', 'evapo_ratio', 'rain_effect', 'moisture_change_rate',
    'temp_scaled', 'npk_balance', 'wind_ratio'
]
# Load dataset from correct path
try:
    # Try different possible paths
    data_paths = [
        "../../data/Final_irregation_optimization_data.csv",  # From Smart_Irrigation_Classifier folder
        "../data/Final_irregation_optimization_data.csv",  # From models folder
        "data/Final_irregation_optimization_data.csv",  # From root
        "Final_irregation_optimization_data.csv"  # Same folder
    ]
    
    merged_df = None
    for path in data_paths:
        try:
            merged_df = pd.read_csv(path)
            print(f"✅ Data loaded successfully from: {path}")
            print(f"📊 Shape: {merged_df.shape}")
            print(f"📋 Columns: {list(merged_df.columns)}")
            break
        except FileNotFoundError:
            print(f"❌ File not found at: {path}")
            continue
    
    if merged_df is None:
        raise FileNotFoundError("Data file not found in any expected location!")
        
except Exception as e:
    print(f"❌ Error loading data: {e}")
    exit(1)
# ===============================
# 🧠 SPLIT DATA INTO X AND y
# ===============================
X = merged_df[important_features]
y = merged_df['status']

# Fill missing values with column means
X = X.fillna(X.mean())

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ===============================
# 🐱 INITIAL CATBOOST MODEL
# ===============================
print("🔹 Training initial CatBoost model...")

cat = CatBoostClassifier(
    iterations=1500,
    learning_rate=0.02,
    depth=10,
    l2_leaf_reg=5,
    random_strength=1.5,
    bagging_temperature=0.8,
    border_count=128,
    verbose=False,
    random_seed=42
)

cat.fit(X_train, y_train)
y_pred_cat = cat.predict(X_test)

print(f"Initial Accuracy: {accuracy_score(y_test, y_pred_cat):.4f}")
print("\nInitial Classification Report:")
print(classification_report(y_test, y_pred_cat))

# ===============================
# 🎯 OPTUNA HYPERPARAMETER TUNING WITH MLFLOW
# ===============================
print("\n🔹 Starting Optuna optimization...")

# Setup MLflow
setup_mlflow('smart_irrigation_classifier')

def objective(trial):
    with mlflow.start_run(run_name=f"Optuna_Trial_{trial.number}", nested=True):
        params = {
            'iterations': trial.suggest_int('iterations', 300, 1000),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.1, log=True),
            'depth': trial.suggest_int('depth', 4, 10),
            'l2_leaf_reg': trial.suggest_float('l2_leaf_reg', 1, 10),
            'random_strength': trial.suggest_float('random_strength', 0.5, 2.0),
            'bagging_temperature': trial.suggest_float('bagging_temperature', 0.5, 1.0),
            'border_count': trial.suggest_int('border_count', 32, 128),
            'verbose': False,
            'random_seed': 42
        }
        
        # Log parameters
        for key, value in params.items():
            mlflow.log_param(key, value)

        model = CatBoostClassifier(**params)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        
        # Log metrics
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("trial_number", trial.number)
        
        return acc

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=10)

print("\n🏆 Best Parameters:", study.best_params)
print(f"🎯 Best Accuracy: {study.best_value:.4f}")

# ===============================
# 🚀 TRAIN FINAL MODEL WITH BEST PARAMS
# ===============================
best_params = study.best_params
best_params['verbose'] = False
best_params['random_seed'] = 42

# Start final MLflow run
with mlflow.start_run(run_name="Final_Best_Model"):
    
    print("\n🔹 Training final CatBoost model with best parameters...")
    
    # Log dataset info
    log_dataset_info(merged_df, "irrigation_classifier_dataset")
    mlflow.log_param("train_samples", X_train.shape[0])
    mlflow.log_param("test_samples", X_test.shape[0])
    mlflow.log_param("num_features", len(important_features))
    mlflow.log_param("features", important_features)
    
    # Log best parameters
    for key, value in best_params.items():
        mlflow.log_param(f"best_{key}", value)
    
    best_cat = CatBoostClassifier(**best_params)
    best_cat.fit(X_train, y_train)
    
    # ===============================
    # 📊 EVALUATE FINAL MODEL
    # ===============================
    y_pred = best_cat.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    report = classification_report(y_test, y_pred, output_dict=True)
    
    print(f"\n✅ Final Accuracy: {acc:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print("\nFinal Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Log metrics
    mlflow.log_metric("accuracy", acc)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1_score", f1)
    
    # ===============================
    # 🌟 FEATURE IMPORTANCE
    # ===============================
    feature_importance = pd.DataFrame({
        'Feature': X_train.columns,
        'Importance': best_cat.feature_importances_
    }).sort_values(by='Importance', ascending=False)
    print("\nTop 10 Important Features:")
    print(feature_importance.head(10))
    
    # Log feature importance
    for idx, row in feature_importance.iterrows():
        mlflow.log_metric(f"importance_{row['Feature']}", row['Importance'])
    
    # ===============================
    # 💾 SAVE RESULTS AND MODEL
    # ===============================
    report_df = pd.DataFrame(report).transpose()
    report_df.to_csv("model_report.csv", index=True)
    mlflow.log_artifact("model_report.csv")
    
    with open("model_accuracy.txt", "w") as f:
        f.write(f"Final Accuracy: {acc:.4f}\n")
        f.write(f"Precision: {precision:.4f}\n")
        f.write(f"Recall: {recall:.4f}\n")
        f.write(f"F1 Score: {f1:.4f}\n")
    mlflow.log_artifact("model_accuracy.txt")
    
    # Save trained model
    joblib.dump(best_cat, "catboost_model.pkl")
    mlflow.log_artifact("catboost_model.pkl")
    
    # Log model with signature
    signature = infer_signature(X_train, best_cat.predict(X_train))
    mlflow.catboost.log_model(
        best_cat,
        "smart_irrigation_classifier_model",
        signature=signature,
        registered_model_name="SmartIrrigationClassifierModel"
    )
    
    print("\n✅ Model and reports saved successfully!")
    print("📁 Files created: model_report.csv, model_accuracy.txt, catboost_model.pkl")
    print(f"🔗 MLflow Run ID: {mlflow.active_run().info.run_id}")
    print("📊 View results: mlflow ui")
