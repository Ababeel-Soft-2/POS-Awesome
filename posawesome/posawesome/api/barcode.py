import frappe
from frappe import _
from io import BytesIO
import barcode
from barcode.writer import ImageWriter
import base64

@frappe.whitelist()
def generate_bar_code(barcode_data, item,price=None):
    ean = barcode.get_barcode_class('ean')
    barcode_instance = ean(barcode_data, writer=ImageWriter())
    barcode_path = BytesIO()
    barcode_instance.write(barcode_path)
    barcode_base64 = base64.b64encode(barcode_path.getvalue()).decode()

    html_content = """
    <div style="text-align: center;margin:auto;max-width:500px;">
    <p style="font-size:32px; font-weight: bold;margin-top:-5px;margin-bottom:-5px;text-align: center; text-wrap: balance;">{1}</p>
    </div>
    <div style="text-align: center;margin:auto;margin-top:-5px ;">
    <img  style="align:center" src="data:image/png;base64,{0}" alt="Barcode">
    </div>
    <div style="text-align: center;margin:auto;max-width:500px;">
    <p style="font-size:32px; font-weight: bold;margin-top:-5px;margin-bottom:-5px;text-align: center; text-wrap: balance;">{2}</p>
    </div>
    """.format(barcode_base64, item,price)
    
    return html_content