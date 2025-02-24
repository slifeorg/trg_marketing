from frappe import _

def get_data():
    return {
        'fieldname': 'customer_info',
        'non_standard_fieldnames': {
            'Lead': 'customer_info'
        },
        'transactions': [
            {
                'label': _('Related Documents'),
                'items': ['Lead']
            }
        ],
        'charts': [
            {
                'name': 'Customer Distribution by Status',
                'chart_name': 'Customer Status Distribution',
                'chart_type': 'Pie',
                'doctype': 'Customer Info',
                'group_by_field': 'marital_status',
                'number_of_groups': 3
            }
        ]
    }