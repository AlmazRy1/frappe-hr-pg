import frappe
from frappe.model.utils.rename_field import rename_field


def execute():
	frappe.reload_doc("hr", "doctype", "hr_settings")

	if frappe.db.exists("HR Settings", "stop_birthday_reminders"):
		try:
			# Rename the field
			rename_field("HR Settings", "stop_birthday_reminders", "send_birthday_reminders")

			# Reverse the value
			old_value = frappe.db.get_single_value("HR Settings", "send_birthday_reminders")

			frappe.db.set_single_value("HR Settings", "send_birthday_reminders", 1 if old_value == 0 else 0)

		except Exception as e:
			if e.args[0] != 1054:
				raise
	else:
		frappe.log_error("Field 'stop_birthday_reminders' not found in HR Settings", "Patch Error")
