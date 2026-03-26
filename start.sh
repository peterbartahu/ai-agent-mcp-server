#!/bin/bash
# Quick Start Script for AI Study Helper Agent
# This script creates venv if needed, installs dependencies, starts MongoDB, and runs the server

echo "🚀 Starting AI Study Helper Agent..."
echo ""

# Check and create venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
    echo "   ✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""
echo "🐍 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies if needed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install --upgrade pip -q
    pip install fastapi uvicorn pymongo python-dotenv -q
    echo "   ✅ Dependencies installed"
fi

echo ""

# Check if MongoDB is running
echo "📦 Checking MongoDB..."
if ! docker ps | grep -q "ai_agent_mongodb"; then
    echo "   Starting MongoDB container..."
    docker-compose up -d
    sleep 3
    echo "   ✅ MongoDB started"
else
    echo "   ✅ MongoDB already running"
fi

echo ""
echo "🔧 Starting FastAPI server..."
echo "   Server will run on: http://localhost:8000"
echo "   Swagger UI:        http://localhost:8000/docs"
echo "   API Docs:          http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python -m uvicorn app.web:app --reload --host 0.0.0.0 --port 8000