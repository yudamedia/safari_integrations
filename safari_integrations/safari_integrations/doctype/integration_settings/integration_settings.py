import frappe
from frappe import _
from frappe.model.document import Document

class IntegrationSettings(Document):
    def validate(self):
        self.validate_thresholds()
        
    def validate_thresholds(self):
        """Validate threshold values"""
        if self.alert_threshold_percentage < 0 or self.alert_threshold_percentage > 100:
            frappe.throw(_("Alert threshold percentage must be between 0 and 100"))
            
        if self.default_monthly_quota < 0:
            frappe.throw(_("Default monthly quota cannot be negative"))