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
					account_type:["in",["Expense Account","Expenses Included In Valuation","Chargeable"]],
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

	},account_currency : function(frm){
		chek_exchange_rate(frm);
	},paid_amount : function(frm){
		set_total_local_currancy(frm);
	},
	exchange_rate : function(frm){
		set_total_local_currancy(frm);
	},refresh : function(frm){
		chek_exchange_rate(frm);
	},expance_account_currency : function(frm){
		chek_exchange_rate(frm);
	}
	
	

});

function chek_exchange_rate (frm){
let enable = 0;
if(frm.doc.account_currency !='LYD' || frm.doc.expance_account_currency !='LYD'){ enable = 1 ;}
frm.toggle_display('exchange_rate',enable);
frm.set_df_property('exchange_rate', 'reqd',enable);

}

function set_total_local_currancy(frm){
	if(frm.doc.paid_amount && frm.doc.exchange_rate){
		let num = frm.doc.paid_amount  * frm.doc.exchange_rate
	   frm.set_value("local_currency_value",num);
	}else{
	   frm.set_value("local_currency_value","");
	}	
}


function set_exchange_rate(frm){
	if(frm.doc.account_paid_from){
		frappe.call({
			method: "posawesome.posawesome.doctype.expense_entry.expense_entry.get_old_exhange_rate",
			args: {
			account:frm.doc.account_paid_from
			},
			callback: function(r) {
			frm.set_value("exchange_rate",r.message);
			}
			});
	}
	
	
	
}