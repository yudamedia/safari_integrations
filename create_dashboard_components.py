#!/usr/bin/env python3

import frappe
import json
from datetime import datetime

def create_number_cards():
    """Create missing number cards for the safari_integrations dashboard"""
    
    number_cards = [
        {
            "name": "Monthly API Costs",
            "label": "Monthly API Costs", 
            "doctype": "Number Card",
            "module": "Safari Integrations",
            "document_type": "API Usage Log",
            "function": "Sum",
            "aggregate_function_based_on": "cost_incurred",
            "filters_json": "[]",
            "dynamic_filters_json": "[]",
            "color": "#FF8C00",
            "is_public": 1,
            "is_standard": 1,
            "stats_time_interval": "Monthly",
            "show_percentage_stats": 1
        },
        {
            "name": "Companies with Access",
            "label": "Companies with Access",
            "doctype": "Number Card", 
            "module": "Safari Integrations",
            "document_type": "Company API Access",
            "function": "Count",
            "filters_json": "[[\"Company API Access\",\"is_active\",\"=\",1,false]]",
            "dynamic_filters_json": "[]",
            "color": "#9932CC",
            "is_public": 1,
            "is_standard": 1,
            "stats_time_interval": "Daily",
            "show_percentage_stats": 0
        }
    ]
    
    for card_data in number_cards:
        try:
            if not frappe.db.exists("Number Card", card_data["name"]):
                doc = frappe.get_doc(card_data)
                doc.insert()
                print(f"✅ Created Number Card: {card_data['name']}")
            else:
                print(f"⚠️  Number Card already exists: {card_data['name']}")
        except Exception as e:
            print(f"❌ Error creating Number Card {card_data['name']}: {str(e)}")

def create_dashboard_charts():
    """Create dashboard charts for the safari_integrations workspace"""
    
    charts = [
        {
            "name": "API Usage Trends",
            "chart_name": "API Usage Trends",
            "doctype": "Dashboard Chart",
            "module": "Safari Integrations", 
            "chart_type": "Line",
            "document_type": "API Usage Log",
            "based_on": "creation",
            "value_based_on": "",
            "number_of_groups": 0,
            "filters_json": "[]",
            "time_interval": "Daily",
            "timespan": "Last Month",
            "color": "#4463F0",
            "is_public": 1,
            "is_standard": 1,
            "source": "API Usage Log",
            "x_field": "creation",
            "y_axis": [
                {
                    "y_field": "name",
                    "color": "#4463F0"
                }
            ]
        },
        {
            "name": "Cost by Provider",
            "chart_name": "Cost by Provider", 
            "doctype": "Dashboard Chart",
            "module": "Safari Integrations",
            "chart_type": "Donut",
            "document_type": "API Usage Log",
            "based_on": "api_provider",
            "value_based_on": "cost_incurred",
            "number_of_groups": 6,
            "filters_json": "[]",
            "time_interval": "Daily",
            "timespan": "Last Month",
            "color": "#FF8C00",
            "is_public": 1,
            "is_standard": 1,
            "source": "API Usage Log",
            "group_by_type": "Count",
            "aggregate_function_based_on": "cost_incurred"
        },
        {
            "name": "Monthly Quota Usage",
            "chart_name": "Monthly Quota Usage",
            "doctype": "Dashboard Chart", 
            "module": "Safari Integrations",
            "chart_type": "Bar",
            "document_type": "API Usage Log",
            "based_on": "safari_company",
            "value_based_on": "",
            "number_of_groups": 10,
            "filters_json": "[]",
            "time_interval": "Monthly", 
            "timespan": "This Month",
            "color": "#28a745",
            "is_public": 1,
            "is_standard": 1,
            "source": "API Usage Log",
            "group_by_type": "Count"
        }
    ]
    
    for chart_data in charts:
        try:
            if not frappe.db.exists("Dashboard Chart", chart_data["name"]):
                doc = frappe.get_doc(chart_data)
                doc.insert()
                print(f"✅ Created Dashboard Chart: {chart_data['name']}")
            else:
                print(f"⚠️  Dashboard Chart already exists: {chart_data['name']}")
        except Exception as e:
            print(f"❌ Error creating Dashboard Chart {chart_data['name']}: {str(e)}")

