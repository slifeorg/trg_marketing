frappe.ui.form.on('Product', {
    refresh: function(frm) {
        // Add custom buttons
        if(!frm.is_new()) {
            frm.add_custom_button(__('Copy Product'), function() {
                frm.call('copy_product')
                    .then(r => {
                        if (r.message) {
                            frappe.model.sync(r.message);
                            frappe.set_route('Form', 'Product', r.message.name);
                        }
                    });
            });
            
            if (frm.doc.rank) {
                frm.add_custom_button(__('Remove from Top 10'), function() {
                    frm.call('update_rank', { new_rank: null })
                        .then(() => frm.reload_doc());
                });
            }
        }
        
        // Add quick rank buttons
        if (!frm.doc.rank) {
            let wrapper = frm.get_field('rank').$wrapper;
            let html = '<div class="rank-buttons" style="margin-top: 10px;">';
            for (let i = 1; i <= 10; i++) {
                html += `<button class="btn btn-xs btn-default" data-rank="${i}">${i}</button> `;
            }
            html += '</div>';
            wrapper.append(html);
            
            wrapper.find('.rank-buttons button').click(function() {
                let rank = $(this).data('rank');
                frm.call('update_rank', { new_rank: rank })
                    .then(() => frm.reload_doc());
            });
        }
    },
    
    validate: function(frm) {
        // Validate price
        if (frm.doc.base_price && frm.doc.base_price < 0) {
            frappe.throw(__('Base Price cannot be negative'));
            frappe.validated = false;
        }
    },
    
    enabled: function(frm) {
        // Update availability status when disabled
        if (!frm.doc.enabled) {
            frm.set_value('availability_status', 'Discontinued');
        }
    },
    
    category: function(frm) {
        // Clear sub_category when category changes
        if (frm.doc.category) {
            frm.set_value('sub_category', '');
        }
    }
});