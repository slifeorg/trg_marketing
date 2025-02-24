// Copyright (c) 2024, TRG and contributors
// For license information, please see license.txt

frappe.ui.form.on('NewLead', {
	refresh: function(frm) {
		// Add custom button or logic on form refresh
	},

	lead_id: function(frm) {
		// Validate lead_id format if needed
	},

	new_lead_category: function(frm) {
		// Add any category change related logic
	},

	lead_rating: function(frm) {
		// Add any rating change related logic
	}
});
