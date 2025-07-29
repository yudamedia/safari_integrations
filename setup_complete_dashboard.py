#!/usr/bin/env python3

import frappe
import json
from datetime import datetime

def setup_safari_integrations_dashboard():
    """Complete setup for Safari Integrations dashboard with all components"""
    
    print("🚀 Setting up Safari Integrations Dashboard...")
    print("=" * 60)
    
    # 1. Create Number Cards
    create_number_cards()
    
    # 2. Create Dashboard Charts  
    create_dashboard_charts()
    
    # 3. Create Query Reports
    create_query_reports()
    
    # 4. Update Workspace with new components
    update_workspace()
    
    print("\n✨ Safari Integrations Dashboard setup completed!")

def create_number_cards():
    """Create all number cards for the dashboard"""
    
    print("\n📊 Creating Number Cards...")
    
    cards = [
        {
            "name": "Active API Providers",
            "label": "Active API Providers",
            "document_type": "API Provider",
            "function": "Count", 
            "filters_json": "[[\"API Provider\",\"is_active\",\"=\",1,false]]",
            "color": "#4463F0"
        },
        {
            "name": "Total API Calls Today",
            "label": "Total API Calls Today",
            "document_type": "API Usage Log",
            "function": "Count",
            "filters_json": "[[\"API Usage Log\",\"creation\",\">=\",\"Today\",false]]",
            "color": "#28a745"
        },
        {
            "name": "Monthly API Costs",
            "label": "Monthly API Costs", 
            "document_type": "API Usage Log",
            "function": "Sum",
            "aggregate_function_based_on": "cost_incurred",
            "filters_json": "[[\"API Usage Log\",\"creation\",\">=\",\"This Month\",false]]",
            "color": "#FF8C00"
        },
        {
            "name": "Companies with Access",
            "label": "Companies with Access",
            "document_type": "Company API Access",
            "function": "Count",
            "filters_json": "[[\"Company API Access\",\"is_active\",\"=\",1,false]]", 
            "color": "#6f42c1"
        },
        {
            "name": "Failed API Calls Today",
            "label": "Failed API Calls Today",
            "document_type": "API Usage Log", 
            "function": "Count",
            "filters_json": "[[\"API Usage Log\",\"creation\",\">=\",\"Today\",false],[\"API Usage Log\",\"response_status\",\">=\",400,false]]",
            "color": "#dc3545"
        },
        {
            "name": "Average Response Time",
            "label": "Average Response Time",
            "document_type": "API Usage Log",
            "function": "Average",
            "aggregate_function_based_on": "response_time_ms",
            "filters_json": "[[\"API Usage Log\",\"creation\",\">=\",\"Today\",false]]",
            "color": "#17a2b8"
        }
    ]
    
    for card_data in cards:
        create_number_card(card_data)

def create_number_card(card_data):
    """Create individual number card"""
    
    full_card = {
        "doctype": "Number Card",
        "module": "Safari Integrations",
        "is_public": 1,
        "is_standard": 1,
        "stats_time_interval": "Daily",
        "show_percentage_stats": 0,
        **card_data
    }
    
    try:
        if not frappe.db.exists("Number Card", card_data["name"]):
            doc = frappe.get_doc(full_card)
            doc.insert()
            print(f"   ✅ Created: {card_data['name']}")
        else:
            print(f"   ⚠️  Exists: {card_data['name']}")
    except Exception as e:
        print(f"   ❌ Error creating {card_data['name']}: {str(e)}")

