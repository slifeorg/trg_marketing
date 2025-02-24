# Copyright (c) 2024, TRG and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class PropertyDetails(Document):
	def validate(self):
		if self.year_built:
			current_year = datetime.now().year
			if self.year_built > current_year:
				frappe.throw(f"Year Built cannot be in the future. Current year is {current_year}")
			if self.year_built < 1800:
				frappe.throw("Year Built seems too old. Please verify the year.")
