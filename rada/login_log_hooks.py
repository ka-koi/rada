# rada/login_log_hooks.py

from datetime import date, datetime
from math import atan2, cos, radians, sin, sqrt

import frappe
import requests
from frappe.email.smtp import OutgoingEmailError

# in apps/rada/rada/login_log_hooks.py


def autoname(doc, method):
	now = datetime.now().strftime("%H%M%S")
	login_dt = doc.login_date
	if isinstance(login_dt, str):
		date_str = login_dt.replace("-", "")
	elif login_dt:
		date_str = login_dt.strftime("%Y%m%d")
	else:
		date_str = datetime.now().strftime("%Y%m%d")
	doc.name = f"{doc.user}-{date_str}-{now}"
	doc.coordinates = doc.coordinates or "0.0,0.0"  # Ensure coordinates are set


def get_ip():
	try:
		return frappe.local.request_ip or frappe.local.request.remote_addr
	except AttributeError:
		# Safe fallback when no request context (e.g. bench console)
		return "127.0.0.1"


def get_geolocation(ip):
	try:
		res = requests.get(f"https://ipinfo.io/{ip}/json")
		if res.status_code == 200:
			data = res.json()
			loc = data.get("loc", "")
			lat, lon = (float(x) for x in loc.split(",")) if loc else (None, None)
			return {
				"city": data.get("city", ""),
				"region": data.get("region", ""),
				"country": data.get("country", ""),
				"loc": loc,
				"lat": lat,
				"lon": lon,
			}
	except Exception as e:
		frappe.log_error(str(e), "Login Log: Geo IP Lookup Failed")
	return {}


def calculate_distance_km(lat1, lon1, lat2, lon2):
	R = 6371
	dlat = radians(lat2 - lat1)
	dlon = radians(lon2 - lon1)
	a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
	return R * 2 * atan2(sqrt(a), sqrt(1 - a))


def record_login(login_manager):
	frappe.log_error("record_login triggered", "Login Log Debug")
	user = frappe.session.user
	today = date.today().isoformat()
	ip = get_ip()
	geo = get_geolocation(ip)

	location = ", ".join(filter(None, [geo.get("city"), geo.get("region"), geo.get("country")]))
	coordinates = geo.get("loc")
	lat, lon = geo.get("lat"), geo.get("lon")
	is_unusual = False

	# Get last login log entry
	last_login = frappe.get_all(
		"Login Log", filters={"user": user}, fields=["coordinates"], order_by="creation desc", limit=1
	)

	if last_login and last_login[0].coordinates and coordinates:
		try:
			prev_lat, prev_lon = map(float, last_login[0].coordinates.split(","))
			distance = calculate_distance_km(prev_lat, prev_lon, lat, lon)
			is_unusual = distance > 50
		except Exception:
			is_unusual = True
	else:
		is_unusual = True

	# Avoid duplicate logs per day
	if not frappe.db.exists("Login Log", {"user": user, "login_date": today}):
		doc = frappe.get_doc(
			{
				"doctype": "Login Log",
				"user": user,
				"login_date": today,
				"login_time": datetime.now().time(),
				"ip_address": ip,
				"location": location,
				"coordinates": coordinates,
				"is_unusual": is_unusual,
				"notified": 0,
			}
		)
		doc.insert(ignore_permissions=True)

		if is_unusual:
			try:
				frappe.sendmail(
					recipients=["admin@example.com"],  # Change this
					subject=f"🚨 Unusual Login Detected: {user}",
					message=f"{user} logged in from:\n\n"
					f"IP: {ip}\n"
					f"Location: {location}\n"
					f"Coordinates: {coordinates}\n"
					f"Time: {doc.login_time} on {today}",
				)
			except OutgoingEmailError as e:
				frappe.log_error(str(e), "Unusual Login Alert Email Failed")
