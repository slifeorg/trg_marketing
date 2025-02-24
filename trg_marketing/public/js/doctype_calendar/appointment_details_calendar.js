frappe.views.calendar["Appointment Details"] = {
    field_map: {
        "start": "appointment_datetime",
        "end": "appointment_datetime",
        "id": "name",
        "title": "parent",
        "allDay": 0,
        "status": "availability_confirmation"
    },
    gantt: false,
    filters: [
        {
            "fieldtype": "Select",
            "fieldname": "availability_confirmation",
            "options": "\nConfirmed\nPending\nRescheduled",
            "label": __("Availability")
        }
    ],
    get_events_method: "trg_marketing.trg_marketing.doctype.appointment_details.appointment_details.get_events",
    style_map: {
        "Confirmed": "green",
        "Pending": "orange",
        "Rescheduled": "red"
    }
};