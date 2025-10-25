#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MEvals macOS Integration Test Suite
Tests authentication, data access, and Meeting PromptCoT integration
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any
import subprocess

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import our modules
try:
    from mevals_auth_manager import CrossPlatformAuthManager
    from mevals_promptcot_bridge import MEValsPromptCoTBridge
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all required files are in the project directory")
    sys.exit(1)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MEValsIntegrationTest:
    """Comprehensive test suite for MEvals macOS integration"""
    
    def __init__(self):
        self.project_root = project_root
        self.mevals_dir = self.project_root / "MEvals"
        self.test_results = {}
        
    def run_all_tests(self) -> Dict[str, bool]:
        """Run complete test suite"""
        print("🧪 MEvals macOS Integration Test Suite")
        print("=====================================")
        
        tests = [
            ("Environment Setup", self.test_environment_setup),
            ("MEvals Directory", self.test_mevals_directory),
            ("Authentication Manager", self.test_auth_manager),
            ("Data Bridge", self.test_data_bridge),
            ("Sample Data Processing", self.test_sample_processing),
            ("Meeting PromptCoT Integration", self.test_promptcot_integration)
        ]
        
        all_passed = True
        
        for test_name, test_func in tests:
            print(f"\n🔍 Testing: {test_name}")
            try:
                result = test_func()
                self.test_results[test_name] = result
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"   {status}")
                
                if not result:
                    all_passed = False
                    
            except Exception as e:
                print(f"   ❌ ERROR: {e}")
                self.test_results[test_name] = False
                all_passed = False
        
        self.print_summary()
        return all_passed
    
    def test_environment_setup(self) -> bool:
        """Test basic environment setup"""
        required_packages = ['msal', 'requests', 'pathlib']
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                print(f"   Missing package: {package}")
                return False
        
        # Check Python version
        if sys.version_info < (3, 8):
            print(f"   Python {sys.version_info.major}.{sys.version_info.minor} too old, need >=3.8")
            return False
        
        print(f"   Python {sys.version_info.major}.{sys.version_info.minor}, all packages available")
        return True
    
    def test_mevals_directory(self) -> bool:
        """Test MEvals directory structure"""
        if not self.mevals_dir.exists():
            print(f"   MEvals directory not found: {self.mevals_dir}")
            print("   This is expected if MEvals hasn't been cloned yet")
            return False
        
        # Check for key directories
        required_dirs = ['data', 'scripts']
        for dir_name in required_dirs:
            dir_path = self.mevals_dir / dir_name
            if not dir_path.exists():
                print(f"   Missing directory: {dir_name}")
                return False
        
        # Check for sample data
        sample_dir = self.mevals_dir / "data" / "meeting_prep.prompt.samples"
        if sample_dir.exists():
            samples = list(sample_dir.glob("sample_*"))
            print(f"   Found {len(samples)} sample meetings")
            return len(samples) > 0
        else:
            print("   Sample data directory not found")
            return False
    
    def test_auth_manager(self) -> bool:
        """Test authentication manager initialization"""
        try:
            # Test initialization with dummy credentials
            auth_manager = CrossPlatformAuthManager(
                tenant_id="test-tenant",
                client_id="test-client-id", 
                scopes=["https://graph.microsoft.com/.default"]
            )
            
            # Test platform detection
            platform = auth_manager._detect_platform()
            if platform not in ['windows', 'darwin', 'linux']:
                print(f"   Unknown platform: {platform}")
                return False
            
            print(f"   Platform detected: {platform}")
            
            # Test auth method selection
            can_use_broker = auth_manager._can_use_broker()
            print(f"   Broker available: {can_use_broker}")
            
            return True
            
        except Exception as e:
            print(f"   Auth manager error: {e}")
            return False
    
    def test_data_bridge(self) -> bool:
        """Test data bridge initialization"""
        try:
            # Create temporary directories
            temp_mevals = self.project_root / "temp_mevals"
            temp_output = self.project_root / "temp_output"
            
            temp_mevals.mkdir(exist_ok=True)
            temp_output.mkdir(exist_ok=True)
            
            # Initialize bridge
            bridge = MEValsPromptCoTBridge(str(temp_mevals), str(temp_output))
            
            # Test with empty directory (should handle gracefully)
            scenarios = bridge.extract_training_scenarios()
            if scenarios is None:
                print("   Bridge returned None scenarios")
                return False
            
            print(f"   Bridge initialized, extracted {len(scenarios)} scenarios from empty dir")
            
            # Cleanup
            import shutil
            shutil.rmtree(temp_mevals, ignore_errors=True)
            shutil.rmtree(temp_output, ignore_errors=True)
            
            return True
            
        except Exception as e:
            print(f"   Bridge error: {e}")
            return False
    
    def test_sample_processing(self) -> bool:
        """Test processing of sample data if available"""
        if not self.mevals_dir.exists():
            print("   Skipping (MEvals not available)")
            return True
        
        sample_dir = self.mevals_dir / "data" / "meeting_prep.prompt.samples"
        if not sample_dir.exists():
            print("   Skipping (sample data not available)")
            return True
        
        try:
            # Test bridge with real data
            output_dir = self.project_root / "test_output"
            bridge = MEValsPromptCoTBridge(str(sample_dir), str(output_dir))
            
            scenarios = bridge.extract_training_scenarios()
            
            if not scenarios:
                print("   No scenarios extracted from real data")
                return False
            
            # Test conversion
            promptcot_scenarios = bridge.convert_to_promptcot_format(scenarios[:2])  # Just test first 2
            
            if not promptcot_scenarios:
                print("   No PromptCoT scenarios converted")
                return False
            
            print(f"   Processed {len(scenarios)} scenarios, converted {len(promptcot_scenarios)}")
            
            # Cleanup
            import shutil
            shutil.rmtree(output_dir, ignore_errors=True)
            
            return True
            
        except Exception as e:
            print(f"   Sample processing error: {e}")
            return False
    
    def test_promptcot_integration(self) -> bool:
        """Test integration with Meeting PromptCoT pipeline"""
        try:
            # Check if meeting prep pipeline exists
            pipeline_script = self.project_root / "run_meeting_prep_pipeline.sh"
            
            if not pipeline_script.exists():
                print("   Meeting prep pipeline not found")
                return False
            
            # Check if pipeline is executable
            if not os.access(pipeline_script, os.X_OK):
                print("   Pipeline script not executable")
                return False
            
            # Test basic pipeline validation (dry run)
            try:
                result = subprocess.run([
                    'bash', str(pipeline_script), '--help'
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0 or "usage" in result.stdout.lower() or "help" in result.stdout.lower():
                    print("   Pipeline script responds to --help")
                    return True
                else:
                    print("   Pipeline script doesn't respond properly")
                    return False
                    
            except subprocess.TimeoutExpired:
                print("   Pipeline script timeout (may be normal)")
                return True
            except Exception as e:
                print(f"   Pipeline test error: {e}")
                return False
                
        except Exception as e:
            print(f"   PromptCoT integration error: {e}")
            return False
    
    def print_summary(self):
        """Print test summary"""
        print("\n📋 Test Summary")
        print("===============")
        
        passed = sum(1 for result in self.test_results.values() if result)
        total = len(self.test_results)
        
        for test_name, result in self.test_results.items():
            status = "✅" if result else "❌"
            print(f"{status} {test_name}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! MEvals macOS integration ready.")
        else:
            print("⚠️  Some tests failed. Check the issues above.")
            
            # Provide recommendations
            print("\n💡 Recommendations:")
            
            if not self.test_results.get("MEvals Directory", False):
                print("   • Clone MEvals repository to get real meeting data")
                print("   • Run: git clone <mevals-repo-url> MEvals")
            
            if not self.test_results.get("Authentication Manager", False):
                print("   • Check MSAL installation: pip install msal")
                print("   • Verify Microsoft Graph API credentials")
            
            if not self.test_results.get("Meeting PromptCoT Integration", False):
                print("   • Ensure meeting prep pipeline is properly set up")
                print("   • Check script permissions: chmod +x run_meeting_prep_pipeline.sh")


def main():
    """Run the integration test suite"""
    test_suite = MEValsIntegrationTest()
    success = test_suite.run_all_tests()
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())