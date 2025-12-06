#!/usr/bin/env python3
"""
Soil Type Classification Model Training Script
Trains a CNN model on soil images from uploads/train directory
Saves model to soil_model_savedmodel/my_soil_model.h5
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from pathlib import Path

# Set seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

# Configuration
IMG_SIZE = (224, 224)
BATCH_SIZE = 8  # Small batch size due to limited data
EPOCHS = 20  # Reduced for faster training
LEARNING_RATE = 0.0001

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent  # Go up to project root
TRAIN_DATA_DIR = PROJECT_ROOT / "data/soil_images/train"
MODEL_SAVE_DIR = PROJECT_ROOT / "models/soil_classification"
MODEL_SAVE_PATH = MODEL_SAVE_DIR / "my_soil_model.h5"

print("="*60)
print("🌱 Soil Type Classification Model Training")
print("="*60)
print(f"\n📁 Training data: {TRAIN_DATA_DIR}")
print(f"💾 Model will be saved to: {MODEL_SAVE_PATH}")
print(f"🖼️  Image size: {IMG_SIZE}")
print(f"📦 Batch size: {BATCH_SIZE}")
print(f"🔄 Epochs: {EPOCHS}")

# Create model save directory
MODEL_SAVE_DIR.mkdir(parents=True, exist_ok=True)

# Data augmentation for training (to handle small dataset)
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    vertical_flip=True,
    fill_mode='nearest',
    validation_split=0.2  # 20% for validation
)

# Load training data
print("\n📊 Loading training data...")
train_generator = train_datagen.flow_from_directory(
    TRAIN_DATA_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True,
    seed=42
)

# Load validation data
validation_generator = train_datagen.flow_from_directory(
    TRAIN_DATA_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=False,
    seed=42
)

# Get class information
class_names = list(train_generator.class_indices.keys())
num_classes = len(class_names)

print(f"\n✅ Data loaded successfully!")
print(f"📋 Classes found: {class_names}")
print(f"🔢 Number of classes: {num_classes}")
print(f"📈 Training samples: {train_generator.samples}")
print(f"📉 Validation samples: {validation_generator.samples}")

# Build the CNN model (MobileNetV2-based transfer learning)
print("\n🏗️  Building model architecture...")

base_model = keras.applications.MobileNetV2(
    input_shape=(*IMG_SIZE, 3),
    include_top=False,
    weights='imagenet'
)

# Freeze base model layers initially
base_model.trainable = False

# Build the complete model
model = keras.Sequential([
    # Preprocessing
    layers.Input(shape=(*IMG_SIZE, 3)),
    
    # Base model (MobileNetV2)
    base_model,
    
    # Custom top layers
    layers.GlobalAveragePooling2D(),
    layers.BatchNormalization(),
    layers.Dropout(0.5),
    layers.Dense(256, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.3),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(num_classes, activation='softmax', name='predictions')
])

# Compile model
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
    loss='categorical_crossentropy',
    metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
)

print("\n📐 Model architecture:")
model.summary()

# Callbacks
callbacks = [
    keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True,
        verbose=1
    ),
    keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=5,
        min_lr=1e-7,
        verbose=1
    ),
    keras.callbacks.ModelCheckpoint(
        filepath=str(MODEL_SAVE_PATH),
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    )
]

# Train the model
print("\n🚀 Starting training...")
print("="*60)

history = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=EPOCHS,
    callbacks=callbacks,
    verbose=1
)

# Fine-tuning phase: Unfreeze some layers
print("\n🔧 Fine-tuning: Unfreezing top layers of base model...")
base_model.trainable = True

# Freeze all layers except the last 20
for layer in base_model.layers[:-20]:
    layer.trainable = False

# Recompile with lower learning rate
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE/10),
    loss='categorical_crossentropy',
    metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
)

# Continue training
print("\n🚀 Continuing training with fine-tuning...")
history_fine = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=10,  # Reduced for faster training
    callbacks=callbacks,
    verbose=1
)

# Save final model
print(f"\n💾 Saving final model to: {MODEL_SAVE_PATH}")
model.save(MODEL_SAVE_PATH)

# Evaluate on validation set
print("\n📊 Final Evaluation on Validation Set:")
val_loss, val_accuracy, val_precision, val_recall = model.evaluate(validation_generator)
print(f"  Loss: {val_loss:.4f}")
print(f"  Accuracy: {val_accuracy*100:.2f}%")
print(f"  Precision: {val_precision*100:.2f}%")
print(f"  Recall: {val_recall*100:.2f}%")
print(f"  F1-Score: {2*(val_precision*val_recall)/(val_precision+val_recall)*100:.2f}%")

# Save class labels
labels_file = MODEL_SAVE_DIR / "class_labels.txt"
with open(labels_file, 'w') as f:
    for i, label in enumerate(class_names):
        f.write(f"{i}: {label}\n")

print(f"\n✅ Training completed successfully!")
print(f"📝 Class labels saved to: {labels_file}")
print(f"📦 Model ready at: {MODEL_SAVE_PATH}")
print(f"📋 Classes (in order): {class_names}")
print("\n" + "="*60)
print("🎉 Done! You can now use this model in Streamlit.")
print("="*60)
