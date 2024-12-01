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
# DB
from mock_database import init_db, insert_transaction
from tkinter import ttk
# Initialize the database at the start of the application
init_db()


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

        # Insert transactions into the mock database
        insert_transaction(scanned_products, total_price)

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

def show_transactions():
    from mock_database import fetch_transactions
    for row in transaction_table.get_children():
        transaction_table.delete(row)

    # Fetch transactions from the database
    transactions = fetch_transactions()
    for transaction in transactions:
        transaction_table.insert("", tk.END, values=transaction)

# show_transactions
def toggle_transaction_table():
    if not transaction_table.winfo_ismapped():  # Check if the table is not currently displayed
        transaction_table.pack(pady=20, fill="both", expand=True)
        show_transactions()  # Populate the table with data
        btn_debug.config(text="Hide Transactions")
    else:
        transaction_table.pack_forget()  # Hide the table
        btn_debug.config(text="Show Transactions")

# GUI Application
app = tk.Tk()
app.title("Barcode Scanner GUI")
app.geometry("800x670")

# Buttons
btn_video = tk.Button(app, text="Process Video", command=process_video, width=20)
btn_video.pack(pady=10)

btn_images = tk.Button(app, text="Process Images", command=process_images, width=20)
btn_images.pack(pady=10)


results_label = tk.Label(app, text="", justify="left", wraplength=500)
results_label.pack(pady=10)

qr_label = tk.Label(app)
qr_label.pack(pady=10)

# Disable the "Save PDF" button initially
btn_save_pdf = tk.Button(app, text="Print Receipt", command=save_pdf, width=20, state=tk.DISABLED)
btn_save_pdf.pack(pady=10)

btn_debug = tk.Button(app, text="Show Transactions", command=toggle_transaction_table, width=20)
btn_debug.pack(pady=10)

# Add a Table to Display Transactions
transaction_table = ttk.Treeview(app, columns=("ID", "Product Name", "Final Price", "Total Price", "Timestamp"), show="headings")
transaction_table.heading("ID", text="ID")
transaction_table.heading("Product Name", text="Product Name")
transaction_table.heading("Final Price", text="Final Price (₹)")
transaction_table.heading("Total Price", text="Total Price (₹)")
transaction_table.heading("Timestamp", text="Timestamp")
transaction_table.column("ID", width=50)
transaction_table.column("Product Name", width=200)
transaction_table.column("Final Price", width=100)
transaction_table.column("Total Price", width=100)
transaction_table.column("Timestamp", width=200)


app.mainloop()
