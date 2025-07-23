#!/usr/bin/env python3
"""Minimal test to check if the basic imports work"""

# Test basic Python imports first
print("1. Testing basic imports...")
import os
import sys
import time
print("✅ Basic imports work")

# Test fastapi imports
print("2. Testing FastAPI imports...")
try:
    from fastapi import FastAPI
    print("✅ FastAPI import works")
except ImportError as e:
    print(f"❌ FastAPI import failed: {e}")

# Test our module step by step
print("3. Testing tire_detection_system import...")
try:
    import tire_detection_system
    print("✅ Module imported successfully")
except Exception as e:
    print(f"❌ Module import failed: {e}")
    import traceback
    traceback.print_exc()

print("4. Done - if you see this, imports are working!")