def create_dashboard_charts():
    """Create all dashboard charts"""
    
    print("\n📈 Creating Dashboard Charts...")
    
    # API Usage Trends Chart
    api_trends = {
        "name": "API Usage Trends",
        "chart_name": "API Usage Trends",
        "chart_type": "Line",
        "source": "Query",
        "custom_query": """
            SELECT 
                DATE(creation) as `Date`,
                COUNT(*) as `Total Calls`,
                SUM(CASE WHEN response_status < 400 THEN 1 ELSE 0 END) as `Successful`,
                SUM(CASE WHEN response_status >= 400 THEN 1 ELSE 0 END) as `Failed`
            FROM `tabAPI Usage Log`
            WHERE creation >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            GROUP BY DATE(creation)
            ORDER BY DATE(creation)
        """,
        "x_field": "Date",
        "y_axis": [
            {"y_field": "Total Calls", "color": "#4463F0"},
            {"y_field": "Successful", "color": "#28a745"},
            {"y_field": "Failed", "color": "#dc3545"}
        ],
        "custom_options": json.dumps({
            "title": "API Usage Trends (30 Days)",
            "colors": ["#4463F0", "#28a745", "#dc3545"],
            "height": 300,
            "lineOptions": {"hideDots": 0, "heatline": 0},
            "axisOptions": {"xAxisMode": "tick", "yAxisMode": "tick"}
        })
    }
    
    # Cost by Provider Chart  
    cost_provider = {
        "name": "Cost by Provider",
        "chart_name": "Cost by Provider",
        "chart_type": "Donut",
        "source": "Query",
        "custom_query": """
            SELECT 
                api_provider as `Provider`,
                SUM(cost_incurred) as `Total Cost`
            FROM `tabAPI Usage Log`
            WHERE creation >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                AND cost_incurred > 0
            GROUP BY api_provider
            ORDER BY `Total Cost` DESC
            LIMIT 8
        """,
        "x_field": "Provider",
        "y_axis": [{"y_field": "Total Cost", "color": "#FF8C00"}],
        "custom_options": json.dumps({
            "title": "API Costs by Provider",
            "colors": ["#FF8C00", "#4463F0", "#28a745", "#dc3545", "#6f42c1", "#fd7e14"],
            "height": 300,
            "maxSlices": 6
        })
    }
    
    # Monthly Quota Usage Chart
    quota_usage = {
        "name": "Monthly Quota Usage", 
        "chart_name": "Monthly Quota Usage",
        "chart_type": "Bar",
        "source": "Query",
        "custom_query": """
            SELECT 
                CONCAT(aul.safari_company, ' - ', aul.api_provider) as `Company Provider`,
                COUNT(*) as `Usage`,
                caa.monthly_quota as `Quota`,
                ROUND((COUNT(*) / caa.monthly_quota) * 100, 1) as `Usage %`
            FROM `tabAPI Usage Log` aul
            LEFT JOIN `tabCompany API Access` caa 
                ON caa.safari_company = aul.safari_company 
                AND caa.api_provider = aul.api_provider
            WHERE aul.creation >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                AND caa.is_active = 1 AND caa.monthly_quota > 0
            GROUP BY aul.safari_company, aul.api_provider, caa.monthly_quota
            ORDER BY `Usage %` DESC
            LIMIT 10
        """,
        "x_field": "Company Provider",
        "y_axis": [
            {"y_field": "Usage", "color": "#28a745"},
            {"y_field": "Quota", "color": "#ffc107"}
        ],
        "custom_options": json.dumps({
            "title": "Quota Usage by Company",
            "colors": ["#28a745", "#ffc107"],
            "height": 350,
            "barOptions": {"stacked": 0, "spaceRatio": 0.2}
        })
    }
    
    # Provider Performance Chart
    performance = {
        "name": "Provider Performance",
        "chart_name": "Provider Performance", 
        "chart_type": "Bar",
        "source": "Query",
        "custom_query": """
            SELECT 
                api_provider as `Provider`,
                AVG(response_time_ms) as `Avg Response Time (ms)`,
                ROUND((SUM(CASE WHEN response_status < 400 THEN 1 ELSE 0 END) / COUNT(*)) * 100, 1) as `Success Rate %`
            FROM `tabAPI Usage Log`
            WHERE creation >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
            GROUP BY api_provider
            HAVING COUNT(*) >= 5
            ORDER BY `Success Rate %` DESC
        """,
        "x_field": "Provider",
        "y_axis": [
            {"y_field": "Avg Response Time (ms)", "color": "#17a2b8"},
            {"y_field": "Success Rate %", "color": "#28a745"}
        ],
        "custom_options": json.dumps({
            "title": "Provider Performance (7 Days)",
            "colors": ["#17a2b8", "#28a745"],
            "height": 300
        })
    }
    
    charts = [api_trends, cost_provider, quota_usage, performance]
    
    for chart_data in charts:
        create_dashboard_chart(chart_data)

