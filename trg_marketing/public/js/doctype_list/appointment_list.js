frappe.listview_settings['Appointment'] = {
    add_fields: ["status", "appointment_date", "customer_name", "time", "time_slot", "lead"],
    get_indicator: function(doc) {
        return [
            __(doc.status),
            {
                "Scheduled": "blue",
                "Completed": "green",
                "Cancelled": "red"
            }[doc.status],
            "status,=," + doc.status
        ];
    },
    onload: function(listview) {
        listview.page.add_inner_button(__('Create Appointment'), function() {
            frappe.new_doc('Appointment');
        });
    },
    formatters: {
        appointment_date: function(value, df, doc) {
            return frappe.datetime.str_to_user(value) + ' ' + doc.time;
        }
    }
};
