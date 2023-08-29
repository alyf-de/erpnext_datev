# Copyright (c) 2021, ALYF GmbH and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.core.doctype.communication.email import make as make_communication
from frappe.translate import print_language

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
		filename = attach_print(
			doc.doctype,
			doc.name,
			doc.language,
			voucher_config.print_format,
		)
		attachments.append(filename)

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
	)


def attach_print(doctype, name, language, print_format):
	with print_language(language):
		data = frappe.get_print(doctype, name, print_format, as_pdf=True)

	file = frappe.new_doc("File")
	file.file_name = f"{name}.pdf"
	file.content = data
	file.attached_to_doctype = doctype
	file.attached_to_name = name
	file.is_private = 1
	file.save()

	return file.name


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
		pluck="name",
	)
