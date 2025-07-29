
from frappe.model.document import Document
import frappe
from frappe import _

class APICredential(Document):
    def validate(self):
        self.validate_credential_value()
        
    def validate_credential_value(self):
        """Validate that credential value is not empty"""
        if not self.credential_value:
            frappe.throw(_("Credential value is required"))
            
    def before_save(self):
        """Encrypt sensitive credential data"""
        # Add encryption logic here if needed
        pass
