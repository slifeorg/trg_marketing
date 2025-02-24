frappe.views.calendar["Appointment"] = {
    field_map: {
        "start": "appointment_date",
        "end": "appointment_date",
        "id": "name",
        "title": "customer_name",
        "allDay": 0,
        "status": "status"
    },
    gantt: false,
    filters: [
        {
            "fieldtype": "Select",
            "fieldname": "status",
            "options": "Scheduled\nCompleted\nCancelled",
            "label": __("Status")
        }
    ],
    get_events_method: "trg_marketing.trg_marketing.doctype.appointment.appointment.get_events",
    style_map: {
        "Scheduled": "blue",
        "Completed": "green",
        "Cancelled": "red"
    }
};
