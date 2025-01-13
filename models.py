from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

Base = declarative_base()

class EmailRecord(Base):
    __tablename__ = 'emails'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)  
    email = Column(String, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow) 
    wants_newsletter = Column(Boolean, nullable=False, default=True)  