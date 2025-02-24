# Copyright (c) 2024, TRG and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CustomerInfo(Document):
	def validate(self):
		if self.contact_number:
			# Remove any non-numeric characters from phone number
			self.contact_number = ''.join(filter(str.isdigit, self.contact_number))
