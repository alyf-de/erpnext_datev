// Copyright (c) 2021, Alyf and contributors
// For license information, please see license.txt

frappe.ui.form.on("DATEV Unternehmen Online Settings", {
	refresh: function (frm) {
		frm.set_query("print_format", "datev_voucher_config", function (doc, cdt, cdn) {
			let row = locals[cdt][cdn];
			return {
				filters: {
					doc_type: row.voucher_type,
				},
			};
		});

		frappe.call({
			method: "erpnext_datev_uo.erpnext_datev_uo.doctype.datev_unternehmen_online_settings.datev_unternehmen_online_settings.get_options_for_recipient",
			callback: function (r) {
				if (r && r.message) {
					frm.email_options = r.message;
				}
			},
		});
	},
});

frappe.ui.form.on("DATEV Voucher Config", {
	voucher_type: function (frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		set_recipient_options(frm, row)
	},
});

function set_recipient_options(frm, row) {
	if (!row.voucher_type) {
		return;
	}

	frm.fields_dict.datev_voucher_config.grid.update_docfield_property(
		"recipient",
		"options",
		[""].concat(frm.email_options[row.voucher_type])
	);
}