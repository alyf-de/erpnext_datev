# Copyright (c) 2021, Alyf and contributors
# For license information, please see license.txt

import json

import frappe
from frappe.model.document import Document
from frappe.utils.data import evaluate_filters


class DATEVVoucherConfig(Document):
<<<<<<< HEAD
	pass
=======
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		attach_files: DF.Check
		attach_print: DF.Check
		filters: DF.Code | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		print_format: DF.Link | None
		recipient: DF.Data
		voucher_type: DF.Link
	# end: auto-generated types

	def validate_filters(self):
		if not self.filters:
			return

		filters = json.loads(self.filters)
		dummy_doc = frappe.new_doc(self.voucher_type)
		evaluate_filters(dummy_doc, filters)
>>>>>>> 6235034 (feat(DATEV): filter voucher emails by document fields (#36))
