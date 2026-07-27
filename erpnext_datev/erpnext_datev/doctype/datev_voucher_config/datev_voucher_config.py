# Copyright (c) 2021, Alyf and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class DATEVVoucherConfig(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		attach_files: DF.Check
		attach_print: DF.Check
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		print_format: DF.Link | None
		recipient: DF.Data
		voucher_type: DF.Link
	# end: auto-generated types

	pass
