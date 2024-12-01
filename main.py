# tkinter is a standard Python interface to the Tk GUI toolkit
import tkinter as tk
from tkinter import filedialog, messagebox
# Import the scan_video function from video_processor.py
from video_processor import scan_video
# Import the scan_barcodes function from image_processor.py
from image_processor import scan_barcodes
# Import the generate_combined_payment_qr function from qr_code_generator.py
from qr_code_generator import generate_combined_payment_qr
# Import the generate_pdf_receipt function from pdf_generator.py
from pdf_generator import generate_pdf_receipt
# Import the Image and ImageTk classes from the PIL module
from PIL import Image, ImageTk
# Import the Thread class from the threading module
from threading import Thread
# Import the os module to check if a file exists
import os
from tkinter import filedialog
# Database imports for mock_database.py
from mock_database import init_db, insert_transaction
from tkinter import ttk
# Initialize the database at the start of the application
init_db()


PDF_FILENAME = "./pdf/receipt.pdf"  
# Name of the PDF file to be printed
# Function to process the video file
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
    # Create a new thread to process the video
    thread = Thread(target=process)
    thread.start()
# Function to process the images
def process_images():
    file_paths = filedialog.askopenfilenames(title="Select Barcode Images", filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if not file_paths:
        messagebox.showinfo("No Files Selected", "Please select at least one image.")
        return
    # Call the scan_barcodes function to process the images
    scanned_products, total_price = scan_barcodes(file_paths)
    display_results(scanned_products, total_price)
# Function to display the results
def display_results(scanned_products, total_price):
    if scanned_products:
        qr_image = generate_combined_payment_qr(total_price)
        qr_image.save("./payment_qr/payment_qr.png")
        # Generate a PDF receipt with the scanned products and total price
        shop_name = "SuperMart"
        shop_address = "123 Market Street, City, Country"
        generate_pdf_receipt(scanned_products, total_price, shop_name, shop_address)

        # Insert transactions into the mock database
        insert_transaction(scanned_products, total_price)
        # Display the scanned products and total price in the GUI
        results_text = "\n".join([f"{p['name']}: ₹{p['final_price']:.2f}" for p in scanned_products])
        results_label.config(text=f"Scanned Products:\n{results_text}\n\nTotal Price: ₹{total_price:.2f}")
        # Display the QR code in the GUI
        qr_img = ImageTk.PhotoImage(qr_image)
        qr_label.config(image=qr_img)
        qr_label.image = qr_img
        messagebox.showinfo("Success", "QR Code and PDF Receipt generated.")
        
        # Enable the "Save PDF" button after the QR code is generated
        btn_save_pdf.config(state=tk.NORMAL)
    else:
        messagebox.showwarning("No Barcodes Found", "No valid barcodes were found.")
# Function to save the generated PDF receipt
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
# Function to show transactions in the table
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

# Buttons for processing video
btn_video = tk.Button(app, text="Process Video", command=process_video, width=20)
btn_video.pack(pady=10)
# Buttons for processing images
btn_images = tk.Button(app, text="Process Images", command=process_images, width=20)
btn_images.pack(pady=10)

# Label to display the results
results_label = tk.Label(app, text="", justify="left", wraplength=500)
results_label.pack(pady=10)
# Label to display the QR code
qr_label = tk.Label(app)
qr_label.pack(pady=10)

# Disable the "Save PDF" button initially
btn_save_pdf = tk.Button(app, text="Print Receipt", command=save_pdf, width=20, state=tk.DISABLED)
btn_save_pdf.pack(pady=10)
# Button to show transactions
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

# Run the Tkinter event loop
app.mainloop()
