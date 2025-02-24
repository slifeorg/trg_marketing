import frappe
from frappe.model.document import Document
from frappe.utils import validate_phone_number

class Lead(Document):
    def validate(self):
        self.validate_phone_numbers()
        self.validate_state()
        self.validate_salesmen()

    def validate_phone_numbers(self):
        """Validate phone number format"""
        if self.phone_number:
            if not self.phone_number.isdigit():
                frappe.throw("Phone Number should contain only digits")
            if len(self.phone_number) != 10:
                frappe.throw("Phone Number should be 10 digits long")

        if self.alternate_phone_number:
            if not self.alternate_phone_number.isdigit():
                frappe.throw("Alternate Phone Number should contain only digits")
            if len(self.alternate_phone_number) != 10:
                frappe.throw("Alternate Phone Number should be 10 digits long")

    def validate_state(self):
        """Ensure state is uppercase and valid"""
        if self.state:
            self.state = self.state.upper()
            # Add additional state validation if needed

    def validate_salesmen(self):
        """Validate salesmen assignments"""
        if self.salesmen:
            assigned_salesmen = []
            for salesman in self.salesmen:
                if salesman.salesman in assigned_salesmen:
                    frappe.throw(f"Salesman {salesman.salesman} is assigned multiple times")
                assigned_salesmen.append(salesman.salesman)

    def before_save(self):
        """Actions before saving the document"""
        self.update_property_details()

    def update_property_details(self):
        """Update property details if needed"""
        if self.property_details:
            # Add logic to update property details
            pass

    def after_insert(self):
        """Actions after inserting new lead"""
        self.create_customer_info()
        self.notify_salesmen()

    def create_customer_info(self):
        """Create customer info record if not exists"""
        if not self.customer_info:
            customer_info = frappe.get_doc({
                "doctype": "Customer Info",
                "lead": self.name,
                "homeowner_name": self.customer_name
            })
            customer_info.insert()
            self.customer_info = customer_info.name
            self.save()

    def notify_salesmen(self):
        """Notify assigned salesmen"""
        if self.salesmen:
            for salesman in self.salesmen:
                frappe.sendmail(
                    recipients=[frappe.db.get_value("User", salesman.salesman, "email")],
                    subject=f"New Lead Assigned - {self.customer_name}",
                    message=f"""
                        Dear {salesman.salesman},

                        A new lead has been assigned to you:

                        Customer: {self.customer_name}
                        Address: {self.street}
                        Phone: {self.phone_number}

                        Please follow up accordingly.

                        Regards,
                        System
                    """
                )
