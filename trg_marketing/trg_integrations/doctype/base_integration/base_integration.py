import frappe
from frappe.model.document import Document
import json
from frappe import _
from frappe.utils import now_datetime

class BaseIntegration(Document):
    def validate(self):
        self.validate_api_key()
        
    def validate_api_key(self):
        if not self.api_key:
            frappe.throw(_("API Key is required"))
            
    def before_save(self):
        self.last_sync = now_datetime()
        
    def fetch_external_data(self):
        """Abstract method to be implemented by child classes"""
        raise NotImplementedError
        
    def create_integration_log(self, data, reference_doctype=None, reference_docname=None):
        """Create integration request log"""
        try:
            log = frappe.new_doc("Integration Request")
            log.update({
                "integration_request_service": self.doctype,
                "status": "Completed",
                "reference_doctype": reference_doctype,
                "reference_docname": reference_docname,
                "data": json.dumps(data, indent=2),
                "output": json.dumps({
                    "message": f"Successfully synced {self.doctype}",
                    "timestamp": str(now_datetime())
                }, indent=2)
            })
            log.insert(ignore_permissions=True)
            
        except Exception as e:
            frappe.log_error(
                message=f"Integration Log Error: {str(e)}\nIntegration: {self.name}",
                title=f"{self.doctype} Integration Log Error"
            )