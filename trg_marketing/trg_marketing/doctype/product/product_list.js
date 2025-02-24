frappe.listview_settings['Product'] = {
    add_fields: ["product_name", "rank", "is_top_10", "enabled", "availability_status"],
    
    get_indicator: function(doc) {
        if (!doc.enabled) {
            return [__("Disabled"), "red", "enabled,=,0"];
        }
        
        if (doc.is_top_10) {
            return [__("Top 10"), "blue", "is_top_10,=,1"];
        }
        
        return [__(doc.availability_status), {
            "In Stock": "green",
            "Out of Stock": "orange",
            "Discontinued": "red"
        }[doc.availability_status] || "gray"];
    },
    
    formatters: {
        rank: function(value) {
            if (!value) return "";
            return `<span class="indicator-pill blue">#${value}</span>`;
        }
    },
    
    onload: function(listview) {
        listview.page.add_inner_button(__('Update Rankings'), function() {
            frappe.route_options = {
                "rank": ["is", "set"]
            };
            frappe.set_route("List", "Product", "Report");
        });
    }
};