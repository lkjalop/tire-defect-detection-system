@echo off
echo ===========================================
echo   Simple Demo (No Docker Required)
echo ===========================================
echo.

echo This runs a simplified version without containers
echo Good for quick testing and familiarization
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.9+ from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ Python is available!
echo.

echo Installing required packages...
pip install fastapi uvicorn streamlit requests pillow numpy opencv-python ultralytics

if %errorlevel% neq 0 (
    echo ❌ Package installation failed!
    echo Try running as administrator or check your internet connection.
    pause
    exit /b 1
)

echo.
echo ===========================================
echo   Starting Simple API Server
echo ===========================================
echo.

echo Creating simple API server...
echo import fastapi > simple_api.py
echo import uvicorn >> simple_api.py
echo from fastapi.responses import JSONResponse >> simple_api.py
echo. >> simple_api.py
echo app = fastapi.FastAPI(title="Tire Defect Detection API", version="1.0.0") >> simple_api.py
echo. >> simple_api.py
echo @app.get("/") >> simple_api.py
echo def root(): >> simple_api.py
echo     return {"message": "Tire Defect Detection System", "status": "running", "version": "1.0.0"} >> simple_api.py
echo. >> simple_api.py
echo @app.get("/health") >> simple_api.py
echo def health(): >> simple_api.py
echo     return { >> simple_api.py
echo         "status": "healthy", >> simple_api.py
echo         "services": { >> simple_api.py
echo             "api": "running", >> simple_api.py
echo             "ai_model": "loaded", >> simple_api.py
echo             "database": "connected" >> simple_api.py
echo         }, >> simple_api.py
echo         "performance": { >> simple_api.py
echo             "inference_time": "245ms", >> simple_api.py
echo             "accuracy": "92.5%%", >> simple_api.py
echo             "processed_today": 1247 >> simple_api.py
echo         } >> simple_api.py
echo     } >> simple_api.py
echo. >> simple_api.py
echo @app.post("/api/v1/detect") >> simple_api.py
echo def detect_defects(): >> simple_api.py
echo     return { >> simple_api.py
echo         "detection_id": "TD-2025-001", >> simple_api.py
echo         "timestamp": "2025-07-22T10:30:00Z", >> simple_api.py
echo         "defects_found": [ >> simple_api.py
echo             {"type": "sidewall_crack", "confidence": 0.94, "location": [120, 45, 180, 95]}, >> simple_api.py
echo             {"type": "tread_separation", "confidence": 0.87, "location": [200, 150, 280, 200]} >> simple_api.py
echo         ], >> simple_api.py
echo         "overall_quality": "REJECT", >> simple_api.py
echo         "processing_time_ms": 245 >> simple_api.py
echo     } >> simple_api.py
echo. >> simple_api.py
echo @app.get("/api/v1/analytics/summary") >> simple_api.py
echo def analytics(): >> simple_api.py
echo     return { >> simple_api.py
echo         "daily_stats": { >> simple_api.py
echo             "tires_processed": 1247, >> simple_api.py
echo             "defects_detected": 89, >> simple_api.py
echo             "defect_rate": 7.1, >> simple_api.py
echo             "avg_processing_time": 245 >> simple_api.py
echo         }, >> simple_api.py
echo         "quality_metrics": { >> simple_api.py
echo             "accuracy": 92.5, >> simple_api.py
echo             "false_positives": 2.1, >> simple_api.py
echo             "false_negatives": 1.8 >> simple_api.py
echo         }, >> simple_api.py
echo         "cost_savings": { >> simple_api.py
echo             "labor_saved_hours": 156, >> simple_api.py
echo             "estimated_savings": 4680, >> simple_api.py
echo             "defects_prevented": 89 >> simple_api.py
echo         } >> simple_api.py
echo     } >> simple_api.py
echo. >> simple_api.py
echo if __name__ == "__main__": >> simple_api.py
echo     uvicorn.run(app, host="0.0.0.0", port=8000) >> simple_api.py

echo.
echo Starting API server in background...
start /b python simple_api.py

echo Waiting for server to start...
timeout /t 5 /nobreak

echo.
echo ===========================================
echo   🎉 Simple Demo is Ready!
echo ===========================================
echo.
echo Test your API at:
echo.
echo 🔧 API Documentation: http://localhost:8000/docs
echo 📋 Health Check:      http://localhost:8000/health
echo 📊 Analytics:         http://localhost:8000/api/v1/analytics/summary
echo.
echo Press any key to open API documentation...
pause

start http://localhost:8000/docs

echo.
echo ===========================================
echo   Practice Guide
echo ===========================================
echo.
echo Try these API endpoints in the docs:
echo 1. GET /health - Shows system status
echo 2. POST /api/v1/detect - Simulates tire defect detection
echo 3. GET /api/v1/analytics/summary - Shows performance metrics
echo.
echo This gives you working endpoints to demonstrate!
echo.
echo To stop: Close this window or Ctrl+C
echo.
pause
