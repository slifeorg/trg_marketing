import frappe
from frappe.model.document import Document

class Agent(Document):
    def before_save(self):
        self.set_full_name()

    def set_full_name(self):
        """Auto-generate full name from first and last name"""
        if self.first_name or self.last_name:
            self.full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()

    def validate(self):
        self.validate_email()

    def validate_email(self):
        """Validate email format"""
        if self.email and not frappe.utils.validate_email_address(self.email):
            frappe.throw("Please enter a valid email address")
