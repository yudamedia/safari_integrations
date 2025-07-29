import frappe

def create_accommodation_dashboard():
    """Create dashboard components for Accommodation Management"""
    
    print("🏨 Creating Accommodation Management Dashboard...")
    
    # Number Cards
    accommodation_cards = [
        {
            "name": "Total Accommodations",
            "label": "Total Accommodations",
            "document_type": "Accommodation",
            "function": "Count",
            "filters_json": "[]",
            "color": "#4463F0",
            "module": "Safari Accommodation"
        },
        {
            "name": "Active Bookings Today",
            "label": "Active Bookings Today", 
            "document_type": "Accommodation Booking",
            "function": "Count",
            "filters_json": "[[\"Accommodation Booking\",\"creation\",\">=\",\"Today\",false]]",
            "color": "#28a745",
            "module": "Safari Accommodation"
        },
        {
            "name": "Revenue This Month",
            "label": "Revenue This Month",
            "document_type": "Accommodation Booking",
            "function": "Sum",
            "aggregate_function_based_on": "total_amount",
            "filters_json": "[[\"Accommodation Booking\",\"creation\",\">=\",\"This Month\",false]]",
            "color": "#FF8C00",
            "module": "Safari Accommodation"
        },
        {
            "name": "Average Occupancy Rate",
            "label": "Average Occupancy Rate",
            "document_type": "Accommodation Booking",
            "function": "Average",
            "aggregate_function_based_on": "occupancy_rate",
            "filters_json": "[]",
            "color": "#6f42c1",
            "module": "Safari Accommodation"
        }
    ]
    
    # Dashboard Charts
    accommodation_charts = [
        {
            "name": "Booking Trends",
            "chart_name": "Booking Trends",
            "chart_type": "Count",
            "document_type": "Accommodation Booking",
            "based_on": "creation",
            "time_interval": "Daily",
            "timespan": "Last Month",
            "filters_json": "[]",
            "module": "Safari Accommodation"
        },
        {
            "name": "Revenue by Accommodation",
            "chart_name": "Revenue by Accommodation",
            "chart_type": "Group By",
            "document_type": "Accommodation Booking", 
            "based_on": "accommodation",
            "group_by_based_on": "accommodation",
            "value_based_on": "total_amount",
            "number_of_groups": 8,
            "time_interval": "Monthly",
            "timespan": "Last Month",
            "filters_json": "[]",
            "module": "Safari Accommodation"
        },
        {
            "name": "Occupancy by Property",
            "chart_name": "Occupancy by Property",
            "chart_type": "Group By",
            "document_type": "Accommodation Booking",
            "based_on": "accommodation",
            "group_by_based_on": "accommodation",
            "number_of_groups": 10,
            "time_interval": "Monthly",
            "timespan": "Last Month",
            "filters_json": "[]",
            "module": "Safari Accommodation"
        }
    ]
    
    create_dashboard_components("Safari Accommodation", accommodation_cards, accommodation_charts)

