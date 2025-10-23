from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from uuid import UUID, uuid4


class Contact(BaseModel):
    """
    Pydantic model representing a contact submission.
    """
    # The UUID is required for the database/retrieval, but auto-generated here
    contact_id: UUID = Field(default_factory=uuid4, description="Unique identifier for the contact.")

    name: str = Field(..., description="Full name of the contact.")
    email: EmailStr = Field(..., description="Contact's email address.")
    company: str = Field(..., description="Name of the contact's company.")
    use_case: str = Field(..., description="Primary interest/use case selected from the dropdown.")
    message: str = Field(..., description="Detailed message about the project/request.")

    # Optional configuration for Pydantic (e.g., example data for docs)
    class Config:
        json_schema_extra = {
            "example": {
                "contact_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "name": "Jane Doe",
                "email": "jane@company.com",
                "company": "Innovate Corp",
                "use_case": "API Integration",
                "message": "We need a secure way to connect our legacy system to a new cloud service."
            }
        }
