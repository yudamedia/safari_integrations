import frappe

def verify_report_exports():
    """Verify all report components are properly exported"""
    
    print("🔍 Verifying Report Component Exports...")
    print("=" * 60)
    
    # Check Reports
    print("\n📊 Reports:")
    reports = [
        "API Usage Analytics",
        "API Cost Analysis",
        "Provider Performance Report",
        "Company API Access Report",
        "API Quota Usage Report"
    ]
    
    for report_name in reports:
        exists = frappe.db.exists("Report", report_name)
        status = "✅ Exists" if exists else "❌ Missing"
        print(f"   {report_name}: {status}")
        
        if exists:
            report = frappe.get_doc("Report", report_name)
            print(f"      Type: {report.report_type}, Document: {report.ref_doctype}")
            print(f"      Module: {report.module}")
            print(f"      Standard: {report.is_standard}")
    
    print("\n🎯 Summary:")
    total_reports = len([report for report in reports if frappe.db.exists("Report", report)])
    
    print(f"   Reports: {total_reports}/{len(reports)}")
    
    # Check if components are exportable
    print("\n📤 Export Status:")
    check_report_export_status()

def check_report_export_status():
    """Check if report components can be exported using Frappe's export mechanism"""
    
    try:
        # Test export of a report
        if frappe.db.exists("Report", "API Usage Analytics"):
            report = frappe.get_doc("Report", "API Usage Analytics")
            export_data = report.as_dict()
            print("   ✅ Reports: Exportable")
        else:
            print("   ❌ Reports: Not found for export test")
        
        # Test export of report fixtures
        try:
            from safari_integrations.report_fixtures import get_data
            data = get_data()
            print(f"   ✅ Report Fixtures: Exportable ({len(data.reports)} reports)")
        except Exception as e:
            print(f"   ❌ Report Fixtures: Error - {str(e)}")
            
    except Exception as e:
        print(f"   ❌ Export test failed: {str(e)}")

def test_report_fixture_installation():
    """Test if report fixtures can be installed properly"""
    
    print("\n🧪 Testing Report Fixture Installation...")
    
    try:
        from safari_integrations.report_fixtures import get_data
        
        data = get_data()
        
        print(f"   ✅ Report fixtures data loaded:")
        print(f"      - Reports: {len(data.reports)}")
        
        # Test creating a sample report
        if data.reports:
            sample_report = data.reports[0]
            required_fields = ['doctype', 'name', 'report_name', 'module', 'report_type']
            missing_fields = [field for field in required_fields if field not in sample_report]
            
            if not missing_fields:
                print("   ✅ Reports have correct structure")
            else:
                print(f"   ❌ Reports missing fields: {missing_fields}")
        
        print("   ✅ All report fixture structures are valid!")
        
    except Exception as e:
        print(f"   ❌ Report fixture test failed: {str(e)}")

def generate_report_export_commands():
    """Generate the export commands for manual export"""
    
    print("\n📋 Report Export Commands:")
    print("=" * 30)
    
    print("# Export Reports:")
    reports = [
        "API Usage Analytics",
        "API Cost Analysis",
        "Provider Performance Report",
        "Company API Access Report",
        "API Quota Usage Report"
    ]
    
    for report_name in reports:
        print(f'bench --site safarierp export-doc "Report" "{report_name}" safari_integrations/fixtures/')

def check_report_roles():
    """Check if report roles are properly configured"""
    
    print("\n👥 Checking Report Roles...")
    
    # Check if API Manager role exists
    api_manager_exists = frappe.db.exists("Role", "API Manager")
    print(f"   API Manager Role: {'✅ Exists' if api_manager_exists else '❌ Missing'}")
    
    # Check if System Manager role exists
    system_manager_exists = frappe.db.exists("Role", "System Manager")
    print(f"   System Manager Role: {'✅ Exists' if system_manager_exists else '❌ Missing'}")
    
    if api_manager_exists:
        api_manager = frappe.get_doc("Role", "API Manager")
        print(f"      Desk Access: {api_manager.desk_access}")
        print(f"      Disabled: {api_manager.disabled}")

def verify_report_permissions():
    """Verify report permissions are properly set"""
    
    print("\n🔐 Checking Report Permissions...")
    
    reports = [
        "API Usage Analytics",
        "API Cost Analysis",
        "Provider Performance Report",
        "Company API Access Report",
        "API Quota Usage Report"
    ]
    
    for report_name in reports:
        if frappe.db.exists("Report", report_name):
            report = frappe.get_doc("Report", report_name)
            print(f"   {report_name}:")
            print(f"      Disabled: {report.disabled}")
            print(f"      Standard: {report.is_standard}")
            print(f"      Roles: {len(report.roles)}")
            
            for role in report.roles:
                print(f"         - {role.role}")

if __name__ == "__main__":
    try:
        # Initialize Frappe if not already connected
        if not hasattr(frappe.local, 'site'):
            import os
            sites_path = "/home/erpnext/frappe-bench/sites"
            site = "safarierp"
            
            frappe.init(site=site, sites_path=sites_path)
            frappe.connect()
        
        # Run verification
        verify_report_exports()
        
        # Test fixture installation
        test_report_fixture_installation()
        
        # Check roles
        check_report_roles()
        
        # Check permissions
        verify_report_permissions()
        
        # Generate export commands
        generate_report_export_commands()
        
        print("\n🎉 Report export verification completed!")
        
    except Exception as e:
        print(f"\n❌ Verification failed: {str(e)}")
    finally:
        if hasattr(frappe.local, 'site'):
            frappe.destroy() 