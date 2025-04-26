from pydantic import BaseModel, EmailStr
from uuid import UUID

class MailRequest(BaseModel):
    email: EmailStr  
    password: str
    token: str

class LinkRequest(BaseModel):
    email: EmailStr
    link: str

class TextMessageRequest(BaseModel):
    email: EmailStr
    subject: str
    message: str

class TextWithIdRequest(BaseModel):
    id: UUID
    email: EmailStr
    subject: str
    message: str

class EmailRecordCreate(BaseModel):
    email: str

    class Config:
        orm_mode = True
