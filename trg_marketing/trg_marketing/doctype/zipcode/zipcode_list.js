frappe.listview_settings['Zipcode'] = {
    add_fields: ["zipcode", "city", "state", "county"],
    
    formatters: {
        zipcode: function(value) {
            return value.replace(/(\d{5})(\d{4})?/, "$1-$2");
        }
    },
    
    onload: function(listview) {
        listview.page.add_inner_button(__('Import Zipcodes'), function() {
            frappe.prompt([
                {
                    label: 'CSV File',
                    fieldname: 'file',
                    fieldtype: 'Attach'
                }
            ],
            function(values) {
                frappe.call({
                    method: 'trg_marketing.trg_marketing.doctype.zipcode.zipcode.import_zipcodes',
                    args: {
                        file: values.file
                    },
                    callback: function(r) {
                        if (!r.exc) {
                            frappe.show_alert({
                                message: __('Zipcodes imported successfully'),
                                indicator: 'green'
                            });
                            listview.refresh();
                        }
                    }
                });
            },
            __('Import Zipcodes'),
            __('Import')
            );
        });
    }
};