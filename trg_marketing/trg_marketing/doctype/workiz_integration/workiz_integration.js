// Copyright (c) 2024, TRG and contributors
// For license information, please see license.txt

frappe.ui.form.on('Workiz Integration', {
	refresh: function(frm) {
		// Add custom buttons
		if (frm.doc.workiz_uuid && frm.doc.api_key) {
			frm.add_custom_button(__('Sync Now'), function() {
				frm.save().then(() => {
					frappe.show_alert({
						message: __('Syncing with Workiz...'),
						indicator: 'blue'
					});
				});
			});
		}

		// Add button to view lead if exists
		if (frm.doc.lead) {
			frm.add_custom_button(__('View Lead'), function() {
				frappe.set_route('Form', 'Lead', frm.doc.lead);
			}, __('Actions'));
		}

		// Add button to sync all jobs
		if (frm.doc.api_key) {
			frm.add_custom_button(__('Sync All Jobs'), function() {
				frappe.call({
					method: 'trg_marketing.trg_marketing.doctype.workiz_integration.workiz_integration.sync_workiz_jobs',
					callback: function(r) {
						if (r.message) {
							let msg = `
								Successfully synced: ${r.message.success}<br>
								Failed: ${r.message.failed}
							`;
							if (r.message.errors.length > 0) {
								msg += '<br><br>Errors:<br>' + r.message.errors.join('<br>');
							}
							frappe.msgprint({
								title: __('Sync Results'),
								message: msg,
								indicator: r.message.failed > 0 ? 'orange' : 'green'
							});
						}
					}
				});
			}, __('Actions'));
		}

		// Show API response in a formatted way
		if (frm.doc.api_response) {
			try {
				let data = JSON.parse(frm.doc.api_response);
				let $wrapper = $(frm.fields_dict.api_response.wrapper);
				$wrapper.html(`
					<pre style="max-height: 300px; overflow-y: auto;">
						<code>${JSON.stringify(data, null, 2)}</code>
					</pre>
				`);
			} catch (e) {
				console.error('Error parsing API response:', e);
			}
		}
	},

	workiz_uuid: function(frm) {
		if (frm.doc.workiz_uuid) {
			const uuidPattern = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
			if (!uuidPattern.test(frm.doc.workiz_uuid)) {
				frappe.msgprint(__('Invalid Workiz UUID format. Expected format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'));
				frm.doc.workiz_uuid = '';
				frm.refresh_field('workiz_uuid');
			}
		}
	},

	validate: function(frm) {
		if (!frm.doc.api_key) {
			frappe.throw(__('API Key is required for Workiz integration'));
		}
	}
});
