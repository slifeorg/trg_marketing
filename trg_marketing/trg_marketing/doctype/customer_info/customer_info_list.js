frappe.listview_settings['Customer Info'] = {
    add_fields: ["homeowner_name", "contact_number", "marital_status", "lead"],
    
    get_indicator: function(doc) {
        return [__(doc.marital_status), {
            "Single": "blue",
            "Married": "green",
            "Divorced": "orange"
        }[doc.marital_status] || "gray"];
    },

    onload: function(listview) {
        listview.page.add_inner_button(__('Create Lead'), function() {
            frappe.new_doc('Lead');
        });
    },

    button: {
        show: function(doc) {
            return doc.lead;
        },
        get_label: function() {
            return __('View Lead');
        },
        get_description: function(doc) {
            return __('Open Lead {0}', [doc.lead]);
        },
        action: function(doc) {
            frappe.set_route('Form', 'Lead', doc.lead);
        }
    }
};