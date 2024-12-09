# This file contains the code to generate a PDF receipt for the scanned products.
from reportlab.lib.pagesizes import letter
# Import the canvas class from the reportlab.pdfgen module
from reportlab.pdfgen import canvas
# Import the datetime and pytz modules
from datetime import datetime
# Import the pytz module to get the timezone
import pytz
# function to generate a PDF receipt
def generate_pdf_receipt(scanned_products, total_price, shop_name, shop_address):
    filename = "./pdf/receipt.pdf"
    india_timezone = pytz.timezone('Asia/Kolkata')
    current_datetime = datetime.now(india_timezone).strftime("%Y-%m-%d %H:%M:%S")

    # Create a new PDF document
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    # Set the font and font size
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 40, shop_name)
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 60, shop_address)
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 80, f"Date: {current_datetime}")
    c.line(50, height - 90, width - 50, height - 90)
    # Draw the table headers
    y_position = height - 120
    c.setFont("Helvetica", 10)
    c.drawString(50, y_position, "Product")
    c.drawString(300, y_position, "Price")
    c.drawString(400, y_position, "Discount (%)")
    c.drawString(500, y_position, "Final Price")
    y_position -= 20
    # Draw the scanned products in the table
    for product in scanned_products:
        c.drawString(50, y_position, product['name'])
        c.drawString(300, y_position, f"$ {product['price']:.2f}")
        c.drawString(400, y_position, f"{product['discount']}%")
        c.drawString(500, y_position, f"$ {product['final_price']:.2f}")
        y_position -= 20


    # Draw the total price at the bottom of the receipt
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, f"Total Price: $ {total_price:.2f}")
    c.save()
    return filename
# Call the generate_pdf_receipt function with sample data