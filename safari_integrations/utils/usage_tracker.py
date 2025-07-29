import frappe
from frappe import _
from frappe.utils import today, get_first_day, flt, now_datetime
from datetime import datetime

def send_quota_alerts():
    """Send quota alerts to companies approaching their limits - called by scheduler"""
    try:
        # Get all active company API accesses
        api_accesses = frappe.get_all("Company API Access",
            filters={"is_active": 1},
            fields=["name", "safari_company", "api_provider", "monthly_quota"]
        )
        
        alerts_sent = 0
        
        for access in api_accesses:
            try:
                access_doc = frappe.get_doc("Company API Access", access.name)
                
                # Calculate current usage
                current_usage = get_monthly_usage(access.safari_company, access.api_provider)
                usage_percentage = (current_usage / access.monthly_quota) * 100 if access.monthly_quota > 0 else 0
                
                # Check each alert threshold
                for alert in access_doc.usage_alerts:
                    if alert.is_active and usage_percentage >= alert.threshold_percentage:
                        if should_send_alert(access.safari_company, access.api_provider, alert.alert_type):
                            send_usage_alert(access_doc, alert, current_usage, usage_percentage)
                            alerts_sent += 1
                            
            except Exception as e:
                frappe.log_error(f"Error processing alerts for {access.name}: {str(e)}")
                
        if alerts_sent > 0:
            frappe.logger().info(f"Sent {alerts_sent} quota alerts")
            
    except Exception as e:
        frappe.log_error(f"Error sending quota alerts: {str(e)}", "Usage Tracker Error")

def get_monthly_usage(safari_company, api_provider, month=None, year=None):
    """Get monthly API usage count for a company and provider"""
    try:
        if not month:
            month = datetime.now().month
        if not year:
            year = datetime.now().year
            
        first_day = get_first_day(f"{year}-{month:02d}-01")
        
        usage_count = frappe.db.count("API Usage Log", {
            "safari_company": safari_company,
            "api_provider": api_provider,
            "creation": [">=", first_day]
        })
        
        return usage_count
        
    except Exception as e:
        frappe.log_error(f"Error getting monthly usage: {str(e)}")
        return 0

def should_send_alert(safari_company, api_provider, alert_type):
    """Check if alert should be sent (avoid spam)"""
    try:
        # Check if similar alert was sent in last 24 hours
        last_alert = frappe.db.get_value("API Usage Log",
            filters={
                "safari_company": safari_company,
                "api_provider": api_provider,
                "error_message": ["like", f"%{alert_type}%"],
                "creation": [">=", frappe.utils.add_days(now_datetime(), -1)]
            },
            fieldname="creation"
        )
        
        return not last_alert
        
    except Exception as e:
        frappe.log_error(f"Error checking alert frequency: {str(e)}")
        return True  # Default to sending alert

def send_usage_alert(access_doc, alert, current_usage, usage_percentage):
    """Send usage alert notification"""
    try:
        safari_company = access_doc.safari_company
        api_provider = access_doc.api_provider
        
        # Get company details for email
        company_doc = frappe.get_doc("Safari Company", safari_company)
        recipients = []
        
        if hasattr(company_doc, 'email') and company_doc.email:
            recipients.append(company_doc.email)
            
        # Add system administrators
        admin_users = frappe.get_all("User", 
            filters={"role_profile_name": "System Manager", "enabled": 1},
            fields=["email"]
        )
        recipients.extend([user.email for user in admin_users if user.email])
        
        if not recipients:
            frappe.log_error(f"No recipients found for quota alert: {safari_company}")
            return
            
        # Prepare email content
        subject = f"API Quota Alert - {alert.alert_type} for {api_provider}"
        
        message = f"""
        <h3>API Usage Alert</h3>
        <p><strong>Company:</strong> {safari_company}</p>
        <p><strong>API Provider:</strong> {api_provider}</p>
        <p><strong>Alert Type:</strong> {alert.alert_type}</p>
        
        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0;">
            <h4>Usage Summary</h4>
            <p><strong>Current Usage:</strong> {current_usage:,} calls</p>
            <p><strong>Monthly Quota:</strong> {access_doc.monthly_quota:,} calls</p>
            <p><strong>Usage Percentage:</strong> {usage_percentage:.1f}%</p>
            <p><strong>Remaining:</strong> {max(0, access_doc.monthly_quota - current_usage):,} calls</p>
        </div>
        
        <p>Please review your API usage and consider optimizing calls or requesting a quota increase if necessary.</p>
        
        <p><small>This alert was triggered at {usage_percentage:.1f}% usage threshold.</small></p>
        """
        
        # Send email based on notification method
        if alert.notification_method == "Email":
            frappe.sendmail(
                recipients=recipients,
                subject=subject,
                message=message
            )
            
        # Log the alert
        frappe.logger().info(f"Quota alert sent: {safari_company} - {api_provider} at {usage_percentage:.1f}%")
        
        # Create a usage log entry for tracking
        frappe.get_doc({
            "doctype": "API Usage Log",
            "safari_company": safari_company,
            "api_provider": api_provider,
            "endpoint": "system/quota-alert",
            "request_method": "SYSTEM",
            "response_status": 200,
            "cost_incurred": 0,
            "user": "System",
            "error_message": f"Quota Alert Sent: {alert.alert_type} at {usage_percentage:.1f}%"
        }).insert(ignore_permissions=True)
        
    except Exception as e:
        frappe.log_error(f"Error sending usage alert: {str(e)}", "Usage Alert Error")

