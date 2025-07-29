app_name = "safari_integrations"
app_title = "Safari Integrations"
app_publisher = "Yuda Media"
app_description = "Administrative API Management app for SafariERP"
app_email = "yuda@graphicstation.co.ke"
app_license = "mit"

# Workspaces
workspaces = [
    {
        "doctype": "Workspace",
        "name": "Integrations Management",
        "label": "Integrations Management",
        "icon": "api",
        "module": "Safari Integrations",
        "is_hidden": 0
    }
]

# Include JS and CSS files
app_include_js = [
    "/assets/safari_integrations/js/api_manager.js"
]

app_include_css = [
    "/assets/safari_integrations/css/integrations.css"
]

# Document Events
doc_events = {
    "API Usage Log": {
        "after_insert": "safari_integrations.utils.usage_tracker.update_quota_usage"
    },
    "Company API Access": {
        "validate": "safari_integrations.utils.api_manager.validate_api_credentials"
    }
}

# Scheduled Tasks
scheduler_events = {
    "daily": [
        "safari_integrations.utils.cost_calculator.calculate_daily_costs",
        "safari_integrations.utils.usage_tracker.send_quota_alerts"
    ],
    "hourly": [
        "safari_integrations.utils.rate_limiter.reset_hourly_limits"
    ]
}

# Override whitelisted methods for API access
override_whitelisted_methods = {
    "safari_integrations.api.call_external_api": "safari_integrations.utils.api_manager.call_external_api"
}

# Jinja environment methods
jenv = {
    "methods": [
        "safari_integrations.utils.api_manager.get_api_status",
        "safari_integrations.utils.cost_calculator.format_api_cost"
    ]
}

# Installation hooks
after_install = "safari_integrations.setup.install.after_install"

# Fixtures for master data and dashboard components
fixtures = [
    {
        "doctype": "API Provider",
        "filters": [
            ["name", "in", ["Amadeus", "VertoFx", "Chipper", "eCitizen", "Google Places", "OpenRouteService"]]
        ]
    },
    {
        "doctype": "Number Card",
        "filters": [
            [
                "name", 
                "in", 
                [
                    "Active API Providers",
                    "Total API Calls Today",
                    "Monthly API Costs",
                    "Companies with Access",
                    "Failed API Calls Today"
                ]
            ]
        ]
    },
    {
        "doctype": "Dashboard Chart",
        "filters": [
            [
                "name",
                "in",
                [
                    "API Usage Trends",
                    "Cost by Provider",
                    "Monthly Quota Usage",
                    "Provider Performance"
                ]
            ]
        ]
    },
    {
        "doctype": "Dashboard",
        "filters": [
            ["name", "=", "Integrations Management"]
        ]
    },
    {
        "doctype": "Report",
        "filters": [
            [
                "name",
                "in",
                [
                    "API Usage Analytics",
                    "API Cost Analysis",
                    "Provider Performance Report",
                    "Company API Access Report",
                    "API Quota Usage Report"
                ]
            ]
        ]
    }
]