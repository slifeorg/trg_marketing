frappe.listview_settings['Appointment Details'] = {
    add_fields: ["appointment_datetime", "availability_confirmation", "parent"],
    get_indicator: function(doc) {
        return [
            __(doc.availability_confirmation || "Pending"),
            {
                "Confirmed": "green",
                "Pending": "orange",
                "Rescheduled": "red"
            }[doc.availability_confirmation] || "orange",
            "availability_confirmation,=," + doc.availability_confirmation
        ];
    },
    formatters: {
        appointment_datetime: function(value) {
            return frappe.datetime.str_to_user(value);
        }
    }
};