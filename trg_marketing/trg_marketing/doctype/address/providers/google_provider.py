import requests
from .base_provider import BaseAddressProvider
import frappe
from frappe import _

class GoogleProvider(BaseAddressProvider):
    def validate_settings(self):
        if not self.settings.google_api_key:
            frappe.throw(_("Google API Key is required for Google Geocoding"))

    def geocode(self, address_str):
        try:
            url = "https://maps.googleapis.com/maps/api/geocode/json"
            params = {
                "address": address_str,
                "key": self.settings.google_api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            result = response.json()
            
            if result["status"] != "OK":
                frappe.log_error(
                    f"Google Geocoding Error: {result['status']} - {result.get('error_message', '')}",
                    "Google Geocoding"
                )
                return None
                
            location = result["results"][0]["geometry"]["location"]
            components = self._extract_address_components(result["results"][0]["address_components"])
            
            return self.format_response({
                "status": "verified",
                "lat": location["lat"],
                "lon": location["lng"],
                "formatted_address": result["results"][0]["formatted_address"],
                **components
            })
            
        except Exception as e:
            frappe.log_error(f"Google Geocoding Error: {str(e)}", "Google Geocoding")
            return None

    def validate_address(self, address_dict):
        address_str = ", ".join(filter(None, [
            address_dict.get("address_line1"),
            address_dict.get("city"),
            address_dict.get("state"),
            address_dict.get("postal_code"),
            address_dict.get("country")
        ]))
        return self.geocode(address_str)

    def _extract_address_components(self, components):
        result = {
            "street_number": "",
            "street": "",
            "city": "",
            "state": "",
            "postal_code": "",
            "country": ""
        }
        
        component_mapping = {
            "street_number": "street_number",
            "route": "street",
            "locality": "city",
            "administrative_area_level_1": "state",
            "postal_code": "postal_code",
            "country": "country"
        }
        
        for component in components:
            for type in component["types"]:
                if type in component_mapping:
                    result[component_mapping[type]] = component["long_name"]
                    
        return result