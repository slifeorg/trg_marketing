# Copyright (c) 2024, TRG and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cstr
import json

class Address(Document):
    def validate(self):
        self.validate_address()
        if self.pincode:
            self.set_zipcode_data()
        self.set_validated_address()

    def validate_address(self):
        """Validate address using configured provider"""
        try:
            settings = frappe.get_doc("Geolocation Settings")
            if not settings.enable_address_autocompletion:
                return

            provider = self.get_provider(settings)
            if not provider:
                return

            address_dict = {
                "address_line1": self.address_line1,
                "address_line2": self.address_line2,
                "city": self.city,
                "state": self.state,
                "postal_code": self.pincode,
                "country": self.country
            }

            result = provider.validate_address(address_dict)
            if result:
                self.geocoding_data = json.dumps(result, indent=2)
                if result["status"] == "verified":
                    self.update_from_validation(result)
        except Exception as e:
            frappe.log_error(f"Address validation failed: {str(e)}", "Address Validation")

    def get_provider(self, settings):
        """Get configured address validation provider"""
        provider_mapping = {
            "Geoapify": "geoapify_provider.Geoapify",
            "HERE": "here_provider.Here",
            "Nomatim": "nomatim_provider.Nomatim",
            "Google": "google_provider.GoogleProvider",
            "ShipEngine": "shipengine_provider.ShipEngineProvider",
            "BridgeData": "bridgedata_provider.BridgeDataProvider"
        }

        provider_name = settings.provider
        provider_module = provider_mapping.get(provider_name)

        if not provider_module:
            return None

        try:
            module_path = f"trg_marketing.trg_marketing.doctype.address.providers.{provider_module}"
            provider_class = frappe.get_attr(module_path)
            return provider_class(settings)
        except Exception as e:
            frappe.log_error(f"Failed to load provider {provider_name}: {str(e)}", "Address Provider")

            # Try fallback provider
            if settings.fallback_provider and settings.fallback_provider != provider_name:
                fallback_module = provider_mapping.get(settings.fallback_provider)
                if fallback_module:
                    try:
                        module_path = f"trg_marketing.trg_marketing.doctype.address.providers.{fallback_module}"
                        provider_class = frappe.get_attr(module_path)
                        return provider_class(settings)
                    except Exception as e:
                        frappe.log_error(f"Failed to load fallback provider {settings.fallback_provider}: {str(e)}", "Address Provider")

            return None

    def update_from_validation(self, result):
        """Update address fields from validation result"""
        components = result.get("components", {})
        self.address_line1 = f"{components.get('street_number')} {components.get('street')}".strip()
        self.city = components.get('city') or self.city
        self.state = components.get('state') or self.state
        self.pincode = components.get('postal_code') or self.pincode
        self.country = components.get('country') or self.country

        # Store coordinates if available
        coordinates = result.get("coordinates", {})
        if coordinates.get("latitude") and coordinates.get("longitude"):
            self.latitude = coordinates["latitude"]
            self.longitude = coordinates["longitude"]

    def set_validated_address(self):
        """Format and set the validated address"""
        template = """
        {address_line1}<br>
        {address_line2}<br>
        {city}, {state} {pincode}<br>
        {county}<br>
        {country}
        """
        self.validated_address = template.format(
            address_line1=cstr(self.address_line1),
            address_line2=cstr(self.address_line2 or ""),
            city=cstr(self.city),
            state=cstr(self.state),
            pincode=cstr(self.pincode),
            county=cstr(self.county or ""),
            country=cstr(self.country)
        ).strip()
