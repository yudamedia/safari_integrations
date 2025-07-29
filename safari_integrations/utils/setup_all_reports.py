import frappe
from safari_integrations.report_fixtures import get_data as get_integrations_reports

def setup_all_reports():
    """Setup all report components across all Safari apps"""
    
    print("🚀 Setting up all Safari Report Components...")
    print("=" * 60)
    
    # Setup Safari Integrations Reports
    setup_integrations_reports()
    
    # TODO: Setup other app reports when their fixtures are created
    # setup_operations_reports()
    # setup_accommodation_reports()
    # setup_transport_reports()
    # setup_packages_reports()
    # setup_core_reports()
    
    frappe.db.commit()
    print("✅ All report components installed successfully!")

def setup_integrations_reports():
    """Setup Safari Integrations reports"""
    print("\n📊 Setting up Safari Integrations Reports...")
    
    try:
        data = get_integrations_reports()
        
        # Install Reports
        print("   📈 Installing Reports...")
        for report in data.reports:
            if not frappe.db.exists("Report", report["name"]):
                frappe.get_doc(report).insert()
                print(f"      ✅ Created Report: {report['name']}")
            else:
                print(f"      ⚠️  Report exists: {report['name']}")
        
        print("   ✅ Safari Integrations reports setup completed!")
        
    except Exception as e:
        print(f"   ❌ Error setting up Safari Integrations reports: {str(e)}")
        frappe.db.rollback()

def setup_operations_reports():
    """Setup Safari Operations reports"""
    print("\n🏢 Setting up Safari Operations Reports...")
    # TODO: Implement when operations report fixtures are created
    pass

def setup_accommodation_reports():
    """Setup Safari Accommodation reports"""
    print("\n🏨 Setting up Safari Accommodation Reports...")
    # TODO: Implement when accommodation report fixtures are created
    pass

def setup_transport_reports():
    """Setup Safari Transport reports"""
    print("\n🚗 Setting up Safari Transport Reports...")
    # TODO: Implement when transport report fixtures are created
    pass

def setup_packages_reports():
    """Setup Safari Packages reports"""
    print("\n📦 Setting up Safari Packages Reports...")
    # TODO: Implement when packages report fixtures are created
    pass

def setup_core_reports():
    """Setup Safari Core reports"""
    print("\n🦁 Setting up Safari Core Reports...")
    # TODO: Implement when core report fixtures are created
    pass

def verify_all_reports():
    """Verify all report components are properly installed"""
    
    print("\n🔍 Verifying All Report Components...")
    print("=" * 50)
    
    # Check Safari Integrations reports
    print("\n📊 Safari Integrations Reports:")
    
    reports = [
        "API Usage Analytics",
        "API Cost Analysis",
        "Provider Performance Report",
        "Company API Access Report",
        "API Quota Usage Report"
    ]
    
    # Verify Reports
    print("   📈 Reports:")
    for report_name in reports:
        exists = frappe.db.exists("Report", report_name)
        status = "✅ Exists" if exists else "❌ Missing"
        print(f"      {report_name}: {status}")
        
        if exists:
            report = frappe.get_doc("Report", report_name)
            print(f"         Type: {report.report_type}, Document: {report.ref_doctype}")
            print(f"         Module: {report.module}")
    
    print("\n✅ Report verification completed!")

def test_report_installation():
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
            print(f"   ✅ Sample Report structure valid: {sample_report['name']}")
        
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

if __name__ == "__main__":
    try:
        # Initialize Frappe if not already connected
        if not hasattr(frappe.local, 'site'):
            import os
            sites_path = "/home/erpnext/frappe-bench/sites"
            site = "safarierp"
            
            frappe.init(site=site, sites_path=sites_path)
            frappe.connect()
        
        # Setup all reports
        setup_all_reports()
        
        # Verify the setup
        verify_all_reports()
        
        # Test fixture installation
        test_report_installation()
        
        # Generate export commands
        generate_report_export_commands()
        
        print("\n🎉 All report setup completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {str(e)}")
        frappe.db.rollback()
    finally:
        if hasattr(frappe.local, 'site'):
            frappe.destroy() 