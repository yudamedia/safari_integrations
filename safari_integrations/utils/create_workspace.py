import frappe

def create_integrations_workspace():
    """Create the Integrations Management workspace"""
    
    print("🚀 Creating Integrations Management Workspace...")
    
    if frappe.db.exists("Workspace", "Integrations Management"):
        print("⚠️  Workspace already exists")
        return
    
    workspace_data = {
        "doctype": "Workspace",
        "name": "Integrations Management",
        "label": "Integrations Management",
        "module": "Safari Integrations",
        "icon": "api",
        "is_hidden": 0,
        "public": 1,
        "sequence_id": 10,
        "title": "Integrations Management",
        
        # Charts
        "charts": [
            {
                "chart_name": "API Usage Trends",
                "label": "API Usage Trends"
            },
            {
                "chart_name": "Cost by Provider",
                "label": "Cost by Provider"
            },
            {
                "chart_name": "Monthly Quota Usage",
                "label": "Monthly Quota Usage"
            }
        ],
        
        # Number Cards
        "number_cards": [
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
        ],
        
        # Links
        "links": [
            {
                "label": "API Providers",
                "type": "Card Break",
                "link_count": 2
            },
            {
                "label": "API Provider",
                "link_to": "API Provider",
                "link_type": "DocType",
                "type": "Link"
            },
            {
                "label": "Integration Settings",
                "link_to": "Integration Settings",
                "link_type": "DocType", 
                "type": "Link"
            },
            {
                "label": "Company Access",
                "type": "Card Break",
                "link_count": 2
            },
            {
                "label": "Company API Access",
                "link_to": "Company API Access",
                "link_type": "DocType",
                "type": "Link"
            },
            {
                "label": "API Usage Log",
                "link_to": "API Usage Log",
                "link_type": "DocType",
                "type": "Link"
            }
        ],
        
        # Shortcuts
        "shortcuts": [
            {
                "color": "Green",
                "doc_view": "New",
                "label": "New API Provider",
                "link_to": "API Provider",
                "type": "DocType"
            },
            {
                "color": "Blue", 
                "doc_view": "List",
                "label": "Company API Access",
                "link_to": "Company API Access",
                "type": "DocType"
            },
            {
                "color": "Purple",
                "label": "Integration Settings",
                "link_to": "Integration Settings",
                "type": "DocType"
            }
        ]
    }
    
    try:
        workspace = frappe.get_doc(workspace_data)
        workspace.insert()
        frappe.db.commit()
        print("✅ Integrations Management Workspace created successfully!")
        return workspace
    except Exception as e:
        print(f"❌ Error creating workspace: {str(e)}")
        return None

def setup_complete_dashboard():
    """Setup complete dashboard with workspace"""
    create_integrations_workspace()
    print("🎉 Complete dashboard setup finished!")