def create_parks_dashboard():
    """Create dashboard components for Parks Management"""
    
    print("🌲 Creating Parks Management Dashboard...")
    
    # Number Cards
    parks_cards = [
        {
            "name": "Total National Parks",
            "label": "Total National Parks",
            "document_type": "National Park",
            "function": "Count",
            "filters_json": "[]",
            "color": "#228B22",
            "module": "Safari Parks"
        },
        {
            "name": "Park Bookings Today",
            "label": "Park Bookings Today",
            "document_type": "Park Booking", 
            "function": "Count",
            "filters_json": "[[\"Park Booking\",\"creation\",\">=\",\"Today\",false]]",
            "color": "#32CD32",
            "module": "Safari Parks"
        },
        {
            "name": "Monthly Park Revenue",
            "label": "Monthly Park Revenue",
            "document_type": "Park Fee Calculation",
            "function": "Sum",
            "aggregate_function_based_on": "total_fee",
            "filters_json": "[[\"Park Fee Calculation\",\"creation\",\">=\",\"This Month\",false]]",
            "color": "#FF8C00",
            "module": "Safari Parks"
        },
        {
            "name": "Active Fee Structures",
            "label": "Active Fee Structures", 
            "document_type": "Park Fee Structure",
            "function": "Count",
            "filters_json": "[[\"Park Fee Structure\",\"is_active\",\"=\",1,false]]",
            "color": "#20B2AA",
            "module": "Safari Parks"
        }
    ]
    
    # Dashboard Charts
    parks_charts = [
        {
            "name": "Park Visits Trend",
            "chart_name": "Park Visits Trend",
            "chart_type": "Count",
            "document_type": "Park Booking",
            "based_on": "creation",
            "time_interval": "Daily",
            "timespan": "Last Month",
            "filters_json": "[]",
            "module": "Safari Parks"
        },
        {
            "name": "Revenue by Park",
            "chart_name": "Revenue by Park",
            "chart_type": "Group By",
            "document_type": "Park Fee Calculation",
            "based_on": "national_park",
            "group_by_based_on": "national_park", 
            "value_based_on": "total_fee",
            "number_of_groups": 8,
            "time_interval": "Monthly",
            "timespan": "Last Month",
            "filters_json": "[]",
            "module": "Safari Parks"
        },
        {
            "name": "Fee Types Distribution",
            "chart_name": "Fee Types Distribution",
            "chart_type": "Group By",
            "document_type": "Park Fee Calculation",
            "based_on": "fee_type",
            "group_by_based_on": "fee_type",
            "number_of_groups": 6,
            "time_interval": "Monthly",
            "timespan": "Last Month",
            "filters_json": "[]",
            "module": "Safari Parks"
        }
    ]
    
    create_dashboard_components("Safari Parks", parks_cards, parks_charts)

def create_transport_dashboard():
    """Create dashboard components for Transport Management"""
    
    print("🚗 Creating Transport Management Dashboard...")
    
    # Number Cards
    transport_cards = [
        {
            "name": "Total Vehicles",
            "label": "Total Vehicles",
            "document_type": "Safari Vehicle",
            "function": "Count",
            "filters_json": "[]",
            "color": "#4169E1",
            "module": "Safari Transport"
        },
        {
            "name": "Transport Bookings Today",
            "label": "Transport Bookings Today",
            "document_type": "Transport Booking",
            "function": "Count",
            "filters_json": "[[\"Transport Booking\",\"creation\",\">=\",\"Today\",false]]",
            "color": "#32CD32",
            "module": "Safari Transport"
        },
        {
            "name": "Vehicles Under Maintenance",
            "label": "Vehicles Under Maintenance",
            "document_type": "Vehicle Maintenance",
            "function": "Count", 
            "filters_json": "[[\"Vehicle Maintenance\",\"status\",\"in\",[\"In Progress\",\"Scheduled\"],false]]",
            "color": "#FF6B6B",
            "module": "Safari Transport"
        },
        {
            "name": "Flight Bookings This Month",
            "label": "Flight Bookings This Month",
            "document_type": "Flight Booking",
            "function": "Count",
            "filters_json": "[[\"Flight Booking\",\"creation\",\">=\",\"This Month\",false]]",
            "color": "#87CEEB",
            "module": "Safari Transport"
        }
    ]
    
    # Dashboard Charts
    transport_charts = [
        {
            "name": "Transport Bookings Trend",
            "chart_name": "Transport Bookings Trend",
            "chart_type": "Count",
            "document_type": "Transport Booking",
            "based_on": "creation",
            "time_interval": "Daily",
            "timespan": "Last Month",
            "filters_json": "[]",
            "module": "Safari Transport"
        },
        {
            "name": "Vehicle Utilization",
            "chart_name": "Vehicle Utilization", 
            "chart_type": "Group By",
            "document_type": "Vehicle Assignment",
            "based_on": "vehicle",
            "group_by_based_on": "vehicle",
            "number_of_groups": 10,
            "time_interval": "Monthly",
            "timespan": "Last Month",
            "filters_json": "[]",
            "module": "Safari Transport"
        },
        {
            "name": "Maintenance Schedule",
            "chart_name": "Maintenance Schedule",
            "chart_type": "Count",
            "document_type": "Vehicle Maintenance",
            "based_on": "scheduled_date",
            "time_interval": "Weekly",
            "timespan": "Last Month",
            "filters_json": "[]",
            "module": "Safari Transport"
        }
    ]
    
    create_dashboard_components("Safari Transport", transport_cards, transport_charts)

