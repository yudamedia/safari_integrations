import frappe

def verify_all_safari_dashboards():
    """Verify all Safari dashboard components across all workspaces"""
    
    print("🔍 Verifying All Safari Dashboard Components...")
    print("=" * 70)
    
    # Define expected components for each workspace
    workspaces_config = {
        "Accommodation Management": {
            "module": "Safari Accommodation",
            "number_cards": [
                "Total Accommodations",
                "Active Bookings Today", 
                "Revenue This Month",
                "Average Occupancy Rate"
            ],
            "charts": [
                "Booking Trends",
                "Revenue by Accommodation",
                "Occupancy by Property"
            ]
        },
        "Parks Management": {
            "module": "Safari Parks",
            "number_cards": [
                "Total National Parks",
                "Park Bookings Today"
            ],
            "charts": [
                "Park Visits Trend"
            ]
        },
        "Transport Management": {
            "module": "Safari Transport",
            "number_cards": [
                "Total Vehicles",
                "Transport Bookings Today",
                "Vehicles Under Maintenance",
                "Flight Bookings This Month"
            ],
            "charts": [
                "Transport Bookings Trend",
                "Vehicle Utilization",
                "Maintenance Schedule"
            ]
        },
        "Safari Packages": {
            "module": "Safari Packages",
            "number_cards": [
                "Total Safari Packages",
                "Quotes Generated Today",
                "Average Package Duration"
            ],
            "charts": [
                "Package Creation Trend",
                "Quote Generation Activity",
                "Popular Package Types"
            ]
        },
        "Safari Dashboard": {
            "module": "Safari Core",
            "number_cards": [
                "Total Safari Companies",
                "Total Safari Guests",
                "Active Booking Parties",
                "Seasonal Configurations"
            ],
            "charts": [
                "Guest Registration Trend",
                "Booking Parties by Size",
                "Companies by Country"
            ]
        },
        "Integrations Management": {
            "module": "Safari Integrations",
            "number_cards": [
                "Active API Providers",
                "Total API Calls Today",
                "Monthly API Costs",
                "Companies with Access"
            ],
            "charts": [
                "API Usage Trends",
                "Cost by Provider",
                "Monthly Quota Usage"
            ]
        }
    }
    
    total_expected_cards = 0
    total_expected_charts = 0
    total_found_cards = 0
    total_found_charts = 0
    total_workspace_issues = 0
    
    for workspace_name, config in workspaces_config.items():
        print(f"\n{get_workspace_icon(workspace_name)} {workspace_name}:")
        print("-" * 50)
        
        # Check if workspace exists
        workspace_exists = frappe.db.exists("Workspace", workspace_name)
        if not workspace_exists:
            print(f"   ❌ Workspace not found!")
            total_workspace_issues += 1
            continue
            
        print(f"   ✅ Workspace exists")
        
        # Check Number Cards
        print(f"\n   📊 Number Cards ({len(config['number_cards'])} expected):")
        found_cards = 0
        for card_name in config['number_cards']:
            exists = frappe.db.exists("Number Card", card_name)
            status = "✅" if exists else "❌"
            print(f"      {status} {card_name}")
            if exists:
                found_cards += 1
                
        # Check Dashboard Charts
        print(f"\n   📈 Dashboard Charts ({len(config['charts'])} expected):")
        found_charts = 0
        for chart_name in config['charts']:
            exists = frappe.db.exists("Dashboard Chart", chart_name)
            status = "✅" if exists else "❌"
            print(f"      {status} {chart_name}")
            if exists:
                found_charts += 1
                
        # Check Workspace Configuration
        try:
            workspace = frappe.get_doc("Workspace", workspace_name)
            workspace_cards_count = len(workspace.number_cards)
            workspace_charts_count = len(workspace.charts)
            
            print(f"\n   ⚙️  Workspace Configuration:")
            print(f"      Number Cards in workspace: {workspace_cards_count}")
            print(f"      Charts in workspace: {workspace_charts_count}")
            
        except Exception as e:
            print(f"   ❌ Error accessing workspace: {str(e)}")
            total_workspace_issues += 1
            
        # Update totals
        total_expected_cards += len(config['number_cards'])
        total_expected_charts += len(config['charts'])
        total_found_cards += found_cards
        total_found_charts += found_charts
        
        # Summary for this workspace
        cards_percentage = (found_cards / len(config['number_cards'])) * 100 if config['number_cards'] else 100
        charts_percentage = (found_charts / len(config['charts'])) * 100 if config['charts'] else 100
        
        print(f"\n   🎯 Summary:")
        print(f"      Cards: {found_cards}/{len(config['number_cards'])} ({cards_percentage:.0f}%)")
        print(f"      Charts: {found_charts}/{len(config['charts'])} ({charts_percentage:.0f}%)")
        
        if cards_percentage == 100 and charts_percentage == 100:
            print(f"      Status: 🎉 Complete!")
        else:
            print(f"      Status: ⚠️  Incomplete")
    
    # Overall Summary
    print(f"\n🎯 OVERALL SUMMARY:")
    print("=" * 70)
    
    cards_percentage = (total_found_cards / total_expected_cards) * 100 if total_expected_cards > 0 else 0
    charts_percentage = (total_found_charts / total_expected_charts) * 100 if total_expected_charts > 0 else 0
    
    print(f"📊 Number Cards: {total_found_cards}/{total_expected_cards} ({cards_percentage:.1f}%)")
    print(f"📈 Dashboard Charts: {total_found_charts}/{total_expected_charts} ({charts_percentage:.1f}%)")
    print(f"⚙️  Workspaces: {len(workspaces_config) - total_workspace_issues}/{len(workspaces_config)}")
    
    # Status determination
    if cards_percentage >= 90 and charts_percentage >= 90 and total_workspace_issues == 0:
        print(f"\n🎉 EXCELLENT! All Safari dashboards are successfully deployed!")
        return True
    elif cards_percentage >= 75 and charts_percentage >= 75:
        print(f"\n✅ GOOD! Most dashboard components are working.")
        if total_workspace_issues > 0:
            print(f"⚠️  {total_workspace_issues} workspace(s) need attention.")
        return True
    else:
        print(f"\n⚠️  NEEDS ATTENTION! Some dashboard components are missing.")
        return False

