import frappe
from frappe import _
import json

@frappe.whitelist()
def get_property_locations(properties):
    if isinstance(properties, str):
        properties = json.loads(properties)

    property_list = []
    
    for prop_name in properties:
        prop = frappe.get_doc('Property Details', prop_name)
        
        # Extract coordinates from Zillow data if available
        coordinates = extract_coordinates_from_zillow(prop.zillow_data)
        
        if coordinates:
            property_list.append({
                'name': prop.name,
                'year_built': prop.year_built,
                'lead': prop.lead,
                'latitude': coordinates['latitude'],
                'longitude': coordinates['longitude']
            })
    
    return property_list

def extract_coordinates_from_zillow(zillow_data):
    """Extract latitude and longitude from Zillow API response"""
    if not zillow_data:
        return None
        
    try:
        data = json.loads(zillow_data)
        # Adjust this based on actual Zillow API response structure
        return {
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude')
        }
    except:
        return None