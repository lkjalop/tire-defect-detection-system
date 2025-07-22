"""
Tire Defect Detection Edge Module
================================

Production-grade tire defect detection system using YOLOv8 computer vision.

This module provides enterprise-ready computer vision capabilities for
automated tire quality control in manufacturing environments.
"""

__version__ = "1.0.0"
__author__ = "Kevin J - Go Cloud Careers Enterprise AI Program"

# Import main classes for easy access
try:
    from .detection.tire_detector import TireDefectDetector, DetectionResult, InferenceMetrics, DefectType
except ImportError:
    # Graceful degradation if dependencies not installed
    pass

__all__ = [
    "TireDefectDetector",
    "DetectionResult", 
    "InferenceMetrics",
    "DefectType"
]
