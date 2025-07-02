@echo off
echo 🚀 Setting up University Project Allocation System...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed. Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is required but not installed. Please install Node.js 16+ and try again.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed

REM Backend Setup
echo 📦 Setting up Backend...

cd backend

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    copy env.example .env
    echo ⚠️  Please edit backend\.env with your configuration
)

REM Run migrations
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate

echo ✅ Backend setup complete!
echo 💡 To start the backend server, run:
echo    cd backend
echo    venv\Scripts\activate.bat
echo    python manage.py runserver

cd ..

REM Frontend Setup
echo 📦 Setting up Frontend...

cd frontend

REM Install dependencies
echo Installing Node.js dependencies...
npm install

echo ✅ Frontend setup complete!
echo 💡 To start the frontend server, run:
echo    cd frontend
echo    npm start

cd ..

echo.
echo 🎉 Setup complete!
echo.
echo Next steps:
echo 1. Edit backend\.env with your configuration
echo 2. Create a superuser: cd backend ^&^& python manage.py createsuperuser
echo 3. Start the backend: cd backend ^&^& python manage.py runserver
echo 4. Start the frontend: cd frontend ^&^& npm start
echo.
echo Backend will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:3000
echo Django Admin will be available at: http://localhost:8000/admin/

pause 