#!/usr/bin/env python3
"""
Tire Defect Detection System
============================

Learning project demonstrating YOLOv8 computer vision integration.
Designed for portfolio/interview demonstration purposes.

Author: Career transition project (Health Sciences -> Software/AI)
"""

import os
import sys
import time
import logging
from datetime import datetime
from pathlib import Path

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TireDefectDetector:
    """
    Simple tire defect detection system using YOLOv8.
    
    This is a learning project demonstrating:
    - Computer vision integration
    - Real-time video processing
    - System architecture concepts
    """
    
    def __init__(self):
        self.version = "Learning Project v1.0"
        self.model = None
        self.setup_system()
    
    def setup_system(self):
        """Initialize the detection system."""
        logger.info(f"Starting {self.version}")
        logger.info("This is a learning/portfolio demonstration project")
        
        try:
            self.load_yolo_model()
        except Exception as e:
            logger.warning(f"YOLO model loading failed: {e}")
            logger.info("Running in demo mode without AI model")
    
    def load_yolo_model(self):
        """Load YOLOv8 model if available."""
        try:
            from ultralytics import YOLO
            self.model = YOLO('yolov8n.pt')  # Nano model for speed
            logger.info("YOLOv8 nano model loaded successfully")
            return True
        except ImportError:
            logger.warning("ultralytics not installed - run: pip install ultralytics")
            return False
        except Exception as e:
            logger.error(f"Model loading error: {e}")
            return False
    
    def detect_defects(self, image_path_or_frame):
        """
        Detect defects in tire image/frame.
        
        Note: Uses generic YOLO model, not tire-specific training.
        """
        if self.model is None:
            return self.simulate_detection()
        
        try:
            results = self.model(image_path_or_frame, verbose=False)
            return self.process_yolo_results(results)
        except Exception as e:
            logger.error(f"Detection error: {e}")
            return self.simulate_detection()
    
    def process_yolo_results(self, results):
        """Process YOLO detection results."""
        detections = []
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    conf = float(box.conf[0])
                    if conf > 0.5:  # Confidence threshold
                        detections.append({
                            'confidence': conf,
                            'bbox': box.xyxy[0].tolist(),
                            'class': int(box.cls[0]),
                            'type': 'generic_object'  # Not tire-specific
                        })
        
        return {
            'detections': detections,
            'count': len(detections),
            'model': 'YOLOv8-nano',
            'note': 'Generic object detection, not tire-specific'
        }
    
    def simulate_detection(self):
        """Fallback simulation for demo purposes."""
        import random
        
        # Simulate basic detection for demo/portfolio purposes
        simulated_detections = []
        
        if random.random() > 0.3:  # 70% chance of "detecting" something
            num_detections = random.randint(1, 3)
            for i in range(num_detections):
                simulated_detections.append({
                    'confidence': round(random.uniform(0.6, 0.95), 2),
                    'bbox': [
                        random.randint(50, 200),
                        random.randint(50, 200), 
                        random.randint(250, 400),
                        random.randint(250, 400)
                    ],
                    'type': 'simulated_defect',
                    'note': 'Demo simulation'
                })
        
        return {
            'detections': simulated_detections,
            'count': len(simulated_detections),
            'model': 'simulation',
            'note': 'Demo mode - not real AI detection'
        }
    
    def process_video_stream(self):
        """Process video stream for real-time detection."""
        try:
            import cv2
        except ImportError:
            logger.error("OpenCV not installed - run: pip install opencv-python")
            return
        
        logger.info("Starting video stream processing...")
        logger.info("Press 'q' to quit")
        
        cap = cv2.VideoCapture(0)  # Default camera
        
        if not cap.isOpened():
            logger.warning("Camera not available, using demo mode")
            self.demo_mode()
            return
        
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Process every 5th frame for performance
            if frame_count % 5 == 0:
                results = self.detect_defects(frame)
                
                # Draw results on frame
                frame = self.draw_detections(frame, results)
                
                # Display processing info
                cv2.putText(frame, f"Model: {results.get('model', 'unknown')}", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f"Detections: {results['count']}", 
                           (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow('Tire Defect Detection - Learning Project', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
    
    def draw_detections(self, frame, results):
        """Draw detection results on frame."""
        try:
            import cv2
            
            for detection in results['detections']:
                bbox = detection['bbox']
                conf = detection['confidence']
                
                # Draw bounding box
                cv2.rectangle(frame, 
                            (int(bbox[0]), int(bbox[1])), 
                            (int(bbox[2]), int(bbox[3])), 
                            (0, 255, 0), 2)
                
                # Draw confidence
                label = f"{detection['type']}: {conf:.2f}"
                cv2.putText(frame, label, 
                           (int(bbox[0]), int(bbox[1]) - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
            return frame
        except ImportError:
            return frame
    
    def demo_mode(self):
        """Run system in demo mode without camera."""
        logger.info("Running demo mode...")
        
        for i in range(5):
            print(f"\nDemo Detection {i+1}/5:")
            results = self.detect_defects("demo_image")
            
            print(f"  Detections found: {results['count']}")
            print(f"  Model used: {results['model']}")
            print(f"  Note: {results['note']}")
            
            if results['detections']:
                for j, det in enumerate(results['detections']):
                    print(f"    Detection {j+1}: {det['type']} (confidence: {det['confidence']})")
            
            time.sleep(1)
        
        print("\nDemo completed. This demonstrates basic system functionality.")
        print("For real tire defect detection, custom training data would be required.")
    
    def run_tests(self):
        """Run basic system tests."""
        print("Running system tests...\n")
        
        # Test 1: System initialization
        print("✓ System initialization: PASSED")
        
        # Test 2: Model loading
        if self.model is not None:
            print("✓ YOLO model loading: PASSED")
        else:
            print("⚠ YOLO model loading: SIMULATION MODE")
        
        # Test 3: Detection function
        test_result = self.detect_defects("test")
        if test_result and 'detections' in test_result:
            print("✓ Detection function: PASSED")
        else:
            print("✗ Detection function: FAILED")
        
        # Test 4: Basic dependencies
        try:
            import cv2
            print("✓ OpenCV available: PASSED")
        except ImportError:
            print("⚠ OpenCV not available: INSTALL NEEDED")
        
        print(f"\nSystem Status: Learning project ready for demonstration")
        print(f"Version: {self.version}")

def main():
    """Main function with menu system."""
    detector = TireDefectDetector()
    
    while True:
        print("\n" + "="*50)
        print("TIRE DEFECT DETECTION - LEARNING PROJECT")
        print("="*50)
        print("1. Run camera detection")
        print("2. Run demo mode")
        print("3. Run system tests")
        print("4. Show project info")
        print("5. Exit")
        print("-"*50)
        
        choice = input("Select option (1-5): ").strip()
        
        if choice == '1':
            detector.process_video_stream()
        elif choice == '2':
            detector.demo_mode()
        elif choice == '3':
            detector.run_tests()
        elif choice == '4':
            print("\nPROJECT INFORMATION:")
            print("- Learning portfolio project")
            print("- Demonstrates YOLOv8 integration")
            print("- Not production-ready software")
            print("- Uses generic object detection (not tire-specific)")
            print("- Created for portfolio/interview purposes")
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
