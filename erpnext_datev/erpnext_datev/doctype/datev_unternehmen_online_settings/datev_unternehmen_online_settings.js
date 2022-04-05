// Copyright (c) 2021, Alyf and contributors
// For license information, please see license.txt

frappe.ui.form.on("DATEV Unternehmen Online Settings", {
	refresh: function (frm) {
		frm.set_query("voucher_type", "datev_voucher_config", function (doc, cdt, cdn) {
			return {
				filters: {
					name: ["in", ["Sales Invoice", "Purchase Invoice", "Expense Claim"]],
				},
			};
		});

		frm.set_query("print_format", "datev_voucher_config", function (doc, cdt, cdn) {
			let row = locals[cdt][cdn];
			return {
				filters: {
					doc_type: row.voucher_type,
				},
			};
		});
	},
});
