# Copyright (c) 2023, Ababeel Soft and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ExpenseEntry(Document):

	def before_insert(self):
		if self.amended_from:
			self.journal_entry=""


	def before_submit(self):
		journal_entry=frappe.new_doc("Journal Entry")
		journal_entry.voucher_type="Journal Entry"
		journal_entry.company= frappe.defaults.get_global_default("company")
		journal_entry.posting_date=self.posting_date
		journal_entry.user_remark=self.user_remark
		journal_entry.branch=self.branch
		journal_entry.append("accounts", {
		"account":self.account_paid_from,
		"cost_center":self.cost_center,
		"credit_in_account_currency":self.paid_amount,
		"debit_in_account_currency":0,
		})
		journal_entry.append("accounts", {
		"account":self.account_paid_to,
		"cost_center":self.cost_center,
		"credit_in_account_currency":0,
		"debit_in_account_currency":self.paid_amount,
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
		
	