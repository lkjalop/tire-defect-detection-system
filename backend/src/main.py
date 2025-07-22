#!/usr/bin/env python3
"""
Laptop Backend API
=================
"""

from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title="Tire Defect Detection API - Laptop Edition",
    description="Laptop-optimized API for tire defect detection",
    version="1.0.0-laptop"
)

@app.get("/")
async def root():
    return {
        "message": "Tire Defect Detection API - Laptop Edition",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "device": "laptop",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/v1/analytics/summary")
async def analytics():
    return {
        "summary": {
            "total_processed": 42,
            "defects_found": 3,
            "defect_rate": 7.1,
            "avg_inference_time_ms": 245.0,
            "active_devices": 1
        },
        "message": "Laptop demo data"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
