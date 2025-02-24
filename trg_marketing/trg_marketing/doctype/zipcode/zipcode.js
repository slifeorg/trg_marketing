frappe.ui.form.on('Zipcode', {
    refresh: function(frm) {
        // Add button to get geocoding data
        frm.add_custom_button(__('Get Geocoding Data'), function() {
            frm.call('get_geocoding_data')
                .then(r => {
                    if (r.message) {
                        let html = '<div class="geocoding-results">';
                        html += `<p><strong>Latitude:</strong> ${r.message.latitude}</p>`;
                        html += `<p><strong>Longitude:</strong> ${r.message.longitude}</p>`;
                        if (r.message.confidence) {
                            html += `<p><strong>Confidence:</strong> ${r.message.confidence}</p>`;
                        }
                        html += '</div>';
                        
                        frappe.msgprint({
                            title: __('Geocoding Results'),
                            message: html,
                            indicator: 'green'
                        });
                    }
                });
        });

        // Add button to view related addresses
        frm.add_custom_button(__('View Related Addresses'), function() {
            frm.call('get_related_addresses')
                .then(r => {
                    if (r.message && r.message.length > 0) {
                        let html = '<div class="related-addresses">';
                        r.message.forEach(addr => {
                            html += `<p><a href="/app/address/${addr.name}">${addr.address_line1}, ${addr.city}, ${addr.state}</a></p>`;
                        });
                        html += '</div>';
                        
                        frappe.msgprint({
                            title: __('Related Addresses'),
                            message: html
                        });
                    } else {
                        frappe.msgprint(__('No related addresses found'));
                    }
                });
        });
    },

    validate: function(frm) {
        // Format zipcode
        if (frm.doc.zipcode) {
            frm.doc.zipcode = frm.doc.zipcode.replace(/\s+/g, '').replace(/-/g, '');
        }
    }
});