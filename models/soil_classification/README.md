# 🌱 Soil Type Classification System

A machine learning project that classifies different types of soil (e.g., **Alluvial**, **Black**, **Red**, **Sandy**, etc.) using classical machine learning models. This system uses **image processing** techniques (color histograms) for feature extraction and applies algorithms like **Support Vector Machines (SVM)** and **Random Forest** for classification.

---

## 🧠 Problem Statement

Farmers and agronomists often struggle with identifying soil types accurately without laboratory testing. This project aims to build an **automated soil classification system** that predicts the type of soil from an image using classical ML techniques.

---

## 🧪 Technologies Used

- Python 🐍
- OpenCV (Image Processing)
- NumPy & Pandas (Data handling)
- Scikit-learn (ML Models)
- Matplotlib / Seaborn (Visualization)
- `dill` (for saving models & objects)
- HTML/CSS (UI Designing)
- VS Code (IDE)

---

## ⚙️ How It Works

1. **Data Ingestion**  
   Reads raw image files from `data/raw/soil-types/` and labels them based on folder names.

2. **Data Transformation**  
   - Resizes images to `128x128`
   - Extracts color histogram features in HSV space
   - Encodes labels numerically
   - Saves processed `X.pkl` and `y.pkl`

3. **Model Training**  
   - Uses algorithms like `SVM`, `RandomForest`, etc.
   - Hyperparameter tuning via `GridSearchCV`
   - Saves the best performing model as `model.pkl`

4. **Evaluation**  
   - Evaluates on accuracy, confusion matrix, classification report
   - Achieved up to **41% accuracy** (can be improved using deep learning)

---

## ✅ Features

- Image-based soil classification
- Classical ML approach (fast, interpretable)
- Label encoding & preprocessing pipeline
- Modular code with exception handling & logging
- Easily extendable to add new models or deep learning

---

## 🚀 How to Run

```bash
# Clone the repo
git clone https://github.com/your-username/Soil-Type-Classification-System.git

# Navigate into the folder
cd Soil-Type-Classification-System

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate on Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run main app
python app.py
