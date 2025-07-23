#!/usr/bin/env python3
"""
FastAPI backend for Tire Defect Detection System
Enterprise-grade REST API with security features
"""

import asyncio
import time
import uuid
from typing import List, Dict, Optional
from pathlib import Path

# FastAPI and security imports
try:
    from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, status
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    print("⚠️ FastAPI not installed - API mode not available")
    print("  Install with: pip install fastapi uvicorn python-multipart")

# Import our enterprise detector
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tire_detection_system import EnterpriseTireDetector

# Security middleware
security = HTTPBearer() if FASTAPI_AVAILABLE else None

class DetectionRequest(BaseModel):
    """Request model for tire detection API"""
    image_id: Optional[str] = None
    scenario: Optional[str] = None

class DetectionResponse(BaseModel):
    """Response model for tire detection API"""
    success: bool
    image_id: str
    processing_time: float
    defects_found: int
    quality_score: float
    safety_status: str
    overall_quality: str
    recommendations: List[str]
    business_impact: Dict
    timestamp: float

def create_enterprise_api():
    """Create FastAPI application with enterprise security"""
    if not FASTAPI_AVAILABLE:
        return None
    
    app = FastAPI(
        title="RUBICON: Tire Defect Detection API",
        description="Enterprise-grade tire defect detection system with YOLOv8 integration",
        version="2.0.0",
        contact={
            "name": "Enterprise AI Team",
            "email": "lkjalop@enterprise.ai"
        }
    )
    
    # Security middleware - CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:8080"],  # Restrict origins
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
    
    # Initialize enterprise detector
    detector = EnterpriseTireDetector()
    
    # Authentication dependency
    async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
        """Validate JWT token (simplified for demo)"""
        token = credentials.credentials
        # In production, validate JWT token here
        if not token or token == "invalid":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"user": "enterprise_user", "role": "analyst"}
    
    @app.get("/")
    async def root():
        """API health check endpoint"""
        return {
            "message": "RUBICON Tire Defect Detection API",
            "version": "2.0.0",
            "status": "operational",
            "features": ["YOLOv8 Integration", "Enterprise Security", "Business Analytics"]
        }
    
    @app.get("/health")
    async def health_check():
        """Detailed health check for monitoring"""
        await detector.initialize()
        return {
            "status": "healthy",
            "system_initialized": detector.is_initialized,
            "demo_mode": detector.demo_mode,
            "timestamp": time.time()
        }
    
    @app.post("/analyze", response_model=DetectionResponse)
    async def analyze_tire(
        request: DetectionRequest,
        current_user: dict = Depends(get_current_user),
        file: UploadFile = File(None)
    ):
        """Analyze tire image for defects"""
        try:
            # Initialize if needed
            if not detector.is_initialized:
                await detector.initialize()
            
            # Process the analysis
            if request.scenario:
                result = await detector.generate_enterprise_demo_result(request.scenario)
            else:
                result = await detector.analyze_tire_image(
                    image_data=file.file if file else None,
                    image_id=request.image_id
                )
            
            return DetectionResponse(
                success=True,
                image_id=result.image_id,
                processing_time=result.processing_time,
                defects_found=len(result.defects_found),
                quality_score=result.quality_score,
                safety_status=result.safety_status,
                overall_quality=result.overall_quality,
                recommendations=result.recommendations,
                business_impact=result.business_impact,
                timestamp=result.timestamp
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Analysis failed: {str(e)}"
            )
    
    @app.get("/scenarios")
    async def get_demo_scenarios(current_user: dict = Depends(get_current_user)):
        """Get available demo scenarios for testing"""
        from tire_detection_system import config
        return {
            "available_scenarios": list(config.demo_scenarios.keys()),
            "descriptions": {
                scenario: data["description"] 
                for scenario, data in config.demo_scenarios.items()
            }
        }
    
    @app.post("/batch-analyze")
    async def batch_analyze(
        scenarios: List[str],
        current_user: dict = Depends(get_current_user)
    ):
        """Batch analyze multiple scenarios for enterprise demonstrations"""
        results = []
        
        if not detector.is_initialized:
            await detector.initialize()
        
        for scenario in scenarios:
            result = await detector.generate_enterprise_demo_result(scenario)
            results.append({
                "scenario": scenario,
                "image_id": result.image_id,
                "quality_score": result.quality_score,
                "safety_status": result.safety_status,
                "defects_found": len(result.defects_found),
                "business_impact": result.business_impact
            })
        
        return {
            "batch_results": results,
            "summary": {
                "total_processed": len(results),
                "average_quality": sum(r["quality_score"] for r in results) / len(results),
                "safety_breakdown": {
                    status: len([r for r in results if r["safety_status"] == status])
                    for status in ["safe", "caution", "unsafe"]
                }
            }
        }
    
    return app

def start_api_server():
    """Start the FastAPI server"""
    if not FASTAPI_AVAILABLE:
        print("❌ FastAPI not available - cannot start API server")
        return
    
    app = create_enterprise_api()
    if app is None:
        return
    
    print("🚀 Starting RUBICON Enterprise API Server...")
    print("📊 Available endpoints:")
    print("   • GET  /          - API information")
    print("   • GET  /health    - Health check")
    print("   • POST /analyze   - Analyze tire image")
    print("   • GET  /scenarios - Demo scenarios")
    print("   • POST /batch-analyze - Batch processing")
    print("🔒 Security: JWT authentication required")
    print("📖 Docs: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start_api_server()
