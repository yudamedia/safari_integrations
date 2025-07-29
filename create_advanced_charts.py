#!/usr/bin/env python3

import frappe
import json
from datetime import datetime, timedelta

class SafariIntegrationsDashboard:
    """Advanced dashboard chart creator for Safari Integrations"""
    
    def __init__(self):
        self.module = "Safari Integrations"
        self.colors = {
            'primary': '#4463F0',
            'success': '#28a745', 
            'warning': '#ffc107',
            'danger': '#dc3545',
            'info': '#17a2b8',
            'orange': '#FF8C00',
            'purple': '#6f42c1'
        }
    
    def create_api_usage_trends_chart(self):
        """Create API Usage Trends line chart"""
        
        chart_config = {
            "doctype": "Dashboard Chart",
            "name": "API Usage Trends",
            "chart_name": "API Usage Trends",
            "module": self.module,
            "chart_type": "Line",
            "source": "Query",
            "is_public": 1,
            "is_standard": 1,
            "custom_query": """
                SELECT 
                    DATE(creation) as `date`,
                    COUNT(*) as `api_calls`,
                    SUM(CASE WHEN response_status < 400 THEN 1 ELSE 0 END) as `successful`,
                    SUM(CASE WHEN response_status >= 400 THEN 1 ELSE 0 END) as `failed`
                FROM `tabAPI Usage Log`
                WHERE creation >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                GROUP BY DATE(creation)
                ORDER BY DATE(creation)
            """,
            "x_field": "date",
            "y_axis": [
                {
                    "y_field": "api_calls",
                    "color": self.colors['primary']
                },
                {
                    "y_field": "successful", 
                    "color": self.colors['success']
                },
                {
                    "y_field": "failed",
                    "color": self.colors['danger']
                }
            ],
            "custom_options": json.dumps({
                "title": "API Usage Trends (Last 30 Days)",
                "colors": [self.colors['primary'], self.colors['success'], self.colors['danger']],
                "height": 300,
                "axisOptions": {
                    "xAxisMode": "tick",
                    "yAxisMode": "tick",
                    "xIsSeries": 1
                },
                "lineOptions": {
                    "hideDots": 0,
                    "heatline": 0,
                    "regionFill": 0
                },
                "tooltipOptions": {
                    "formatTooltipX": "MMM DD",
                    "formatTooltipY": ",.0f calls"
                }
            })
        }
        
        return self._create_or_update_chart(chart_config)
    
    def create_cost_by_provider_chart(self):
        """Create Cost by Provider donut chart"""
        
        chart_config = {
            "doctype": "Dashboard Chart",
            "name": "Cost by Provider", 
            "chart_name": "Cost by Provider",
            "module": self.module,
            "chart_type": "Donut",
            "source": "Query",
            "is_public": 1,
            "is_standard": 1,
            "custom_query": """
                SELECT 
                    api_provider as `provider`,
                    SUM(cost_incurred) as `total_cost`,
                    COUNT(*) as `call_count`
                FROM `tabAPI Usage Log`
                WHERE creation >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                    AND cost_incurred > 0
                GROUP BY api_provider
                ORDER BY total_cost DESC
                LIMIT 10
            """,
            "x_field": "provider",
            "y_axis": [
                {
                    "y_field": "total_cost",
                    "color": self.colors['orange']
                }
            ],
            "custom_options": json.dumps({
                "title": "API Costs by Provider (Last 30 Days)",
                "colors": [
                    self.colors['orange'], self.colors['primary'], self.colors['success'],
                    self.colors['danger'], self.colors['purple'], self.colors['info']
                ],
                "height": 300,
                "maxSlices": 6,
                "truncateLegends": 1,
                "tooltipOptions": {
                    "formatTooltipY": "$ ,.2f"
                }
            })
        }
        
        return self._create_or_update_chart(chart_config)
    
    def create_quota_usage_chart(self):
        """Create Monthly Quota Usage bar chart"""
        
        chart_config = {
            "doctype": "Dashboard Chart",
            "name": "Monthly Quota Usage",
            "chart_name": "Monthly Quota Usage", 
            "module": self.module,
            "chart_type": "Bar",
            "source": "Query",
            "is_public": 1,
            "is_standard": 1,
            "custom_query": """
                SELECT 
                    CONCAT(aul.safari_company, ' - ', aul.api_provider) as `company_provider`,
                    COUNT(*) as `usage_count`,
                    caa.monthly_quota as `quota`,
                    ROUND((COUNT(*) / caa.monthly_quota) * 100, 1) as `usage_percentage`
                FROM `tabAPI Usage Log` aul
                LEFT JOIN `tabCompany API Access` caa 
                    ON caa.safari_company = aul.safari_company 
                    AND caa.api_provider = aul.api_provider
                WHERE aul.creation >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                    AND caa.is_active = 1
                    AND caa.monthly_quota > 0
                GROUP BY aul.safari_company, aul.api_provider, caa.monthly_quota
                ORDER BY usage_percentage DESC
                LIMIT 15
            """,
            "x_field": "company_provider",
            "y_axis": [
                {
                    "y_field": "usage_count",
                    "color": self.colors['success']
                },
                {
                    "y_field": "quota", 
                    "color": self.colors['warning']
                }
            ],
            "custom_options": json.dumps({
                "title": "Quota Usage by Company & Provider",
                "colors": [self.colors['success'], self.colors['warning']],
                "height": 350,
                "barOptions": {
                    "stacked": 0,
                    "spaceRatio": 0.2
                },
                "axisOptions": {
                    "xAxisMode": "tick",
                    "yAxisMode": "tick",
                    "shortenYAxisNumbers": 1
                },
                "tooltipOptions": {
                    "formatTooltipY": ",.0f calls"
                }
            })
        }
        
        return self._create_or_update_chart(chart_config)
    
    def create_provider_performance_chart(self):
        """Create Provider Performance heatmap chart"""
        
        chart_config = {
            "doctype": "Dashboard Chart",
            "name": "Provider Performance",
            "chart_name": "Provider Performance",
            "module": self.module,
            "chart_type": "Bar",
            "source": "Query", 
            "is_public": 1,
            "is_standard": 1,
            "custom_query": """
                SELECT 
                    api_provider as `provider`,
                    AVG(response_time_ms) as `avg_response_time`,
                    (SUM(CASE WHEN response_status < 400 THEN 1 ELSE 0 END) / COUNT(*)) * 100 as `success_rate`,
                    COUNT(*) as `total_calls`
                FROM `tabAPI Usage Log`
                WHERE creation >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
                GROUP BY api_provider
                HAVING COUNT(*) >= 10
                ORDER BY success_rate DESC
            """,
            "x_field": "provider",
            "y_axis": [
                {
                    "y_field": "avg_response_time",
                    "color": self.colors['info']
                },
                {
                    "y_field": "success_rate",
                    "color": self.colors['success']
                }
            ],
            "custom_options": json.dumps({
                "title": "API Provider Performance (Last 7 Days)", 
                "colors": [self.colors['info'], self.colors['success']],
                "height": 300,
                "barOptions": {
                    "stacked": 0,
                    "spaceRatio": 0.3
                },
                "tooltipOptions": {
                    "formatTooltipY": ",.1f"
                }
            })
        }
        
        return self._create_or_update_chart(chart_config)
    
    def create_real_time_usage_chart(self):
        """Create real-time API usage chart"""
        
        chart_config = {
            "doctype": "Dashboard Chart",
            "name": "Real Time API Usage",
            "chart_name": "Real Time API Usage",
            "module": self.module,
            "chart_type": "Line",
            "source": "Query",
            "is_public": 1,
            "is_standard": 1,
            "custom_query": """
                SELECT 
                    DATE_FORMAT(creation, '%H:%i') as `time`,
                    COUNT(*) as `calls_per_minute`
                FROM `tabAPI Usage Log`
                WHERE creation >= DATE_SUB(NOW(), INTERVAL 4 HOUR)
                GROUP BY DATE_FORMAT(creation, '%Y-%m-%d %H:%i')
                ORDER BY creation DESC
                LIMIT 240
            """,
            "x_field": "time",
            "y_axis": [
                {
                    "y_field": "calls_per_minute",
                    "color": self.colors['primary']
                }
            ],
            "custom_options": json.dumps({
                "title": "Real-time API Usage (Last 4 Hours)",
                "colors": [self.colors['primary']],
                "height": 250,
                "lineOptions": {
                    "hideDots": 1,
                    "heatline": 1,
                    "regionFill": 1
                },
                "axisOptions": {
                    "xAxisMode": "tick",
                    "yAxisMode": "tick"
                }
            })
        }
        
        return self._create_or_update_chart(chart_config)
    
    def _create_or_update_chart(self, chart_config):
        """Helper method to create or update dashboard chart"""
        
        try:
            chart_name = chart_config["name"]
            
            if frappe.db.exists("Dashboard Chart", chart_name):
                # Update existing chart
                doc = frappe.get_doc("Dashboard Chart", chart_name)
                for key, value in chart_config.items():
                    if key not in ["name", "doctype"]:
                        setattr(doc, key, value)
                doc.save()
                print(f"🔄 Updated Dashboard Chart: {chart_name}")
                return doc
            else:
                # Create new chart
                doc = frappe.get_doc(chart_config)
                doc.insert()
                print(f"✅ Created Dashboard Chart: {chart_name}")
                return doc
                
        except Exception as e:
            print(f"❌ Error with Dashboard Chart {chart_config['name']}: {str(e)}")
            return None
    
    def create_all_charts(self):
        """Create all dashboard charts"""
        
        print("📈 Creating Safari Integrations Dashboard Charts...")
        print("=" * 50)
        
        charts_created = []
        
        # Create each chart
        chart_methods = [
            self.create_api_usage_trends_chart,
            self.create_cost_by_provider_chart, 
            self.create_quota_usage_chart,
            self.create_provider_performance_chart,
            self.create_real_time_usage_chart
        ]
        
        for create_method in chart_methods:
            try:
                chart = create_method()
                if chart:
                    charts_created.append(chart.name)
            except Exception as e:
                print(f"❌ Error creating chart: {str(e)}")
        
        print(f"\n✨ Successfully created/updated {len(charts_created)} dashboard charts:")
        for chart_name in charts_created:
            print(f"   📊 {chart_name}")
        
        return charts_created

def main():
    """Main function to create advanced dashboard charts"""
    
    try:
        # Initialize Frappe if running standalone
        if not hasattr(frappe.local, 'site'):
            import os
            sites_path = "/home/erpnext/frappe-bench/sites"
            site = "safarierp"
            
            frappe.init(site=site, sites_path=sites_path)
            frappe.connect()
        
        # Create dashboard instance and charts
        dashboard = SafariIntegrationsDashboard()
        charts_created = dashboard.create_all_charts()
        
        # Commit changes
        frappe.db.commit()
        
        print(f"\n🎉 Advanced dashboard charts creation completed!")
        print(f"   Total charts: {len(charts_created)}")
        
    except Exception as e:
        print(f"❌ Error in main execution: {str(e)}")
        frappe.db.rollback()
    finally:
        frappe.destroy()

if __name__ == "__main__":
    main()