import cv2
from pyzbar.pyzbar import decode
from database import get_product_info

def scan_barcodes(image_paths):
    scanned_products = []
    total_price = 0.0

    for image_path in image_paths:
        img = cv2.imread(image_path)
        barcodes = decode(img)

        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            product_info = get_product_info(barcode_data)
            if product_info:
                product_name = product_info["name"]
                product_price = product_info["price"]
                product_discount = product_info["discount"]

                discounted_price = product_price * (1 - product_discount / 100) if product_discount > 0 else product_price

                scanned_products.append({
                    "name": product_name,
                    "price": product_price,
                    "discount": product_discount,
                    "final_price": discounted_price
                })
                total_price += discounted_price

    return scanned_products, total_price