def create_custom_dashboard_charts():
    """Create custom dashboard charts with more sophisticated data handling"""
    
    # API Usage Trends Chart
    api_usage_chart = {
        "doctype": "Dashboard Chart",
        "name": "API Usage Trends",
        "chart_name": "API Usage Trends", 
        "module": "Safari Integrations",
        "chart_type": "Line",
        "source": "API Usage Log",
        "x_field": "creation",
        "is_public": 1,
        "is_standard": 1,
        "filters_json": "[]",
        "y_axis": [
            {
                "y_field": "name",
                "color": "#4463F0"
            }
        ],
        "custom_options": json.dumps({
            "colors": ["#4463F0", "#28a745", "#ff6b6b"],
            "axisOptions": {
                "xAxisMode": "tick",
                "yAxisMode": "tick", 
                "xIsSeries": 1
            },
            "tooltipOptions": {
                "formatTooltipX": "mmm dd",
                "formatTooltipY": ",.0f"
            }
        })
    }
    
    # Cost by Provider Donut Chart
    cost_provider_chart = {
        "doctype": "Dashboard Chart",
        "name": "Cost by Provider",
        "chart_name": "Cost by Provider",
        "module": "Safari Integrations", 
        "chart_type": "Donut",
        "source": "API Usage Log",
        "x_field": "api_provider",
        "y_axis": [
            {
                "y_field": "cost_incurred",
                "color": "#FF8C00"
            }
        ],
        "is_public": 1,
        "is_standard": 1,
        "filters_json": "[]",
        "custom_options": json.dumps({
            "colors": ["#FF8C00", "#4463F0", "#28a745", "#dc3545", "#6f42c1", "#fd7e14"],
            "maxSlices": 6,
            "truncateLegends": 1
        })
    }
    
    # Monthly Quota Usage Bar Chart
    quota_usage_chart = {
        "doctype": "Dashboard Chart", 
        "name": "Monthly Quota Usage",
        "chart_name": "Monthly Quota Usage",
        "module": "Safari Integrations",
        "chart_type": "Bar",
        "source": "API Usage Log", 
        "x_field": "safari_company",
        "y_axis": [
            {
                "y_field": "name",
                "color": "#28a745"
            }
        ],
        "is_public": 1,
        "is_standard": 1,
        "filters_json": "[]",
        "custom_options": json.dumps({
            "colors": ["#28a745", "#ffc107", "#dc3545"],
            "barOptions": {
                "stacked": 0,
                "spaceRatio": 0.1
            },
            "axisOptions": {
                "xAxisMode": "tick",
                "yAxisMode": "tick"
            }
        })
    }
    
    charts = [api_usage_chart, cost_provider_chart, quota_usage_chart]
    
    for chart_data in charts:
        try:
            if not frappe.db.exists("Dashboard Chart", chart_data["name"]):
                doc = frappe.get_doc(chart_data)
                doc.insert() 
                print(f"✅ Created Custom Dashboard Chart: {chart_data['name']}")
            else:
                # Update existing chart
                doc = frappe.get_doc("Dashboard Chart", chart_data["name"])
                for key, value in chart_data.items():
                    if key != "name" and key != "doctype":
                        setattr(doc, key, value)
                doc.save()
                print(f"🔄 Updated Dashboard Chart: {chart_data['name']}")
        except Exception as e:
            print(f"❌ Error creating Custom Dashboard Chart {chart_data['name']}: {str(e)}")

def create_query_reports():
    """Create query reports for detailed analytics"""
    
    reports = [
        {
            "name": "API Usage Report",
            "doctype": "Report", 
            "module": "Safari Integrations",
            "report_name": "API Usage Report",
            "report_type": "Query Report",
            "is_standard": "Yes",
            "query": """
                SELECT 
                    DATE(aul.creation) as `Date`,
                    aul.safari_company as `Company`,
                    aul.api_provider as `Provider`,
                    COUNT(*) as `Total Calls`,
                    SUM(CASE WHEN aul.response_status < 400 THEN 1 ELSE 0 END) as `Successful`,
                    SUM(CASE WHEN aul.response_status >= 400 THEN 1 ELSE 0 END) as `Failed`,
                    AVG(aul.response_time_ms) as `Avg Response Time (ms)`,
                    SUM(aul.cost_incurred) as `Total Cost`
                FROM `tabAPI Usage Log` aul
                WHERE aul.creation >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                GROUP BY DATE(aul.creation), aul.safari_company, aul.api_provider
                ORDER BY aul.creation DESC, aul.safari_company, aul.api_provider
            """
        },
        {
            "name": "Cost Analysis Report",
            "doctype": "Report",
            "module": "Safari Integrations", 
            "report_name": "Cost Analysis Report",
            "report_type": "Query Report",
            "is_standard": "Yes",
            "query": """
                SELECT 
                    aul.safari_company as `Company`,
                    aul.api_provider as `Provider`,
                    DATE_FORMAT(aul.creation, '%Y-%m') as `Month`,
                    COUNT(*) as `API Calls`,
                    SUM(aul.cost_incurred) as `Total Cost`,
                    AVG(aul.cost_incurred) as `Avg Cost per Call`,
                    caa.monthly_quota as `Monthly Quota`,
                    ROUND((COUNT(*) / caa.monthly_quota) * 100, 2) as `Quota Utilization %`
                FROM `tabAPI Usage Log` aul
                LEFT JOIN `tabCompany API Access` caa ON caa.safari_company = aul.safari_company 
                    AND caa.api_provider = aul.api_provider
                WHERE aul.creation >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
                GROUP BY aul.safari_company, aul.api_provider, DATE_FORMAT(aul.creation, '%Y-%m')
                ORDER BY aul.creation DESC, `Total Cost` DESC
            """
        }
    ]
    
    for report_data in reports:
        try:
            if not frappe.db.exists("Report", report_data["name"]):
                doc = frappe.get_doc(report_data)
                doc.insert()
                print(f"✅ Created Query Report: {report_data['name']}")
            else:
                print(f"⚠️  Query Report already exists: {report_data['name']}")
        except Exception as e:
            print(f"❌ Error creating Query Report {report_data['name']}: {str(e)}")

def main():
    """Main function to create all dashboard components"""
    
    print("🚀 Creating Safari Integrations Dashboard Components...")
    print("=" * 60)
    
    # Initialize Frappe if running standalone
    try:
        if not hasattr(frappe.local, 'site'):
            import os
            sites_path = "/home/erpnext/frappe-bench/sites"
            site = "safarierp"
            
            frappe.init(site=site, sites_path=sites_path)
            frappe.connect()
            
        print("📊 Creating Number Cards...")
        create_number_cards()
        
        print("\n📈 Creating Dashboard Charts...")
        create_custom_dashboard_charts()
        
        print("\n📋 Creating Query Reports...")
        create_query_reports()
        
        print("\n✨ Dashboard components creation completed!")
        
        frappe.db.commit()
        
    except Exception as e:
        print(f"❌ Error in main execution: {str(e)}")
        frappe.db.rollback()
    finally:
        frappe.destroy()

if __name__ == "__main__":
    main()