import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from io import BytesIO
from generateQr import generate_qr
email_accounts = [
    {"email": "kannadarajyothsava1@gmail.com", "password": ""},
    {"email": "kannadarajyothsava2@gmail.com", "password": ""},
    {"email": "kannadarajyothsava3@gmail.com", "password": ""},
]

email_index = 0

def send_email(target_email, name, PRN, pdf_buffer):
    '''
    Function to send an email to the target email address with an attached PDF document using SSL.
    target_email: Email address of the recipient
    name: Name of the recipient
    PRN: PRN of the recipient
    pdf_buffer: BytesIO object containing the PDF document
    '''

    global email_index  

    # Get the sender's email and password
    sender_email = email_accounts[email_index]["email"]
    sender_password = email_accounts[email_index]["password"]

    # Update the index to use the next email account for the next call
    email_index = (email_index + 1) % len(email_accounts)

    subject = f"Document for {name} (PRN: {PRN})"
    
    # Create the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = target_email
    message['Subject'] = subject

    # Email body
    body = f"Dear {name},\n\nPlease find attached the required document.\n\nBest regards,\nYour Name"
    message.attach(MIMEText(body, 'plain'))

    # Attach the PDF document from the BytesIO buffer
    try:
        pdf_buffer.seek(0)  # Ensure we're at the start of the BytesIO buffer
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(pdf_buffer.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename=document.pdf')
        message.attach(part)
    except Exception as e:
        print(f"Failed to attach the PDF document: {e}")
        return

    # Send the email using SMTP SSL
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:  
            server.login(sender_email, sender_password)  
            server.sendmail(sender_email, target_email, message.as_string())
            print(f"Email sent successfully to {target_email} using {sender_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Sample function call to test the email sending functionality
if __name__ == "__main__":
    # Example usage with a sample PDF buffer
    from generatePDF import generate_pdf  # Import the function from your generatePDF.py

    # Generate a sample PDF in memory
    PRN = ""
    sample_name = ""
    sample_phone = ""
    is_vip = True
   # Generate the QR code image buffer
    qr_data = f"{PRN}, {sample_name}, {sample_phone}"  # Customize this as needed
    qr_buffer = generate_qr(qr_data)
    pdf_buffer = generate_pdf(PRN, sample_name, sample_phone, qr_buffer, is_vip)

    send_email("", sample_name, PRN, pdf_buffer)
