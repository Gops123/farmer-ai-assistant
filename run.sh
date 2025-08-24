#!/bin/bash

# Farmer AI Agriculture Assistant - Local Development Startup Script

echo "🌱 Starting Farmer AI Agriculture Assistant..."
echo "🚀 Starting server on port 8000..."
echo "📱 Open your browser and go to: http://localhost:8000"
echo "⏹️  Press Ctrl+C to stop the server"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Please create one with your API keys."
    echo "   Required variables: OPENAI_API_KEY, HUGGINGFACE_KEY"
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

# Set port for local development
export PORT=8000

# Run the application
python main.py
