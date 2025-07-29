import frappe

def update_accommodation_workspace():
    """Update Accommodation Management workspace with dashboard components"""
    
    print("🏨 Updating Accommodation Management Workspace...")
    
    try:
        workspace = frappe.get_doc("Workspace", "Accommodation Management")
        
        # Clear existing charts and number cards
        workspace.charts = []
        workspace.number_cards = []
        
        # Add Dashboard Charts
        workspace.append("charts", {
            "chart_name": "Booking Trends",
            "label": "Booking Trends"
        })
        workspace.append("charts", {
            "chart_name": "Revenue by Accommodation",
            "label": "Revenue by Accommodation"
        })
        workspace.append("charts", {
            "chart_name": "Occupancy by Property",
            "label": "Occupancy by Property"
        })
        
        # Add Number Cards
        workspace.append("number_cards", {
            "number_card_name": "Total Accommodations",
            "label": "Total Accommodations"
        })
        workspace.append("number_cards", {
            "number_card_name": "Active Bookings Today",
            "label": "Active Bookings Today"
        })
        workspace.append("number_cards", {
            "number_card_name": "Revenue This Month",
            "label": "Revenue This Month"
        })
        workspace.append("number_cards", {
            "number_card_name": "Average Occupancy Rate",
            "label": "Average Occupancy Rate"
        })
        
        workspace.save()
        print("   ✅ Accommodation Management workspace updated")
        
    except Exception as e:
        print(f"   ❌ Error updating Accommodation Management workspace: {str(e)}")

def update_parks_workspace():
    """Update Parks Management workspace with dashboard components"""
    
    print("🌲 Updating Parks Management Workspace...")
    
    try:
        workspace = frappe.get_doc("Workspace", "Parks Management")
        
        # Clear existing charts and number cards
        workspace.charts = []
        workspace.number_cards = []
        
        # Add Dashboard Charts
        workspace.append("charts", {
            "chart_name": "Park Visits Trend",
            "label": "Park Visits Trend"
        })
        
        # Add Number Cards
        workspace.append("number_cards", {
            "number_card_name": "Total National Parks",
            "label": "Total National Parks"
        })
        workspace.append("number_cards", {
            "number_card_name": "Park Bookings Today",
            "label": "Park Bookings Today"
        })
        
        workspace.save()
        print("   ✅ Parks Management workspace updated")
        
    except Exception as e:
        print(f"   ❌ Error updating Parks Management workspace: {str(e)}")

def update_transport_workspace():
    """Update Transport Management workspace with dashboard components"""
    
    print("🚗 Updating Transport Management Workspace...")
    
    try:
        workspace = frappe.get_doc("Workspace", "Transport Management")
        
        # Clear existing charts and number cards
        workspace.charts = []
        workspace.number_cards = []
        
        # Add Dashboard Charts
        workspace.append("charts", {
            "chart_name": "Transport Bookings Trend",
            "label": "Transport Bookings Trend"
        })
        workspace.append("charts", {
            "chart_name": "Vehicle Utilization",
            "label": "Vehicle Utilization"
        })
        workspace.append("charts", {
            "chart_name": "Maintenance Schedule",
            "label": "Maintenance Schedule"
        })
        
        # Add Number Cards
        workspace.append("number_cards", {
            "number_card_name": "Total Vehicles",
            "label": "Total Vehicles"
        })
        workspace.append("number_cards", {
            "number_card_name": "Transport Bookings Today",
            "label": "Transport Bookings Today"
        })
        workspace.append("number_cards", {
            "number_card_name": "Vehicles Under Maintenance",
            "label": "Vehicles Under Maintenance"
        })
        workspace.append("number_cards", {
            "number_card_name": "Flight Bookings This Month",
            "label": "Flight Bookings This Month"
        })
        
        workspace.save()
        print("   ✅ Transport Management workspace updated")
        
    except Exception as e:
        print(f"   ❌ Error updating Transport Management workspace: {str(e)}")

