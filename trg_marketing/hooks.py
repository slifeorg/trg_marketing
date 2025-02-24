app_name = "trg_marketing"
app_title = "Trg Marketing"
app_publisher = "slife"
app_description = "TRG Marketing"
app_email = "info@slife.guru"
app_license = "mit"
app_icon = "octicon octicon-file-directory"

# Apps
add_to_apps_screen = [
    {
        "name": "trg_marketing",
        "logo": "/assets/trg_marketing/images/desk.png",
        "title": "TRG Marketing",
        "route": "/trg_marketing",
        "has_permission": "trg_marketing.api.permission.has_app_permission"
    }
]

# Patches
patches = [
    "trg_marketing.trg_marketing.patches.create_marketing_settings"
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/trg_marketing/css/trg_marketing.css"
# app_include_js = "/assets/trg_marketing/js/trg_marketing.js"

# include js, css files in header of web template
# web_include_css = "/assets/trg_marketing/css/trg_marketing.css"
# web_include_js = "/assets/trg_marketing/js/trg_marketing.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "trg_marketing/public/scss/website"

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

fixtures = [
    {
        "doctype": "DocType",
        "filters": {"module":"Trg Marketing"}  # An empty filter means no restrictions.
    }
]

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "trg_marketing/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "trg_marketing.utils.jinja_methods",
# 	"filters": "trg_marketing.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "trg_marketing.install.before_install"
# after_install = "trg_marketing.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "trg_marketing.uninstall.before_uninstall"
# after_uninstall = "trg_marketing.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "trg_marketing.utils.before_app_install"
# after_app_install = "trg_marketing.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "trg_marketing.utils.before_app_uninstall"
# after_app_uninstall = "trg_marketing.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "trg_marketing.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"trg_marketing.tasks.all"
# 	],
# 	"daily": [
# 		"trg_marketing.tasks.daily"
# 	],
# 	"hourly": [
# 		"trg_marketing.tasks.hourly"
# 	],
# 	"weekly": [
# 		"trg_marketing.tasks.weekly"
# 	],
# 	"monthly": [
# 		"trg_marketing.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "trg_marketing.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "trg_marketing.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "trg_marketing.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["trg_marketing.utils.before_request"]
# after_request = ["trg_marketing.utils.after_request"]

# Job Events
# ----------
# before_job = ["trg_marketing.utils.before_job"]
# after_job = ["trg_marketing.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"trg_marketing.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

