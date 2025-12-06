#!/usr/bin/env python3
"""
MLflow UI Launcher for Intelligent Crop Irrigation Advisor
==========================================================
This script launches the MLflow UI to view and compare experiment results.
"""

import os
import subprocess
from pathlib import Path

# Get project root (go up one level from mlflow_tools)
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
MLRUNS_PATH = PROJECT_ROOT / "mlruns"

def launch_mlflow_ui(host="127.0.0.1", port=5000):
    """
    Launch MLflow UI.
    
    Args:
        host: Host to bind to (default: 127.0.0.1)
        port: Port to bind to (default: 5000)
    """
    print("🚀 Launching MLflow UI...")
    print(f"📁 Tracking URI: {MLRUNS_PATH}")
    print(f"🔗 URL: http://{host}:{port}")
    print("\nPress Ctrl+C to stop the server\n")
    
    # Change to project root
    os.chdir(PROJECT_ROOT)
    
    # Launch MLflow UI
    try:
        subprocess.run([
            "mlflow", "ui",
            "--host", host,
            "--port", str(port),
            "--backend-store-uri", f"file://{MLRUNS_PATH}"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 MLflow UI stopped")
    except Exception as e:
        print(f"❌ Error launching MLflow UI: {e}")
        print("\nMake sure MLflow is installed:")
        print("  pip install mlflow")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Launch MLflow UI")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind to")
    
    args = parser.parse_args()
    launch_mlflow_ui(args.host, args.port)
