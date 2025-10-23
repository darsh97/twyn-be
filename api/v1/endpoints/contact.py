from fastapi import APIRouter, HTTPException, Path
from typing import List, Dict, Any
from uuid import UUID
from models.contact import Contact

router = APIRouter(tags=["Contacts"])

# --- Mock Data Store ---
# In a real application, this would be a database connection.
MOCK_CONTACTS: Dict[UUID, Contact] = {
    UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef"): Contact(
        name="John Smith",
        email="john@example.com",
        company="Tech Solutions",
        use_case="Data Analysis",
        message="Looking for a custom data pipeline.",
        contact_id=UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef")
    ),
    UUID("b0c1d2e3-f4a5-6789-0123-456789fedcba"): Contact(
        name="Alice Johnson",
        email="alice@web.net",
        company="Web Services Inc.",
        use_case="Frontend Development",
        message="Need an API to power our new website.",
        contact_id=UUID("b0c1d2e3-f4a5-6789-0123-456789fedcba")
    )
}

# --------------------------

@router.get(
    "/contacts",
    response_model=List[Contact],
    summary="Retrieve a list of all contact submissions"
)
async def get_all_contacts() -> List[Contact]:
    """
    Returns a list of all contact submissions in the mock store.
    """
    # FastAPI automatically serializes the list of Pydantic models to JSON
    return list(MOCK_CONTACTS.values())


@router.get(
    "/contact/{contact_id}",
    response_model=Contact,
    summary="Retrieve a specific contact submission by ID"
)
async def get_contact_by_id(
    contact_id: UUID = Path(
        ...,
        title="Contact ID",
        description="The UUID of the contact to retrieve."
    )
) -> Contact:
    """
    Retrieves a single contact based on its unique UUID.
    Raises a 404 error if the ID is not found.
    """
    contact = MOCK_CONTACTS.get(contact_id)
    if contact is None:
        # Use HTTPException for standardized FastAPI error responses
        raise HTTPException(
            status_code=404,
            detail=f"Contact with ID {contact_id} not found"
        )
    return contact