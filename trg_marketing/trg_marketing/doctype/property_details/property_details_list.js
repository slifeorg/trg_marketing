frappe.listview_settings['Property Details'] = {
    add_fields: ["year_built", "lead", "zillow_data"],
    
    get_indicator: function(doc) {
        const currentYear = new Date().getFullYear();
        const age = currentYear - doc.year_built;
        
        if (age <= 10) {
            return [__("New Construction"), "green", "year_built,>=," + (currentYear - 10)];
        } else if (age <= 30) {
            return [__("Modern"), "blue", "year_built,>=," + (currentYear - 30)];
        } else {
            return [__("Classic"), "orange", "year_built,<," + (currentYear - 30)];
        }
    },

    onload: function(listview) {
        listview.page.add_inner_button(__('View Map'), function() {
            frappe.route_options = {
                'property_details': listview.get_checked_items().map(d => d.name)
            };
            frappe.set_route('property-map-view');
        });
    },

    formatters: {
        year_built: function(value) {
            if (!value) return '';
            const age = new Date().getFullYear() - value;
            return `${value} (${age} years old)`;
        }
    }
};