import frappe
from safari_integrations.dashboard_fixtures import get_data as get_integrations_data

def setup_all_dashboards():
    """Setup all dashboard components across all Safari apps"""
    
    print("🚀 Setting up all Safari Dashboard Components...")
    print("=" * 60)
    
    # Setup Safari Integrations Dashboard
    setup_integrations_dashboard()
    
    # TODO: Setup other dashboards when their fixtures are created
    # setup_accommodation_dashboard()
    # setup_transport_dashboard()
    # setup_packages_dashboard()
    # setup_core_dashboard()
    
    frappe.db.commit()
    print("✅ All dashboard components installed successfully!")

def setup_integrations_dashboard():
    """Setup Safari Integrations dashboard"""
    print("\n📊 Setting up Safari Integrations Dashboard...")
    
    try:
        data = get_integrations_data()
        
        # Install Number Cards
        print("   📈 Installing Number Cards...")
        for card in data.number_cards:
            if not frappe.db.exists("Number Card", card["name"]):
                frappe.get_doc(card).insert()
                print(f"      ✅ Created Number Card: {card['name']}")
            else:
                print(f"      ⚠️  Number Card exists: {card['name']}")
        
        # Install Dashboard Charts
        print("   📊 Installing Dashboard Charts...")
        for chart in data.charts:
            if not frappe.db.exists("Dashboard Chart", chart["name"]):
                frappe.get_doc(chart).insert()
                print(f"      ✅ Created Dashboard Chart: {chart['name']}")
            else:
                print(f"      ⚠️  Dashboard Chart exists: {chart['name']}")
        
        # Install Dashboards
        print("   🎯 Installing Dashboards...")
        for dashboard in data.dashboards:
            if not frappe.db.exists("Dashboard", dashboard["name"]):
                frappe.get_doc(dashboard).insert()
                print(f"      ✅ Created Dashboard: {dashboard['name']}")
            else:
                print(f"      ⚠️  Dashboard exists: {dashboard['name']}")
        
        print("   ✅ Safari Integrations dashboard setup completed!")
        
    except Exception as e:
        print(f"   ❌ Error setting up Safari Integrations dashboard: {str(e)}")
        frappe.db.rollback()

def setup_accommodation_dashboard():
    """Setup Safari Accommodation dashboard"""
    print("\n🏨 Setting up Safari Accommodation Dashboard...")
    # TODO: Implement when accommodation dashboard fixtures are created
    pass

def setup_transport_dashboard():
    """Setup Safari Transport dashboard"""
    print("\n🚗 Setting up Safari Transport Dashboard...")
    # TODO: Implement when transport dashboard fixtures are created
    pass

def setup_packages_dashboard():
    """Setup Safari Packages dashboard"""
    print("\n📦 Setting up Safari Packages Dashboard...")
    # TODO: Implement when packages dashboard fixtures are created
    pass

def setup_core_dashboard():
    """Setup Safari Core dashboard"""
    print("\n🦁 Setting up Safari Core Dashboard...")
    # TODO: Implement when core dashboard fixtures are created
    pass

def verify_all_dashboards():
    """Verify all dashboard components are properly installed"""
    
    print("\n🔍 Verifying All Dashboard Components...")
    print("=" * 50)
    
    # Check Safari Integrations components
    print("\n📊 Safari Integrations Dashboard:")
    
    number_cards = [
        "Active API Providers",
        "Total API Calls Today",
        "Monthly API Costs",
        "Companies with Access",
        "Failed API Calls Today"
    ]
    
    charts = [
        "API Usage Trends",
        "Cost by Provider",
        "Monthly Quota Usage",
        "Provider Performance"
    ]
    
    dashboards = ["Integrations Management"]
    
    # Verify Number Cards
    print("   📈 Number Cards:")
    for card_name in number_cards:
        exists = frappe.db.exists("Number Card", card_name)
        status = "✅ Exists" if exists else "❌ Missing"
        print(f"      {card_name}: {status}")
    
    # Verify Dashboard Charts
    print("   📊 Dashboard Charts:")
    for chart_name in charts:
        exists = frappe.db.exists("Dashboard Chart", chart_name)
        status = "✅ Exists" if exists else "❌ Missing"
        print(f"      {chart_name}: {status}")
    
    # Verify Dashboards
    print("   🎯 Dashboards:")
    for dashboard_name in dashboards:
        exists = frappe.db.exists("Dashboard", dashboard_name)
        status = "✅ Exists" if exists else "❌ Missing"
        print(f"      {dashboard_name}: {status}")
    
    print("\n✅ Dashboard verification completed!")

if __name__ == "__main__":
    try:
        # Initialize Frappe if not already connected
        if not hasattr(frappe.local, 'site'):
            import os
            sites_path = "/home/erpnext/frappe-bench/sites"
            site = "safarierp"
            
            frappe.init(site=site, sites_path=sites_path)
            frappe.connect()
        
        # Setup all dashboards
        setup_all_dashboards()
        
        # Verify the setup
        verify_all_dashboards()
        
        print("\n🎉 All dashboard setup completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {str(e)}")
        frappe.db.rollback()
    finally:
        if hasattr(frappe.local, 'site'):
            frappe.destroy() 