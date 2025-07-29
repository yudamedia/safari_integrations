#!/usr/bin/env python3

import frappe

def verify_dashboard_components():
    """Verify all dashboard components are created"""
    
    print("🔍 Verifying Safari Integrations Dashboard Components...")
    print("=" * 60)
    
    # Check Number Cards
    print("\n📊 Number Cards:")
    number_cards = [
        "Active API Providers",
        "Total API Calls Today", 
        "Monthly API Costs",
        "Companies with Access"
    ]
    
    for card_name in number_cards:
        exists = frappe.db.exists("Number Card", card_name)
        status = "✅ Exists" if exists else "❌ Missing"
        print(f"   {card_name}: {status}")
    
    # Check Dashboard Charts
    print("\n📈 Dashboard Charts:")
    charts = [
        "API Usage Trends",
        "Cost by Provider",
        "Monthly Quota Usage"
    ]
    
    for chart_name in charts:
        exists = frappe.db.exists("Dashboard Chart", chart_name)
        status = "✅ Exists" if exists else "❌ Missing"
        print(f"   {chart_name}: {status}")
        
        if exists:
            chart = frappe.get_doc("Dashboard Chart", chart_name)
            print(f"      Type: {chart.chart_type}, Document: {chart.document_type}")
    
    # Check Workspace
    print("\n⚙️  Workspace Configuration:")
    workspace_exists = frappe.db.exists("Workspace", "Integrations Management")
    print(f"   Integrations Management: {'✅ Exists' if workspace_exists else '❌ Missing'}")
    
    if workspace_exists:
        workspace = frappe.get_doc("Workspace", "Integrations Management")
        print(f"   Charts in workspace: {len(workspace.charts)}")
        print(f"   Number cards in workspace: {len(workspace.number_cards)}")
    
    print("\n🎯 Summary:")
    total_cards = len([card for card in number_cards if frappe.db.exists("Number Card", card)])
    total_charts = len([chart for chart in charts if frappe.db.exists("Dashboard Chart", chart)])
    
    print(f"   Number Cards: {total_cards}/{len(number_cards)}")
    print(f"   Dashboard Charts: {total_charts}/{len(charts)}")
    print(f"   Workspace: {'✅' if workspace_exists else '❌'}")
    
    if total_cards == len(number_cards) and total_charts == len(charts) and workspace_exists:
        print("\n🎉 All dashboard components are successfully created!")
    else:
        print("\n⚠️  Some components may be missing or need attention.")

if __name__ == "__main__":
    frappe.init(site="safarierp", sites_path="/home/erpnext/frappe-bench/sites")
    frappe.connect()
    verify_dashboard_components()
    frappe.destroy()