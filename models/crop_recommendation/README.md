# 🌾 Smart Crop Recommendation System

## Overview
The Smart Crop Recommendation System is a machine learning-powered application that helps farmers make informed decisions about which crops to plant based on soil and environmental conditions.

## 🎯 Features
- **22 Crop Types Supported**: Rice, Maize, Chickpea, Kidney Beans, Pigeon Peas, Moth Beans, Mung Bean, Black Gram, Lentil, Pomegranate, Banana, Mango, Grapes, Watermelon, Muskmelon, Apple, Orange, Papaya, Coconut, Cotton, Jute, and Coffee
- **High Accuracy**: 99.3% model accuracy
- **Real-time Predictions**: Instant crop recommendations
- **User-friendly Interface**: Interactive Streamlit web application
- **Confidence Scoring**: Shows prediction confidence level
- **Crop Information**: Detailed information about each recommended crop

## 📊 Dataset Information

### Dataset Source
- **Name**: Crop Recommendation Dataset
- **Source**: Kaggle - Atharva Ingle
- **URL**: https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset
- **Samples**: 2,200 records across 22 crop types
- **Features**: 7 environmental and soil parameters
- **Format**: CSV file with clean, balanced data

## 📊 Input Parameters
The model requires 7 environmental and soil parameters:

| Parameter | Description | Range | Unit |
|-----------|-------------|-------|------|
| **Nitrogen (N)** | Nitrogen content in soil | 0-200 | - |
| **Phosphorus (P)** | Phosphorus content in soil | 0-200 | - |
| **Potassium (K)** | Potassium content in soil | 0-200 | - |
| **Temperature** | Average temperature | 0-50 | °C |
| **Humidity** | Relative humidity | 0-100 | % |
| **pH** | Soil pH level | 0-14 | - |
| **Rainfall** | Annual rainfall | 0-300 | mm |

## 🏗️ Project Structure
```
Crop Recommendation/
├── app.py                  # Main Streamlit application
├── model_training.py       # Model training script
├── crop_data.csv          # Training dataset
├── crop_model.pkl         # Trained model file
├── launch_app.py          # Application launcher
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── docs/                 # Documentation folder
│   ├── MODEL_DOCS.md     # Model documentation
│   └── USER_GUIDE.md     # User guide
└── .venv/                # Virtual environment
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+ recommended (works on Linux/macOS/Windows)

### Installation
1. Clone or download the project
2. Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Running the Application

#### Method 1: Launcher Script (if present)
```bash
# from repo root
python frontend/streamlit_dashboard/launch_app.py
```

#### Method 2: Direct Streamlit
```bash
python -m streamlit run frontend/streamlit_dashboard/app.py --server.port=8503
```

#### Method 3: VS Code Tasks
Use the predefined VS Code tasks:
- **🌾 Run Crop Recommendation App**
- **🚀 Launch App with Browser**

### Stopping the Application
- Press `Ctrl+C` in terminal
- Or use VS Code task termination

## 🧠 Model Information
- **Algorithm**: Random Forest Classifier
- **Training Data**: 2,200 samples across 22 crop types
- **Features**: 7 environmental/soil parameters
- **Accuracy**: 99.32%
- **Cross-validation**: 80/20 train-test split

## 📱 Web Interface
The application provides:
- **Input Form**: Easy-to-use parameter inputs
- **Real-time Prediction**: Instant crop recommendations
- **Confidence Score**: Prediction reliability indicator
- **Crop Information**: Detailed crop characteristics
- **Input Summary**: Review of entered parameters

## 🌐 Access URLs
Once running, the application is available at:
- **Local**: http://localhost:8501 (or auto-assigned port)
- **Network**: Available to other devices on your network

## 🔧 Technical Requirements
- **Python**: 3.11.9
- **Key Dependencies**:
  - streamlit==1.50.0
  - pandas==2.3.3
  - scikit-learn==1.7.2
  - numpy==2.3.3
  - joblib==1.5.2

## 📈 Performance Metrics
- **Accuracy**: 99.32%
- **Response Time**: < 1 second
- **Memory Usage**: ~50MB
- **Startup Time**: ~3-5 seconds

## 🐛 Troubleshooting

### Common Issues
1. **Port Already in Use**
   - Solution: Use `launch_app.py` (auto-finds free port)
   - Or restart the application

2. **Module Not Found**
   - Solution: Ensure virtual environment is activated
   - Check `requirements.txt` installation

3. **Model File Missing**
   - Solution: Run `python model_training.py`

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License
This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author
Created for DEPI Capstone Project (Digital Egypt Pioneers Initiative) Smart Farming Assistant

## 📞 Support
For issues and questions:
- Check the documentation in `docs/` folder
- Review troubleshooting section
- Create an issue in the repository

---
**Last Updated**: 2025-11-14
**Version**: 1.0.1