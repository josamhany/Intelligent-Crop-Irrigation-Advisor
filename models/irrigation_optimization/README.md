## 🌾 Intelligent Crop Irrigation Advisor

### 📘 Overview

This project focuses on **data-driven irrigation and fertilizer optimization** using machine learning. It combines **environmental, soil, and weather data** to recommend the optimal water amount (in mm) and balanced NPK (Nitrogen, Phosphorus, Potassium) fertilizer values for different crops.

The model leverages **CatBoost Regression** to predict water requirements scientifically and efficiently, ensuring sustainable irrigation management.

---

### 🧩 Dataset Description

**File:** `Final_irregation_optimization_data_m2.csv`

Each row represents a daily record of soil, crop, and weather conditions with the corresponding irrigation recommendations.

| Feature                                           | Description                                          |
| ------------------------------------------------- | ---------------------------------------------------- |
| `soil_moisture`                                   | Current soil moisture percentage (%)                 |
| `temperature`                                     | Ambient temperature (°C)                             |
| `soil_humidity`                                   | Soil humidity level (%)                              |
| `air_temperature_(c)`                             | Air temperature in Celsius                           |
| `wind_speed_(km/h)`                               | Wind speed in kilometers per hour                    |
| `humidity`                                        | Relative humidity (%)                                |
| `wind_gust_(km/h)`                                | Maximum wind gust speed                              |
| `pressure_(kpa)`                                  | Atmospheric pressure (kPa)                           |
| `ph`                                              | Soil pH value                                        |
| `rainfall`                                        | Daily rainfall amount (mm)                           |
| `n`, `p`, `k`                                     | Soil nutrient concentrations                         |
| `Evapotranspiration`                              | Crop water loss due to evaporation and transpiration |
| `rain_3days`                                      | Accumulated rainfall over the last 3 days            |
| `np_ratio`, `nk_ratio`, `npk_balance`             | Calculated nutrient balance ratios                   |
| `crop`                                            | Crop type (e.g., rice, maize, banana, mango, etc.)   |
| `status`                                          | Boolean indicator (True = needs irrigation)          |
| `recommended_water_mm`                            | Predicted irrigation water amount in mm              |
| `recommended_N`, `recommended_P`, `recommended_K` | Recommended NPK fertilizer levels                    |
| `soil_moisture_updated`                           | Updated soil moisture after irrigation               |

Total Features: **40 columns**
Total Rows: Depends on collected data records.

---

### ⚙️ Workflow Summary

1. **Data Loading & Inspection**

   * Read dataset using pandas.
   * Display structure, missing values, and duplicates.

2. **Feature Importance Extraction**

   * Load a pre-trained `CatBoost` model (`catboost_model.pkl`).
   * Visualize feature importance to understand influential factors in irrigation needs.

3. **Water & Nutrient Simulation**

   * Iterates through each data row to:

     * Compute **ETc (Evapotranspiration × Kc)**.
     * Calculate **water deficit** adjusted by soil moisture and rainfall.
     * Recommend **NPK values** based on crop, pH, and irrigation level.
   * Updates soil moisture dynamically after each irrigation step.
   * Results stored in `irrigation_npk_scientific_safe.csv`.

4. **Model Training (CatBoost Regressor)**

   * Uses `status = True` records (when soil needs water).
   * Features selected carefully to avoid multicollinearity.
   * Trains CatBoost model with:

     * 1000 iterations
     * Learning rate = 0.05
     * Depth = 8
     * Evaluation metric = R²
   * Model performance metrics:

     * **MAE**
     * **RMSE**
     * **R² Score**
     * **Adjusted R²**

5. **Model Saving**

   * The final model is saved as `catboost_irrigation_model.pkl`.

---

### 📊 Example Output

| Crop  | Status | Recommended Water (mm) | N    | P    | K    |
| ----- | ------ | ---------------------- | ---- | ---- | ---- |
| Rice  | True   | 50.0                   | 4.67 | 0.09 | 3.82 |
| Maize | False  | 0.0                    | 0.00 | 0.00 | 0.00 |
| Mango | True   | 50.0                   | 8.80 | 0.09 | 4.69 |

---

### 📈 Model Evaluation

| Metric      | Description                  | Example Value |
| ----------- | ---------------------------- | ------------- |
| MAE         | Mean Absolute Error          | `0.123`       |
| RMSE        | Root Mean Squared Error      | `0.342`       |
| R²          | Coefficient of Determination | `0.95`        |
| Adjusted R² | Adjusted for feature count   | `0.948`       |

---

### 🧠 Algorithms & Logic

* **CatBoost Regressor:** Gradient boosting on decision trees optimized for non-linear relationships.
* **FAO Evapotranspiration (ETc) principle:** Ensures scientifically accurate water recommendation.
* **Dynamic Soil Moisture Update:** Tracks moisture changes after each irrigation cycle.
* **NPK Scaling:** Adjusts nutrients based on pH, ratios, and irrigation level.

---

### 🗂️ Outputs

| File                                 | Description                                                       |
| ------------------------------------ | ----------------------------------------------------------------- |
| `irrigation_npk_scientific_safe.csv` | Final dataset with computed water and fertilizer recommendations. |
| `catboost_irrigation_model.pkl`      | Trained regression model for irrigation prediction.               |
| `feature_importance.png`             | Visualization of the most impactful features.                     |

---

### 🧪 Dependencies

Install all dependencies before running the notebook:

```bash
!pip install catboost lightgbm joblib pandas scikit-learn seaborn matplotlib numpy
```

---

### 💡 Key Insights

* Evapotranspiration, rainfall, and soil moisture are **the top 3 predictive features** for irrigation needs.
* Soil pH and nutrient ratios have a significant effect on NPK adjustments.
* The model ensures **scientific safety limits** on both irrigation and fertilizer recommendations.
