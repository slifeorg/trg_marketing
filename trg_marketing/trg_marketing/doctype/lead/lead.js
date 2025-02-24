frappe.ui.form.on('Lead', {
    refresh: function(frm) {
        // Add custom buttons
        if(!frm.is_new()) {
            frm.add_custom_button(__('Create Appointment'), function() {
                frappe.new_doc('Appointment', {
                    lead: frm.doc.name,
                    customer_name: frm.doc.customer_name
                });
            });
            
            frm.add_custom_button(__('View Property Details'), function() {
                if(frm.doc.property_details) {
                    frappe.set_route('Form', 'Property Details', frm.doc.property_details);
                } else {
                    frappe.msgprint(__('No property details linked to this lead'));
                }
            });
        }
    },

    validate: function(frm) {
        // Custom validations
        if(frm.doc.phone_number && frm.doc.phone_number.length !== 10) {
            frappe.msgprint(__('Phone number should be 10 digits'));
            frappe.validated = false;
        }
    },

    phone_number: function(frm) {
        // Format phone number
        if(frm.doc.phone_number) {
            frm.doc.phone_number = frm.doc.phone_number.replace(/\D/g, '');
            frm.refresh_field('phone_number');
        }
    },

    alternate_phone_number: function(frm) {
        // Format alternate phone number
        if(frm.doc.alternate_phone_number) {
            frm.doc.alternate_phone_number = frm.doc.alternate_phone_number.replace(/\D/g, '');
            frm.refresh_field('alternate_phone_number');
        }
    }
});

frappe.ui.form.on('Lead Salesman', {
    salesmen_add: function(frm, cdt, cdn) {
        // Logic when adding new salesman
        let row = locals[cdt][cdn];
        // Add any initialization logic
    },

    salesman: function(frm, cdt, cdn) {
        // Logic when salesman is selected
        let row = locals[cdt][cdn];
        // Add validation or additional logic
    }
});