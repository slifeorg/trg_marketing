# Copyright (c) 2025, slife and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class FAQArticles(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.core.doctype.has_role.has_role import HasRole
		from frappe.types import DF
		from trg_marketing.trg_marketing.doctype.faq_category_link.faq_category_link import FAQCategoryLink

		author: DF.Link | None
		categories: DF.TableMultiSelect[FAQCategoryLink]
		content: DF.TextEditor | None
		header: DF.Data | None
		role: DF.Table[HasRole]
		status: DF.Literal["Draft", "New", "Read"]
	# end: auto-generated types

	pass
