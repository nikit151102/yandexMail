from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from config import conf
import crudEmail
from pydantic import BaseModel, EmailStr
import schemas
from database.database_app import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Union
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from datetime import datetime
import re
import openpyxl
from io import BytesIO

from database.database_app import get_session
from schemas import EmailRecord, EmailRecordOut
from models import EmailRecord 
from pydantic import BaseModel, EmailStr
from services.security_service import verify_credentials


router = APIRouter()
security = HTTPBasic()



def is_valid_email(email: str) -> bool:
    """Проверка на валидность email."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(email_regex, email))


def extract_emails_from_excel(file_content: bytes) -> List[str]:
    """Извлечение email из Excel файла."""
    try:
        workbook = openpyxl.load_workbook(filename=BytesIO(file_content))
        sheet = workbook.active
    except Exception:
        raise HTTPException(status_code=400, detail="Ошибка при чтении Excel файла")

    emails = []
    for row in sheet.iter_rows(min_row=2, min_col=1, max_col=1):  # Начинаем с 2-й строки
        cell_value = row[0].value
        if cell_value and isinstance(cell_value, str) and is_valid_email(cell_value):
            emails.append(cell_value)

    return emails



class TextMessageRequest(BaseModel):
    email: EmailStr
    subject: str
    message: str

class EmailRecordCreate(BaseModel):
    email: str
    wants_newsletter: bool = True
    class Config:
        orm_mode = True


# Эндпоинт для получения всех email записей
@router.get("/", response_model=list[schemas.EmailRecordOut])
async def get_emails(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_session),
    credentials: HTTPBasicCredentials = Depends(security)
):
    verify_credentials(credentials)
    print("Request authorized!")

    db_emails = await crudEmail.get_emails_to_db(db=db, skip=skip, limit=limit)
    return db_emails



# Эндпоинт для создания email записи
@router.post("/", response_model=schemas.EmailRecord)
async def create_email_endpoint(
    email_request: EmailRecordCreate,
    db: AsyncSession = Depends(get_session),
    credentials: HTTPBasicCredentials = Depends(security)
):
    verify_credentials(credentials)
    print("Request authorized!")

    db_email = await crudEmail.add_email_to_db(
        db=db, email=email_request.email, wants_newsletter=email_request.wants_newsletter
    )
    return db_email



@router.post("/all", response_model=Union[List[EmailRecordOut], List[dict]])
async def create_email_records(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_session),
    credentials: HTTPBasicCredentials = Depends(security)
):
    verify_credentials(credentials)
    print("Request authorized!")

    file_content = await file.read()
    emails = extract_emails_from_excel(file_content)

    if not emails:
        raise HTTPException(
            status_code=400, detail="Файл не содержит валидных email адресов"
        )

    email_records = []
    failed_records = []

    for email in emails:
        try:
            existing_email = await db.execute(
                select(EmailRecord).filter(EmailRecord.email == email)
            )
            if existing_email.scalar():
                failed_records.append({"email": email, "error": "Email уже существует"})
                continue

            db_record = EmailRecord(
                email=email, date=datetime.utcnow(), wants_newsletter=True  
            )
            db.add(db_record)
            email_records.append(db_record)
        except Exception as e:
            failed_records.append({"email": email, "error": str(e)})

    try:
        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка сохранения в БД: {str(e)}")
    finally:
        await db.close()

    if failed_records:
        return failed_records

    return [EmailRecordOut.from_orm(record) for record in email_records]


@router.post("/all/txt", response_model=Union[List[EmailRecordOut], List[dict]])
async def create_email_records_from_txt(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_session),
    credentials: HTTPBasicCredentials = Depends(security)
):

    verify_credentials(credentials)

    file_content = (await file.read()).decode("utf-8")
    emails = []
    
    for line in file_content.splitlines():
        line = line.strip()
        if line and re.match(r"[^@]+@[^@]+\.[^@]+", line): 
            emails.append(line)

    if not emails:
        raise HTTPException(
            status_code=400, detail="Файл не содержит валидных email адресов"
        )

    email_records = []
    failed_records = []

    for email in emails:
        try:
            existing_email = await db.execute(
                select(EmailRecord).filter(EmailRecord.email == email)
            )
            if existing_email.scalar():
                failed_records.append({"email": email, "error": "Email уже существует"})
                continue

            db_record = EmailRecord(
                email=email, date=datetime.utcnow(), wants_newsletter=True
            )
            db.add(db_record)
            email_records.append(db_record)
        except Exception as e:
            failed_records.append({"email": email, "error": str(e)})

    try:
        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка сохранения в БД: {str(e)}")
    finally:
        await db.close()

    if failed_records:
        return failed_records

    return [EmailRecordOut.from_orm(record) for record in email_records]
    
# Эндпоинт для удаления email записи
@router.delete("/{email_id}/", response_model=schemas.EmailRecord)
async def delete_email(
    email_id: UUID,
    db: AsyncSession = Depends(get_session),
    credentials: HTTPBasicCredentials = Depends(security)
):
    verify_credentials(credentials)
    print("Request authorized!")

    db_email = await crudEmail.delete_email_from_db(db=db, email_id=email_id)
    return db_email


# Эндпоинт для обновления записи
@router.put("/{email_id}/", response_model=schemas.EmailRecord)
async def update_email(
    email_id: UUID, 
    email_request: schemas.EmailRecordCreate, 
    db: AsyncSession = Depends(get_session),
    credentials: HTTPBasicCredentials = Depends(security)
):
    verify_credentials(credentials)
    print("Request authorized!")

    db_email = await crudEmail.update_email_in_db(
        db=db, 
        email_id=email_id, 
        new_email=email_request.email, 
        wants_newsletter=email_request.wants_newsletter
    )
    return db_email

