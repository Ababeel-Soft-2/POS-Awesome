# Copyright (c) 2023, Ababeel Soft and contributors
# For license information, please see license.txt
from functools import reduce
import frappe
from frappe.model.document import Document

class ExpenseEntry(Document):

	def before_insert(self):
		if self.amended_from:
			self.journal_entry=""


	def before_submit(self):
		exchange_rate = self.exchange_rate
		local_currency_value= self.local_currency_value
		if self.account_currency =="LYD":
			exchange_rate=1
			local_currency_value = self.paid_amount


		journal_entry=frappe.new_doc("Journal Entry")
		journal_entry.voucher_type="Journal Entry"
		journal_entry.company= frappe.defaults.get_global_default("company")
		journal_entry.posting_date=self.posting_date
		journal_entry.user_remark=self.user_remark
		journal_entry.branch=self.branch
		journal_entry.multi_currency=1
		journal_entry.append("accounts",{
		"account":self.account_paid_from,
		"cost_center":self.cost_center,
		"credit_in_account_currency":self.paid_amount,
		"debit_in_account_currency":0,
		"exchange_rate":exchange_rate
		})
		journal_entry.append("accounts", {
		"account":self.account_paid_to,
		"cost_center":self.cost_center,
		"credit_in_account_currency":0,
		"debit_in_account_currency":local_currency_value,
		})
		journal_entry.save()
		journal_entry.submit()
		self.journal_entry=journal_entry.name
		self.canceled_docs=""

	def on_cancel(self):
		journal_entry=frappe.get_doc("Journal Entry",self.journal_entry)
		journal_entry.cancel()
		self.journal_entry=""
		
	
	def before_cancel(self):
		self.canceled_docs=self.journal_entry
		
	


@frappe.whitelist()
def get_old_exhange_rate(account):
	old_exhange_rate=0.0
	account_balance,account_currency_balance=get_account_balance(account)
	if not account_currency_balance:
		msg="Account ' "+str(account)+" ' Balance Is :"+str(account_currency_balance)+""
		frappe.throw(msg)

	old_exhange_rate =round((account_balance/account_currency_balance),3)
	return old_exhange_rate


def get_account_balance(account):
	gls=frappe.db.get_all("GL Entry", filters={"account":account,"is_cancelled":0},fields="*")
	if not gls:
		return 0,0
	account_balance=reduce(sum_account_balance,list(map(get_gl_balance,gls)))
	account_currancy_balance=reduce(sum_account_balance,list(map(get_gl_currancy_balance,gls)))
	# print(account_balance,account_currancy_balance)

	print(account_balance,account_currancy_balance)
	return account_balance,account_currancy_balance


def sum_account_balance(num,num2):
    return (num)+(num2)

def get_gl_balance(gl):
    return (gl.debit)-(gl.credit)


def get_gl_currancy_balance(gl):
    return (gl.debit_in_account_currency)-(gl.credit_in_account_currency)