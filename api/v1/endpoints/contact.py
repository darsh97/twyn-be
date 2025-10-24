from fastapi import APIRouter, HTTPException, Path, status, BackgroundTasks
from typing import List, Dict, Any
from uuid import UUID
from models.contact import Contact, ContactResponse
from core.email import send_contact_notification

router = APIRouter(tags=["Contacts"])


# --------------------------

@router.post(
    "/contacts",
    response_model=ContactResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Submit contact form and queue email notification via Resend"
)
async def create_contact_and_email(
        contact_data: Contact,
        background_tasks: BackgroundTasks
) -> ContactResponse:
    """
    Receives contact data from the front-end and queues an email notification.
    The database step is skipped for the MVP.
    Returns 202 Accepted immediately as the email is processed in the background.
    """
    print(contact_data)
    # Schedule the email sending task
    await send_contact_notification(background_tasks, contact_data)

    # Return immediate success (202 Accepted) to the client
    return ContactResponse(
        **contact_data.model_dump(),
        confirmation_message="Your message has been received and the notification email is being sent via Resend."
    )
