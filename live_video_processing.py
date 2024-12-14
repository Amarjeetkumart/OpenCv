import cv2
from pyzbar.pyzbar import decode
from PIL import Image, ImageTk
from threading import Thread
from tkinter import messagebox

# Import necessary functions
from database import database
from qr_code_generator import generate_combined_payment_qr
from pdf_generator import generate_pdf_receipt

# Global variable for webcam capture
cap = None  # Keeps track of the webcam instance

def start_live_video_processing(video_label, results_label, qr_label, scanned_products, total_price):
    """
    Starts live video processing using the webcam.
    """
    global cap
    

    cap = cv2.VideoCapture(0)  # Open webcam (0 is the default camera)

    if not cap.isOpened():
        messagebox.showerror("Error", "Could not access webcam.")
        return

    def process_frame():
        nonlocal total_price

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Decode barcodes from the current frame
            barcodes = decode(frame)
            for barcode in barcodes:
                barcode_data = barcode.data.decode("utf-8")
                product_info = database.get(barcode_data)
                if product_info:
                    product_name = product_info["name"]
                    product_price = product_info["price"]
                    product_discount = product_info["discount"]

                    discounted_price = product_price * (1 - product_discount / 100) if product_discount > 0 else product_price

                    # Avoid duplicate entries
                    if not any(p["name"] == product_name for p in scanned_products):
                        scanned_products.append({
                            "name": product_name,
                            "price": product_price,
                            "discount": product_discount,
                            "final_price": discounted_price
                        })
                        total_price += discounted_price

            # Display the live video feed
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_image = Image.fromarray(frame_rgb)
            frame_image = ImageTk.PhotoImage(frame_image)

            video_label.config(image=frame_image)
            video_label.image = frame_image

        cap.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Live Video Stopped", "Video processing has stopped.")
        update_results(results_label, qr_label, scanned_products, total_price)

    # Start processing in a separate thread
    thread = Thread(target=process_frame, daemon=True)
    thread.start()

def stop_live_video():
    """
    Stops the live video processing.
    """
    global cap
    if cap and cap.isOpened():
        cap.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Stopped", "Live video processing has been stopped.")

def update_results(results_label, qr_label, scanned_products, total_price):
    """
    Updates the GUI with scanned products, total price, and generates a QR code and PDF receipt.
    """
    if scanned_products:
        results_text = "\n".join([f"{p['name']}: ₹{p['final_price']:.2f}" for p in scanned_products])
        results_label.config(text=f"Scanned Products:\n{results_text}\n\nTotal Price: ₹{total_price:.2f}")

        qr_image = generate_combined_payment_qr(total_price)
        qr_image.save("./payment_qr/payment_qr.png")

        qr_img = ImageTk.PhotoImage(qr_image)
        qr_label.config(image=qr_img)
        qr_label.image = qr_img

        # Generate PDF Receipt
        shop_name = "SuperMart"
        shop_address = "123 Market Street, City, Country"
        generate_pdf_receipt(scanned_products, total_price, shop_name, shop_address)
    else:
        results_label.config(text="No products scanned.")
