from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class EmailRecordBase(BaseModel):
    email: str

class EmailRecordCreate(EmailRecordBase):
    wants_newsletter: bool = True
    pass

class EmailRecord(EmailRecordBase):
    id: UUID
    date: datetime

    class Config:
        orm_mode = True
        
class EmailRecordOut(BaseModel):
    id: UUID
    email: str
    date: datetime
    wants_newsletter: bool
    
    class Config:
        orm_mode = True 