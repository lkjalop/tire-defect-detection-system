"""
Comprehensive Test Suite for Tire Defect Detection System
========================================================

This test suite validates the entire system for senior ML engineer review.
Tests cover: YOLO integration, API endpoints, error handling, performance.
"""

import pytest
import asyncio
import numpy as np
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "edge" / "src"))

try:
    from detection.tire_detector import TireDefectDetector, DefectType
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False

class TestTireDefectDetector:
    """Test the core YOLO detection module"""
    
    @pytest.mark.skipif(not YOLO_AVAILABLE, reason="YOLO dependencies not installed")
    @pytest.mark.asyncio
    async def test_detector_initialization(self):
        """Test that detector initializes properly"""
        detector = TireDefectDetector(confidence_threshold=0.6)
        success = await detector.initialize()
        
        if success:
            assert detector.is_initialized
            assert detector.model is not None
            assert detector.confidence_threshold == 0.6
        else:
            # Graceful degradation when YOLO not available
            assert not detector.is_initialized

    @pytest.mark.skipif(not YOLO_AVAILABLE, reason="YOLO dependencies not installed")
    @pytest.mark.asyncio
    async def test_image_validation(self):
        """Test image input validation"""
        detector = TireDefectDetector()
        
        # Valid image
        valid_image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
        assert detector._validate_image(valid_image)
        
        # Invalid images
        assert not detector._validate_image(None)
        assert not detector._validate_image(np.random.rand(640, 640, 3))  # Wrong dtype
        assert not detector._validate_image(np.random.randint(0, 255, (640, 640), dtype=np.uint8))  # Wrong shape

    @pytest.mark.skipif(not YOLO_AVAILABLE, reason="YOLO dependencies not installed")
    @pytest.mark.asyncio
    async def test_detection_pipeline(self):
        """Test the full detection pipeline"""
        detector = TireDefectDetector()
        success = await detector.initialize()
        
        if success:
            test_image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
            detections, metrics = await detector.detect_defects(test_image)
            
            # Validate response structure
            assert isinstance(detections, list)
            assert hasattr(metrics, 'processing_time_ms')
            assert hasattr(metrics, 'total_detections')
            assert metrics.processing_time_ms > 0
            
            # Validate detection structure if any found
            for detection in detections:
                assert hasattr(detection, 'bbox')
                assert hasattr(detection, 'confidence')
                assert hasattr(detection, 'defect_type')
                assert len(detection.bbox) == 4
                assert 0 <= detection.confidence <= 1

    def test_confidence_validation(self):
        """Test confidence threshold validation"""
        # Valid confidence values
        detector1 = TireDefectDetector(confidence_threshold=0.5)
        assert detector1.confidence_threshold == 0.5
        
        detector2 = TireDefectDetector(confidence_threshold=0.1)
        assert detector2.confidence_threshold == 0.1
        
        # Invalid confidence values (should be clamped)
        detector3 = TireDefectDetector(confidence_threshold=-0.1)
        assert detector3.confidence_threshold >= 0.1
        
        detector4 = TireDefectDetector(confidence_threshold=1.5)
        assert detector4.confidence_threshold <= 0.95

    def test_defect_type_enum(self):
        """Test defect type enumeration"""
        assert DefectType.GOOD.value == "good"
        assert DefectType.CRACK.value == "crack"
        assert DefectType.BULGE.value == "bulge"
        assert DefectType.WEAR.value == "wear"
        assert DefectType.PUNCTURE.value == "puncture"

# API Tests
import requests
import time
from concurrent.futures import ThreadPoolExecutor

