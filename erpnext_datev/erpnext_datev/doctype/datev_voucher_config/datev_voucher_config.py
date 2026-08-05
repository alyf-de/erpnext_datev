# Copyright (c) 2021, Alyf and contributors
# For license information, please see license.txt

import json

import frappe
from frappe.model.document import Document
from frappe.utils.data import evaluate_filters


class DATEVVoucherConfig(Document):
	def validate_filters(self):
		if not self.filters:
			return

		filters = json.loads(self.filters)
		dummy_doc = frappe.new_doc(self.voucher_type)
		evaluate_filters(dummy_doc, filters)
