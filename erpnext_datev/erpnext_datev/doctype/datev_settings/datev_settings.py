# Copyright (c) 2023, ALYF GmbH and contributors
# For license information, please see license.txt

from frappe import _, throw
from frappe.model.document import Document


class DATEVSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		account_number_length: DF.Int
		client: DF.Link
		client_number: DF.Data
		consultant: DF.Link | None
		consultant_number: DF.Data
		opening_against_account_number: DF.Data | None
		temporary_against_account_number: DF.Data
	# end: auto-generated types

	def validate(self):
		if (
			self.temporary_against_account_number
			and len(self.temporary_against_account_number) != self.account_number_length
		):
			throw(
				_("Temporary Against Account Number must be {0} digits long").format(
					self.account_number_length
				)
			)

		if (
			self.opening_against_account_number
			and len(self.opening_against_account_number) != self.account_number_length
		):
			throw(
				_("Opening Against Account Number must be {0} digits long").format(self.account_number_length)
			)
