from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader  # Import for handling BytesIO images
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
    
    # Create a BytesIO buffer to store the PDF
    pdf_buffer = BytesIO()

    # Create the PDF document
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)

    # Add background color (white) in case the template is not fully covered
    pdf.setFillColorRGB(1, 1, 1)  # White background
    pdf.rect(0, 0, letter[0], letter[1], fill=True, stroke=False)

    # Load the correct template (VIP or General)
    template_path = (
        "C:\\Users\\Bharath K\\Documents\\Kk\\ticket_template_vip.jpg" if isVip else "C:\\Users\\Bharath K\\Documents\\Kk\\ticket_template_general.jpg"
    )
    pdf.drawImage(template_path, 0, 0, letter[0], letter[1])

    # Set font for the name text
    pdf.setFont("Helvetica", 12)
    pdf.setFillColor(colors.lightyellow)

    # Add attendee name at specific coordinates
    pdf.drawString(80, 340, f"Dear {name},")

    # Convert the QR code buffer into an image using ImageReader
    qr_image = ImageReader(qr_buffer)

    # Draw the QR code onto the PDF at the specified coordinates
    pdf.drawImage(qr_image, 236, 118, width=1.8 * inch, height=1.7 * inch)

    # Save the PDF content to the buffer
    pdf.save()

    # Move the buffer position to the beginning of the PDF
    pdf_buffer.seek(0)

    return pdf_buffer