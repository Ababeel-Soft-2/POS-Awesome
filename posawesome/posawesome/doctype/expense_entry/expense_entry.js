// Copyright (c) 2023, Ababeel Soft and contributors
// For license information, please see license.txt

frappe.ui.form.on('Expense Entry', {
	onload: function(frm) {
		frm.set_query('account_paid_from', () => {
			return {
				filters: {
					account_type:"Cash",
					is_group:0
				}
			}
		});
		frm.set_query('account_paid_to', () => {
			return {
				filters: {
					account_type:["in",["Expense Account","Expenses Included In Valuation"]],
					is_group:0
				}
			}
		});
		frm.set_query('cost_center', () => {
			return {
				filters: {
					is_group:0
				}
			}
		});

	}
});


