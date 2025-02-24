// Copyright (c) 2024, TRG and contributors
// For license information, please see license.txt

frappe.ui.form.on('Customer Info', {
	refresh: function(frm) {
		// Add custom client-side logic here
	},
	
	contact_number: function(frm) {
		// Format phone number if needed
		if (frm.doc.contact_number) {
			frm.doc.contact_number = frm.doc.contact_number.replace(/\D/g, '');
			frm.refresh_field('contact_number');
		}
	}
});
