import tkinter as tk
from tkinter import filedialog, messagebox
from video_processor import scan_video
from image_processor import scan_barcodes
from qr_code_generator import generate_combined_payment_qr
from pdf_generator import generate_pdf_receipt
from PIL import Image, ImageTk
from threading import Thread
import os
from tkinter import filedialog


PDF_FILENAME = "./pdf/receipt.pdf"  # Name of the PDF file to be printed

def process_video():
    video_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
    if not video_path:
        messagebox.showinfo("No File Selected", "Please select a video file.")
        return

    def process():
        try:
            scanned_products, total_price = scan_video(video_path)
            display_results(scanned_products, total_price)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    thread = Thread(target=process)
    thread.start()

def process_images():
    file_paths = filedialog.askopenfilenames(title="Select Barcode Images", filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if not file_paths:
        messagebox.showinfo("No Files Selected", "Please select at least one image.")
        return

    scanned_products, total_price = scan_barcodes(file_paths)
    display_results(scanned_products, total_price)

def display_results(scanned_products, total_price):
    if scanned_products:
        qr_image = generate_combined_payment_qr(total_price)
        qr_image.save("./payment_qr/payment_qr.png")

        shop_name = "SuperMart"
        shop_address = "123 Market Street, City, Country"
        generate_pdf_receipt(scanned_products, total_price, shop_name, shop_address)

        results_text = "\n".join([f"{p['name']}: ₹{p['final_price']:.2f}" for p in scanned_products])
        results_label.config(text=f"Scanned Products:\n{results_text}\n\nTotal Price: ₹{total_price:.2f}")

        qr_img = ImageTk.PhotoImage(qr_image)
        qr_label.config(image=qr_img)
        qr_label.image = qr_img
        messagebox.showinfo("Success", "QR Code and PDF Receipt generated.")
        
        # Enable the "Save PDF" button after the QR code is generated
        btn_save_pdf.config(state=tk.NORMAL)
    else:
        messagebox.showwarning("No Barcodes Found", "No valid barcodes were found.")

def save_pdf():
    if os.path.exists(PDF_FILENAME):
        # Ask the user where to save the file
        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save PDF As"
        )
        if save_path:
            try:
                # Copy the generated receipt.pdf to the chosen path
                import shutil
                shutil.copy(PDF_FILENAME, save_path)
                messagebox.showinfo("Success", f"PDF saved as {save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save the PDF: {e}")
    else:
        messagebox.showwarning("File Not Found", f"{PDF_FILENAME} not found. Please generate the PDF first.")

# GUI Application
app = tk.Tk()
app.title("Barcode Scanner GUI")
app.geometry("800x670")

btn_video = tk.Button(app, text="Process Video", command=process_video, width=20)
btn_video.pack(pady=20)

btn_images = tk.Button(app, text="Process Images", command=process_images, width=20)
btn_images.pack(pady=20)


results_label = tk.Label(app, text="", justify="left", wraplength=500)
results_label.pack(pady=10)

qr_label = tk.Label(app)
qr_label.pack(pady=10)

# Disable the "Save PDF" button initially
btn_save_pdf = tk.Button(app, text="Print Receipt", command=save_pdf, width=20, state=tk.DISABLED)
btn_save_pdf.pack(pady=20)

app.mainloop()
