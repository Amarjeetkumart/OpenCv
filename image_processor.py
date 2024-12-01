# This file contains the function to scan barcodes from images
import cv2
# Import the decode function from the pyzbar library
from pyzbar.pyzbar import decode
# Import the get_product_info function from the database module
from database import get_product_info
# function to scan barcodes from images
def scan_barcodes(image_paths):
    scanned_products = []
    total_price = 0.0
    # Loop through each image path
    for image_path in image_paths:
        img = cv2.imread(image_path)
        barcodes = decode(img)
        # Loop through each barcode detected in the image
        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            product_info = get_product_info(barcode_data)
            if product_info:
                product_name = product_info["name"]
                product_price = product_info["price"]
                product_discount = product_info["discount"]
                # Calculate the discounted price
                discounted_price = product_price * (1 - product_discount / 100) if product_discount > 0 else product_price
                # Avoid duplicate products
                scanned_products.append({
                    "name": product_name,
                    "price": product_price,
                    "discount": product_discount,
                    "final_price": discounted_price
                })
                total_price += discounted_price
    # Return the scanned products and total price
    return scanned_products, total_price
# return the list of transactions