// Copyright (c) 2024, TRG and contributors
// For license information, please see license.txt

frappe.ui.form.on('Property Details', {
	refresh: function(frm) {
		// Add custom client-side logic here
	},

	year_built: function(frm) {
		if (frm.doc.year_built) {
			const currentYear = new Date().getFullYear();
			if (frm.doc.year_built > currentYear) {
				frappe.msgprint(__('Year Built cannot be in the future'));
				frm.doc.year_built = '';
				frm.refresh_field('year_built');
			}
			if (frm.doc.year_built < 1800) {
				frappe.msgprint(__('Year Built seems too old. Please verify the year.'));
			}
		}
	}
});
