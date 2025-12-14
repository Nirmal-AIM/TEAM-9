#!/bin/bash
# Quick Start Script for ML Pipeline

echo "🚀 Credit Score ML Pipeline - Quick Start"
echo "=========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate  # For Linux/Mac
# venv\Scripts\activate  # For Windows

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Train model
echo "🎯 Training model..."
python train_pipeline.py

# Start API server
echo "🚀 Starting API server..."
echo "API will be available at http://localhost:8000"
python api_server.py

