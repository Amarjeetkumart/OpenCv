# This file contains the function to scan a video file for barcodes and retrieve product information from the database.
import cv2
# Import the decode function from the pyzbar library
from pyzbar.pyzbar import decode
# Import the get_product_info function from the database module
from database import get_product_info
# Function to scan a video file for barcodes
def scan_video(video_path):
    scanned_products = []
    total_price = 0.0
# Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Could not open video file.")
# Loop through each frame in the video
    while True:
        ret, frame = cap.read()
        if not ret:
            break
# Decode the barcodes in the frame
        barcodes = decode(frame)
        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            product_info = get_product_info(barcode_data)
            if product_info:
                product_name = product_info["name"]
                product_price = product_info["price"]
                product_discount = product_info["discount"]
                # Calculate the discounted price
                discounted_price = product_price * (1 - product_discount / 100) if product_discount > 0 else product_price

                # Avoid duplicate barcodes
                if not any(p["name"] == product_name for p in scanned_products):
                    scanned_products.append({
                        "name": product_name,
                        "price": product_price,
                        "discount": product_discount,
                        "final_price": discounted_price
                    })
                    total_price += discounted_price
    # Release the video capture object
    cap.release()
    return scanned_products, total_price
# Call the scan_video function with a sample video file