def create_packages_dashboard():
    """Create dashboard components for Safari Packages"""
    
    print("📦 Creating Safari Packages Dashboard...")
    
    # Number Cards
    packages_cards = [
        {
            "name": "Total Safari Packages",
            "label": "Total Safari Packages",
            "document_type": "Safari Package",
            "function": "Count",
            "filters_json": "[]",
            "color": "#8B4513",
            "module": "Safari Packages"
        },
        {
            "name": "Quotes Generated Today",
            "label": "Quotes Generated Today", 
            "document_type": "Safari Quote Generator",
            "function": "Count",
            "filters_json": "[[\"Safari Quote Generator\",\"creation\",\">=\",\"Today\",false]]",
            "color": "#DAA520",
            "module": "Safari Packages"
        },
        {
            "name": "Average Package Duration",
            "label": "Average Package Duration",
            "document_type": "Safari Package",
            "function": "Average",
            "aggregate_function_based_on": "duration_days",
            "filters_json": "[]",
            "color": "#CD853F",
            "module": "Safari Packages"
        },
        {
            "name": "Popular Destinations",
            "label": "Popular Destinations",
            "document_type": "Package Operating Country",
            "function": "Count",
            "filters_json": "[]",
            "color": "#DEB887",
            "module": "Safari Packages"
        }
    ]
    
    # Dashboard Charts
    packages_charts = [
        {
            "name": "Package Creation Trend",
            "chart_name": "Package Creation Trend",
            "chart_type": "Count",
            "document_type": "Safari Package",
            "based_on": "creation",
            "time_interval": "Monthly",
            "timespan": "Last Year",
            "filters_json": "[]",
            "module": "Safari Packages"
        },
        {
            "name": "Quote Generation Activity",
            "chart_name": "Quote Generation Activity",
            "chart_type": "Count", 
            "document_type": "Safari Quote Generator",
            "based_on": "creation",
            "time_interval": "Daily",
            "timespan": "Last Month",
            "filters_json": "[]",
            "module": "Safari Packages"
        },
        {
            "name": "Popular Package Types",
            "chart_name": "Popular Package Types",
            "chart_type": "Group By",
            "document_type": "Safari Package",
            "based_on": "package_type",
            "group_by_based_on": "package_type",
            "number_of_groups": 8,
            "time_interval": "Monthly",
            "timespan": "Last Month",
            "filters_json": "[]",
            "module": "Safari Packages"
        }
    ]
    
    create_dashboard_components("Safari Packages", packages_cards, packages_charts)

