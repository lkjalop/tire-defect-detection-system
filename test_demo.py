#!/usr/bin/env python3
"""Quick test of the hybrid detector system"""

import asyncio
from tire_detection_system import HybridTireDetector

async def test_hybrid_detector():
    """Test the hybrid detector functionality"""
    print("🔧 Testing hybrid detector...")
    
    detector = HybridTireDetector()
    await detector.initialize()
    
    # Test simulation mode
    result = await detector.generate_simulation_result('good')
    
    print(f"✅ Demo working:")
    print(f"   Quality: {result.overall_quality}")
    print(f"   Score: {result.quality_score}")
    print(f"   Defects: {len(result.defects_found)}")
    print(f"   Safety: {result.safety_status}")
    print(f"   Recommendations: {len(result.recommendations)}")
    print(f"   Processing time: {result.processing_time:.3f}s")
    
    return result

if __name__ == "__main__":
    asyncio.run(test_hybrid_detector())
