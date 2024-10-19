from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader  
from PIL import Image as PILImage
from io import BytesIO
import tempfile
import os

def generate_pdf(id, name, phone, qr_buffer, isVip):
    """
    Generate a PDF ticket with the attendee's details and QR code.

    Parameters:
    id (str): Attendee's ID
    name (str): Attendee's name
    phone (str): Attendee's phone number
    qr_buffer (BytesIO): QR code image buffer in BytesIO format
    isVip (bool): Boolean indicating if the attendee is a VIP or not

    Returns:
    pdf_buffer (BytesIO): The generated PDF as a BytesIO object
    """
    
    pdf_buffer = BytesIO()

    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)

    pdf.setFillColorRGB(1, 1, 1) 
    pdf.rect(0, 0, letter[0], letter[1], fill=True, stroke=False)

    template_path = (
        "C:\\Users\\Bharath K\\Documents\\Kk\\ticket_template_vip.jpg" if isVip else "C:\\Users\\Bharath K\\Documents\\Kk\\ticket_template_general.jpg"
    )
    pdf.drawImage(template_path, 0, 0, letter[0], letter[1])

    pdf.setFont("Helvetica", 12)
    pdf.setFillColor(colors.lightyellow)

    pdf.drawString(80, 340, f"Dear {name},")

    qr_image = ImageReader(qr_buffer)

    pdf.drawImage(qr_image, 236, 118, width=1.8 * inch, height=1.7 * inch)

    pdf.save()

    pdf_buffer.seek(0)

    return pdf_buffer