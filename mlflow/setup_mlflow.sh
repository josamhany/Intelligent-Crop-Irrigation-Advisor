#!/bin/bash

# MLflow Setup Script for Intelligent Crop Irrigation Advisor
# This script sets up a virtual environment and installs all dependencies

# Change to project root
cd "$(dirname "$0")/.."

echo "🌾 Intelligent Crop Irrigation Advisor - MLflow Setup"
echo "======================================================"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "📦 Virtual environment already exists"
    read -p "Do you want to recreate it? (y/n): " recreate
    if [ "$recreate" = "y" ]; then
        echo "🗑️  Removing old virtual environment..."
        rm -rf venv
    else
        echo "✅ Using existing virtual environment"
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
    
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet

# Install requirements
echo "📥 Installing requirements..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install requirements"
    exit 1
fi

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "🚀 Next steps:"
echo "   1. Activate environment: source venv/bin/activate"
echo "   2. Train models: python train_all_models.py"
echo "   3. Launch MLflow UI: python launch_mlflow.py"
echo ""
