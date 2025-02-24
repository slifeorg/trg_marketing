frappe.listview_settings['Lead'] = {
    add_fields: ["customer_name", "result", "phone_number"],
    get_indicator: function(doc) {
        return [
            __(doc.result),
            {
                "NO MONEY": "red",
                "PENDING": "orange",
                "CLOSED": "green"
            }[doc.result] || "grey",
            "result,=," + doc.result
        ];
    },
    onload: function(listview) {
        listview.page.add_inner_button(__('Create Appointment'), function() {
            frappe.new_doc('Appointment');
        });
    }
};