@echo off
REM Quick Start Script for ML Pipeline (Windows)

echo 🚀 Credit Score ML Pipeline - Quick Start
echo ==========================================

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Train model
echo 🎯 Training model...
python train_pipeline.py

REM Start API server
echo 🚀 Starting API server...
echo API will be available at http://localhost:8000
python api_server.py

pause

