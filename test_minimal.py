#!/usr/bin/env python3
"""Minimal test"""

print("Testing basic imports...")
from tire_detection_system import ProductionDemoConfig

print("Testing config creation...")
config = ProductionDemoConfig()
print(f"✅ Config has {len(config.demo_scenarios)} scenarios")

print("Done!")
