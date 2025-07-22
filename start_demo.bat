@echo off
echo ===========================================
echo   Quick Demo Setup Guide
echo ===========================================
echo.

echo STEP 1: Install Docker Desktop
echo.
echo Please download and install Docker Desktop:
echo https://www.docker.com/products/docker-desktop/
echo.
echo After installation:
echo 1. Restart your computer
echo 2. Start Docker Desktop
echo 3. Wait for it to fully start (Docker icon in system tray)
echo 4. Come back and run this script again
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker is not installed or not in PATH.
    echo Please install Docker Desktop first.
    echo.
    echo Opening Docker Desktop download page...
    start https://www.docker.com/products/docker-desktop/
    echo.
    pause
    exit /b 1
)

echo ===========================================
echo   Docker is installed! Starting demo...
echo ===========================================
echo.

echo Checking Docker Desktop is running...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker Desktop is not running.
    echo Please start Docker Desktop and wait for it to fully load.
    echo You'll see the Docker whale icon in your system tray when ready.
    echo.
    pause
    exit /b 1
)

echo ✅ Docker is running!
echo.

echo ===========================================
echo   Building and Starting Demo System
echo ===========================================
echo.

echo Building services (this may take 5-10 minutes first time)...
docker-compose build

if %errorlevel% neq 0 (
    echo ❌ Build failed! Check error messages above.
    pause
    exit /b 1
)

echo.
echo Starting all services...
docker-compose up -d

if %errorlevel% neq 0 (
    echo ❌ Startup failed! Check error messages above.
    pause
    exit /b 1
)

echo.
echo ✅ Demo system is starting up!
echo.
echo Please wait 30-60 seconds for all services to initialize...
timeout /t 45 /nobreak

echo.
echo ===========================================
echo   Testing System Health
echo ===========================================
echo.

echo Checking service status...
docker-compose ps

echo.
echo ===========================================
echo   🎉 DEMO IS READY!
echo ===========================================
echo.
echo Access your demo at:
echo.
echo 📊 Dashboard (Main Demo): http://localhost:8501
echo 🔧 API Documentation:    http://localhost:8000/docs
echo 📋 System Health:        http://localhost:8000/health
echo.
echo Press any key to open the dashboard in your browser...
pause

start http://localhost:8501

echo.
echo ===========================================
echo   Demo Tips for Practice
echo ===========================================
echo.
echo 1. Dashboard: Shows real-time tire defect detection
echo 2. API Docs: Interactive documentation for integration
echo 3. Health Check: System status and performance metrics
echo.
echo To stop the demo: docker-compose down
echo To restart: docker-compose up -d
echo To view logs: docker-compose logs
echo.
echo Happy practicing! 🚀
echo.
pause
