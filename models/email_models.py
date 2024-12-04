from pydantic import BaseModel, EmailStr

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
