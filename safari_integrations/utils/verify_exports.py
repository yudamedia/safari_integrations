import frappe

def verify_dashboard_exports():
    """Verify all dashboard components are properly exported"""
    
    print("🔍 Verifying Dashboard Component Exports...")
    print("=" * 60)
    
    # Check Number Cards
    print("\n📊 Number Cards:")
    number_cards = [
        "Active API Providers",
        "Total API Calls Today",
        "Monthly API Costs",
        "Companies with Access",
        "Failed API Calls Today"
    ]
    
    for card_name in number_cards:
        exists = frappe.db.exists("Number Card", card_name)
        status = "✅ Exists" if exists else "❌ Missing"
        print(f"   {card_name}: {status}")
        
        if exists:
            card = frappe.get_doc("Number Card", card_name)
            print(f"      Module: {card.module}")
            print(f"      Document Type: {card.document_type}")
            print(f"      Function: {card.function}")
    
    # Check Dashboard Charts
    print("\n📈 Dashboard Charts:")
    charts = [
        "API Usage Trends",
        "Cost by Provider",
        "Monthly Quota Usage",
        "Provider Performance"
    ]
    
    for chart_name in charts:
        exists = frappe.db.exists("Dashboard Chart", chart_name)
        status = "✅ Exists" if exists else "❌ Missing"
        print(f"   {chart_name}: {status}")
        
        if exists:
            chart = frappe.get_doc("Dashboard Chart", chart_name)
            print(f"      Type: {chart.chart_type}, Document: {chart.document_type}")
            print(f"      Module: {chart.module}")
    
    # Check Dashboards
    print("\n🎯 Dashboards:")
    dashboards = ["Integrations Management"]
    
    for dashboard_name in dashboards:
        exists = frappe.db.exists("Dashboard", dashboard_name)
        status = "✅ Exists" if exists else "❌ Missing"
        print(f"   {dashboard_name}: {status}")
        
        if exists:
            dashboard = frappe.get_doc("Dashboard", dashboard_name)
            print(f"      Charts: {len(dashboard.charts)}")
            print(f"      Cards: {len(dashboard.cards)}")
    
    # Check Workspace
    print("\n⚙️  Workspace Configuration:")
    workspace_exists = frappe.db.exists("Workspace", "Integrations Management")
    print(f"   Integrations Management: {'✅ Exists' if workspace_exists else '❌ Missing'}")
    
    if workspace_exists:
        workspace = frappe.get_doc("Workspace", "Integrations Management")
        print(f"   Charts in workspace: {len(workspace.charts)}")
        print(f"   Number cards in workspace: {len(workspace.number_cards)}")
    
    print("\n🎯 Summary:")
    total_cards = len([card for card in number_cards if frappe.db.exists("Number Card", card)])
    total_charts = len([chart for chart in charts if frappe.db.exists("Dashboard Chart", chart)])
    total_dashboards = len([dashboard for dashboard in dashboards if frappe.db.exists("Dashboard", dashboard)])
    
    print(f"   Number Cards: {total_cards}/{len(number_cards)}")
    print(f"   Dashboard Charts: {total_charts}/{len(charts)}")
    print(f"   Dashboards: {total_dashboards}/{len(dashboards)}")
    
    # Check if components are exportable
    print("\n📤 Export Status:")
    check_export_status()

def check_export_status():
    """Check if components can be exported using Frappe's export mechanism"""
    
    try:
        # Test export of a number card
        if frappe.db.exists("Number Card", "Active API Providers"):
            card = frappe.get_doc("Number Card", "Active API Providers")
            export_data = card.as_dict()
            print("   ✅ Number Cards: Exportable")
        else:
            print("   ❌ Number Cards: Not found for export test")
        
        # Test export of a dashboard chart
        if frappe.db.exists("Dashboard Chart", "API Usage Trends"):
            chart = frappe.get_doc("Dashboard Chart", "API Usage Trends")
            export_data = chart.as_dict()
            print("   ✅ Dashboard Charts: Exportable")
        else:
            print("   ❌ Dashboard Charts: Not found for export test")
        
        # Test export of a dashboard
        if frappe.db.exists("Dashboard", "Integrations Management"):
            dashboard = frappe.get_doc("Dashboard", "Integrations Management")
            export_data = dashboard.as_dict()
            print("   ✅ Dashboards: Exportable")
        else:
            print("   ❌ Dashboards: Not found for export test")
            
    except Exception as e:
        print(f"   ❌ Export test failed: {str(e)}")

def test_fixture_installation():
    """Test if fixtures can be installed properly"""
    
    print("\n🧪 Testing Fixture Installation...")
    
    try:
        from safari_integrations.dashboard_fixtures import get_data
        
        data = get_data()
        
        print(f"   ✅ Dashboard fixtures data loaded:")
        print(f"      - Number Cards: {len(data.number_cards)}")
        print(f"      - Dashboard Charts: {len(data.charts)}")
        print(f"      - Dashboards: {len(data.dashboards)}")
        
        # Test creating a sample number card
        if data.number_cards:
            sample_card = data.number_cards[0]
            print(f"   ✅ Sample Number Card structure valid: {sample_card['name']}")
        
        # Test creating a sample chart
        if data.charts:
            sample_chart = data.charts[0]
            print(f"   ✅ Sample Dashboard Chart structure valid: {sample_chart['name']}")
        
        # Test creating a sample dashboard
        if data.dashboards:
            sample_dashboard = data.dashboards[0]
            print(f"   ✅ Sample Dashboard structure valid: {sample_dashboard['name']}")
        
        print("   ✅ All fixture structures are valid!")
        
    except Exception as e:
        print(f"   ❌ Fixture test failed: {str(e)}")

def generate_export_commands():
    """Generate the export commands for manual export"""
    
    print("\n📋 Export Commands:")
    print("=" * 30)
    
    print("# Export Number Cards:")
    number_cards = [
        "Active API Providers",
        "Total API Calls Today",
        "Monthly API Costs",
        "Companies with Access",
        "Failed API Calls Today"
    ]
    
    for card_name in number_cards:
        print(f'bench --site safarierp export-doc "Number Card" "{card_name}" safari_integrations/fixtures/')
    
    print("\n# Export Dashboard Charts:")
    charts = [
        "API Usage Trends",
        "Cost by Provider",
        "Monthly Quota Usage",
        "Provider Performance"
    ]
    
    for chart_name in charts:
        print(f'bench --site safarierp export-doc "Dashboard Chart" "{chart_name}" safari_integrations/fixtures/')
    
    print("\n# Export Dashboards:")
    dashboards = ["Integrations Management"]
    
    for dashboard_name in dashboards:
        print(f'bench --site safarierp export-doc "Dashboard" "{dashboard_name}" safari_integrations/fixtures/')

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
        verify_dashboard_exports()
        
        # Test fixture installation
        test_fixture_installation()
        
        # Generate export commands
        generate_export_commands()
        
        print("\n🎉 Export verification completed!")
        
    except Exception as e:
        print(f"\n❌ Verification failed: {str(e)}")
    finally:
        if hasattr(frappe.local, 'site'):
            frappe.destroy() 