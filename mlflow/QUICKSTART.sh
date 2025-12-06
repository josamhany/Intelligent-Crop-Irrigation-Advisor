#!/bin/bash

# Quick Start Script for MLflow Tools
# This script provides instructions for getting started with MLflow

echo "═══════════════════════════════════════════════════════════"
echo "  MLflow Tools - Quick Start Guide"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "⚠️  Before running MLflow tools, you need to install dependencies:"
echo ""
echo "Option 1: Virtual Environment (Recommended)"
echo "  1. python -m venv venv"
echo "  2. source venv/bin/activate"
echo "  3. pip install -r requirements.txt"
echo ""
echo "Option 2: System Package Manager (Arch Linux)"
echo "  sudo pacman -S python-mlflow python-optuna"
echo ""
echo "Option 3: Using pipx"
echo "  pipx install mlflow"
echo "  pipx install optuna"
echo ""
echo "─────────────────────────────────────────────────────────"
echo ""
echo "After installation, you can:"
echo ""
echo "1. Test MLflow:"
echo "   python mlflow_tools/demo_mlflow.py"
echo ""
echo "2. Launch MLflow UI:"
echo "   python mlflow_tools/launch_mlflow.py"
echo ""
echo "3. Train all models:"
echo "   python mlflow_tools/train_all_models.py"
echo ""
echo "4. Analyze results:"
echo "   python mlflow_tools/mlflow_analysis.py --action all"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""
read -p "Press Enter to check if MLflow is installed..."
echo ""

# Check if mlflow is installed
if python -c "import mlflow" 2>/dev/null; then
    echo "✅ MLflow is installed!"
    python -c "import mlflow; print('   Version:', mlflow.__version__)"
    echo ""
    echo "You're ready to go! Try:"
    echo "   python mlflow_tools/demo_mlflow.py"
else
    echo "❌ MLflow is not installed"
    echo ""
    echo "Please install it first using one of the methods above."
fi

echo ""
