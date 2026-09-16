"""
Provide a GDPdU index.xml describing the CSV files of the DATEV export.

The tax office may demand the recording- and retention-relevant data in
machine-evaluable form, together with the structural information needed to
evaluate them (BMF letter of 11.03.2024, Anlage 1.4). index.xml is that
structural information: it names every delivered file, its columns in physical
order, their data types and the separators used. It follows the description
standard (Beschreibungsstandard) 1.6 of CaseWare Germany GmbH and is validated
against a DTD that has to sit next to it, so both files travel in the ZIP.
"""

import xml.etree.ElementTree as ET
from pathlib import Path

DTD_FILE_NAME = "gdpdu-01-03-2019.dtd"
INDEX_FILE_NAME = "index.xml"

PROLOG = (
	f'<?xml version="1.0" encoding="utf-8" standalone="no"?>\n<!DOCTYPE DataSet SYSTEM "{DTD_FILE_NAME}">\n'
)

# Row 1 of a DATEV CSV holds the meta header, row 2 the column headings. The
# payload starts in row 3 (see `get_datev_csv`). There is no element that
# declares a header record, it is skipped by starting to read later.
FIRST_DATA_ROW = "3"

# Columns that are not delivered as text. Everything else stays AlphaNumeric so
# that leading zeros of account numbers survive.
NUMERIC_COLUMNS = {
	# always filled, rounded to two decimals
	"Umsatz (ohne Soll/Haben-Kz)": "2",
}
DATE_COLUMNS = {
	# explicitly formatted in `get_datev_csv`
	"Beleginfo - Inhalt 6": "DDMMYYYY",
	"Fälligkeit": "DDMMYYYY",
	# `release_date` of the Supplier, written by pandas as an ISO date
	"Zahlungssperre bis": "YYYY-MM-DD",
}

# `Format` of a Date only knows the symbols DD, MM and YY/YYYY, so a date
# without a year cannot be declared as one. Say so in plain text instead.
DESCRIPTIONS = {
	# DATEV writes the Belegdatum as DDMM, the year is the one of `Validity`
	"Belegdatum": "Tag und Monat (DDMM), Jahr siehe Validity",
}

# First column of the table, identifies the row.
PRIMARY_KEYS = {
	"Kontenbeschriftungen": "Konto",
	"Kunden": "Konto",
	"Lieferanten": "Konto",
}

# Links between the tables, required as part of the data set.
# {table: [(own column, referenced table, referenced column)]}
FOREIGN_KEYS = {
	"Buchungsstapel": [
		("Konto", "Kontenbeschriftungen", "Konto"),
		("Gegenkonto (ohne BU-Schlüssel)", "Kontenbeschriftungen", "Konto"),
		# "Beleginfo - Art 4" tells whether the number is a debtor or a creditor
		("Beleginfo - Inhalt 4", "Kunden", "Konto"),
		("Beleginfo - Inhalt 4", "Lieferanten", "Konto"),
	],
}


def get_gdpdu_files(tables, valid_from, valid_to, supplier_name, supplier_location):
	"""
	Return index.xml and its DTD, ready to be zipped next to the CSV files.

	Arguments:
	tables -- list of (file name, table name, list of column names)
	valid_from, valid_to -- validity period of the data, formatted as YYYYMMDD
	supplier_name, supplier_location -- who hands the data over
	"""
	return [
		{
			"file_name": INDEX_FILE_NAME,
			"csv_data": get_index_xml(tables, valid_from, valid_to, supplier_name, supplier_location),
		},
		{
			"file_name": DTD_FILE_NAME,
			"csv_data": (Path(__file__).parent / DTD_FILE_NAME).read_bytes(),
		},
	]


def get_index_xml(tables, valid_from, valid_to, supplier_name, supplier_location):
	"""Describe the delivered CSV files according to the description standard."""
	data_set = ET.Element("DataSet")
	# version of the data delivery, not of the description standard
	ET.SubElement(data_set, "Version").text = "1.0"

	data_supplier = ET.SubElement(data_set, "DataSupplier")
	ET.SubElement(data_supplier, "Name").text = supplier_name
	ET.SubElement(data_supplier, "Location").text = supplier_location
	ET.SubElement(data_supplier, "Comment").text = "ERPNext DATEV Export"

	media = ET.SubElement(data_set, "Media")
	ET.SubElement(media, "Name").text = "DATEV"

	for file_name, table_name, columns in tables:
		add_table(media, file_name, table_name, columns, valid_from, valid_to)

	ET.indent(data_set)
	xml = PROLOG + ET.tostring(data_set, encoding="unicode") + "\n"

	# a literal CR in the record delimiter would be normalized to LF by any XML
	# parser, so it has to be a character reference
	return xml.replace("\r\n", "&#13;&#10;").encode("utf-8")


def add_table(media, file_name, table_name, columns, valid_from, valid_to):
	"""Describe one CSV file. Child order is prescribed by the DTD."""
	table = ET.SubElement(media, "Table")
	# relative to the directory of index.xml, absolute URLs are not allowed
	ET.SubElement(table, "URL").text = file_name
	ET.SubElement(table, "Name").text = table_name

	validity = ET.SubElement(table, "Validity")
	validity_range = ET.SubElement(validity, "Range")
	ET.SubElement(validity_range, "From").text = valid_from
	ET.SubElement(validity_range, "To").text = valid_to
	ET.SubElement(validity, "Format").text = "YYYYMMDD"

	# cp1252, the Windows "ANSI" code page
	ET.SubElement(table, "ANSI")
	ET.SubElement(table, "DecimalSymbol").text = ","
	ET.SubElement(table, "DigitGroupingSymbol").text = "."

	# skip the DATEV meta header and the column headings
	row_range = ET.SubElement(table, "Range")
	ET.SubElement(row_range, "From").text = FIRST_DATA_ROW

	variable_length = ET.SubElement(table, "VariableLength")
	ET.SubElement(variable_length, "ColumnDelimiter").text = ";"
	ET.SubElement(variable_length, "RecordDelimiter").text = "\r\n"
	ET.SubElement(variable_length, "TextEncapsulator").text = '"'

	primary_key = PRIMARY_KEYS.get(table_name)
	for column in columns:
		add_column(variable_length, column, is_primary_key=column == primary_key)

	for column, references, referenced_column in FOREIGN_KEYS.get(table_name, []):
		foreign_key = ET.SubElement(variable_length, "ForeignKey")
		ET.SubElement(foreign_key, "Name").text = column
		ET.SubElement(foreign_key, "References").text = references
		if column != referenced_column:
			alias = ET.SubElement(foreign_key, "Alias")
			ET.SubElement(alias, "From").text = column
			ET.SubElement(alias, "To").text = referenced_column


def add_column(variable_length, column, is_primary_key=False):
	"""Describe one column. Columns must be listed in the order of the file."""
	tag = "VariablePrimaryKey" if is_primary_key else "VariableColumn"
	variable_column = ET.SubElement(variable_length, tag)
	ET.SubElement(variable_column, "Name").text = column

	if column in DESCRIPTIONS:
		ET.SubElement(variable_column, "Description").text = DESCRIPTIONS[column]

	if column in NUMERIC_COLUMNS:
		numeric = ET.SubElement(variable_column, "Numeric")
		ET.SubElement(numeric, "Accuracy").text = NUMERIC_COLUMNS[column]
	elif column in DATE_COLUMNS:
		date = ET.SubElement(variable_column, "Date")
		ET.SubElement(date, "Format").text = DATE_COLUMNS[column]
	else:
		ET.SubElement(variable_column, "AlphaNumeric")