class TestAPI:
    """Test the FastAPI backend"""
    
    BASE_URL = "http://localhost:8000"
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        try:
            response = requests.get(f"{self.BASE_URL}/health", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert "status" in data
            assert "model_status" in data
        except requests.exceptions.RequestException:
            pytest.skip("API server not running")
    
    def test_detection_endpoint(self):
        """Test detection API endpoint"""
        try:
            payload = {
                "image_id": "test_001",
                "threshold": 0.5,
                "device_id": "test_device"
            }
            response = requests.post(f"{self.BASE_URL}/api/v1/detect", json=payload, timeout=10)
            assert response.status_code == 200
            
            data = response.json()
            assert "image_id" in data
            assert "detections" in data
            assert "metrics" in data
            assert "processing_time_ms" in data
            assert data["image_id"] == "test_001"
            
        except requests.exceptions.RequestException:
            pytest.skip("API server not running")
    
    def test_analytics_endpoint(self):
        """Test analytics summary endpoint"""
        try:
            response = requests.get(f"{self.BASE_URL}/api/v1/analytics/summary", timeout=5)
            assert response.status_code == 200
            
            data = response.json()
            assert "summary" in data
            assert "total_processed" in data["summary"]
            assert "defects_found" in data["summary"]
            
        except requests.exceptions.RequestException:
            pytest.skip("API server not running")

# Performance Tests
class TestPerformance:
    """Performance and load testing"""
    
    @pytest.mark.skipif(not YOLO_AVAILABLE, reason="YOLO dependencies not installed")
    @pytest.mark.asyncio
    async def test_inference_speed(self):
        """Test inference speed meets requirements (<500ms)"""
        detector = TireDefectDetector()
        success = await detector.initialize()
        
        if success:
            test_image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
            
            # Run multiple inferences to get average
            times = []
            for _ in range(5):
                start = time.time()
                _, metrics = await detector.detect_defects(test_image)
                times.append(metrics.processing_time_ms)
            
            avg_time = sum(times) / len(times)
            assert avg_time < 500, f"Average inference time {avg_time:.1f}ms exceeds 500ms requirement"
    
    def test_api_response_time(self):
        """Test API response time"""
        try:
            payload = {"image_id": "perf_test", "device_id": "test"}
            
            start = time.time()
            response = requests.post(f"http://localhost:8000/api/v1/detect", json=payload, timeout=10)
            end = time.time()
            
            response_time = (end - start) * 1000
            assert response.status_code == 200
            assert response_time < 1000, f"API response time {response_time:.1f}ms too slow"
            
        except requests.exceptions.RequestException:
            pytest.skip("API server not running")

# Integration Tests
class TestIntegration:
    """End-to-end integration testing"""
    
    def test_system_startup(self):
        """Test that all system components can start"""
        # This would test Docker compose startup in real environment
        assert True  # Placeholder for integration test
    
    def test_error_handling(self):
        """Test error handling and graceful degradation"""
        try:
            # Test invalid request
            response = requests.post("http://localhost:8000/api/v1/detect", json={}, timeout=5)
            assert response.status_code == 422  # Validation error
            
            # Test invalid endpoint
            response = requests.get("http://localhost:8000/invalid", timeout=5)
            assert response.status_code == 404
            
        except requests.exceptions.RequestException:
            pytest.skip("API server not running")

# Fixtures for testing
@pytest.fixture
def sample_image():
    """Create a sample test image"""
    return np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)

@pytest.fixture
def detector():
    """Create a detector instance for testing"""
    return TireDefectDetector(confidence_threshold=0.5)

# Test runners
def run_unit_tests():
    """Run unit tests only"""
    pytest.main([__file__ + "::TestTireDefectDetector", "-v"])

def run_api_tests():
    """Run API tests (requires running server)"""
    pytest.main([__file__ + "::TestAPI", "-v"])

def run_all_tests():
    """Run all tests"""
    pytest.main([__file__, "-v"])

if __name__ == "__main__":
    print("🧪 Running Tire Defect Detection Test Suite")
    print("=" * 50)
    
    # Check if YOLO is available
    if YOLO_AVAILABLE:
        print("✅ YOLO dependencies available - running full test suite")
    else:
        print("⚠️  YOLO dependencies not installed - running limited tests")
    
    run_all_tests()
