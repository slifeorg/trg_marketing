import requests
from .base_provider import BaseAddressProvider
import frappe
from frappe import _

class BridgeDataProvider(BaseAddressProvider):
    def validate_settings(self):
        if not self.settings.bridgedata_api_key:
            frappe.throw(_("BridgeData API Key is required for address validation"))

    def geocode(self, address_str):
        try:
            url = "https://api.bridgedataoutput.com/api/v2/pub/assessments"
            params = {
                "access_token": self.settings.bridgedata_api_key,
                "address.full": address_str
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            result = response.json()
            
            if result.get("status", {}).get("code") != 0:
                return None
                
            if not result.get("bundle"):
                return None
                
            property_data = result["bundle"][0]
            address = property_data.get("address", {})
            
            return self.format_response({
                "status": "verified",
                "lat": address.get("latitude"),
                "lon": address.get("longitude"),
                "street_number": address.get("number"),
                "street": address.get("street"),
                "city": address.get("city"),
                "state": address.get("state"),
                "postal_code": address.get("zip"),
                "country": "US",
                "formatted_address": self._format_address(address)
            })
            
        except Exception as e:
            frappe.log_error(f"BridgeData Error: {str(e)}", "BridgeData Address Validation")
            return None

    def validate_address(self, address_dict):
        address_str = ", ".join(filter(None, [
            address_dict.get("address_line1"),
            address_dict.get("city"),
            address_dict.get("state"),
            address_dict.get("postal_code"),
            "USA"
        ]))
        return self.geocode(address_str)

    def _format_address(self, address):
        return f"{address.get('number')} {address.get('street')}, {address.get('city')}, {address.get('state')} {address.get('zip')}, USA"