def create_dashboard_chart(chart_data):
    """Create individual dashboard chart"""
    
    full_chart = {
        "doctype": "Dashboard Chart",
        "module": "Safari Integrations",
        "is_public": 1,
        "is_standard": 1,
        **chart_data
    }
    
    try:
        if not frappe.db.exists("Dashboard Chart", chart_data["name"]):
            doc = frappe.get_doc(full_chart)
            doc.insert()
            print(f"   ✅ Created: {chart_data['name']}")
        else:
            # Update existing chart
            doc = frappe.get_doc("Dashboard Chart", chart_data["name"])
            for key, value in chart_data.items():
                if key not in ["name", "doctype"]:
                    setattr(doc, key, value)
            doc.save()
            print(f"   🔄 Updated: {chart_data['name']}")
    except Exception as e:
        print(f"   ❌ Error with {chart_data['name']}: {str(e)}")

def create_query_reports():
    """Create query reports for detailed analytics"""
    
    print("\n📋 Creating Query Reports...")
    
    reports = [
        {
            "name": "API Usage Report",
            "report_name": "API Usage Report",
            "report_type": "Query Report",
            "query": """
                SELECT 
                    DATE(aul.creation) as `Date`,
                    aul.safari_company as `Company`,
                    aul.api_provider as `Provider`,
                    aul.endpoint as `Endpoint`,
                    COUNT(*) as `Total Calls`,
                    SUM(CASE WHEN aul.response_status < 400 THEN 1 ELSE 0 END) as `Successful`,
                    SUM(CASE WHEN aul.response_status >= 400 THEN 1 ELSE 0 END) as `Failed`,
                    AVG(aul.response_time_ms) as `Avg Response Time`,
                    SUM(aul.cost_incurred) as `Total Cost`
                FROM `tabAPI Usage Log` aul
                WHERE aul.creation >= %(from_date)s
                    AND aul.creation <= %(to_date)s
                GROUP BY DATE(aul.creation), aul.safari_company, aul.api_provider, aul.endpoint
                ORDER BY aul.creation DESC, `Total Cost` DESC
            """
        },
        {
            "name": "Cost Analysis Report",
            "report_name": "Cost Analysis Report", 
            "report_type": "Query Report",
            "query": """
                SELECT 
                    aul.safari_company as `Company`,
                    aul.api_provider as `Provider`,
                    DATE_FORMAT(aul.creation, '%%Y-%%m') as `Month`,
                    COUNT(*) as `API Calls`,
                    SUM(aul.cost_incurred) as `Total Cost`,
                    AVG(aul.cost_incurred) as `Avg Cost per Call`,
                    caa.monthly_quota as `Monthly Quota`,
                    ROUND((COUNT(*) / caa.monthly_quota) * 100, 2) as `Quota Usage %%`
                FROM `tabAPI Usage Log` aul
                LEFT JOIN `tabCompany API Access` caa 
                    ON caa.safari_company = aul.safari_company 
                    AND caa.api_provider = aul.api_provider
                WHERE aul.creation >= %(from_date)s
                    AND aul.creation <= %(to_date)s
                GROUP BY aul.safari_company, aul.api_provider, DATE_FORMAT(aul.creation, '%%Y-%%m')
                ORDER BY `Total Cost` DESC
            """
        },
        {
            "name": "Quota Utilization Report",
            "report_name": "Quota Utilization Report",
            "report_type": "Query Report", 
            "query": """
                SELECT 
                    caa.safari_company as `Company`,
                    caa.api_provider as `Provider`,
                    caa.monthly_quota as `Monthly Quota`,
                    COUNT(aul.name) as `Current Usage`,
                    ROUND((COUNT(aul.name) / caa.monthly_quota) * 100, 2) as `Usage Percentage`,
                    (caa.monthly_quota - COUNT(aul.name)) as `Remaining Quota`,
                    CASE 
                        WHEN (COUNT(aul.name) / caa.monthly_quota) > 0.9 THEN 'Critical'
                        WHEN (COUNT(aul.name) / caa.monthly_quota) > 0.7 THEN 'Warning'  
                        ELSE 'Normal'
                    END as `Status`
                FROM `tabCompany API Access` caa
                LEFT JOIN `tabAPI Usage Log` aul 
                    ON aul.safari_company = caa.safari_company
                    AND aul.api_provider = caa.api_provider
                    AND DATE(aul.creation) >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                WHERE caa.is_active = 1
                GROUP BY caa.safari_company, caa.api_provider, caa.monthly_quota
                ORDER BY `Usage Percentage` DESC
            """
        }
    ]
    
    for report_data in reports:
        create_query_report(report_data)

