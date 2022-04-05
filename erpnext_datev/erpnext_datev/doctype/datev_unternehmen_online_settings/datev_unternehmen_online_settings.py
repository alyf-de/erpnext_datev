# Copyright (c) 2021, ALYF GmbH and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.core.doctype.communication.email import make as make_communication


class DATEVUnternehmenOnlineSettings(Document):
	def validate(self):
		for voucher_config in self.datev_voucher_config:
			if not voucher_config.attach_print and not voucher_config.attach_files:
				frappe.throw(
					_("Please configure attachments for voucher type {}.").format(
						_(voucher_config.voucher_type)
					)
				)


def send(doc, method):
	settings = frappe.get_single("DATEV Unternehmen Online Settings")
	if not settings.enabled:
		return

	voucher_config = get_voucher_config(settings, doc.doctype)
	if not voucher_config:
		return

	attachments = []

	if voucher_config.attach_print:
		attachments.append(
			get_print_config(
				doc.doctype, doc.name, voucher_config.print_format, doc.language
			)
		)

	if voucher_config.attach_files:
		attachments.extend(get_attached_files(doc.doctype, doc.name))

	if not attachments:
		frappe.msgprint(
			# fmt: off
			_("{} was not sent to DATEV because no attachments have been found.").format(_(doc.doctype))
			# fmt: on
		)
		return

	make_communication(
		doctype=doc.doctype,
		name=doc.name,
		content=_("New {0} {1} sent by the ERPNext-DATEV integration.").format(
			_(doc.doctype), doc.name
		),
		subject=f"{_(doc.doctype)}: {doc.name}",
		sender=frappe.get_value("Email Account", settings.sender, "email_id"),
		recipients=[voucher_config.recipient],
		communication_medium="Email",
		send_email=True,
		attachments=attachments,
		communication_type="Automated Message",
		ignore_permissions=True,
	)


def get_voucher_config(settings: DATEVUnternehmenOnlineSettings, doctype: str):
	voucher_config = settings.get(
		"datev_voucher_config", filters={"voucher_type": doctype}
	)
	if not voucher_config:
		return

	return voucher_config[0]


def get_attached_files(doctype: str, docname: str):
	return frappe.get_all(
		"File",
		filters={
			"attached_to_doctype": doctype,
			"attached_to_name": docname,
		},
		fields=["name as fid"],
	)


def get_print_config(
	doctype: str, docname: str, print_format: str, language: str = None
):
	_language = (
		language
		or frappe.db.get_value("Print Format", print_format, "default_print_language")
		or frappe.db.get_single_value("System Settings", "language")
	)

	return {
		"print_format_attachment": 1,
		"doctype": doctype,
		"name": docname,
		"print_format": print_format,
		"lang": _language,
	}
