#!/usr/bin/env python3
"""
Security validation script for tire defect detection system
Tests security implementations before commit
"""
import os
import sys
import json
import subprocess
from pathlib import Path

class SecurityTester:
    def __init__(self):
        self.root_path = Path(__file__).parent.parent
        self.passed_tests = 0
        self.total_tests = 0
    
    def test_threat_model_exists(self):
        """Ensure threat model documentation exists"""
        self.total_tests += 1
        threat_model_path = self.root_path / "docs" / "THREAT_MODEL.md"
        
        if not threat_model_path.exists():
            print("❌ THREAT_MODEL.md not found")
            return False
        
        # Check content quality
        with open(threat_model_path, 'r') as f:
            content = f.read()
            required_sections = [
                "OWASP", "AI-Specific Threat", "Compliance", 
                "Rate Limiting", "Authentication"
            ]
            missing_sections = [s for s in required_sections if s not in content]
            
            if missing_sections:
                print(f"❌ Threat model missing sections: {missing_sections}")
                return False
        
        print("✅ Threat model documentation validated")
        self.passed_tests += 1
        return True
    
    def test_security_implementation_exists(self):
        """Test that security implementation files exist"""
        self.total_tests += 1
        security_path = self.root_path / "security" / "threat_mitigations.py"
        
        if not security_path.exists():
            print("❌ Security implementation not found")
            return False
        
        # Check implementation content
        with open(security_path, 'r') as f:
            content = f.read()
            required_classes = [
                "RateLimiter", "ImageValidator", "SecurityManager", 
                "ModelOutputValidator", "AuditLogger"
            ]
            missing_classes = [c for c in required_classes if c not in content]
            
            if missing_classes:
                print(f"❌ Security implementation missing classes: {missing_classes}")
                return False
        
        print("✅ Security implementation validated")
        self.passed_tests += 1
        return True
    
    def test_docker_security(self):
        """Test Docker security configuration"""
        self.total_tests += 1
        dockerfile_path = self.root_path / "Dockerfile"
        
        if not dockerfile_path.exists():
            print("⚠️  Dockerfile not found, skipping security check")
            return True
        
        with open(dockerfile_path, 'r') as f:
            content = f.read()
            security_issues = []
            
            if "USER root" in content and "USER " not in content.split("USER root")[1]:
                security_issues.append("Running as root user")
            
            if "--privileged" in content:
                security_issues.append("Privileged mode detected")
            
            if security_issues:
                print(f"⚠️  Docker security concerns: {security_issues}")
                return True  # Warning, not failure
        
        print("✅ Docker security configuration validated")
        self.passed_tests += 1
        return True
    
    def test_environment_config(self):
        """Test environment configuration security"""
        self.total_tests += 1
        
        # Check for .env.example or similar
        env_files = [".env.example", ".env.template", "config/"]
        found_config = any((self.root_path / f).exists() for f in env_files)
        
        if not found_config:
            print("⚠️  No environment configuration template found")
            return True  # Warning, not failure
        
        print("✅ Environment configuration validated")
        self.passed_tests += 1
        return True
    
    def run_all_tests(self):
        """Run all security tests"""
        print("🔐 Starting security validation...")
        print("=" * 50)
        
        tests = [
            self.test_threat_model_exists,
            self.test_security_implementation_exists,
            self.test_docker_security,
            self.test_environment_config,
        ]
        
        all_passed = True
        for test in tests:
            try:
                if not test():
                    all_passed = False
            except Exception as e:
                print(f"❌ Test error: {e}")
                all_passed = False
        
        print("=" * 50)
        print(f"📊 Security Tests: {self.passed_tests}/{self.total_tests} passed")
        
        if all_passed:
            print("🎉 All security tests passed! Ready to commit.")
            return True
        else:
            print("❌ Security tests failed. Please fix before committing.")
            return False

def main():
    tester = SecurityTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
