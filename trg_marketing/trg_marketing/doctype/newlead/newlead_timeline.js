frappe.timeline.order_by = "creation";

frappe.timeline.get_events = function(opts) {
    return frappe.call({
        method: "frappe.desk.timeline.get_timeline_data",
        args: {
            doctype: "NewLead",
            name: opts.docname,
            fields: ["lead_id", "new_lead_category", "lead_rating", "workflow_state"]
        }
    });
};