def create_query_report(report_data):
    """Create individual query report"""
    
    full_report = {
        "doctype": "Report",
        "module": "Safari Integrations", 
        "is_standard": "Yes",
        **report_data
    }
    
    try:
        if not frappe.db.exists("Report", report_data["name"]):
            doc = frappe.get_doc(full_report)
            doc.insert()
            print(f"   ✅ Created: {report_data['name']}")
        else:
            print(f"   ⚠️  Exists: {report_data['name']}")
    except Exception as e:
        print(f"   ❌ Error creating {report_data['name']}: {str(e)}")

def update_workspace():
    """Update workspace configuration with new components"""
    
    print("\n⚙️  Updating Workspace Configuration...")
    
    try:
        workspace = frappe.get_doc("Workspace", "Integrations Management")
        
        # Update charts in workspace
        workspace.charts = [
            {"chart_name": "API Usage Trends", "label": "API Usage Trends"},
            {"chart_name": "Cost by Provider", "label": "Cost by Provider"},
            {"chart_name": "Monthly Quota Usage", "label": "Monthly Quota Usage"},
            {"chart_name": "Provider Performance", "label": "Provider Performance"}
        ]
        
        # Update number cards
        workspace.number_cards = [
            {
                "label": "Active API Providers",
                "document_type": "API Provider",
                "function": "Count",
                "filters_json": '{"is_active": 1}',
                "color": "Blue",
                "is_public": 1,
                "stats_time_interval": "Daily"
            },
            {
                "label": "Total API Calls Today", 
                "document_type": "API Usage Log",
                "function": "Count",
                "dynamic_filters_json": '{"creation": ["timespan", "today"]}',
                "color": "Green",
                "is_public": 1,
                "stats_time_interval": "Daily"
            },
            {
                "label": "Monthly API Costs",
                "document_type": "API Usage Log",
                "function": "Sum", 
                "aggregate_function_based_on": "cost_incurred",
                "dynamic_filters_json": '{"creation": ["timespan", "this month"]}',
                "color": "Orange",
                "is_public": 1,
                "stats_time_interval": "Monthly"
            },
            {
                "label": "Companies with Access",
                "document_type": "Company API Access",
                "function": "Count",
                "filters_json": '{"is_active": 1}',
                "color": "Purple", 
                "is_public": 1,
                "stats_time_interval": "Daily"
            }
        ]
        
        workspace.save()
        print("   ✅ Workspace updated successfully")
        
    except Exception as e:
        print(f"   ❌ Error updating workspace: {str(e)}")

def main():
    """Main execution function"""
    
    try:
        # Initialize Frappe
        if not hasattr(frappe.local, 'site'):
            import os
            sites_path = "/home/erpnext/frappe-bench/sites"
            site = "safarierp"
            
            frappe.init(site=site, sites_path=sites_path)
            frappe.connect()
        
        # Setup dashboard
        setup_safari_integrations_dashboard()
        
        # Commit changes
        frappe.db.commit()
        
        print("\n🎉 Complete dashboard setup finished!")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {str(e)}")
        frappe.db.rollback()
    finally:
        frappe.destroy()

if __name__ == "__main__":
    main()