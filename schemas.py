from pydantic import BaseModel, EmailStr
from typing import Optional, List

class ContactIn(BaseModel):
    email: EmailStr
    name: str
    company: Optional[str] = None
    phone: Optional[str] = None
    tags: Optional[List[str]] = None

class ContactOut(ContactIn):
    id: int
