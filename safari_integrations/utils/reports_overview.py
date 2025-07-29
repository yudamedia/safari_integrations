import frappe

def generate_safari_reports_overview():
    """Generate comprehensive overview of all Safari reports"""
    
    print("📊 SAFARI ERP REPORTS OVERVIEW")
    print("=" * 70)
    
    # Get all Safari-specific reports
    safari_reports = frappe.get_all("Report", 
        filters={"module": ["like", "%Safari%"]},
        fields=["name", "report_name", "report_type", "module", "is_standard"]
    )
    
    # Get all ERPNext standard reports that could be useful for Safari
    standard_reports = frappe.get_all("Report",
        filters={"is_standard": "Yes"},
        fields=["name", "report_name", "report_type", "module", "is_standard"]
    )
    
    print(f"\n🎯 SAFARI-SPECIFIC REPORTS ({len(safari_reports)} reports)")
    print("-" * 50)
    
    # Group Safari reports by module
    safari_by_module = {}
    for report in safari_reports:
        module = report.module
        if module not in safari_by_module:
            safari_by_module[module] = []
        safari_by_module[module].append(report)
    
    for module, reports in safari_by_module.items():
        print(f"\n📋 {module} ({len(reports)} reports):")
        for report in reports:
            report_type_icon = "🔍" if report.report_type == "Script Report" else "📊"
            print(f"   {report_type_icon} {report.report_name}")
            print(f"      Type: {report.report_type}")
    
    # Analyze useful standard reports by category
    useful_categories = {
        "📈 Financial Reports": [
            "Accounts", "Payroll"
        ],
        "👥 Human Resources": [
            "HR"
        ],
        "📦 Inventory & Purchasing": [
            "Stock", "Buying"
        ],
        "💰 Sales & Customer Management": [
            "Selling", "CRM"
        ],
        "🏗️ Operations & Projects": [
            "Projects", "Manufacturing"
        ],
        "⚙️ System & Administration": [
            "Core", "Custom"
        ]
    }
    
    print(f"\n🔧 RELEVANT ERPNEXT REPORTS FOR SAFARI")
    print("-" * 50)
    
    for category, modules in useful_categories.items():
        category_reports = [r for r in standard_reports if r.module in modules]
        if category_reports:
            print(f"\n{category} ({len(category_reports)} reports):")
            
            # Show top 5 most relevant reports for each category
            key_reports = {
                "Accounts": ["General Ledger", "Trial Balance", "Profit and Loss Statement", "Balance Sheet", "Cash Flow"],
                "Payroll": ["Salary Register", "Income Tax Computation", "Bank Remittance"],
                "HR": ["Employee Analytics", "Monthly Attendance Sheet", "Employee Leave Balance", "Employee Information"],
                "Stock": ["Stock Balance", "Stock Analytics", "Item Price Stock", "Stock Ageing"],
                "Buying": ["Purchase Analytics", "Purchase Order Analysis", "Procurement Tracker"],
                "Selling": ["Sales Analytics", "Customer Acquisition and Loyalty", "Sales Order Analysis"],
                "CRM": ["Sales Pipeline Analytics", "Lead Details", "Opportunity Summary by Sales Stage"],
                "Projects": ["Project Summary", "Project Billing Summary", "Daily Timesheet Summary"],
                "Core": ["Database Storage Usage By Tables", "Permitted Documents For User"]
            }
            
            for module in modules:
                module_reports = [r for r in category_reports if r.module == module]
                if module_reports:
                    relevant_reports = [r for r in module_reports if r.report_name in key_reports.get(module, [])]
                    if relevant_reports:
                        print(f"   📊 {module}:")
                        for report in relevant_reports[:5]:  # Show top 5
                            print(f"      • {report.report_name}")
    
    # Create summary
    print(f"\n🎯 REPORTS SUMMARY")
    print("-" * 30)
    print(f"Safari-Specific Reports: {len(safari_reports)}")
    print(f"Total Available Reports: {len(standard_reports)}")
    print(f"Safari Modules with Reports: {len(safari_by_module)}")
    
    # Suggest missing reports
    suggest_missing_reports()
    
    return safari_reports, standard_reports