def get_workspace_icon(workspace_name):
    """Get appropriate icon for workspace"""
    icons = {
        "Accommodation Management": "🏨",
        "Parks Management": "🌲", 
        "Transport Management": "🚗",
        "Safari Packages": "📦",
        "Safari Dashboard": "🦁",
        "Integrations Management": "🔗"
    }
    return icons.get(workspace_name, "📋")

def generate_dashboard_report():
    """Generate a comprehensive dashboard report"""
    
    print("\n📋 Generating Dashboard Deployment Report...")
    print("=" * 70)
    
    # Get all dashboard components
    all_cards = frappe.get_all("Number Card", 
        filters={"module": ["in", ["Safari Accommodation", "Safari Parks", "Safari Transport", "Safari Packages", "Safari Core", "Safari Integrations"]]},
        fields=["name", "module", "document_type"]
    )
    
    all_charts = frappe.get_all("Dashboard Chart",
        filters={"module": ["in", ["Safari Accommodation", "Safari Parks", "Safari Transport", "Safari Packages", "Safari Core", "Safari Integrations"]]}, 
        fields=["name", "module", "document_type", "chart_type"]
    )
    
    # Group by module
    cards_by_module = {}
    charts_by_module = {}
    
    for card in all_cards:
        module = card.module
        if module not in cards_by_module:
            cards_by_module[module] = []
        cards_by_module[module].append(card)
        
    for chart in all_charts:
        module = chart.module
        if module not in charts_by_module:
            charts_by_module[module] = []
        charts_by_module[module].append(chart)
    
    # Print detailed report
    print("\n📊 Component Details by Module:")
    print("-" * 50)
    
    for module in ["Safari Accommodation", "Safari Parks", "Safari Transport", "Safari Packages", "Safari Core", "Safari Integrations"]:
        print(f"\n{module}:")
        
        module_cards = cards_by_module.get(module, [])
        module_charts = charts_by_module.get(module, [])
        
        if module_cards:
            print(f"   Number Cards ({len(module_cards)}):")
            for card in module_cards:
                print(f"      • {card.name} ({card.document_type})")
                
        if module_charts:
            print(f"   Dashboard Charts ({len(module_charts)}):")
            for chart in module_charts:
                print(f"      • {chart.name} ({chart.chart_type}, {chart.document_type})")
                
        if not module_cards and not module_charts:
            print(f"   No components found")
    
    print(f"\n🎯 DEPLOYMENT STATISTICS:")
    print("-" * 30)
    print(f"Total Number Cards: {len(all_cards)}")
    print(f"Total Dashboard Charts: {len(all_charts)}")
    print(f"Modules Covered: {len(set(card.module for card in all_cards + all_charts))}")
    
    return len(all_cards), len(all_charts)

if __name__ == "__main__":
    success = verify_all_safari_dashboards()
    generate_dashboard_report()
    
    if success:
        print(f"\n🚀 All Safari dashboards are ready for use!")
    else:
        print(f"\n🔧 Some dashboard components may need attention.")