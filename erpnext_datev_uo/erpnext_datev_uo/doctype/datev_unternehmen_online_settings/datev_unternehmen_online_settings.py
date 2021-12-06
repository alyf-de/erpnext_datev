# Copyright (c) 2021, Alyf and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class DATEVUnternehmenOnlineSettings(Document):
	pass


def send(doc, method):
	settings = frappe.get_single("DATEV Unternehmen Online Settings")

	if not settings.enabled or not doc.items:
		return

	print_settings = settings.get(
		"datev_voucher_config", filters={"voucher_type": doc.doctype}
	)
	print_settings = print_settings and print_settings[0]

	if not print_settings or not doc.get(print_settings.recipient):
		return

	attachments = get_attachments(print_settings, doc)

	frappe.sendmail(
		recipients=[doc.get(print_settings.recipient)],
		subject=f"{_(doc.doctype)}: {_(doc.name)}",
		sender=print_settings.sender,
		message=_(f"New {0} {1} from ERPNext.").format(_(doc.doctype), _(doc.name)),
		reference_doctype=doc.doctype,
		reference_name=doc.name,
		attachments=attachments,
		expose_recipients="header"
	)


def get_attachments(print_settings, doc):
	attachments = [
		{
			"print_format_attachment": 1,
			"doctype": doc.doctype,
			"name": doc.name,
			"print_format": print_settings.print_format,
			"lang": frappe.db.get_value(
				"Print Format", print_settings.print_format, "default_print_language"
			)
			or "de",
		}
	]

	if doc.doctype == "Purchase Invoice":
		attachments.extend(
			frappe.get_all(
				"File",
				filters={
					"attached_to_doctype": doc.doctype,
					"attached_to_name": doc.name,
				},
				fields=["`tabFile`.name as fid"],
			)
		)

	return attachments
