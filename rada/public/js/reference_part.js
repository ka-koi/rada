// Validation for year range in Applicable Units
frappe.ui.form.on('Applicable Units', {
    to_year: function(frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        if (row.to_year && row.from_year && row.to_year < row.from_year) {
            frappe.msgprint(__('To Year cannot be earlier than From Year'));
            frappe.model.set_value(cdt, cdn, 'to_year', row.from_year);
        }
    }
});

// Row-level check to prevent duplicate item_code in Reference Part Item
frappe.ui.form.on('Reference Part Item', {
    item_code: function(frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        const current_code = row.item_code;

        const is_duplicate = frm.doc.items.some(r =>
            r.item_code === current_code && r.name !== row.name
        );

        if (is_duplicate) {
            frappe.msgprint(`Same item cannot be entered multiple times; "${current_code}".`);
            frappe.model.set_value(cdt, cdn, 'item_code', null);
        }
    }
});
