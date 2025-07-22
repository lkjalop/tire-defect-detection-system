@echo off
REM Quick Demo Setup Script for Windows

echo 🎬 Setting up Tire Defect Detection Demo for David Linthicum...
echo =============================================================

REM Check Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is required but not installed
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop
    exit /b 1
)

docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running
    echo Please start Docker Desktop
    exit /b 1
)

echo ✅ Docker is ready

REM Build and start
echo 🔨 Building demo environment...
docker-compose build

echo 🚀 Starting all services...
docker-compose up -d

REM Wait for startup
echo ⏳ Waiting for services to start...
timeout /t 30 /nobreak >nul

REM Health checks
echo 🔍 Checking service health...

docker-compose ps | find "mqtt" | find "Up" >nul
if errorlevel 1 (
    echo ❌ MQTT broker failed to start
) else (
    echo ✅ MQTT broker is running
)

curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Backend API is not responding
) else (
    echo ✅ Backend API is responding
)

echo.
echo 🎉 Demo Setup Complete!
echo =======================
echo.
echo 📊 Dashboard: http://localhost:8501
echo 🔧 API Docs:  http://localhost:8000/docs
echo ❤️  Health:   http://localhost:8000/health
echo.
echo 🎯 Demo is ready for David Linthicum!
echo.
echo 📋 Quick Commands:
echo   View logs:    docker-compose logs -f
echo   Stop demo:    docker-compose down
echo   Restart:      docker-compose restart
echo.
echo 📖 See DEMO_GUIDE.md for full presentation script

pause