def suggest_missing_reports():
    """Suggest missing reports that would be valuable for Safari"""
    
    print(f"\n💡 SUGGESTED REPORTS TO CREATE")
    print("-" * 40)
    
    missing_reports = {
        "🏨 Accommodation Management": [
            "Accommodation Revenue Report",
            "Occupancy Rate Analysis", 
            "Guest Demographics Report",
            "Property Performance Comparison",
            "Seasonal Booking Trends",
            "Average Daily Rate (ADR) Analysis"
        ],
        "🌲 Parks Management": [
            "Park Revenue Summary",
            "Visitor Statistics Report",
            "Park Fee Collection Analysis",
            "Conservation Impact Report",
            "Peak Season Analysis",
            "Park Capacity Utilization"
        ],
        "🚗 Transport Management": [
            "Fleet Efficiency Report",
            "Fuel Consumption Analysis",
            "Driver Performance Report",
            "Maintenance Cost Analysis",
            "Route Optimization Report",
            "Vehicle Downtime Analysis"
        ],
        "📦 Safari Packages": [
            "Package Profitability Report",
            "Quote Conversion Analysis",
            "Popular Destinations Report",
            "Seasonal Package Trends",
            "Customer Preference Analysis",
            "Package Duration Analysis"
        ],
        "🦁 Safari Core": [
            "Guest Satisfaction Report",
            "Booking Party Analytics",
            "Safari Company Performance",
            "Guest Retention Analysis",
            "Seasonal Guest Trends",
            "Country-wise Guest Distribution"
        ],
        "🔗 Integrations Management": [
            "API Performance Report",
            "Cost Optimization Analysis",
            "Provider Reliability Report",
            "Usage Trend Analysis",
            "Error Rate Report",
            "SLA Compliance Report"
        ]
    }
    
    for category, reports in missing_reports.items():
        print(f"\n{category}:")
        for report in reports:
            print(f"   📋 {report}")
    
    print(f"\n🚀 IMPLEMENTATION RECOMMENDATION:")
    print("   1. Start with Revenue and Analytics reports")
    print("   2. Add operational efficiency reports")
    print("   3. Create customer/guest experience reports")
    print("   4. Implement compliance and regulatory reports")

def check_report_permissions():
    """Check report access permissions for Safari users"""
    
    print(f"\n🔐 REPORT PERMISSIONS OVERVIEW")
    print("-" * 40)
    
    # Get Safari-related roles
    safari_roles = frappe.get_all("Role", 
        filters={"name": ["like", "%Safari%"]},
        fields=["name"]
    )
    
    if safari_roles:
        print(f"\nSafari-specific Roles:")
        for role in safari_roles:
            print(f"   👤 {role.name}")
    else:
        print("\n⚠️  No Safari-specific roles found")
        print("   Recommendation: Create roles like 'Safari Manager', 'Safari User', 'Safari Admin'")
    
    # Check standard roles that might be relevant
    relevant_roles = ["System Manager", "Accounts Manager", "HR Manager", "Stock Manager", "Sales Manager"]
    print(f"\nRelevant Standard Roles for Safari:")
    for role in relevant_roles:
        if frappe.db.exists("Role", role):
            print(f"   ✅ {role}")
        else:
            print(f"   ❌ {role} (not found)")

if __name__ == "__main__":
    safari_reports, all_reports = generate_safari_reports_overview()
    check_report_permissions()
    
    print(f"\n🎉 Reports overview completed!")
    print(f"   Safari has access to {len(all_reports)} total reports")
    print(f"   {len(safari_reports)} are Safari-specific")
    print(f"   Ready for advanced business intelligence!")