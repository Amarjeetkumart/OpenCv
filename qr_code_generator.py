import qrcode

def generate_combined_payment_qr(total_price):
    payment_details = f"upi://pay?pa=amarjeetkumart051-4@oksbi&pn=Amarjeet%20kumar&am={total_price}&cu=INR&aid=uGICAgICzhdndCg"

    qr = qrcode.QRCode(version=1, box_size=5, border=5)
    qr.add_data(payment_details)
    qr.make(fit=True)
    return qr.make_image(fill="black", back_color="white")
