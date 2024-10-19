# generateQr.py
import qrcode
from io import BytesIO

def generate_qr(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')  # Save as PNG format
    img_buffer.seek(0)  # Go to the start of the BytesIO buffer

    # Debugging: Check the buffer size
    print(f"QR Buffer Size: {img_buffer.getbuffer().nbytes} bytes")
    return img_buffer
