from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import pytz

def generate_pdf_receipt(scanned_products, total_price, shop_name, shop_address):
    filename = "./pdf/receipt.pdf"
    india_timezone = pytz.timezone('Asia/Kolkata')
    current_datetime = datetime.now(india_timezone).strftime("%Y-%m-%d %H:%M:%S")


    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 40, shop_name)
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 60, shop_address)
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 80, f"Date: {current_datetime}")
    c.line(50, height - 90, width - 50, height - 90)

    y_position = height - 120
    c.setFont("Helvetica", 10)
    c.drawString(50, y_position, "Product")
    c.drawString(300, y_position, "Price")
    c.drawString(400, y_position, "Discount (%)")
    c.drawString(500, y_position, "Final Price")
    y_position -= 20

    for product in scanned_products:
        c.drawString(50, y_position, product['name'])
        c.drawString(300, y_position, f"₹{product['price']:.2f}")
        c.drawString(400, y_position, f"{product['discount']}%")
        c.drawString(500, y_position, f"₹{product['final_price']:.2f}")
        y_position -= 20



    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, f"Total Price: ₹ {total_price:.2f}")
    c.save()
    return filename
