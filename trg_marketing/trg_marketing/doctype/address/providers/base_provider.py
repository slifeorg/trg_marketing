from abc import ABC, abstractmethod
import frappe

class BaseAddressProvider(ABC):
    def __init__(self, settings=None):
        self.settings = settings or frappe.get_doc("Geolocation Settings")
        self.validate_settings()

    @abstractmethod
    def validate_settings(self):
        """Validate provider-specific settings"""
        pass

    @abstractmethod
    def geocode(self, address_str):
        """Geocode the address"""
        pass

    @abstractmethod
    def validate_address(self, address_dict):
        """Validate address details"""
        pass

    def format_response(self, data):
        """Format provider response to standard format"""
        return {
            "status": data.get("status", "unknown"),
            "coordinates": {
                "latitude": data.get("lat"),
                "longitude": data.get("lon")
            },
            "formatted_address": data.get("formatted_address"),
            "components": {
                "street_number": data.get("street_number"),
                "street": data.get("street"),
                "city": data.get("city"),
                "state": data.get("state"),
                "postal_code": data.get("postal_code"),
                "country": data.get("country")
            },
            "metadata": {
                "provider": self.__class__.__name__,
                "raw_response": data
            }
        }