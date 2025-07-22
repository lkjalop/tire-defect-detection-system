import sys
import traceback

def test_imports():
    """Test all critical imports"""
    results = []
    
    try:
        import numpy as np
        results.append(f"NumPy {np.__version__} - OK")
        
        # Test numpy functionality
        arr = np.array([1, 2, 3])
        results.append(f"NumPy operations - OK")
    except Exception as e:
        results.append(f"NumPy - FAILED: {e}")
    
    try:
        import torch
        results.append(f"PyTorch {torch.__version__} - OK")
        
        # Test tensor creation
        tensor = torch.tensor([1.0, 2.0])
        results.append(f"PyTorch tensors - OK")
    except Exception as e:
        results.append(f"PyTorch - FAILED: {e}")
    
    try:
        from ultralytics import YOLO
        results.append("Ultralytics import - OK")
        
        # Test model loading (this will download if needed)
        model = YOLO("yolov8n.pt")
        results.append("YOLO model loading - OK")
    except Exception as e:
        results.append(f"YOLO - FAILED: {e}")
    
    return results

if __name__ == "__main__":
    print("VERIFYING YOLO ENVIRONMENT")
    print("=" * 40)
    
    results = test_imports()
    
    failed = False
    for result in results:
        print(result)
        if "FAILED" in result:
            failed = True
    
    if not failed:
        print("\nSTATUS: ALL TESTS PASSED - READY FOR INVESTOR DEMO!")
        sys.exit(0)
    else:
        print("\nSTATUS: SOME TESTS FAILED - NEEDS FIXING")
        sys.exit(1)
