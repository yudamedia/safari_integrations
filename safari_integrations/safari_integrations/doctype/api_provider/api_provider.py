# API Provider Controller
import frappe
from frappe import _
from frappe.model.document import Document

class APIProvider(Document):
    def validate(self):
        self.validate_base_url()
        self.validate_rate_limits()
        
    def validate_base_url(self):
        """Validate that base URL is properly formatted"""
        if self.base_url and not (self.base_url.startswith('http://') or self.base_url.startswith('https://')):
            frappe.throw(_("Base URL must start with http:// or https://"))
            
    def validate_rate_limits(self):
        """Validate rate limit values"""
        if self.rate_limit_per_minute and self.rate_limit_per_minute < 0:
            frappe.throw(_("Rate limit cannot be negative"))
            
    def get_credentials_for_company(self, safari_company):
        """Get API credentials for a specific safari company"""
        access_doc = frappe.get_value("Company API Access", {
            "safari_company": safari_company,
            "api_provider": self.name,
            "is_active": 1
        })
        
        if access_doc:
            return frappe.get_doc("Company API Access", access_doc)
        return None