def create_safari_core_dashboard():
    """Create dashboard components for Safari Dashboard (Core)"""
    
    print("🦁 Creating Safari Dashboard (Core)...")
    
    # Number Cards
    core_cards = [
        {
            "name": "Total Safari Companies",
            "label": "Total Safari Companies",
            "document_type": "Safari Company",
            "function": "Count",
            "filters_json": "[]",
            "color": "#B8860B",
            "module": "Safari Core"
        },
        {
            "name": "Total Safari Guests",
            "label": "Total Safari Guests",
            "document_type": "Safari Guest",
            "function": "Count", 
            "filters_json": "[]",
            "color": "#CD853F",
            "module": "Safari Core"
        },
        {
            "name": "Active Booking Parties",
            "label": "Active Booking Parties",
            "document_type": "Booking Party",
            "function": "Count",
            "filters_json": "[[\"Booking Party\",\"status\",\"=\",\"Active\",false]]",
            "color": "#DEB887",
            "module": "Safari Core"
        },
        {
            "name": "Seasonal Configurations",
            "label": "Seasonal Configurations",
            "document_type": "Season",
            "function": "Count",
            "filters_json": "[]",
            "color": "#F4A460",
            "module": "Safari Core"
        }
    ]
    
    # Dashboard Charts
    core_charts = [
        {
            "name": "Guest Registration Trend",
            "chart_name": "Guest Registration Trend",
            "chart_type": "Count",
            "document_type": "Safari Guest",
            "based_on": "creation",
            "time_interval": "Monthly",
            "timespan": "Last Year",
            "filters_json": "[]",
            "module": "Safari Core"
        },
        {
            "name": "Booking Parties by Size",
            "chart_name": "Booking Parties by Size",
            "chart_type": "Group By",
            "document_type": "Booking Party",
            "based_on": "party_size",
            "group_by_based_on": "party_size",
            "number_of_groups": 8,
            "time_interval": "Monthly",
            "timespan": "Last Month",
            "filters_json": "[]",
            "module": "Safari Core"
        },
        {
            "name": "Companies by Country",
            "chart_name": "Companies by Country",
            "chart_type": "Group By",
            "document_type": "Safari Company",
            "based_on": "country",
            "group_by_based_on": "country",
            "number_of_groups": 10,
            "time_interval": "Monthly",
            "timespan": "Last Month",
            "filters_json": "[]",
            "module": "Safari Core"
        }
    ]
    
    create_dashboard_components("Safari Core", core_cards, core_charts)

def create_dashboard_components(module_name, cards, charts):
    """Helper function to create number cards and dashboard charts"""
    
    # Create Number Cards
    for card_data in cards:
        full_card = {
            "doctype": "Number Card",
            "is_public": 1,
            "is_standard": 1,
            "stats_time_interval": "Daily",
            **card_data
        }
        
        try:
            if not frappe.db.exists("Number Card", card_data["name"]):
                doc = frappe.get_doc(full_card)
                doc.insert()
                print(f"   ✅ Created Number Card: {card_data['name']}")
            else:
                print(f"   ⚠️  Number Card exists: {card_data['name']}")
        except Exception as e:
            print(f"   ❌ Error creating Number Card {card_data['name']}: {str(e)}")
    
    # Create Dashboard Charts
    for chart_data in charts:
        full_chart = {
            "doctype": "Dashboard Chart",
            "is_public": 1,
            "is_standard": 1,
            **chart_data
        }
        
        try:
            if not frappe.db.exists("Dashboard Chart", chart_data["name"]):
                doc = frappe.get_doc(full_chart)
                doc.insert()
                print(f"   ✅ Created Dashboard Chart: {chart_data['name']}")
            else:
                print(f"   ⚠️  Dashboard Chart exists: {chart_data['name']}")
        except Exception as e:
            print(f"   ❌ Error creating Dashboard Chart {chart_data['name']}: {str(e)}")

def create_all_safari_dashboards():
    """Create dashboard components for all Safari workspaces"""
    
    print("🚀 Creating Dashboard Components for All Safari Workspaces...")
    print("=" * 70)
    
    try:
        create_accommodation_dashboard()
        create_parks_dashboard()
        create_transport_dashboard()
        create_packages_dashboard()
        create_safari_core_dashboard()
        
        frappe.db.commit()
        print("\n🎉 All Safari dashboard components created successfully!")
        
    except Exception as e:
        print(f"\n❌ Error creating dashboards: {str(e)}")
        frappe.db.rollback()

if __name__ == "__main__":
    create_all_safari_dashboards()