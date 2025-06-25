frappe.ui.form.on('Applicable Units', {
    to_year: function(frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        if (row.to_year && row.from_year && row.to_year < row.from_year) {
            frappe.msgprint(__('To Year cannot be earlier than From Year'));
            frappe.model.set_value(cdt, cdn, 'to_year', row.from_year);
        }
    }
});
