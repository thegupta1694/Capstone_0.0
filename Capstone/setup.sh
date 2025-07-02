#!/bin/bash

echo "🚀 Setting up University Project Allocation System..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed. Please install Node.js 16+ and try again."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Backend Setup
echo "📦 Setting up Backend..."

cd backend

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp env.example .env
    echo "⚠️  Please edit backend/.env with your configuration"
fi

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

echo "✅ Backend setup complete!"
echo "💡 To start the backend server, run:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"

cd ..

# Frontend Setup
echo "📦 Setting up Frontend..."

cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

echo "✅ Frontend setup complete!"
echo "💡 To start the frontend server, run:"
echo "   cd frontend"
echo "   npm start"

cd ..

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env with your configuration"
echo "2. Create a superuser: cd backend && python manage.py createsuperuser"
echo "3. Start the backend: cd backend && python manage.py runserver"
echo "4. Start the frontend: cd frontend && npm start"
echo ""
echo "Backend will be available at: http://localhost:8000"
echo "Frontend will be available at: http://localhost:3000"
echo "Django Admin will be available at: http://localhost:8000/admin/" 