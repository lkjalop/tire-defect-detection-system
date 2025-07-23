#!/usr/bin/env python3
"""Simple sync test of the detector"""

print("Testing hybrid detector without async...")

from tire_detection_system import HybridTireDetector, ProductionDemoConfig

config = ProductionDemoConfig()
print(f"✅ Config loaded: {len(config.demo_scenarios)} scenarios")

detector = HybridTireDetector()
print(f"✅ Detector created, demo_mode: {detector.demo_mode}")

print("✅ All basic tests passed!")
