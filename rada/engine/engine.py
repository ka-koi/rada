import frappe
from frappe.model.document import Document
from frappe import _

class Engine(Document):
    def autoname(self):
        missing_fields = []

        if not self.engine_code:
            missing_fields.append("Engine Code")
        if self.displacement is None:
            missing_fields.append("Displacement")
        if not self.configuration:
            missing_fields.append("Configuration")

        config = (self.configuration or "").strip().lower()
        fuel = (self.fuel_type or "").strip().lower()

        # Only require fuel_type if not Electric Motor
        if not self.fuel_type and config != "electric motor":
            missing_fields.append("Fuel Type")

        if missing_fields:
            missing = ", ".join(missing_fields)
            frappe.throw(_("Missing required fields to set engine name: {0}").format(missing))

        # 🚫 Enforce valid displacement rules
        if self.displacement == 0 and config != "electric motor":
            frappe.throw(_("Displacement must be greater than 0 unless configuration is 'Electric Motor'"))

        if config == "electric motor" and self.displacement != 0:
            frappe.throw(_("Displacement must be 0 when configuration is 'Electric Motor'"))

        # 🚫 Disallow Diesel or Petrol for Electric Motor
        if config == "electric motor" and fuel in ("diesel", "petrol"):
            frappe.throw(_("Fuel Type cannot be Diesel or Petrol when configuration is 'Electric Motor'"))

        # ✅ Build name
        name_parts = [self.engine_code]

        if self.displacement > 0:
            name_parts.append(f"{self.displacement}L")

        name_parts.append(self.configuration)

        if self.fuel_type:
            name_parts.append(self.fuel_type)

        self.name = " - ".join([name_parts[0], " ".join(name_parts[1:])])
