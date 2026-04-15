#!/bin/bash
# SmartScreen SaaS - Startup Script

echo "========================================="
echo "  SmartScreen SaaS - Developer Startup"
echo "========================================="
echo ""

# Check Python
echo "✓ Checking Python installation..."
python --version || { echo "✗ Python not found"; exit 1; }

# Check Node
echo "✓ Checking Node.js installation..."
node --version || { echo "⚠ Node not found (needed for frontend)"; }

echo ""
echo "========================================="
echo "  Backend Setup"
echo "========================================="

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate

# Install dependencies
echo "Installing backend dependencies..."
pip install -r requirements.txt -q

# Create .env if it doesn't exist
if [ ! -f "backend/.env" ]; then
    echo "Creating .env file from template..."
    cp .env.example backend/.env
    echo "⚠ Edit backend/.env with your configuration"
fi

echo ""
echo "========================================="
echo "  Frontend Setup"
echo "========================================="

if [ -d "frontend" ]; then
    cd frontend
    
    if [ ! -d "node_modules" ]; then
        echo "Installing frontend dependencies..."
        npm install
    fi
    
    # Create .env for frontend
    if [ ! -f ".env" ]; then
        echo "Creating frontend .env..."
        cp .env.example .env
    fi
    
    cd ..
fi

echo ""
echo "========================================="
echo "  ✅ Setup Complete!"
echo "========================================="
echo ""
echo "To start development, run in separate terminals:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  export PYTHONPATH=."
echo "  uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm start"
echo ""
echo "Then open: http://localhost:3000"
echo "API Docs:  http://localhost:8000/docs"
echo ""
echo "For more info, see:"
echo "  - README_NEW.md"
echo "  - QUICK_REFERENCE.md"
echo "  - BACKEND_SETUP.md"
echo ""
