# Copyright (c) 2024, TRG and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class NewLead(Document):
    def validate(self):
        if not self.lead_id:
            frappe.throw("Lead ID is required")

    def on_submit(self):
        # Add any submission logic here
        pass

    def on_cancel(self):
        # Add any cancellation logic here
        pass
