from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import schemas
from database.database_app import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from database.database_app import get_session
from models import EmailRecord 

router = APIRouter()

@router.post("/{email_id}/subscribe/", response_model=schemas.EmailRecordOut)
async def subscribe_email_by_id(
    email_id: UUID,
    db: AsyncSession = Depends(get_session)
):
    
    result = await db.execute(select(EmailRecord).filter(EmailRecord.id == email_id))
    db_email = result.scalar_one_or_none()
    
    if not db_email:
        raise HTTPException(status_code=404, detail="Email не найден")

    db_email.wants_newsletter = True
    db.add(db_email)
    
    try:
        await db.commit()
        await db.refresh(db_email)
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка обновления подписки: {str(e)}")
    
    return db_email


@router.post("/{email_id}/unsubscribe/", response_model=schemas.EmailRecordOut)
async def unsubscribe_email_by_id(
    email_id: UUID,
    db: AsyncSession = Depends(get_session)
):
    
    result = await db.execute(select(EmailRecord).filter(EmailRecord.id == email_id))
    db_email = result.scalar_one_or_none()
    
    if not db_email:
        raise HTTPException(status_code=404, detail="Email не найден")
    
    db_email.wants_newsletter = False
    db.add(db_email)
    
    try:
        await db.commit()
        await db.refresh(db_email)
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка обновления подписки: {str(e)}")
    
    return db_email

@router.get("/{email_id}/subscription-status/", response_model=schemas.EmailRecordOut)
async def check_subscription_status_by_id(
    email_id: UUID,
    db: AsyncSession = Depends(get_session)
):
    
    result = await db.execute(select(EmailRecord).filter(EmailRecord.id == email_id))
    db_email = result.scalar_one_or_none()
    
    if not db_email:
        raise HTTPException(status_code=404, detail="Email не найден")
    
    return db_email

@router.post("/public/unsubscribe/{email_id}/", response_model=schemas.EmailRecordOut)
async def public_unsubscribe_by_id(
    email_id: UUID,
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(select(EmailRecord).filter(EmailRecord.id == email_id))
    db_email = result.scalar_one_or_none()
    
    if not db_email:
        raise HTTPException(status_code=404, detail="Email не найден")
    
    db_email.wants_newsletter = False
    db.add(db_email)
    
    try:
        await db.commit()
        await db.refresh(db_email)
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка обновления подписки: {str(e)}")
    
    return db_email