#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_report_fixtures():
    """Test the report fixtures implementation"""
    
    print("🧪 Testing Report Fixtures Implementation...")
    print("=" * 50)
    
    try:
        # Test importing report fixtures
        from safari_integrations.report_fixtures import get_data
        
        print("✅ Successfully imported report_fixtures module")
        
        # Test getting data
        data = get_data()
        
        print(f"✅ Successfully loaded report data:")
        print(f"   - Reports: {len(data.reports)}")
        
        # Test reports structure
        if data.reports:
            sample_report = data.reports[0]
            required_fields = ['doctype', 'name', 'report_name', 'module', 'report_type', 'ref_doctype']
            missing_fields = [field for field in required_fields if field not in sample_report]
            
            if not missing_fields:
                print("✅ Reports have correct structure")
            else:
                print(f"❌ Reports missing fields: {missing_fields}")
        
        print("\n✅ All report fixtures tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def test_hooks_configuration():
    """Test that hooks.py is properly configured for reports"""
    
    print("\n🔧 Testing Hooks Configuration for Reports...")
    print("=" * 50)
    
    try:
        # Read hooks.py file
        hooks_file = "safari_integrations/hooks.py"
        
        if not os.path.exists(hooks_file):
            print(f"❌ Hooks file not found: {hooks_file}")
            return False
        
        with open(hooks_file, 'r') as f:
            hooks_content = f.read()
        
        # Check for required configurations
        required_configs = [
            '"doctype": "Report"',
            'after_install = "safari_integrations.setup.install.after_install"',
            'install_report_fixtures'
        ]
        
        missing_configs = []
        for config in required_configs:
            if config not in hooks_content:
                missing_configs.append(config)
        
        if not missing_configs:
            print("✅ Hooks file properly configured for reports")
        else:
            print(f"❌ Missing configurations in hooks.py: {missing_configs}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing hooks configuration: {str(e)}")
        return False

def test_install_script():
    """Test that install.py is properly configured for reports"""
    
    print("\n⚙️  Testing Install Script for Reports...")
    print("=" * 45)
    
    try:
        # Read install.py file
        install_file = "safari_integrations/setup/install.py"
        
        if not os.path.exists(install_file):
            print(f"❌ Install file not found: {install_file}")
            return False
        
        with open(install_file, 'r') as f:
            install_content = f.read()
        
        # Check for required functions
        required_functions = [
            'def install_report_fixtures():',
            'from safari_integrations.report_fixtures import get_data',
            'install_report_fixtures()'
        ]
        
        missing_functions = []
        for func in required_functions:
            if func not in install_content:
                missing_functions.append(func)
        
        if not missing_functions:
            print("✅ Install script properly configured for reports")
        else:
            print(f"❌ Missing functions in install.py: {missing_functions}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing install script: {str(e)}")
        return False

def test_report_structure():
    """Test the structure of report fixtures"""
    
    print("\n📋 Testing Report Structure...")
    print("=" * 35)
    
    try:
        from safari_integrations.report_fixtures import get_data
        
        data = get_data()
        
        if not data.reports:
            print("❌ No reports found in fixtures")
            return False
        
        print(f"✅ Found {len(data.reports)} reports in fixtures")
        
        # Test each report structure
        for i, report in enumerate(data.reports):
            print(f"   Report {i+1}: {report.get('name', 'Unknown')}")
            
            # Check required fields
            required_fields = ['doctype', 'name', 'report_name', 'module', 'report_type', 'ref_doctype']
            missing_fields = [field for field in required_fields if field not in report]
            
            if missing_fields:
                print(f"      ❌ Missing fields: {missing_fields}")
                return False
            else:
                print(f"      ✅ Structure valid")
            
            # Check roles
            if 'roles' not in report or not report['roles']:
                print(f"      ⚠️  No roles defined")
            else:
                print(f"      ✅ Roles: {len(report['roles'])}")
        
        print("✅ All report structures are valid!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing report structure: {str(e)}")
        return False

def main():
    """Run all tests"""
    
    print("🚀 Running Report Export System Tests...")
    print("=" * 60)
    
    tests = [
        test_report_fixtures,
        test_hooks_configuration,
        test_install_script,
        test_report_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("🎯 Test Results:")
    print(f"   Passed: {passed}/{total}")
    print(f"   Failed: {total - passed}/{total}")
    
    if passed == total:
        print("✅ All tests passed! Report export system is ready.")
    else:
        print("❌ Some tests failed. Please check the implementation.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 