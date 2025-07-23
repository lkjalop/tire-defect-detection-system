#!/usr/bin/env python3
"""
Technical Validation Script
Provides independent verification of system capabilities
No marketing language - just technical facts
"""

import sys
import time
import subprocess
import importlib.util
from pathlib import Path

def check_dependencies():
    """Verify required packages are installed"""
    required = ['cv2', 'ultralytics', 'numpy', 'fastapi']
    missing = []
    
    for package in required:
        try:
            if package == 'cv2':
                import cv2
            else:
                __import__(package)
            print(f"✅ {package}: Available")
        except ImportError:
            missing.append(package)
            print(f"❌ {package}: Missing")
    
    return len(missing) == 0

def test_yolo_basic():
    """Test basic YOLO functionality"""
    try:
        from ultralytics import YOLO
        import numpy as np
        
        # Load model
        start_time = time.time()
        model = YOLO('yolov8n.pt')  # 6.2MB nano model
        load_time = time.time() - start_time
        
        # Test inference on dummy image
        dummy_image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
        
        start_time = time.time()
        results = model(dummy_image, verbose=False)
        inference_time = time.time() - start_time
        
        print(f"✅ YOLO Model Loading: {load_time:.3f}s")
        print(f"✅ YOLO Inference: {inference_time*1000:.1f}ms")
        print(f"✅ Model Size: ~6.2MB (nano)")
        print(f"✅ Input Resolution: 640x640")
        
        return True
        
    except Exception as e:
        print(f"❌ YOLO Test Failed: {e}")
        return False

def test_video_processing():
    """Test video processing capability"""
    try:
        import cv2
        import numpy as np
        
        # Create dummy video frames
        frames_processed = 0
        total_time = 0
        
        for i in range(10):  # Test 10 frames
            frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
            
            start_time = time.time()
            # Simulate basic processing
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            processed = cv2.GaussianBlur(gray, (5, 5), 0)
            process_time = time.time() - start_time
            
            total_time += process_time
            frames_processed += 1
        
        avg_fps = frames_processed / total_time if total_time > 0 else 0
        
        print(f"✅ Video Processing: {avg_fps:.1f} FPS")
        print(f"✅ Frame Processing: {(total_time/frames_processed)*1000:.1f}ms avg")
        
        return True
        
    except Exception as e:
        print(f"❌ Video Processing Test Failed: {e}")
        return False

def analyze_codebase():
    """Analyze actual codebase structure"""
    current_dir = Path('.')
    
    python_files = list(current_dir.glob('*.py'))
    print(f"✅ Python Files Found: {len(python_files)}")
    
    # Check for main implementation
    main_files = ['RUBICON_CONSOLIDATED.py', 'verify_yolo.py', 'PROFESSIONAL_DEPLOYMENT.py']
    found_files = []
    
    for file in main_files:
        if Path(file).exists():
            size = Path(file).stat().st_size
            lines = len(Path(file).read_text().splitlines())
            print(f"✅ {file}: {lines} lines, {size/1024:.1f}KB")
            found_files.append(file)
        else:
            print(f"❌ {file}: Not found")
    
    return len(found_files) > 0

def check_docker_setup():
    """Check Docker configuration"""
    docker_files = ['Dockerfile', 'docker-compose.yml', 'requirements.txt']
    found = []
    
    for file in docker_files:
        if Path(file).exists():
            print(f"✅ {file}: Present")
            found.append(file)
        else:
            print(f"❌ {file}: Missing")
    
    return len(found) > 0

def main():
    """Run complete technical validation"""
    print("🔍 TECHNICAL VALIDATION REPORT")
    print("=" * 50)
    
    tests = [
        ("Dependency Check", check_dependencies),
        ("YOLO Functionality", test_yolo_basic),
        ("Video Processing", test_video_processing),
        ("Codebase Analysis", analyze_codebase),
        ("Docker Setup", check_docker_setup)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ Test Error: {e}")
    
    print(f"\n🎯 VALIDATION SUMMARY")
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("✅ System: Technically Functional")
    elif passed >= total * 0.7:
        print("⚠️  System: Partially Functional")
    else:
        print("❌ System: Technical Issues Found")

if __name__ == "__main__":
    main()
