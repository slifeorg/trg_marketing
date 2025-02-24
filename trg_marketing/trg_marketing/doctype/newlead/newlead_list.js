frappe.listview_settings['NewLead'] = {
    add_fields: ["lead_id", "new_lead_category", "lead_rating", "workflow_state"],
    
    get_indicator: function(doc) {
        return [
            __(doc.workflow_state),
            {
                "Draft": "gray",
                "Pending": "orange",
                "Approved": "green",
                "Rejected": "red"
            }[doc.workflow_state] || "gray",
            "workflow_state,=," + doc.workflow_state
        ];
    },

    formatters: {
        lead_rating: function(value) {
            const ratings = {
                "0 - Salesman under 6 months only": "⭐",
                "1 - Salesman under 6 months only": "⭐⭐",
                "5 - Gold Star": "⭐⭐⭐⭐⭐"
            };
            return ratings[value] || value;
        }
    }
};