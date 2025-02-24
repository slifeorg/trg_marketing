import requests
from .base_provider import BaseAddressProvider
import frappe
from frappe import _

class ShipEngineProvider(BaseAddressProvider):
    def validate_settings(self):
        if not self.settings.shipengine_api_key:
            frappe.throw(_("ShipEngine API Key is required for address validation"))

    def geocode(self, address_str):
        # ShipEngine doesn't provide geocoding
        # We'll validate the address and return what we can
        address_parts = self._parse_address_string(address_str)
        return self.validate_address(address_parts)

    def validate_address(self, address_dict):
        try:
            url = "https://api.shipengine.com/v1/addresses/validate"
            headers = {
                "API-Key": self.settings.shipengine_api_key,
                "Content-Type": "application/json"
            }
            
            payload = [{
                "address_line1": address_dict.get("address_line1"),
                "address_line2": address_dict.get("address_line2", ""),
                "city_locality": address_dict.get("city"),
                "state_province": address_dict.get("state"),
                "postal_code": address_dict.get("postal_code"),
                "country_code": address_dict.get("country", "US")
            }]

            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()[0]

            if result["status"] == "verified":
                matched = result["matched_address"]
                return self.format_response({
                    "status": "verified",
                    "street_number": "",  # ShipEngine doesn't separate these
                    "street": matched["address_line1"],
                    "city": matched["city_locality"],
                    "state": matched["state_province"],
                    "postal_code": matched["postal_code"],
                    "country": matched["country_code"],
                    "formatted_address": self._format_address(matched)
                })
            
            return None

        except Exception as e:
            frappe.log_error(f"ShipEngine Validation Error: {str(e)}", "ShipEngine Address Validation")
            return None

    def _parse_address_string(self, address_str):
        # Basic address parser - could be enhanced
        parts = address_str.split(',')
        result = {
            "address_line1": parts[0].strip() if len(parts) > 0 else "",
            "city": parts[1].strip() if len(parts) > 1 else "",
            "state": "",
            "postal_code": "",
            "country": "US"
        }
        
        if len(parts) > 2:
            state_zip = parts[2].strip().split()
            result["state"] = state_zip[0] if len(state_zip) > 0 else ""
            result["postal_code"] = state_zip[1] if len(state_zip) > 1 else ""
            
        return result

    def _format_address(self, address):
        return f"{address['address_line1']}, {address['city_locality']}, {address['state_province']} {address['postal_code']}, {address['country_code']}"