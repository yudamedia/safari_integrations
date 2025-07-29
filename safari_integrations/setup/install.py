import frappe
from frappe import _

def after_install():
    """Install dashboard fixtures and reports after app installation"""
    setup_default_providers()
    setup_default_roles()
    install_dashboard_fixtures()
    install_report_fixtures()

def install_dashboard_fixtures():
    """Install dashboard fixtures for Safari Integrations"""
    try:
        from safari_integrations.dashboard_fixtures import get_data
        
        data = get_data()
        
        # Install Number Cards
        for card in data.number_cards:
            if not frappe.db.exists("Number Card", card["name"]):
                frappe.get_doc(card).insert()
                print(f"✅ Created Number Card: {card['name']}")
        
        # Install Dashboard Charts
        for chart in data.charts:
            if not frappe.db.exists("Dashboard Chart", chart["name"]):
                frappe.get_doc(chart).insert()
                print(f"✅ Created Dashboard Chart: {chart['name']}")
        
        # Install Dashboards
        for dashboard in data.dashboards:
            if not frappe.db.exists("Dashboard", dashboard["name"]):
                frappe.get_doc(dashboard).insert()
                print(f"✅ Created Dashboard: {dashboard['name']}")
        
        frappe.db.commit()
        print("✅ Safari Integrations dashboard fixtures installed successfully!")
        
    except Exception as e:
        print(f"❌ Error installing dashboard fixtures: {str(e)}")
        frappe.db.rollback()

def install_report_fixtures():
    """Install report fixtures for Safari Integrations"""
    try:
        from safari_integrations.report_fixtures import get_data
        
        data = get_data()
        
        # Install Reports
        for report in data.reports:
            if not frappe.db.exists("Report", report["name"]):
                frappe.get_doc(report).insert()
                print(f"✅ Created Report: {report['name']}")
            else:
                print(f"⚠️  Report already exists: {report['name']}")
        
        frappe.db.commit()
        print("✅ Safari Integrations report fixtures installed successfully!")
        
    except Exception as e:
        print(f"❌ Error installing report fixtures: {str(e)}")
        frappe.db.rollback()

def setup_default_providers():
    """Setup default API providers during installation."""
    
    print("🚀 Setting up default API providers...")
    
    default_providers = [
        {
            "doctype": "API Provider",
            "provider_name": "Amadeus",
            "provider_type": "Flight",
            "base_url": "https://api.amadeus.com/v2",
            "auth_type": "OAuth",
            "rate_limit_per_minute": 100,
            "cost_per_request": 0.02,
            "documentation_url": "https://developers.amadeus.com",
            "description": "Flight and hotel booking API",
            "is_active": 1,
            "status": "Active"
        },
        {
            "doctype": "API Provider", 
            "provider_name": "VertoFx",
            "provider_type": "Payment",
            "base_url": "https://api.vertofx.com/v1",
            "auth_type": "API Key",
            "rate_limit_per_minute": 1000,
            "cost_per_request": 0.01,
            "documentation_url": "https://vertofx.com/api-docs",
            "description": "Foreign exchange and payment processing",
            "is_active": 1,
            "status": "Active"
        },
        {
            "doctype": "API Provider",
            "provider_name": "Google Places",
            "provider_type": "Mapping",
            "base_url": "https://maps.googleapis.com/maps/api",
            "auth_type": "API Key", 
            "rate_limit_per_minute": 1000,
            "cost_per_request": 0.005,
            "documentation_url": "https://developers.google.com/maps/documentation/places",
            "description": "Location and place information",
            "is_active": 1,
            "status": "Active"
        },
        {
            "doctype": "API Provider",
            "provider_name": "OpenRouteService", 
            "provider_type": "Mapping",
            "base_url": "https://api.openrouteservice.org",
            "auth_type": "API Key",
            "rate_limit_per_minute": 2000,
            "cost_per_request": 0.0,  # Free tier
            "documentation_url": "https://openrouteservice.org/dev",
            "description": "Route optimization and directions",
            "is_active": 1,
            "status": "Active"
        },
        {
            "doctype": "API Provider",
            "provider_name": "eCitizen",
            "provider_type": "Government", 
            "base_url": "https://api.ecitizen.go.ke/v1",
            "auth_type": "API Key",
            "rate_limit_per_minute": 60,
            "cost_per_request": 0.10,
            "documentation_url": "https://ecitizen.go.ke/api-docs",
            "description": "Kenya government services integration",
            "is_active": 1,
            "status": "Active"
        },
        {
            "doctype": "API Provider",
            "provider_name": "Chipper",
            "provider_type": "Payment",
            "base_url": "https://api.chipper.cash/v1",
            "auth_type": "API Key", 
            "rate_limit_per_minute": 500,
            "cost_per_request": 0.015,
            "documentation_url": "https://developer.chipper.cash",
            "description": "Mobile payment processing",
            "is_active": 1,
            "status": "Active"
        }
    ]
    
    created_count = 0
    for provider_data in default_providers:
        try:
            if not frappe.db.exists("API Provider", provider_data["provider_name"]):
                provider = frappe.get_doc(provider_data)
                provider.insert(ignore_permissions=True)
                created_count += 1
                print(f"✅ Created API Provider: {provider_data['provider_name']}")
            else:
                print(f"⚠️  API Provider already exists: {provider_data['provider_name']}")
        except Exception as e:
            print(f"❌ Error creating {provider_data['provider_name']}: {str(e)}")
            
    frappe.db.commit()
    
    if created_count > 0:
        print(f"🎉 Successfully created {created_count} API providers!")
    else:
        print("ℹ️  All API providers already exist.")
        
    # Create default integration settings
    create_integration_settings()

def create_integration_settings():
    """Create default integration settings"""
    try:
        if not frappe.db.exists("Integration Settings", "Integration Settings"):
            settings = frappe.get_doc({
                "doctype": "Integration Settings",
                "name": "Integration Settings",
                "enable_api_logging": 1,
                "enable_cost_tracking": 1,
                "enable_rate_limiting": 1,
                "default_monthly_quota": 1000,
                "alert_threshold_percentage": 80
            })
            settings.insert(ignore_permissions=True)
            print("✅ Created Integration Settings")
        else:
            print("⚠️  Integration Settings already exist")
            
    except Exception as e:
        print(f"❌ Error creating Integration Settings: {str(e)}")

def setup_default_roles():
    """Setup default roles for API management"""
    try:
        # Create API Manager role if it doesn't exist
        if not frappe.db.exists("Role", "API Manager"):
            role = frappe.get_doc({
                "doctype": "Role",
                "role_name": "API Manager",
                "desk_access": 1
            })
            role.insert(ignore_permissions=True)
            print("✅ Created API Manager role")
            
    except Exception as e:
        print(f"❌ Error creating roles: {str(e)}")

if __name__ == "__main__":
    setup_default_providers()
    setup_default_roles()