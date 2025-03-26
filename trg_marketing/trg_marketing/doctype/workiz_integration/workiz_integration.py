# Copyright (c) 2024, TRG and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import re
import requests
import json
from trg_marketing.trg_integrations.doctype.base_integration.base_integration import BaseIntegration

class WorkizIntegration(BaseIntegration):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		lead: DF.Link | None
		workiz_uuid: DF.Data | None
	# end: auto-generated types

	def validate(self):
		super().validate()
		self.validate_uuid()
		self.integration_id = self.workiz_uuid  # Map UUID to integration_id

	def validate_uuid(self):
		"""Validate Workiz UUID format"""
		if self.workiz_uuid:
			uuid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I)
			if not uuid_pattern.match(self.workiz_uuid):
				frappe.throw(_("Invalid Workiz UUID format. Expected format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"))

	def before_save(self):
		super().before_save()
		if self.workiz_uuid and self.api_key:
			self.fetch_external_data()

	def fetch_external_data(self):
		"""Fetch job details from Workiz API"""
		try:
			headers = {
				'Authorization': f'Bearer {self.api_key}',
				'Content-Type': 'application/json'
			}

			url = f"https://api.workiz.com/v1/jobs/{self.workiz_uuid}"
			response = requests.get(url, headers=headers)
			response.raise_for_status()

			job_data = response.json()
			self.api_response = json.dumps(job_data, indent=2)

			# Create or update lead based on job data
			self.create_or_update_lead(job_data)

		except requests.exceptions.RequestException as e:
			frappe.log_error(
				message=f"Workiz API Error: {str(e)}\nResponse: {getattr(e.response, 'text', '')}",
				title="Workiz Integration Error"
			)
			frappe.throw(_("Failed to fetch job details from Workiz. Check error logs for details."))

	def create_or_update_lead(self, job_data):
		"""Create or update lead based on Workiz job data"""
		try:
			customer_data = job_data.get('customer', {})
			if not customer_data:
				return

			lead_name = customer_data.get('name')
			if not lead_name:
				return

			existing_lead = frappe.db.get_value("Lead",
				filters={"workiz_uuid": self.workiz_uuid},
				fieldname=["name"]
			)

			lead_doc = frappe.get_doc("Lead", existing_lead) if existing_lead else frappe.new_doc("Lead")

			lead_doc.update({
				"lead_name": lead_name,
				"company_name": customer_data.get('company_name'),
				"email_id": customer_data.get('email'),
				"mobile_no": customer_data.get('phone'),
				"address_line1": customer_data.get('address', {}).get('street'),
				"city": customer_data.get('address', {}).get('city'),
				"state": customer_data.get('address', {}).get('state'),
				"pincode": customer_data.get('address', {}).get('zip'),
				"country": customer_data.get('address', {}).get('country'),
				"source": "Workiz",
				"workiz_uuid": self.workiz_uuid,
				"status": "Lead"
			})

			lead_doc.save(ignore_permissions=True)
			self.lead = lead_doc.name

			# Create integration request log
			self.create_integration_log(job_data, "Lead", lead_doc.name)

		except Exception as e:
			frappe.log_error(
				message=f"Lead Creation Error: {str(e)}\nWorkiz UUID: {self.workiz_uuid}",
				title="Workiz Lead Creation Error"
			)
			frappe.throw(_("Failed to create/update lead from Workiz data. Check error logs for details."))

@frappe.whitelist()
def sync_workiz_jobs():
	"""Sync all Workiz jobs"""
	integrations = frappe.get_all("Workiz Integration",
		filters={"enabled": 1},
		fields=["name"]
	)

	results = {
		"success": 0,
		"failed": 0,
		"errors": []
	}

	for integration in integrations:
		try:
			doc = frappe.get_doc("Workiz Integration", integration.name)
			doc.fetch_external_data()
			results["success"] += 1
		except Exception as e:
			results["failed"] += 1
			results["errors"].append(f"Integration {integration.name}: {str(e)}")

	return results