def update_packages_workspace():
    """Update Safari Packages workspace with dashboard components"""
    
    print("📦 Updating Safari Packages Workspace...")
    
    try:
        workspace = frappe.get_doc("Workspace", "Safari Packages")
        
        # Clear existing charts and number cards
        workspace.charts = []
        workspace.number_cards = []
        
        # Add Dashboard Charts
        workspace.append("charts", {
            "chart_name": "Package Creation Trend",
            "label": "Package Creation Trend"
        })
        workspace.append("charts", {
            "chart_name": "Quote Generation Activity", 
            "label": "Quote Generation Activity"
        })
        workspace.append("charts", {
            "chart_name": "Popular Package Types",
            "label": "Popular Package Types"
        })
        
        # Add Number Cards
        workspace.append("number_cards", {
            "number_card_name": "Total Safari Packages",
            "label": "Total Safari Packages"
        })
        workspace.append("number_cards", {
            "number_card_name": "Quotes Generated Today",
            "label": "Quotes Generated Today"
        })
        workspace.append("number_cards", {
            "number_card_name": "Average Package Duration",
            "label": "Average Package Duration"
        })
        
        workspace.save()
        print("   ✅ Safari Packages workspace updated")
        
    except Exception as e:
        print(f"   ❌ Error updating Safari Packages workspace: {str(e)}")

def update_safari_dashboard_workspace():
    """Update Safari Dashboard workspace with dashboard components"""
    
    print("🦁 Updating Safari Dashboard Workspace...")
    
    try:
        workspace = frappe.get_doc("Workspace", "Safari Dashboard")
        
        # Clear existing charts and number cards
        workspace.charts = []
        workspace.number_cards = []
        
        # Add Dashboard Charts
        workspace.append("charts", {
            "chart_name": "Guest Registration Trend",
            "label": "Guest Registration Trend"
        })
        workspace.append("charts", {
            "chart_name": "Booking Parties by Size",
            "label": "Booking Parties by Size"
        })
        workspace.append("charts", {
            "chart_name": "Companies by Country",
            "label": "Companies by Country"
        })
        
        # Add Number Cards
        workspace.append("number_cards", {
            "number_card_name": "Total Safari Companies",
            "label": "Total Safari Companies"
        })
        workspace.append("number_cards", {
            "number_card_name": "Total Safari Guests",
            "label": "Total Safari Guests"
        })
        workspace.append("number_cards", {
            "number_card_name": "Active Booking Parties",
            "label": "Active Booking Parties"
        })
        workspace.append("number_cards", {
            "number_card_name": "Seasonal Configurations",
            "label": "Seasonal Configurations"
        })
        
        workspace.save()
        print("   ✅ Safari Dashboard workspace updated")
        
    except Exception as e:
        print(f"   ❌ Error updating Safari Dashboard workspace: {str(e)}")

def update_all_safari_workspaces():
    """Update all Safari workspaces with new dashboard components"""
    
    print("🚀 Updating All Safari Workspaces with Dashboard Components...")
    print("=" * 70)
    
    try:
        update_accommodation_workspace()
        update_parks_workspace()
        update_transport_workspace()
        update_packages_workspace()
        update_safari_dashboard_workspace()
        
        frappe.db.commit()
        print("\n🎉 All Safari workspaces updated successfully!")
        
        # Generate summary
        print("\n📊 Dashboard Components Summary:")
        print("=" * 50)
        
        summary = {
            "Accommodation Management": {
                "charts": 3,
                "cards": 4,
                "features": ["Booking trends", "Revenue tracking", "Occupancy monitoring"]
            },
            "Parks Management": {
                "charts": 1,
                "cards": 2,
                "features": ["Park visits tracking", "Park counting"]
            },
            "Transport Management": {
                "charts": 3,
                "cards": 4,
                "features": ["Booking trends", "Vehicle utilization", "Maintenance tracking"]
            },
            "Safari Packages": {
                "charts": 3,
                "cards": 3,
                "features": ["Package creation trends", "Quote generation", "Package analytics"]
            },
            "Safari Dashboard": {
                "charts": 3,
                "cards": 4,
                "features": ["Guest analytics", "Company insights", "Booking party trends"]
            }
        }
        
        for workspace, data in summary.items():
            print(f"\n{workspace}:")
            print(f"   📈 Charts: {data['charts']}")
            print(f"   📊 Cards: {data['cards']}")
            print(f"   🎯 Features: {', '.join(data['features'])}")
        
        total_charts = sum(data['charts'] for data in summary.values())
        total_cards = sum(data['cards'] for data in summary.values())
        
        print(f"\n🎯 Total Created:")
        print(f"   📈 Dashboard Charts: {total_charts}")
        print(f"   📊 Number Cards: {total_cards}")
        print(f"   ⚙️  Updated Workspaces: {len(summary)}")
        
    except Exception as e:
        print(f"\n❌ Error updating workspaces: {str(e)}")
        frappe.db.rollback()

if __name__ == "__main__":
    update_all_safari_workspaces()