@frappe.whitelist()
def check_remaining_quota(safari_company, api_provider):
    """Check remaining quota for a company and provider"""
    try:
        access_doc = frappe.get_doc("Company API Access", {
            "safari_company": safari_company,
            "api_provider": api_provider
        })
        
        current_usage = get_monthly_usage(safari_company, api_provider)
        remaining = max(0, access_doc.monthly_quota - current_usage)
        usage_percentage = (current_usage / access_doc.monthly_quota) * 100 if access_doc.monthly_quota > 0 else 0
        
        return {
            "success": True,
            "monthly_quota": access_doc.monthly_quota,
            "current_usage": current_usage,
            "remaining_quota": remaining,
            "usage_percentage": usage_percentage,
            "quota_exceeded": remaining == 0
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "remaining_quota": 0,
            "quota_exceeded": True
        }

@frappe.whitelist()
def get_usage_analytics(safari_company, api_provider=None, days=30):
    """Get comprehensive usage analytics"""
    try:
        from frappe.utils import add_days
        
        end_date = today()
        start_date = add_days(end_date, -days)
        
        filters = {
            "safari_company": safari_company,
            "creation": ["between", [start_date, end_date]]
        }
        
        if api_provider:
            filters["api_provider"] = api_provider
        
        # Get usage statistics
        usage_data = frappe.db.sql("""
            SELECT 
                api_provider,
                COUNT(*) as total_calls,
                SUM(CASE WHEN response_status < 400 THEN 1 ELSE 0 END) as successful_calls,
                SUM(CASE WHEN response_status >= 400 THEN 1 ELSE 0 END) as failed_calls,
                AVG(response_time_ms) as avg_response_time,
                SUM(cost_incurred) as total_cost
            FROM `tabAPI Usage Log`
            WHERE safari_company = %(safari_company)s
            AND DATE(creation) BETWEEN %(start_date)s AND %(end_date)s
            {provider_filter}
            GROUP BY api_provider
        """.format(
            provider_filter="AND api_provider = %(api_provider)s" if api_provider else ""
        ), {
            "safari_company": safari_company,
            "start_date": start_date,
            "end_date": end_date,
            "api_provider": api_provider
        }, as_dict=True)
        
        return {
            "success": True,
            "period": f"{start_date} to {end_date}",
            "analytics": usage_data
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting usage analytics: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "analytics": []
        }

def update_quota_usage(doc, method=None):
    """Update quota usage after API log insertion"""
    try:
        # This is called after each API Usage Log insertion
        # You can add real-time quota checking here
        access_doc = frappe.get_doc("Company API Access", {
            "safari_company": doc.safari_company,
            "api_provider": doc.api_provider
        })
        
        current_usage = get_monthly_usage(doc.safari_company, doc.api_provider)
        
        # Check if quota is exceeded
        if current_usage >= access_doc.monthly_quota:
            frappe.logger().warning(f"Quota exceeded for {doc.safari_company} - {doc.api_provider}")
            
    except Exception as e:
        frappe.log_error(f"Error updating quota usage: {str(e)}")