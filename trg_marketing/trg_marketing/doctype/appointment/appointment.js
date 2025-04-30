frappe.ui.form.on('Appointment', {
	refresh(frm) {
		console.log("test")
		$(".control-input:has(select) use[href='#icon-select']")
			.attr("href", "#icon-arrow-down-trg")
	}
})