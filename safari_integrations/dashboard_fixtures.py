# Copyright (c) 2024, Safari ERP and Contributors
# License: MIT

import json
import frappe
from frappe import _

def get_data():
    return frappe._dict({
        "dashboards": get_dashboards(),
        "charts": get_charts(),
        "number_cards": get_number_cards(),
    })

def get_dashboards():
    return [
        {
            "name": "Integrations Management",
            "dashboard_name": "Integrations Management",
            "charts": [
                {"chart": "API Usage Trends", "width": "Half"},
                {"chart": "Cost by Provider", "width": "Half"},
                {"chart": "Monthly Quota Usage", "width": "Full"},
                {"chart": "Provider Performance", "width": "Full"},
            ],
            "cards": [
                {"card": "Active API Providers"},
                {"card": "Total API Calls Today"},
                {"card": "Monthly API Costs"},
                {"card": "Companies with Access"},
                {"card": "Failed API Calls Today"},
            ],
        }
    ]

def get_charts():
    return [
        {
            "doctype": "Dashboard Chart",
            "name": "API Usage Trends",
            "chart_name": "API Usage Trends",
            "chart_type": "Sum",
            "document_type": "API Usage Log",
            "filters_json": json.dumps([["API Usage Log", "creation", ">=", "Last Month", False]]),
            "group_by_type": "Count",
            "time_interval": "Daily",
            "timespan": "Last Month",
            "owner": "Administrator",
            "type": "Line",
            "value_based_on": "cost_incurred",
            "is_public": 1,
            "timeseries": 1,
            "module": "Safari Integrations"
        },
        {
            "doctype": "Dashboard Chart",
            "name": "Cost by Provider",
            "chart_name": "Cost by Provider",
            "chart_type": "Sum",
            "document_type": "API Usage Log",
            "filters_json": json.dumps([["API Usage Log", "creation", ">=", "This Month", False]]),
            "group_by_type": "Count",
            "time_interval": "Monthly",
            "timespan": "This Month",
            "owner": "Administrator",
            "type": "Donut",
            "value_based_on": "cost_incurred",
            "is_public": 1,
            "timeseries": 0,
            "module": "Safari Integrations"
        },
        {
            "doctype": "Dashboard Chart",
            "name": "Monthly Quota Usage",
            "chart_name": "Monthly Quota Usage",
            "chart_type": "Sum",
            "document_type": "API Usage Log",
            "filters_json": json.dumps([["API Usage Log", "creation", ">=", "This Month", False]]),
            "group_by_type": "Count",
            "time_interval": "Daily",
            "timespan": "This Month",
            "owner": "Administrator",
            "type": "Bar",
            "value_based_on": "quota_used",
            "is_public": 1,
            "timeseries": 1,
            "module": "Safari Integrations"
        },
        {
            "doctype": "Dashboard Chart",
            "name": "Provider Performance",
            "chart_name": "Provider Performance",
            "chart_type": "Count",
            "document_type": "API Usage Log",
            "filters_json": json.dumps([["API Usage Log", "creation", ">=", "Last Week", False]]),
            "group_by_type": "Count",
            "time_interval": "Daily",
            "timespan": "Last Week",
            "owner": "Administrator",
            "type": "Line",
            "value_based_on": "response_time",
            "is_public": 1,
            "timeseries": 1,
            "module": "Safari Integrations"
        }
    ]

def get_number_cards():
    return [
        {
            "doctype": "Number Card",
            "name": "Active API Providers",
            "label": "Active API Providers",
            "document_type": "API Provider",
            "function": "Count",
            "filters_json": json.dumps([["API Provider", "is_active", "=", 1, False]]),
            "is_public": 1,
            "show_percentage_stats": 1,
            "stats_time_interval": "Daily",
            "module": "Safari Integrations"
        },
        {
            "doctype": "Number Card",
            "name": "Total API Calls Today",
            "label": "Total API Calls Today",
            "document_type": "API Usage Log",
            "function": "Count",
            "filters_json": json.dumps([["API Usage Log", "creation", ">=", "Today", False]]),
            "is_public": 1,
            "show_percentage_stats": 1,
            "stats_time_interval": "Hourly",
            "module": "Safari Integrations"
        },
        {
            "doctype": "Number Card",
            "name": "Monthly API Costs",
            "label": "Monthly API Costs",
            "document_type": "API Usage Log",
            "function": "Sum",
            "aggregate_function_based_on": "cost_incurred",
            "filters_json": json.dumps([["API Usage Log", "creation", ">=", "This Month", False]]),
            "is_public": 1,
            "show_percentage_stats": 1,
            "stats_time_interval": "Monthly",
            "module": "Safari Integrations"
        },
        {
            "doctype": "Number Card",
            "name": "Companies with Access",
            "label": "Companies with Access",
            "document_type": "Company API Access",
            "function": "Count",
            "filters_json": json.dumps([["Company API Access", "is_active", "=", 1, False]]),
            "is_public": 1,
            "show_percentage_stats": 1,
            "stats_time_interval": "Daily",
            "module": "Safari Integrations"
        },
        {
            "doctype": "Number Card",
            "name": "Failed API Calls Today",
            "label": "Failed API Calls Today",
            "document_type": "API Usage Log",
            "function": "Count",
            "filters_json": json.dumps([
                ["API Usage Log", "creation", ">=", "Today", False],
                ["API Usage Log", "response_status", ">=", 400, False]
            ]),
            "is_public": 1,
            "show_percentage_stats": 1,
            "stats_time_interval": "Hourly",
            "module": "Safari Integrations"
        }
    ] 