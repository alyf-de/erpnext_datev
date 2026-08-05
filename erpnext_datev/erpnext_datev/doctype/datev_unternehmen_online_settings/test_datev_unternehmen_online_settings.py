# Copyright (c) 2021, Alyf and Contributors
# See license.txt

import json
from unittest import TestCase

import frappe

from erpnext_datev.erpnext_datev.doctype.datev_unternehmen_online_settings.datev_unternehmen_online_settings import (
	get_voucher_config,
)


class TestDATEVUnternehmenOnlineSettings(TestCase):
	def test_get_voucher_config_respects_filters(self):
		settings = frappe.new_doc("DATEV Unternehmen Online Settings")
		row = settings.append(
			"datev_voucher_config",
			{
				"voucher_type": "Sales Invoice",
				"recipient": "datev@example.com",
				"attach_print": 1,
				"print_format": "Standard",
				"filters": json.dumps([["Sales Invoice", "status", "=", "Paid"]]),
			},
		)

		paid = frappe._dict(doctype="Sales Invoice", status="Paid", name="SI-PAID")
		unpaid = frappe._dict(doctype="Sales Invoice", status="Unpaid", name="SI-UNPAID")

		self.assertEqual(get_voucher_config(settings, paid), row)
		self.assertIsNone(get_voucher_config(settings, unpaid))

		row.filters = "[]"
		self.assertEqual(get_voucher_config(settings, unpaid), row)
