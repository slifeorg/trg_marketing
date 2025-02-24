// Copyright (c) 2024, TRG and contributors
// For license information, please see license.txt

frappe.ui.form.on('Address', {
	refresh: function(frm) {
		// Add Validate Address button
		frm.add_custom_button(__('Validate Address'), function() {
			frm.save().then(() => {
				frappe.show_alert({
					message: __('Address validated successfully'),
					indicator: 'green'
				});
			});
		});

		// Show geocoding data in a formatted way
		if (frm.doc.geocoding_data) {
			try {
				let data = JSON.parse(frm.doc.geocoding_data);
				let html = '<div class="geocoding-data">';
				if (data.latitude) html += `<p><strong>Latitude:</strong> ${data.latitude}</p>`;
				if (data.longitude) html += `<p><strong>Longitude:</strong> ${data.longitude}</p>`;
				if (data.confidence) html += `<p><strong>Confidence:</strong> ${data.confidence}</p>`;
				html += '</div>';
				$(frm.fields_dict.geocoding_data.wrapper).html(html);
			} catch (e) {
				console.error('Error parsing geocoding data:', e);
			}
		}
	},

	pincode: function(frm) {
		if (frm.doc.pincode) {
			frappe.db.get_value('Zipcode', frm.doc.pincode, ['city', 'state', 'county'])
				.then(r => {
					if (r.message) {
						if (!frm.doc.city) frm.set_value('city', r.message.city);
						if (!frm.doc.state) frm.set_value('state', r.message.state);
						if (!frm.doc.county) frm.set_value('county', r.message.county);
					}
				});
		}
	},

	validate: function(frm) {
		// Required fields validation
		let required_fields = ['address_line1', 'city', 'state', 'pincode', 'country'];
		let missing_fields = required_fields.filter(field => !frm.doc[field]);

		if (missing_fields.length > 0) {
			frappe.msgprint({
				title: __('Required Fields Missing'),
				message: __('Please fill in the following required fields: {0}',
					[missing_fields.join(', ')]),
				indicator: 'red'
			});
			frappe.validated = false;
		}
	}
});
