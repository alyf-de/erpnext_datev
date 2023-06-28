import datetime
import zipfile
from csv import QUOTE_NONNUMERIC
from io import BytesIO

import frappe
import pandas as pd
from frappe import _

from .datev_constants import DataCategory


def get_datev_csv(data, filters, csv_class):
	"""
	Fill in missing columns and return a CSV in DATEV Format.

	For automatic processing, DATEV requires the first line of the CSV file to
	hold meta data such as the length of account numbers oder the category of
	the data.

	Arguments:
	data -- array of dictionaries
	filters -- dict
	csv_class -- defines DATA_CATEGORY, FORMAT_NAME and COLUMNS
	"""
	empty_df = pd.DataFrame(columns=csv_class.COLUMNS)
	data_df = pd.DataFrame.from_records(data)
	result = empty_df.append(data_df, sort=True)

	if csv_class.DATA_CATEGORY == DataCategory.TRANSACTIONS:
		result['Belegdatum'] = pd.to_datetime(result['Belegdatum'])

		result['Beleginfo - Inhalt 6'] = pd.to_datetime(result['Beleginfo - Inhalt 6'])
		result['Beleginfo - Inhalt 6'] = result['Beleginfo - Inhalt 6'].dt.strftime('%d%m%Y')

		result['Fälligkeit'] = pd.to_datetime(result['Fälligkeit'])
		result['Fälligkeit'] = result['Fälligkeit'].dt.strftime('%d%m%y')

		result.sort_values(by='Belegdatum', inplace=True, kind='stable', ignore_index=True)

	if csv_class.DATA_CATEGORY == DataCategory.ACCOUNT_NAMES:
		result['Sprach-ID'] = 'de-DE'

	data = result.to_csv(
		# Reason for str(';'): https://github.com/pandas-dev/pandas/issues/6035
		sep=';',
		# European decimal seperator
		decimal=',',
		# Windows "ANSI" encoding
		encoding='latin_1',
		# format date as DDMM
		date_format='%d%m',
		# Windows line terminator
		line_terminator='\r\n',
		# Do not number rows
		index=False,
		# Use all columns defined above
		columns=csv_class.COLUMNS,
		# Quote most fields, even currency values with "," separator
		quoting=QUOTE_NONNUMERIC
	)

	data = data.encode('latin_1', errors='replace')

	header = get_header(filters, csv_class)
	header = ';'.join(header).encode('latin_1', errors='replace')

	# 1st Row: Header with meta data
	# 2nd Row: Data heading (Überschrift der Nutzdaten), included in `data` here.
	# 3rd - nth Row: Data (Nutzdaten)
	return header + b'\r\n' + data


def get_header(filters, csv_class):
	description = filters.get('voucher_type', csv_class.FORMAT_NAME)
	company = filters.get('company')
	datev_settings = frappe.get_doc('DATEV Settings', {'client': company})
	default_currency = frappe.get_value('Company', company, 'default_currency')
	coa = frappe.get_value('Company', company, 'chart_of_accounts')
	coa_short_code = '04' if 'SKR04' in coa else ('03' if 'SKR03' in coa else '')

	return [
		'"EXTF"',
		'700',
		csv_class.DATA_CATEGORY,
		f'"{csv_class.FORMAT_NAME}"',
		csv_class.FORMAT_VERSION,
		datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '000',
		'',
		'"EN"',
		f'"{frappe.session.user}"',
		'',
		datev_settings.get('consultant_number', '0000000'),
		datev_settings.get('client_number', '00000'),
		frappe.utils.formatdate(filters.get('fiscal_year_start'), 'yyyyMMdd'),
		str(filters.get('account_number_length', 4)),
		frappe.utils.formatdate(filters.get('from_date'), 'yyyyMMdd')
		if csv_class.DATA_CATEGORY == DataCategory.TRANSACTIONS
		else '',
		frappe.utils.formatdate(filters.get('to_date'), 'yyyyMMdd')
		if csv_class.DATA_CATEGORY == DataCategory.TRANSACTIONS
		else '',
		f'"{_(description)}"'
		if csv_class.DATA_CATEGORY == DataCategory.TRANSACTIONS
		else '',
		'',
		'1' if csv_class.DATA_CATEGORY == DataCategory.TRANSACTIONS else '',
		'0' if csv_class.DATA_CATEGORY == DataCategory.TRANSACTIONS else '',
		'0',
		f'"{default_currency}"'
		if csv_class.DATA_CATEGORY == DataCategory.TRANSACTIONS
		else '',
		'',
		'',
		'',
		'',
		f'"{coa_short_code}"',
		'',
		'',
		'',
		'',
	]


def zip_and_download(zip_filename, csv_files):
	"""
	Put CSV files in a zip archive and send that to the client.

	Params:
	zip_filename	Name of the zip file
	csv_files		list of dicts [{'file_name': 'my_file.csv', 'csv_data': 'comma,separated,values'}]
	"""
	zip_buffer = BytesIO()

	zip_file = zipfile.ZipFile(zip_buffer, mode='w', compression=zipfile.ZIP_DEFLATED)
	for csv_file in csv_files:
		zip_file.writestr(csv_file.get('file_name'), csv_file.get('csv_data'))

	zip_file.close()

	frappe.response['filecontent'] = zip_buffer.getvalue()
	frappe.response['filename'] = zip_filename
	frappe.response['type'] = 'binary'
