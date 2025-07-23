# 🚀 DEPLOYMENT GUIDE

## Quick Start for New Users

### 1. Clone and Test (2 minutes)
```bash
git clone https://github.com/lkjalop/tire-defect-detection-system.git
cd tire-defect-detection-system

# Test immediately (works without any dependencies)
python honest_edge_ai.py --mode demo
```

### 2. Full Installation (5 minutes)
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run with API server
python honest_edge_ai.py --mode api

# Visit documentation
# http://localhost:8000/docs
```

## 📋 System Requirements

### Minimum Requirements
- **Python 3.8+** (tested on 3.11)
- **4GB RAM** (8GB recommended)
- **Windows/Linux/MacOS**

### Dependencies
- **Core**: FastAPI, Pydantic, NumPy (always required)
- **Optional**: OpenCV, ultralytics (graceful fallback if missing)
- **Security**: PyJWT, passlib (for enterprise features)

## 🔧 Troubleshooting

### Common Issues

#### "YOLO import timed out"
- **Expected behavior** - system falls back to educational simulation
- **No action needed** - demonstrates fault tolerance

#### "ModuleNotFoundError: No module named 'cv2'"
```bash
pip install opencv-python
```

#### "ultralytics not found"
```bash
pip install ultralytics
# Note: System works fine without this
```

#### Port already in use
```bash
python honest_edge_ai.py --mode api --port 8001
```

## 🎯 What Works Out of Box

### ✅ Always Works
- **Demo mode**: `python honest_edge_ai.py --mode demo`
- **Educational scenarios**: Shows AI architecture patterns
- **Professional error handling**: Never crashes during demos
- **Security framework**: Complete OWASP implementation

### ✅ Works with Basic Install
- **API server**: FastAPI with OpenAPI docs
- **Image processing**: With OpenCV installation
- **Authentication**: JWT-ready enterprise patterns

### ✅ Works with Full Install
- **Real YOLO integration**: When ultralytics available
- **Production deployment**: Container-ready architecture

## 🏗️ Architecture Overview

```
honest_edge_ai.py          # Main system (START HERE)
├── Demo Mode              # Works instantly, no dependencies
├── API Mode               # FastAPI server with docs
├── Security Framework     # OWASP-compliant patterns
└── YOLO Integration       # Optional, graceful fallback

security/
└── threat_mitigations.py  # Enterprise security implementation

requirements.txt           # All dependencies listed
README.md                   # Project overview
```

## 🎓 For Technical Interviews

### Demo Script (5 minutes)
```bash
# 1. Show it works immediately
python honest_edge_ai.py --mode demo

# 2. Start API server
python honest_edge_ai.py --mode api

# 3. Show documentation (browser)
# http://localhost:8000/docs

# 4. Explain architecture
# - Fault-tolerant design
# - Security-first approach
# - Production-ready patterns
```

### Key Discussion Points
- **Honest engineering**: Transparent about capabilities vs limitations
- **Fault tolerance**: Graceful degradation when dependencies missing
- **Security awareness**: OWASP compliance, input validation
- **Professional patterns**: Modern FastAPI, async processing

## 🚀 Production Deployment

### Container Deployment
```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "honest_edge_ai.py", "--mode", "api", "--port", "8000"]
```

### Environment Variables
```bash
export YOLO_MODEL_PATH="/models/yolov8n.pt"
export JWT_SECRET_KEY="your-production-secret"
export LOG_LEVEL="INFO"
```

## 🔍 Validation Checklist

Before presenting this system:

- [ ] `python honest_edge_ai.py --mode demo` runs successfully
- [ ] API starts with `python honest_edge_ai.py --mode api`
- [ ] Documentation accessible at `http://localhost:8000/docs`
- [ ] Security module imports correctly
- [ ] All educational scenarios work
- [ ] System handles missing dependencies gracefully

---

**This system is designed to work reliably in any environment, making it perfect for demonstrations, interviews, and client presentations.**
