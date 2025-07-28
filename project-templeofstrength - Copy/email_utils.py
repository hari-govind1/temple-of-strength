import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# In email_utils.py
def send_payment_email(recipient_email, name, program_name, program_price):
    try:
        print("Starting email send process...")
        
        if program_price > 0:
            # Payment email (as before)
            subject = f"Welcome to {program_name} at Temple of Strength!"
            body = f"""
            Hello {name},

            Thank you for your interest in the {program_name} at Temple of Strength! We're excited to help you reclaim your ancestral strength.

            Program: {program_name}
            Price: ₹{program_price}

            To complete your payment, use this link: [Your Payment Link, e.g., https://pay.example.com or UPI ID].

            If you have any questions, reply to this email.

            Best regards,
            Temple of Strength Team
            """
        else:
            # Welcome/invitation email for contact form
            subject = f"Invitation to Temple of Strength - Let's Start Your Journey!"
            body = f"""
            Hello {name},

            Thank you for reaching out to Temple of Strength! We're thrilled about your interest in our {program_name} program.

            At Temple of Strength, we guide you on a Dharmic path to reclaim your strength, heal through ancient Vyayam, and live with Virya. Whether you're new to our vegetarian-friendly training or ready to dive deeper, we're here to support you.

            What's next? Book a free consultation or join our next cohort. Reply to this email for personalized guidance.

            Reawaken your Dharma with us!

            Best regards,
            Temple of Strength Team
            info@templeofstrength.in | [Your Phone Number]
            """

        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            print("Logging in...")
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            print("Login successful, sending email...")
            server.sendmail(EMAIL_ADDRESS, recipient_email, msg.as_string())
            print("Email sent successfully!")
    
    except Exception as e:
        print(f"Error sending email: {e}")
        raise
