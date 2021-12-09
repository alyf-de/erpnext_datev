from . import __version__ as app_version

app_name = "erpnext_datev_uo"
app_title = "Erpnext Datev UO"
app_publisher = "ALYF GmbH"
app_description = "DATEV Unternehmen Online integration for ERPNext"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "hallo@alyf.de"
app_license = "GPLv3"

fixtures = [
	{
		"dt": "Translation",
		"filters": {"name": ("in", ("1804206bd0", "105afc9779", "662ec34a30"))}
	}
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/erpnext_datev_uo/css/erpnext_datev_uo.css"
# app_include_js = "/assets/erpnext_datev_uo/js/erpnext_datev_uo.js"

# include js, css files in header of web template
# web_include_css = "/assets/erpnext_datev_uo/css/erpnext_datev_uo.css"
# web_include_js = "/assets/erpnext_datev_uo/js/erpnext_datev_uo.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "erpnext_datev_uo/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "erpnext_datev_uo.utils.jinja_methods",
#	"filters": "erpnext_datev_uo.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "erpnext_datev_uo.install.before_install"
# after_install = "erpnext_datev_uo.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "erpnext_datev_uo.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Sales Invoice": {
		"on_submit": "erpnext_datev_uo.erpnext_datev_uo.doctype.datev_unternehmen_online_settings.datev_unternehmen_online_settings.send",
	},
	"Purchase Invoice": {
		"on_submit": "erpnext_datev_uo.erpnext_datev_uo.doctype.datev_unternehmen_online_settings.datev_unternehmen_online_settings.send",
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"erpnext_datev_uo.tasks.all"
#	],
#	"daily": [
#		"erpnext_datev_uo.tasks.daily"
#	],
#	"hourly": [
#		"erpnext_datev_uo.tasks.hourly"
#	],
#	"weekly": [
#		"erpnext_datev_uo.tasks.weekly"
#	],
#	"monthly": [
#		"erpnext_datev_uo.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "erpnext_datev_uo.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "erpnext_datev_uo.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "erpnext_datev_uo.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"erpnext_datev_uo.auth.validate"# ]

