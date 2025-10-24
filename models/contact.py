from pydantic import BaseModel, Field, EmailStr

class Contact(BaseModel):
    """
    Data model for receiving contact form submissions (request body).
    """
    name: str = Field(..., max_length=100)
    email: EmailStr
    company: str = Field(..., max_length=100)
    use_case: str = Field(..., max_length=50)
    message: str = Field(..., max_length=2000)

class ContactResponse(Contact):
    """
    Data model for the API response after a successful submission.
    """
    confirmation_message: str