// Copyright (c) 2021, Alyf and contributors
// For license information, please see license.txt

frappe.ui.form.on("DATEV Unternehmen Online Settings", {
	refresh: function (frm) {
		frm.set_query("voucher_type", "datev_voucher_config", function (doc, cdt, cdn) {
			return {
				filters: {
					name: ["in", ["Sales Invoice", "Purchase Invoice", "Expense Claim", "E Invoice Import"]],
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
	datev_voucher_config_on_form_rendered(frm) {
		const row = frm.cur_grid.doc;
		const parent = frm.cur_grid.wrapper.find("[data-fieldname='filter_area']");
		parent.empty();

		if (!row.voucher_type) {
			return;
		}

		const filters = row.filters && row.filters !== "[]" ? JSON.parse(row.filters) : [];

		frappe.model.with_doctype(row.voucher_type, () => {
			const filter_group = new frappe.ui.FilterGroup({
				parent: parent,
				doctype: row.voucher_type,
				on_change: () => {
					frappe.model.set_value(
						row.doctype,
						row.name,
						"filters",
						JSON.stringify(filter_group.get_filters())
					);
				},
			});

			filter_group.add_filters_to_filter_group(filters);
		});
	},
});

frappe.ui.form.on("DATEV Voucher Config", {
	voucher_type(frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		frappe.model.set_value(row.doctype, row.name, "filters", "[]");

		if (row.print_format) {
			frappe.db.get_value("Print Format", row.print_format, "doc_type").then((r) => {
				if (r.message.doc_type !== row.voucher_type) {
					frappe.model.set_value(row.doctype, row.name, "print_format", "");
				}
			});
		}

		if (frm.cur_grid) {
			frm.events.datev_voucher_config_on_form_rendered(frm);
		}
	},
});
