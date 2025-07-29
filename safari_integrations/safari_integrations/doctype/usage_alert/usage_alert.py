
from frappe.model.document import Document
import frappe
from frappe import _

class UsageAlert(Document):
    def validate(self):
        self.validate_threshold()
        
    def validate_threshold(self):
        """Validate threshold percentage"""
        if self.threshold_percentage < 0 or self.threshold_percentage > 100:
            frappe.throw(_("Threshold percentage must be between 0 and 100"))
