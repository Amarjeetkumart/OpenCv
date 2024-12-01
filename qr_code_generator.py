# This file contains the code to generate the QR code for the payment.
import qrcode
# function to generate a combined payment QR code
def generate_combined_payment_qr(total_price):
    payment_details = f"upi://pay?pa=amarjeetkumart051-4@oksbi&pn=Amarjeet%20kumar&am={total_price}&cu=INR&aid=uGICAgICzhdndCg"
    # Create a QR code instance
    qr = qrcode.QRCode(version=1, box_size=5, border=5)
    qr.add_data(payment_details)
    qr.make(fit=True)
    return qr.make_image(fill="black", back_color="white")
# Call the generate_combined_payment_qr function with a sample total price