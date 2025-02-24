frappe.listview_settings['Agent'] = {
    add_fields: ["full_name", "email", "phone_number", "position", "inactive"],
    
    get_indicator: function(doc) {
        return [
            doc.inactive ? __("Inactive") : __("Active"),
            doc.inactive ? "gray" : "green",
            "inactive," + (doc.inactive ? "=1" : "=0")
        ];
    },

    formatters: {
        profile_picture: function(value) {
            return value ? 
                `<img src="${value}" style="width: 20px; height: 20px; border-radius: 50%;">` : 
                '';
        }
    }
};