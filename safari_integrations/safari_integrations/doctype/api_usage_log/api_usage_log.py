


import frappe
from frappe import _
from frappe.model.document import Document

class APIUsageLog(Document):
    def validate(self):
        self.validate_response_status()
        self.set_user_if_not_set()
        
    def validate_response_status(self):
        """Validate HTTP response status codes"""
        if self.response_status and (self.response_status < 100 or self.response_status > 599):
            frappe.throw(_("Invalid HTTP response status code"))
            
    def set_user_if_not_set(self):
        """Set current user if not already set"""
        if not self.user:
            self.user = frappe.session.user
            
    def after_insert(self):
        """Check quota and send alerts after logging usage"""
        self.check_and_send_quota_alerts()
        
    def check_and_send_quota_alerts(self):
        """Check if quota alerts need to be sent"""
        try:
            access_doc = frappe.get_doc("Company API Access", {
                "safari_company": self.safari_company,
                "api_provider": self.api_provider
            })
            
            remaining_quota = access_doc.get_remaining_quota()
            quota_percentage = (remaining_quota / access_doc.monthly_quota) * 100
            
            # Check alerts
            for alert in access_doc.usage_alerts:
                if alert.is_active and quota_percentage <= alert.threshold_percentage:
                    self.send_quota_alert(alert, quota_percentage)
                    
        except Exception as e:
            frappe.log_error(f"Error checking quota alerts: {str(e)}")
            
    def send_quota_alert(self, alert, quota_percentage):
        """Send quota alert notification"""
        # Implementation for sending alerts
        frappe.log_error(f"Quota alert: {alert.alert_type} at {quota_percentage}%")
