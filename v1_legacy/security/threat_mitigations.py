"""
Security implementations based on threat model
Addresses OWASP API Top 10 and AI-specific threats
"""
from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from functools import wraps
import time
import logging
import hashlib
import jwt
from typing import Optional, Dict, List
import cv2
import numpy as np

# Configure logging for security events
security_logger = logging.getLogger("security")
security_logger.setLevel(logging.INFO)

# Rate limiting implementation (OWASP API 3.4)
class RateLimiter:
    def __init__(self, max_requests: int = 100, window: int = 3600):
        self.max_requests = max_requests
        self.window = window
        self.requests: Dict[str, List[float]] = {}
    
    def is_allowed(self, client_ip: str) -> bool:
        now = time.time()
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        
        # Clean old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip] 
            if now - req_time < self.window
        ]
        
        if len(self.requests[client_ip]) >= self.max_requests:
            security_logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return False
        
        self.requests[client_ip].append(now)
        return True

# Input validation for AI models (AI Threat 2.2)
class ImageValidator:
    @staticmethod
    def validate_image_input(image_data: bytes) -> bool:
        """Validate image input to prevent malicious payloads"""
        try:
            # Size validation
            max_size = 10 * 1024 * 1024  # 10MB
            if len(image_data) > max_size:
                security_logger.warning("Image size exceeds limit")
                raise HTTPException(status_code=413, detail="Image too large")
            
            # Format validation
            np_arr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            
            if img is None:
                security_logger.warning("Invalid image format detected")
                raise HTTPException(status_code=400, detail="Invalid image format")
            
            # Dimension validation
            height, width = img.shape[:2]
            if height > 4000 or width > 4000:
                security_logger.warning("Image dimensions too large")
                raise HTTPException(status_code=400, detail="Image dimensions too large")
            
            return True
            
        except Exception as e:
            security_logger.error(f"Image validation failed: {str(e)}")
            raise HTTPException(status_code=400, detail="Image validation failed")

# Authentication implementation (OWASP API 3.2)
class SecurityManager:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.security = HTTPBearer()
    
    def verify_token(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        """Verify JWT token for API access"""
        try:
            payload = jwt.decode(credentials.credentials, self.secret_key, algorithms=["HS256"])
            username = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return username
        except jwt.ExpiredSignatureError:
            security_logger.warning("Expired token used")
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.JWTError:
            security_logger.warning("Invalid token used")
            raise HTTPException(status_code=401, detail="Invalid token")

# Output validation (AI Threat 2.3)
class ModelOutputValidator:
    @staticmethod
    def validate_detection_output(predictions: List[Dict], confidence_threshold: float = 0.5) -> List[Dict]:
        """Validate AI model output to prevent hallucination issues"""
        validated_predictions = []
        
        for pred in predictions:
            # Confidence validation
            if pred.get('confidence', 0) < confidence_threshold:
                security_logger.info(f"Low confidence prediction filtered: {pred.get('confidence')}")
                continue
            
            # Reasonable bounds validation
            bbox = pred.get('bbox', {})
            if not (0 <= bbox.get('x1', -1) <= bbox.get('x2', -1) <= 1 and 
                   0 <= bbox.get('y1', -1) <= bbox.get('y2', -1) <= 1):
                security_logger.warning("Invalid bounding box detected")
                continue
            
            validated_predictions.append(pred)
        
        return validated_predictions

# Audit logging (Compliance requirement)
class AuditLogger:
    @staticmethod
    def log_api_access(username: str, endpoint: str, ip_address: str, success: bool):
        """Log API access for audit trails"""
        security_logger.info({
            "event": "api_access",
            "username": username,
            "endpoint": endpoint,
            "ip_address": ip_address,
            "success": success,
            "timestamp": time.time()
        })
    
    @staticmethod
    def log_detection_event(username: str, image_hash: str, detections_count: int, ip_address: str):
        """Log tire detection events"""
        security_logger.info({
            "event": "tire_detection",
            "username": username,
            "image_hash": image_hash,
            "detections_count": detections_count,
            "ip_address": ip_address,
            "timestamp": time.time()
        })

# Initialize security components
rate_limiter = RateLimiter()
image_validator = ImageValidator()
model_output_validator = ModelOutputValidator()
audit_logger = AuditLogger()
