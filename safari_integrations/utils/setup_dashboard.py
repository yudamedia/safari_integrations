import frappe
import json

def setup_dashboard_components():
    """Setup dashboard components for Safari Integrations"""
    
    print("Setting up Safari Integrations Dashboard...")
    
    # Create Number Cards
    create_number_cards()
    
    # Create Dashboard Charts
    create_dashboard_charts()
    
    frappe.db.commit()
    print("Dashboard setup completed!")

def create_number_cards():
    """Create number cards"""
    
    cards = [
        {
            "name": "Monthly API Costs",
            "label": "Monthly API Costs",
            "doctype": "Number Card",
            "module": "Safari Integrations",
            "document_type": "API Usage Log",
            "function": "Sum",
            "aggregate_function_based_on": "cost_incurred",
            "filters_json": "[]",
            "color": "#FF8C00",
            "is_public": 1,
            "is_standard": 1,
            "stats_time_interval": "Monthly"
        },
        {
            "name": "Companies with Access",
            "label": "Companies with Access",
            "doctype": "Number Card",
            "module": "Safari Integrations", 
            "document_type": "Company API Access",
            "function": "Count",
            "filters_json": "[[\"Company API Access\",\"is_active\",\"=\",1,false]]",
            "color": "#6f42c1",
            "is_public": 1,
            "is_standard": 1,
            "stats_time_interval": "Daily"
        }
    ]
    
    for card in cards:
        if not frappe.db.exists("Number Card", card["name"]):
            try:
                doc = frappe.get_doc(card)
                doc.insert()
                print(f"Created Number Card: {card['name']}")
            except Exception as e:
                print(f"Error creating {card['name']}: {str(e)}")

def create_dashboard_charts():
    """Create dashboard charts"""
    
    # API Usage Trends Chart
    usage_chart = {
        "doctype": "Dashboard Chart",
        "name": "API Usage Trends",
        "chart_name": "API Usage Trends",
        "module": "Safari Integrations",
        "chart_type": "Line",
        "source": "Query",
        "is_public": 1,
        "is_standard": 1,
        "custom_query": """
            SELECT 
                DATE(creation) as `date`,
                COUNT(*) as `total_calls`,
                SUM(CASE WHEN response_status < 400 THEN 1 ELSE 0 END) as `successful`,
                SUM(CASE WHEN response_status >= 400 THEN 1 ELSE 0 END) as `failed`
            FROM `tabAPI Usage Log`
            WHERE creation >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            GROUP BY DATE(creation)
            ORDER BY DATE(creation)
        """,
        "x_field": "date",
        "y_axis": [
            {"y_field": "total_calls", "color": "#4463F0"},
            {"y_field": "successful", "color": "#28a745"},
            {"y_field": "failed", "color": "#dc3545"}
        ]
    }
    
    # Cost by Provider Chart
    cost_chart = {
        "doctype": "Dashboard Chart",
        "name": "Cost by Provider", 
        "chart_name": "Cost by Provider",
        "module": "Safari Integrations",
        "chart_type": "Donut",
        "source": "Query",
        "is_public": 1,
        "is_standard": 1,
        "custom_query": """
            SELECT 
                api_provider as `provider`,
                SUM(cost_incurred) as `total_cost`
            FROM `tabAPI Usage Log`
            WHERE creation >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                AND cost_incurred > 0
            GROUP BY api_provider
            ORDER BY total_cost DESC
            LIMIT 6
        """,
        "x_field": "provider",
        "y_axis": [
            {"y_field": "total_cost", "color": "#FF8C00"}
        ]
    }
    
    # Monthly Quota Usage Chart
    quota_chart = {
        "doctype": "Dashboard Chart",
        "name": "Monthly Quota Usage",
        "chart_name": "Monthly Quota Usage", 
        "module": "Safari Integrations",
        "chart_type": "Bar",
        "source": "Query",
        "is_public": 1,
        "is_standard": 1,
        "custom_query": """
            SELECT 
                CONCAT(aul.safari_company, ' - ', aul.api_provider) as `company_provider`,
                COUNT(*) as `usage_count`,
                caa.monthly_quota as `quota`
            FROM `tabAPI Usage Log` aul
            LEFT JOIN `tabCompany API Access` caa 
                ON caa.safari_company = aul.safari_company 
                AND caa.api_provider = aul.api_provider
            WHERE aul.creation >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                AND caa.is_active = 1
                AND caa.monthly_quota > 0
            GROUP BY aul.safari_company, aul.api_provider, caa.monthly_quota
            ORDER BY usage_count DESC
            LIMIT 10
        """,
        "x_field": "company_provider",
        "y_axis": [
            {"y_field": "usage_count", "color": "#28a745"},
            {"y_field": "quota", "color": "#ffc107"}
        ]
    }
    
    charts = [usage_chart, cost_chart, quota_chart]
    
    for chart in charts:
        if not frappe.db.exists("Dashboard Chart", chart["name"]):
            try:
                doc = frappe.get_doc(chart)
                doc.insert()
                print(f"Created Dashboard Chart: {chart['name']}")
            except Exception as e:
                print(f"Error creating {chart['name']}: {str(e)}")
        else:
            try:
                doc = frappe.get_doc("Dashboard Chart", chart["name"])
                for key, value in chart.items():
                    if key not in ["name", "doctype"]:
                        setattr(doc, key, value)
                doc.save()
                print(f"Updated Dashboard Chart: {chart['name']}")
            except Exception as e:
                print(f"Error updating {chart['name']}: {str(e)}")