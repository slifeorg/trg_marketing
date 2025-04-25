// Copyright (c) 2025, slife and contributors
// For license information, please see license.txt

frappe.ui.form.on("FAQ Acticles", {
	refresh(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__("Compare Versions"), () => {
				new frappe.ui.DiffView("FAQ Acticles", "content", frm.doc.name);
			});
		}

	},
});
