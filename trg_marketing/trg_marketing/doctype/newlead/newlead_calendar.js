frappe.views.calendar['NewLead'] = {
    field_map: {
        start: 'creation_date',
        end: 'modified_date',
        id: 'name',
        title: 'lead_id',
        allDay: 0
    },
    
    options: {
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        }
    },

    get_events_method: 'frappe.desk.calendar.get_events',

    filters: [
        {
            fieldtype: 'Select',
            fieldname: 'new_lead_category',
            options: '\nCustomer Info\nSummary\nQC Submit',
            label: __('Lead Category')
        },
        {
            fieldtype: 'Select',
            fieldname: 'lead_rating',
            options: '\n0 - Salesman under 6 months only\n1 - Salesman under 6 months only\n5 - Gold Star',
            label: __('Lead Rating')
        }
    ]
};