#!/usr/bin/env python3
"""Simple test to isolate the hanging issue"""

print("1. Basic imports...")
import time
import asyncio
from dataclasses import dataclass
print("✅ Basic imports work")

print("2. Creating simple dataclass...")
@dataclass
class SimpleConfig:
    value: int = 42
    
config = SimpleConfig()
print(f"✅ Dataclass works: {config.value}")

print("3. Testing async function...")
async def simple_async():
    await asyncio.sleep(0.01)
    return "async works"

result = asyncio.run(simple_async())
print(f"✅ Async works: {result}")

print("4. All tests passed!")
