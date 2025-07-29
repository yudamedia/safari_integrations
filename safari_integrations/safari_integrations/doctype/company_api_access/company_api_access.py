import frappe
from frappe import _
from frappe.model.document import Document

class CompanyAPIAccess(Document):
    def validate(self):
        self.validate_unique_access()
        self.validate_quota_limits()
        
    def validate_unique_access(self):
        """Ensure unique combination of company and provider"""
        existing = frappe.db.exists("Company API Access", {
            "safari_company": self.safari_company,
            "api_provider": self.api_provider,
            "name": ["!=", self.name]
        })
        
        if existing:
            frappe.throw(_("API access already exists for this company and provider"))
            
    def validate_quota_limits(self):
        """Validate quota limits"""
        if self.monthly_quota and self.monthly_quota < 0:
            frappe.throw(_("Monthly quota cannot be negative"))
            
    def get_remaining_quota(self):
        """Calculate remaining quota for current month"""
        from frappe.utils import get_first_day, today
        
        first_day = get_first_day(today())
        
        used_quota = frappe.db.count("API Usage Log", {
            "safari_company": self.safari_company,
            "api_provider": self.api_provider,
            "creation": [">=", first_day]
        })
        
        return max(0, self.monthly_quota - used_quota)
        
    def check_quota_exceeded(self):
        """Check if quota is exceeded"""
        return self.get_remaining_quota() == 0