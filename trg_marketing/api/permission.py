import frappe

def has_app_permission():
    """Check if user has permission to access TRG Marketing app"""
    return frappe.has_permission("TRG Marketing Settings", "read")
