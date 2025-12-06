# Soil Type Classification Dataset

## 📊 Dataset Overview

This dataset contains images of different soil types used to train the soil classification model.

## 📁 Directory Structure

```
data/soil_images/
└── train/
    ├── Peat Soil/      (36 images)
    ├── Sandy Soil/     (20 images)
    └── Silt Soil/      (20 images)
```

## 🏷️ Soil Types

### 1. Peat Soil
- **Count**: 36 images
- **Characteristics**: Dark, organic-rich soil with high water retention
- **Label**: Class 0

### 2. Sandy Soil
- **Count**: 20 images
- **Characteristics**: Coarse texture, good drainage, low water retention
- **Label**: Class 1

### 3. Silt Soil
- **Count**: 20 images
- **Characteristics**: Smooth texture, moderate drainage and water retention
- **Label**: Class 2

## 🔧 Usage

### Training the Model

```python
from pathlib import Path
from tensorflow.keras.preprocessing.image import ImageDataGenerator

TRAIN_DATA_DIR = Path("data/soil_images/train")
IMG_SIZE = (224, 224)
BATCH_SIZE = 8

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    TRAIN_DATA_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)
```

## 📝 Notes

- Images are in JPG/JPEG format
- All images are resized to 224x224 pixels during training
- Data augmentation is applied to handle the limited dataset size
- The dataset is split 80/20 for training/validation

## 🔄 Data Source

This dataset was recovered from Git history (commit: 5feeea7) and reorganized into the `data/` directory for better project structure.

## ⚠️ Important

The soil classification model (`models/soil_classification/my_soil_model.h5`) was trained on this dataset with the following class mapping:
- 0: Peat Soil
- 1: Sandy Soil
- 2: Silt Soil

Make sure to maintain this order when retraining or using the model.
