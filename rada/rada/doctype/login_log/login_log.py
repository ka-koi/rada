# Copyright (c) 2025, Patrick Willy and contributors
# For license information, please see license.txt

from datetime import datetime

from frappe.model.document import Document


class LoginLog(Document):
	def autoname(self):
		now = datetime.now().strftime("%H%M%S")
		login_dt = self.login_date
		if isinstance(login_dt, str):
			date_str = login_dt.replace("-", "")
		elif login_dt:
			date_str = login_dt.strftime("%Y%m%d")
		else:
			date_str = datetime.now().strftime("%Y%m%d")
		self.name = f"{self.user}-{date_str}-{now}"
		self.coordinates = self.coordinates or "0.0,0.0"
