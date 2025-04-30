function applySortArrows(sortBy = "", sortOrder = "") {
	sortBy = sortBy.toLowerCase();
	sortOrder = sortOrder.toLowerCase();

	$('[data-route="List/Appointment/List"] .list-row-col:has(>[data-sort-by])')
	.not(':has(.sort-icon)')
	.not(':has(>[data-sort-by="name"])')
	.each((_, el) => {
		const $col = $(el).find('[data-sort-by]');
		const field = $col.attr('data-sort-by').toLowerCase();

		const href = (field === sortBy)
			? (sortOrder === "asc" ? "#icon-arrow-3-4-trg" : "#icon-arrow-3-3-trg")
			: "#icon-arrow-3-trg";

		const svg = $(`<svg class="sort-icon" aria-hidden="true"><use href="${href}"></use></svg>`);
		$(el).append(svg);
	});
}

frappe.listview_settings["Appointment"] = {
	onload(listview) {
		frappe.after_ajax(() => {
			const wrapper = listview.page.wrapper;

			$(document).ajaxComplete(function (event, xhr, settings) {
				if (settings && settings.url && settings.url.includes('frappe.desk.reportview.get') && settings.type === "GET") {
					applySortArrows(listview.sort_by, listview.sort_order);
				}
			});
		});
	}
};