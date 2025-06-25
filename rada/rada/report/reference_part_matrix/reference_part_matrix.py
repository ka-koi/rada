# Copyright (c) 2025, Patrick Willy and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = [
        {"label": "Reference Part", "fieldname": "reference_part", "fieldtype": "Data", "width": 180},
        {"label": "Category", "fieldname": "part_category", "fieldtype": "Link", "options": "Part Category", "width": 150},
		{"label": "Part Type", "fieldname": "part_type", "fieldtype": "Data", "width": 120},
        {"label": "Item Code", "fieldname": "item_codes", "fieldtype": "Data", "width": 300},
    ]

    data = []

    reference_parts = frappe.get_all("Reference Part", fields=[
        "name", "reference_part", "part_type", "part_category"
    ])

    for ref in reference_parts:
        items = frappe.get_all("Reference Part Item", filters={"parent": ref.name}, fields=["item_code"])
        item_codes = ", ".join([i.item_code for i in items])
        data.append({
            "reference_part": ref.reference_part,
            "part_type": ref.part_type,
            "part_category": ref.part_category,
            "item_codes": item_codes
        })

    return columns, data
