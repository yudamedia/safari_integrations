import frappe

def create_dashboard_charts():
    """Create dashboard charts for Safari Integrations"""
    
    print("Creating Safari Integrations Dashboard Charts...")
    
    # 1. API Usage Trends Chart
    if not frappe.db.exists("Dashboard Chart", "API Usage Trends"):
        chart = frappe.get_doc({
            "doctype": "Dashboard Chart",
            "name": "API Usage Trends",
            "chart_name": "API Usage Trends",
            "module": "Safari Integrations",
            "chart_type": "Count",
            "document_type": "API Usage Log",
            "based_on": "creation",
            "time_interval": "Daily",
            "timespan": "Last Month",
            "filters_json": "[]",
            "is_public": 1,
            "is_standard": 1
        })
        chart.insert()
        print("✅ Created API Usage Trends Chart")
    
    # 2. Cost by Provider Chart
    if not frappe.db.exists("Dashboard Chart", "Cost by Provider"):
        chart = frappe.get_doc({
            "doctype": "Dashboard Chart", 
            "name": "Cost by Provider",
            "chart_name": "Cost by Provider",
            "module": "Safari Integrations",
            "chart_type": "Group By",
            "document_type": "API Usage Log",
            "based_on": "api_provider",
            "value_based_on": "cost_incurred",
            "group_by_based_on": "api_provider",
            "number_of_groups": 6,
            "time_interval": "Daily",
            "timespan": "Last Month",
            "filters_json": "[]",
            "is_public": 1,
            "is_standard": 1
        })
        chart.insert()
        print("✅ Created Cost by Provider Chart")
    
    # 3. Monthly Quota Usage Chart
    if not frappe.db.exists("Dashboard Chart", "Monthly Quota Usage"):
        chart = frappe.get_doc({
            "doctype": "Dashboard Chart",
            "name": "Monthly Quota Usage", 
            "chart_name": "Monthly Quota Usage",
            "module": "Safari Integrations",
            "chart_type": "Group By",
            "document_type": "API Usage Log",
            "based_on": "safari_company",
            "group_by_based_on": "safari_company",
            "time_interval": "Monthly",
            "timespan": "Last Month",
            "number_of_groups": 10,
            "filters_json": "[]",
            "is_public": 1,
            "is_standard": 1
        })
        chart.insert()
        print("✅ Created Monthly Quota Usage Chart")
    
    frappe.db.commit()
    print("Dashboard charts creation completed!")

def create_number_cards():
    """Create missing number cards"""
    
    print("Creating Number Cards...")
    
    # Monthly API Costs Card
    if not frappe.db.exists("Number Card", "Monthly API Costs"):
        card = frappe.get_doc({
            "doctype": "Number Card",
            "name": "Monthly API Costs",
            "label": "Monthly API Costs",
            "module": "Safari Integrations",
            "document_type": "API Usage Log",
            "function": "Sum",
            "aggregate_function_based_on": "cost_incurred",
            "filters_json": "[]",
            "color": "#FF8C00",
            "is_public": 1,
            "is_standard": 1,
            "stats_time_interval": "Monthly"
        })
        card.insert()
        print("✅ Created Monthly API Costs Card")
    
    # Companies with Access Card
    if not frappe.db.exists("Number Card", "Companies with Access"):
        card = frappe.get_doc({
            "doctype": "Number Card",
            "name": "Companies with Access",
            "label": "Companies with Access", 
            "module": "Safari Integrations",
            "document_type": "Company API Access",
            "function": "Count",
            "filters_json": "[[\"Company API Access\",\"is_active\",\"=\",1,false]]",
            "color": "#6f42c1",
            "is_public": 1,
            "is_standard": 1,
            "stats_time_interval": "Daily"
        })
        card.insert()
        print("✅ Created Companies with Access Card")
    
    frappe.db.commit()
    print("Number cards creation completed!")

def setup_all():
    """Setup all dashboard components"""
    create_number_cards()
    create_dashboard_charts()
    print("🎉 All dashboard components created successfully!")