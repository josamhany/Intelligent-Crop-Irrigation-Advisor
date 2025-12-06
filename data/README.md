# AgriTech Data Directory

This directory contains all datasets used in the AgriTech Smart Advisor project.

## 📁 Available Datasets

### 1. Crop Recommendation Data
- **File**: `crop_data.csv`, `crop_data_with_soiltype.csv`
- **Purpose**: Training crop recommendation model
- **Features**: N, P, K, temperature, humidity, pH, rainfall, soil_type
- **Samples**: 2,200 records
- **Classes**: 22 different crops

### 2. Irrigation Optimization Data
- **Files**: `Final_irregation_optimization_data.csv`, `Final_irregation_optimization_data_m2.csv`
- **Purpose**: Training irrigation decision and optimization models
- **Features**: Environmental conditions, soil nutrients, moisture levels

### 3. Soil Type Classification Images
- **Directory**: `soil_images/train/`
- **Purpose**: Training soil type classifier (CNN model)
- **Classes**: 
  - Peat Soil (36 images)
  - Sandy Soil (10 images)
  - Silt Soil (8 images)
- **Total**: 54 images
- **Details**: See `soil_images/README.md`

### 4. TRAP Data
- **File**: `TARP.csv`
- **Source**: https://www.kaggle.com/datasets/nelakurthisudheer/dataset-for-predicting-watering-the-plants

## 🔧 Data Verification

To verify the soil images dataset:
```bash
python data/soil_images/verify_dataset.py
```

## 📝 Notes

- All datasets are preprocessed and ready for model training
- Soil images were recovered from Git history and reorganized
- Data augmentation is recommended for the soil images dataset due to limited size
