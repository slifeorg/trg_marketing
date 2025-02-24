import csv

import frappe
from frappe.model.document import Document


class Zipcode(Document):
    def autoname(self):
        """Set name as zipcode"""
        self.name = self.zipcode

    def validate(self):
        self.validate_zipcode_format()
        self.validate_required_fields()
        self.format_fields()

    def validate_zipcode_format(self):
        """Ensure zipcode is in correct format"""
        if not self.zipcode:
            frappe.throw("Zipcode is required")

        # Remove any spaces or hyphens
        self.zipcode = self.zipcode.replace(" ", "").replace("-", "")

        # Basic US zipcode validation (5 digits or 5+4)
        if not (len(self.zipcode) == 5 or len(self.zipcode) == 9):
            frappe.throw("Invalid zipcode format. Must be 5 digits or 5+4 format")

    def validate_required_fields(self):
        """Ensure all required fields are filled"""
        for field in ['city', 'state', 'county']:
            if not self.get(field):
                frappe.throw(f"{field.title()} is required")

    def format_fields(self):
        """Format fields properly"""
        self.city = self.city.title()
        self.state = self.state.upper()
        self.county = self.county.title()

    @frappe.whitelist()
    def get_geocoding_data(self):
        """Get geocoding data for the zipcode"""
        settings = frappe.get_doc("Geolocation Settings")
        if not settings.enable_address_autocompletion:
            return

        try:
            address_str = f"{self.city}, {self.state} {self.zipcode}, USA"

            if settings.provider == "Geoapify":
                from frappe.integrations.doctype.geolocation_settings.providers.geoapify import Geoapify
                geocoder = Geoapify()
            elif settings.provider == "HERE":
                from frappe.integrations.doctype.geolocation_settings.providers.here import Here
                geocoder = Here()
            elif settings.provider == "Nomatim":
                from frappe.integrations.doctype.geolocation_settings.providers.nomatim import Nomatim
                geocoder = Nomatim()

            return geocoder.geocode(address_str)
        except Exception as e:
            frappe.log_error(f"Zipcode geocoding failed: {str(e)}", "Zipcode Geocoding")

    @frappe.whitelist()
    def get_related_addresses(self):
        """Get all addresses using this zipcode"""
        return frappe.get_all("Address",
            filters={"pincode": self.zipcode},
            fields=["name", "address_line1", "city", "state"]
        )

@frappe.whitelist()
def import_zipcodes(file):
    """Import zipcodes from CSV file"""
    try:
        from frappe.utils.file_manager import get_file

        # Get file content
        fname, fcontent = get_file(file)

        # Read CSV
        decoded_content = fcontent.decode('utf-8').splitlines()
        csv_reader = csv.DictReader(decoded_content)

        success_count = 0
        error_count = 0
        errors = []

        for row in csv_reader:
            try:
                # Check if zipcode already exists
                if frappe.db.exists("Zipcode", row.get("zipcode")):
                    doc = frappe.get_doc("Zipcode", row.get("zipcode"))
                else:
                    doc = frappe.new_doc("Zipcode")

                # Update fields
                doc.update({
                    "zipcode": row.get("zipcode"),
                    "city": row.get("city"),
                    "state": row.get("state"),
                    "county": row.get("county"),
                    "website": row.get("website")
                })

                doc.save()
                success_count += 1

            except Exception as e:
                error_count += 1
                errors.append(f"Row {csv_reader.line_num}: {str(e)}")

        return {
            "success_count": success_count,
            "error_count": error_count,
            "errors": errors
        }

    except Exception as e:
        frappe.throw(f"Error importing zipcodes: {str(e)}")
