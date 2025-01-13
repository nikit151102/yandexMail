from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import EmailRecord
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy.future import select


async def get_emails_to_db(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(EmailRecord).offset(skip).limit(limit)
    )
    return result.scalars().all()  


async def add_email_to_db(db: AsyncSession, email: str, wants_newsletter: bool):
    db_email = EmailRecord(email=email, wants_newsletter=wants_newsletter, date=datetime.now())
    db.add(db_email)
    await db.commit()  
    await db.refresh(db_email) 
    return db_email


async def delete_email_from_db(db: AsyncSession, email_id: UUID):
    db_email = await db.get(EmailRecord, email_id)
    if db_email is None:
        raise HTTPException(status_code=404, detail="Email not found")
    await db.delete(db_email)
    await db.commit()
    return db_email


async def update_email_in_db(db: AsyncSession, email_id: UUID, new_email: str, wants_newsletter: bool):
    db_email = await db.execute(select(EmailRecord).filter(EmailRecord.id == email_id))
    db_email = db_email.scalar()

    if db_email:
        db_email.email = new_email
        db_email.wants_newsletter = wants_newsletter
        db_email.date = datetime.utcnow()
        await db.commit()
        await db.refresh(db_email) 
        return db_email
    else:
        raise HTTPException(status_code=404, detail="Email record not found")


