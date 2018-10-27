# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt
from __future__ import unicode_literals

import json
import frappe
import frappe.handler
import frappe.client
from frappe.utils.response import build_response
from frappe import _
from six.moves.urllib.parse import urlparse, urlencode

@frappe.whitelist()	
def hit_docstatus(doctype,docname):
	val = frappe.get_value(str(doctype), str(docname), "docstatus")
	if val == 2 :
		frappe.db.sql("""update `tab{}` set docstatus=0 where name='{}'""".format(doctype,docname))
		doc = frappe.get_doc(str(doctype),str(docname))
		doc.save()
		return "1"
	else:
		frappe.throw("Record must be Cancelled to Make it Draft again ")

def renaming_doc(doc, method):
	# import pdb;pdb.set_trace()
	if hasattr(doc , "amended_from"):
		if doc.get('amended_from') != None :
			# import pdb;pdb.set_trace()
			amended_from = doc.get('amended_from')
			doc.amended_from = None # remove entry with key 'amended_from'
			doc.amendment_date = None
			doc.docstatus = 0
			doc.status = "Draft"
			doc.name = amended_from
			frappe.delete_doc(doc.doctype, amended_from ,force=1,ignore_permissions=True)
			frappe.db.commit()


			# frappe.rename_doc(doc.doctype,doc.name,amended_from,force=1)
			# frappe.db.commit()

			# draft_doc.insert()

			# # new_doc.name=amended_from
			# new_doc = frappe.copy_doc(doc)
			# new_doc.name = amended_from
			# new_doc.insert(ignore_permissions=True)
			# frappe.db.commit()


			# frappe.delete_doc(doc.doctype, doc.name, force=1,ignore_permissions=True)
			# frappe.db.commit()
			# frappe.delete_doc()

		else:
			print("Normal Insert")
