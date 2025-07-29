#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_dashboard_fixtures():
    """Test the dashboard fixtures implementation"""
    
    print("🧪 Testing Dashboard Fixtures Implementation...")
    print("=" * 50)
    
    try:
        # Test importing dashboard fixtures
        from safari_integrations.dashboard_fixtures import get_data
        
        print("✅ Successfully imported dashboard_fixtures module")
        
        # Test getting data
        data = get_data()
        
        print(f"✅ Successfully loaded dashboard data:")
        print(f"   - Number Cards: {len(data.number_cards)}")
        print(f"   - Dashboard Charts: {len(data.charts)}")
        print(f"   - Dashboards: {len(data.dashboards)}")
        
        # Test number cards structure
        if data.number_cards:
            sample_card = data.number_cards[0]
            required_fields = ['doctype', 'name', 'label', 'document_type', 'function']
            missing_fields = [field for field in required_fields if field not in sample_card]
            
            if not missing_fields:
                print("✅ Number cards have correct structure")
            else:
                print(f"❌ Number cards missing fields: {missing_fields}")
        
        # Test charts structure
        if data.charts:
            sample_chart = data.charts[0]
            required_fields = ['doctype', 'name', 'chart_name', 'document_type']
            missing_fields = [field for field in required_fields if field not in sample_chart]
            
            if not missing_fields:
                print("✅ Dashboard charts have correct structure")
            else:
                print(f"❌ Dashboard charts missing fields: {missing_fields}")
        
        # Test dashboards structure
        if data.dashboards:
            sample_dashboard = data.dashboards[0]
            required_fields = ['name', 'dashboard_name']
            missing_fields = [field for field in required_fields if field not in sample_dashboard]
            
            if not missing_fields:
                print("✅ Dashboards have correct structure")
            else:
                print(f"❌ Dashboards missing fields: {missing_fields}")
        
        print("\n✅ All dashboard fixtures tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def test_hooks_configuration():
    """Test that hooks.py is properly configured"""
    
    print("\n🔧 Testing Hooks Configuration...")
    print("=" * 40)
    
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
            'after_install = "safari_integrations.setup.install.after_install"',
            '"doctype": "Number Card"',
            '"doctype": "Dashboard Chart"',
            '"doctype": "Dashboard"'
        ]
        
        missing_configs = []
        for config in required_configs:
            if config not in hooks_content:
                missing_configs.append(config)
        
        if not missing_configs:
            print("✅ Hooks file properly configured")
        else:
            print(f"❌ Missing configurations in hooks.py: {missing_configs}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing hooks configuration: {str(e)}")
        return False

def test_install_script():
    """Test that install.py is properly configured"""
    
    print("\n⚙️  Testing Install Script...")
    print("=" * 35)
    
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
            'def after_install():',
            'def install_dashboard_fixtures():',
            'from safari_integrations.dashboard_fixtures import get_data'
        ]
        
        missing_functions = []
        for func in required_functions:
            if func not in install_content:
                missing_functions.append(func)
        
        if not missing_functions:
            print("✅ Install script properly configured")
        else:
            print(f"❌ Missing functions in install.py: {missing_functions}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing install script: {str(e)}")
        return False

def main():
    """Run all tests"""
    
    print("🚀 Running Dashboard Export System Tests...")
    print("=" * 60)
    
    tests = [
        test_dashboard_fixtures,
        test_hooks_configuration,
        test_install_script
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
        print("✅ All tests passed! Dashboard export system is ready.")
    else:
        print("❌ Some tests failed. Please check the implementation.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 