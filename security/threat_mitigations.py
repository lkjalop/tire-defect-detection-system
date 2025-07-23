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

# Try to import OpenCV with fallback
try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError as e:
    CV2_AVAILABLE = False
    print(f"⚠️ OpenCV/NumPy import issue: {e}")
    print("  Image validation will use basic checks only")
    # Create dummy numpy for type hints
    class DummyNumPy:
        uint8 = None
    np = DummyNumPy()

# Configure logging for security events
security_logger = logging.getLogger("security")
security_logger.setLevel(logging.INFO)

# Rate limiting implementation (OWASP API 3.4)
class RateLimiter:
    def __init__(self, max_requests: int = 100, window: int = 60):
        self.max_requests = max_requests
        self.window = window
        self.requests = {}
    
    def is_allowed(self, client_ip: str) -> bool:
        """Check if request is within rate limits"""
        current_time = time.time()
        
        # Clean old entries
        self.requests = {
            ip: timestamps 
            for ip, timestamps in self.requests.items()
            if timestamps and current_time - timestamps[-1] < self.window
        }
        
        # Check rate limit for this IP
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        
        # Remove timestamps outside window
        self.requests[client_ip] = [
            ts for ts in self.requests[client_ip]
            if current_time - ts < self.window
        ]
        
        # Check if under limit
        if len(self.requests[client_ip]) >= self.max_requests:
            security_logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return False
        
        # Add current timestamp
        self.requests[client_ip].append(current_time)
        return True

# Input validation for AI models (AI Threat 2.2)
class ImageValidator:
    def __init__(self):
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.allowed_formats = ['.jpg', '.jpeg', '.png', '.bmp']
        self.max_dimensions = (4096, 4096)
    
    def validate_image(self, image_data: bytes, filename: str) -> bool:
        """Validate image for security threats"""
        try:
            # Check file size
            if len(image_data) > self.max_file_size:
                security_logger.warning(f"Image too large: {len(image_data)} bytes")
                return False
            
            # Check file extension
            file_ext = '.' + filename.split('.')[-1].lower()
            if file_ext not in self.allowed_formats:
                security_logger.warning(f"Invalid file format: {file_ext}")
                return False
            
            # Basic validation without OpenCV if not available
            if not CV2_AVAILABLE:
                security_logger.info("OpenCV not available - using basic validation")
                # Basic checks: file has data, reasonable size
                return len(image_data) > 100  # At least 100 bytes
            
            # Full validation with OpenCV
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                security_logger.warning("Invalid image data - could not decode")
                return False
            
            # Check dimensions
            height, width = img.shape[:2]
            if width > self.max_dimensions[0] or height > self.max_dimensions[1]:
                security_logger.warning(f"Image dimensions too large: {width}x{height}")
                return False
            
            return True
            
        except Exception as e:
            security_logger.error(f"Image validation error: {e}")
            return False

# Authentication implementation (OWASP API 3.2)
class SecurityManager:
    def __init__(self, secret_key: str = "your-secret-key-change-in-production"):
        self.secret_key = secret_key
        self.algorithm = "HS256"
        self.token_expiry = 3600  # 1 hour
    
    def create_token(self, user_data: Dict) -> str:
        """Create JWT token"""
        payload = {
            "user": user_data,
            "exp": time.time() + self.token_expiry,
            "iat": time.time()
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload.get("exp", 0) < time.time():
                return None
            return payload.get("user")
        except jwt.InvalidTokenError:
            return None

# Output validation (AI Threat 2.3)
class ModelOutputValidator:
    def __init__(self):
        self.confidence_threshold = 0.1
        self.max_detections = 50
        self.valid_defect_types = [
            "minor_wear", "uneven_wear", "surface_crack", "deep_crack",
            "sidewall_bubble", "puncture", "foreign_object", "tread_separation"
        ]
    
    def validate_detection_result(self, result: Dict) -> bool:
        """Validate AI model output for security"""
        try:
            # Check result structure
            required_fields = ["detections", "quality_score", "safety_status"]
            if not all(field in result for field in required_fields):
                security_logger.warning("Invalid result structure")
                return False
            
            # Validate detections
            detections = result.get("detections", [])
            if len(detections) > self.max_detections:
                security_logger.warning(f"Too many detections: {len(detections)}")
                return False
            
            for detection in detections:
                # Check confidence bounds
                confidence = detection.get("confidence", 0)
                if not (0 <= confidence <= 1):
                    security_logger.warning(f"Invalid confidence: {confidence}")
                    return False
                
                # Check defect type
                defect_type = detection.get("defect_type", "")
                if defect_type not in self.valid_defect_types:
                    security_logger.warning(f"Invalid defect type: {defect_type}")
                    return False
            
            # Validate quality score
            quality_score = result.get("quality_score", 0)
            if not (0 <= quality_score <= 100):
                security_logger.warning(f"Invalid quality score: {quality_score}")
                return False
            
            return True
            
        except Exception as e:
            security_logger.error(f"Output validation error: {e}")
            return False

# Audit logging (Compliance requirement)
class AuditLogger:
    def __init__(self):
        self.logger = logging.getLogger("audit")
        self.logger.setLevel(logging.INFO)
    
    def log_api_access(self, request: Request, user: str, endpoint: str):
        """Log API access for audit trail"""
        self.logger.info({
            "event": "api_access",
            "user": user,
            "endpoint": endpoint,
            "ip": request.client.host,
            "user_agent": request.headers.get("user-agent"),
            "timestamp": time.time()
        })
    
    def log_security_event(self, event_type: str, details: Dict):
        """Log security events"""
        self.logger.warning({
            "event": "security_event",
            "type": event_type,
            "details": details,
            "timestamp": time.time()
        })

# Initialize security components
rate_limiter = RateLimiter()
image_validator = ImageValidator()
model_output_validator = ModelOutputValidator()
security_manager = SecurityManager()
audit_logger = AuditLogger()

# Security middleware functions
async def verify_rate_limit(request: Request):
    """Rate limiting middleware"""
    client_ip = request.client.host
    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please try again later."
        )

async def verify_authentication(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    """Authentication middleware"""
    user = security_manager.verify_token(credentials.credentials)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    return user

# Security decorators
def require_auth(func):
    """Decorator to require authentication"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Authentication handled by FastAPI Depends
        return await func(*args, **kwargs)
    return wrapper

def audit_access(endpoint: str):
    """Decorator to audit API access"""
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            user = kwargs.get('current_user', {}).get('username', 'unknown')
            audit_logger.log_api_access(request, user, endpoint)
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator
