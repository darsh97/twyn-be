import os
import resend
from fastapi import BackgroundTasks
from models.contact import Contact
from dotenv import load_dotenv
from typing import Optional

# Load environment variables for local development
load_dotenv()

# --- Resend Configuration ---
# Fetch credentials securely from environment variables
RESEND_API_KEY: Optional[str] = os.getenv('RESEND_API_KEY')
MAIL_FROM: Optional[str] = os.getenv('MAIL_FROM')
RECIPIENT_EMAIL = "info@twynetic.com"  # The fixed target inbox for notifications

# Initialize the Resend client
if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY
    print("Resend client initialized successfully.")
else:
    print("WARNING: RESEND_API_KEY not found. Emails will NOT be sent.")


def send_contact_notification_sync(contact: Contact):
    """
    Synchronous function to send email via Resend API.
    This must run in a background thread to prevent blocking the main request loop.
    """
    if not resend.api_key or not MAIL_FROM:
        print("Resend configuration incomplete. Skipping email send.")
        return 500

    # 1. Construct the HTML content for the email body
    # Using inline styles for email compatibility
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
            <h2 style="color: #333;">New Contact Form Submission - Twynetic</h2>
            <p>A new inquiry has been received through the contact form:</p>
            <ul style="list-style: none; padding: 0;">
                <li style="margin-bottom: 10px;"><strong>Name:</strong> {contact.name}</li>
                <li style="margin-bottom: 10px;"><strong>Email:</strong> <a href="mailto:{contact.email}">{contact.email}</a></li>
                <li style="margin-bottom: 10px;"><strong>Company:</strong> {contact.company}</li>
                <li style="margin-bottom: 10px;"><strong>Use Case:</strong> {contact.use_case}</li>
            </ul>
            <h3 style="color: #555;">Message:</h3>
            <p style="background-color: #f9f9f9; padding: 15px; border-left: 3px solid #007bff; white-space: pre-wrap;">{contact.message}</p>
            <p style="font-size: 0.9em; color: #777; margin-top: 20px;">Sent via FastAPI Resend Service.</p>
        </div>
    </body>
    </html>
    """

    # 2. Prepare the Resend payload
    params = {
        "from": f"{MAIL_FROM}",
        "to": RECIPIENT_EMAIL,
        "subject": f"New Inquiry: {contact.name} ({contact.company})",
        "html": html_content
    }

    # 3. Make the synchronous API call
    try:
        response = resend.Emails.send(params)
        print(f"Resend Status: Email queued successfully. ID: {response['id']}")
        return 202
    except Exception as e:
        print(f"Resend API Error during send: {e}")
        return 500


async def send_contact_notification(
        background_tasks: BackgroundTasks,
        contact: Contact
):
    """
    Schedules the email sending function to run in a background task using FastAPI's executor.
    """
    background_tasks.add_task(send_contact_notification_sync, contact)