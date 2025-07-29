import frappe

def create_simple_workspace():
    """Create a simplified Integrations Management workspace"""
    
    print("🚀 Creating Simple Integrations Management Workspace...")
    
    if frappe.db.exists("Workspace", "Integrations Management"):
        print("⚠️  Workspace already exists, updating...")
        workspace = frappe.get_doc("Workspace", "Integrations Management")
    else:
        workspace = frappe.get_doc({
            "doctype": "Workspace",
            "name": "Integrations Management",
            "label": "Integrations Management",
            "module": "Safari Integrations",
            "icon": "api",
            "is_hidden": 0,
            "public": 1,
            "sequence_id": 10,
            "title": "Integrations Management"
        })
    
    # Add charts
    workspace.charts = []
    workspace.append("charts", {
        "chart_name": "API Usage Trends",
        "label": "API Usage Trends"
    })
    workspace.append("charts", {
        "chart_name": "Cost by Provider", 
        "label": "Cost by Provider"
    })
    workspace.append("charts", {
        "chart_name": "Monthly Quota Usage",
        "label": "Monthly Quota Usage"
    })
    
    # Add number cards
    workspace.number_cards = []
    workspace.append("number_cards", {
        "number_card_name": "Active API Providers",
        "label": "Active API Providers"
    })
    workspace.append("number_cards", {
        "number_card_name": "Total API Calls Today",
        "label": "Total API Calls Today"
    })
    workspace.append("number_cards", {
        "number_card_name": "Monthly API Costs",
        "label": "Monthly API Costs"
    })
    workspace.append("number_cards", {
        "number_card_name": "Companies with Access",
        "label": "Companies with Access"
    })
    
    # Add basic links
    workspace.links = []
    workspace.append("links", {
        "label": "API Management",
        "type": "Card Break",
        "link_count": 3
    })
    workspace.append("links", {
        "label": "API Provider",
        "link_to": "API Provider",
        "link_type": "DocType",
        "type": "Link"
    })
    workspace.append("links", {
        "label": "Company API Access", 
        "link_to": "Company API Access",
        "link_type": "DocType",
        "type": "Link"
    })
    workspace.append("links", {
        "label": "API Usage Log",
        "link_to": "API Usage Log",
        "link_type": "DocType",
        "type": "Link"
    })
    
    # Add shortcuts
    workspace.shortcuts = []
    workspace.append("shortcuts", {
        "color": "Green",
        "doc_view": "New",
        "label": "New API Provider",
        "link_to": "API Provider",
        "type": "DocType"
    })
    workspace.append("shortcuts", {
        "color": "Blue",
        "doc_view": "List", 
        "label": "Company API Access",
        "link_to": "Company API Access",
        "type": "DocType"
    })
    
    try:
        if frappe.db.exists("Workspace", "Integrations Management"):
            workspace.save()
            print("🔄 Updated existing workspace")
        else:
            workspace.insert()
            print("✅ Created new workspace")
            
        frappe.db.commit()
        print("✅ Integrations Management Workspace setup completed!")
        return workspace
        
    except Exception as e:
        print(f"❌ Error with workspace: {str(e)}")
        return None