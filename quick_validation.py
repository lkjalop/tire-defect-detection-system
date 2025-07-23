#!/usr/bin/env python3
"""
QUICK SYSTEM VALIDATION
Fast check for critical issues
"""

def quick_validation():
    print("🚀 QUICK EXPERT VALIDATION")
    print("=" * 40)
    
    issues = []
    
    # Test 1: Core import
    try:
        import honest_edge_ai
        print("✅ Core system imports")
    except Exception as e:
        issues.append(f"Core import failed: {e}")
        print(f"❌ Core import: {e}")
    
    # Test 2: Configuration
    try:
        config = honest_edge_ai.config
        if config.yolo_accuracy_coco50 == 0.528:  # Official YOLOv8n spec
            print("✅ Evidence-based metrics")
        else:
            issues.append("Non-evidence based metrics")
    except Exception as e:
        issues.append(f"Config error: {e}")
    
    # Test 3: Security
    try:
        from security.threat_mitigations import rate_limiter
        print("✅ Security framework")
    except Exception as e:
        issues.append(f"Security import: {e}")
        print(f"❌ Security: {e}")
    
    # Test 4: FastAPI
    try:
        app = honest_edge_ai.app
        if "demonstration" in app.description.lower():
            print("✅ Honest API documentation")
        else:
            issues.append("API not clearly marked as demo")
    except Exception as e:
        issues.append(f"FastAPI error: {e}")
    
    print(f"\n🎯 RESULT: {len(issues)} issues found")
    if issues:
        for issue in issues:
            print(f"   • {issue}")
        return False
    else:
        print("✅ System ready for expert review")
        return True

if __name__ == "__main__":
    success = quick_validation()
    exit(0 if success else 1)
